from collections import Counter
from dataclasses import dataclass

from app.services.github import GitHubRepo


@dataclass
class UserPreferenceProfile:
    languages: dict[str, float]   # {"python": 0.75, "typescript": 0.4}
    topics: dict[str, float]      # {"machine-learning": 0.8, "cli": 0.3}
    keywords: dict[str, float]    # extracted from descriptions
    total_stars_analyzed: int


def build_preference_profile(starred_repos: list[GitHubRepo]) -> UserPreferenceProfile:
    lang_counter: Counter[str] = Counter()
    topic_counter: Counter[str] = Counter()
    keyword_counter: Counter[str] = Counter()

    for repo in starred_repos:
        if repo.primary_language:
            lang_counter[repo.primary_language.lower()] += 1

        for topic in repo.topics:
            topic_counter[topic.lower()] += 1

        if repo.description:
            words = _extract_keywords(repo.description)
            for word in words:
                keyword_counter[word] += 1

    total = len(starred_repos) or 1

    return UserPreferenceProfile(
        languages=_normalize(lang_counter, total),
        topics=_normalize(topic_counter, total),
        keywords=_normalize(keyword_counter, total),
        total_stars_analyzed=len(starred_repos),
    )


def _normalize(counter: Counter, total: int) -> dict[str, float]:
    """Return weights as a fraction of total repos analyzed.

    M-6 fix: previously divided by max_count, which always gave the most
    common item a weight of 1.0 regardless of how dominant it was. A user
    with 5 Python repos (out of 5 total) and one with 5 Python repos (out
    of 200 total) got the same weight. Dividing by total reflects actual
    depth of interest: 5/5=1.0 vs 5/200=0.025.
    """
    if not counter:
        return {}
    return {
        key: round(count / total, 4)
        for key, count in counter.most_common(50)
    }


# L-3: Only include words that are NOT already filtered by `len(w) > 3`.
# Words ≤ 3 chars (a, an, the, and, or, in, on, at, to, of, is, it, are,
# was, be, by, as, you, we, our, has, can, not, but, any, all, new, use,
# via, its) are redundant here — keep only 4+ char meaningful stop words.
_STOP_WORDS = {
    "with", "this", "that", "from", "your", "have", "will",
    "also", "more", "fast", "simple", "easy", "based", "using",
    "used", "like", "just", "into",
}


def _extract_keywords(description: str) -> list[str]:
    words = description.lower().replace("-", " ").split()
    return [
        w.strip(".,!?:;()[]\"'")
        for w in words
        if len(w) > 3 and w not in _STOP_WORDS
    ]
