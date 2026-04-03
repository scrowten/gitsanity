from datetime import UTC, datetime, timedelta
from dataclasses import dataclass

from app.services.github import GitHubRepo
from app.services.preference import UserPreferenceProfile


@dataclass
class ScoredRepo:
    repo: GitHubRepo
    score: float
    reason: str


LANGUAGE_WEIGHT = 0.4
TOPIC_WEIGHT = 0.4
KEYWORD_WEIGHT = 0.2
FRESHNESS_BOOST = 1.2
FRESHNESS_DAYS = 90
MIN_STARS = 10


def score_repos(
    candidates: list[GitHubRepo],
    profile: UserPreferenceProfile,
    already_seen_ids: set[int] | None = None,
) -> list[ScoredRepo]:
    seen = already_seen_ids or set()
    scored: list[ScoredRepo] = []

    for repo in candidates:
        if repo.github_id in seen:
            continue
        if repo.star_count < MIN_STARS:
            continue

        lang_score = _language_score(repo, profile)
        topic_score = _topic_score(repo, profile)
        kw_score = _keyword_score(repo, profile)

        raw_score = (
            lang_score * LANGUAGE_WEIGHT
            + topic_score * TOPIC_WEIGHT
            + kw_score * KEYWORD_WEIGHT
        )

        if _is_fresh(repo):
            raw_score *= FRESHNESS_BOOST

        reason = _build_reason(repo, profile, lang_score, topic_score)

        scored.append(ScoredRepo(repo=repo, score=round(raw_score, 4), reason=reason))

    scored.sort(key=lambda x: x.score, reverse=True)
    return _diversify(scored)


def _language_score(repo: GitHubRepo, profile: UserPreferenceProfile) -> float:
    if not repo.primary_language:
        return 0.0
    lang = repo.primary_language.lower()
    return profile.languages.get(lang, 0.0)


def _topic_score(repo: GitHubRepo, profile: UserPreferenceProfile) -> float:
    if not repo.topics or not profile.topics:
        return 0.0
    matches = [profile.topics.get(t.lower(), 0.0) for t in repo.topics]
    return min(sum(matches) / max(len(repo.topics), 1), 1.0)


def _keyword_score(repo: GitHubRepo, profile: UserPreferenceProfile) -> float:
    if not repo.description or not profile.keywords:
        return 0.0
    words = repo.description.lower().split()
    matches = [profile.keywords.get(w, 0.0) for w in words]
    return min(sum(matches) / max(len(words), 1), 1.0)


def _is_fresh(repo: GitHubRepo) -> bool:
    if not repo.updated_at:
        return False
    cutoff = datetime.now(UTC) - timedelta(days=FRESHNESS_DAYS)
    try:
        updated = datetime.fromisoformat(repo.updated_at.replace("Z", "+00:00"))
        return updated > cutoff
    except ValueError:
        return False


def _build_reason(
    repo: GitHubRepo,
    profile: UserPreferenceProfile,
    lang_score: float,
    topic_score: float,
) -> str:
    reasons: list[str] = []

    if lang_score > 0.3 and repo.primary_language:
        reasons.append(f"matches your interest in {repo.primary_language}")

    matched_topics = [
        t for t in repo.topics if profile.topics.get(t.lower(), 0) > 0.2
    ]
    if matched_topics:
        reasons.append(f"related to {', '.join(matched_topics[:2])}")

    if not reasons:
        reasons.append(f"popular {repo.primary_language or 'repository'} with {repo.star_count:,} stars")

    return "Because it " + " and ".join(reasons)


def _diversify(scored: list[ScoredRepo], max_per_owner: int = 3) -> list[ScoredRepo]:
    owner_count: dict[str, int] = {}
    result: list[ScoredRepo] = []

    for item in scored:
        owner = item.repo.full_name.split("/")[0]
        if owner_count.get(owner, 0) >= max_per_owner:
            continue
        owner_count[owner] = owner_count.get(owner, 0) + 1
        result.append(item)

    return result
