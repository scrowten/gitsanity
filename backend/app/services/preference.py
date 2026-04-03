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
    if not counter:
        return {}
    max_count = counter.most_common(1)[0][1]
    return {
        key: round(count / max_count, 4)
        for key, count in counter.most_common(50)
    }


_STOP_WORDS = {
    "a", "an", "the", "and", "or", "for", "in", "on", "at", "to", "of",
    "with", "is", "it", "this", "that", "are", "was", "be", "by", "from",
    "as", "your", "you", "we", "our", "has", "have", "can", "will", "not",
    "but", "also", "any", "all", "more", "new", "fast", "simple", "easy",
    "based", "using", "use", "used", "via", "like", "just", "its", "into",
}


def _extract_keywords(description: str) -> list[str]:
    words = description.lower().replace("-", " ").split()
    return [
        w.strip(".,!?:;()[]\"'")
        for w in words
        if len(w) > 3 and w not in _STOP_WORDS
    ]
