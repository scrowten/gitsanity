from app.services.github import GitHubRepo
from app.services.preference import UserPreferenceProfile
from app.services.recommender import MIN_STARS, score_repos


def _make_repo(
    github_id: int,
    language: str | None = None,
    topics: list[str] | None = None,
    stars: int = 500,
    updated_at: str | None = "2025-01-01T00:00:00Z",
) -> GitHubRepo:
    return GitHubRepo(
        github_id=github_id,
        full_name=f"owner/repo-{github_id}",
        description=f"A great repo number {github_id}",
        primary_language=language,
        topics=topics or [],
        star_count=stars,
        fork_count=50,
        html_url=f"https://github.com/owner/repo-{github_id}",
        homepage=None,
        created_at=None,
        updated_at=updated_at,
    )


def _make_profile(
    languages: dict[str, float] | None = None,
    topics: dict[str, float] | None = None,
) -> UserPreferenceProfile:
    return UserPreferenceProfile(
        languages=languages or {},
        topics=topics or {},
        keywords={},
        total_stars_analyzed=10,
    )


def test_score_repos_empty_candidates():
    result = score_repos([], _make_profile())
    assert result == []


def test_score_repos_filters_low_stars():
    repos = [_make_repo(1, stars=MIN_STARS - 1)]
    result = score_repos(repos, _make_profile())
    assert result == []


def test_score_repos_language_match():
    profile = _make_profile(languages={"python": 1.0, "go": 0.3})
    repos = [
        _make_repo(1, language="Python"),
        _make_repo(2, language="Go"),
        _make_repo(3, language="Rust"),
    ]
    result = score_repos(repos, profile)
    assert len(result) == 3
    scores = {r.repo.github_id: r.score for r in result}
    assert scores[1] > scores[2] > scores[3]


def test_score_repos_filters_already_seen():
    profile = _make_profile(languages={"python": 1.0})
    repos = [_make_repo(1, language="Python"), _make_repo(2, language="Python")]
    result = score_repos(repos, profile, already_seen_ids={1})
    assert all(r.repo.github_id != 1 for r in result)


def test_score_repos_diversification():
    profile = _make_profile(languages={"python": 1.0})
    # 5 repos from same owner
    repos = [_make_repo(i, language="Python") for i in range(1, 6)]
    for repo in repos:
        repo = GitHubRepo(
            github_id=repo.github_id,
            full_name=f"same-owner/repo-{repo.github_id}",
            description=repo.description,
            primary_language=repo.primary_language,
            topics=repo.topics,
            star_count=repo.star_count,
            fork_count=repo.fork_count,
            html_url=repo.html_url,
            homepage=repo.homepage,
            created_at=repo.created_at,
            updated_at=repo.updated_at,
        )
    result = score_repos(repos, profile)
    owners = [r.repo.full_name.split("/")[0] for r in result]
    from collections import Counter
    assert max(Counter(owners).values()) <= 3


def test_score_repos_reason_not_empty():
    profile = _make_profile(languages={"python": 1.0})
    repos = [_make_repo(1, language="Python")]
    result = score_repos(repos, profile)
    assert result[0].reason != ""
