from app.services.github import GitHubRepo
from app.services.preference import build_preference_profile


def _make_repo(
    github_id: int,
    language: str | None = None,
    topics: list[str] | None = None,
    description: str | None = None,
) -> GitHubRepo:
    return GitHubRepo(
        github_id=github_id,
        full_name=f"owner/repo-{github_id}",
        description=description,
        primary_language=language,
        topics=topics or [],
        star_count=100,
        fork_count=10,
        html_url=f"https://github.com/owner/repo-{github_id}",
        homepage=None,
        created_at=None,
        updated_at=None,
    )


def test_build_preference_empty():
    profile = build_preference_profile([])
    assert profile.languages == {}
    assert profile.topics == {}
    assert profile.total_stars_analyzed == 0


def test_build_preference_languages():
    repos = [
        _make_repo(1, language="Python"),
        _make_repo(2, language="Python"),
        _make_repo(3, language="TypeScript"),
    ]
    profile = build_preference_profile(repos)
    assert "python" in profile.languages
    assert "typescript" in profile.languages
    # M-6: weights are now count/total, not count/max_count
    # python: 2/3 ≈ 0.6667, typescript: 1/3 ≈ 0.3333
    assert profile.languages["python"] == round(2 / 3, 4)
    assert profile.languages["typescript"] == round(1 / 3, 4)
    assert profile.languages["python"] > profile.languages["typescript"]
    assert all(0.0 < w <= 1.0 for w in profile.languages.values())


def test_build_preference_topics():
    repos = [
        _make_repo(1, topics=["machine-learning", "python"]),
        _make_repo(2, topics=["machine-learning"]),
        _make_repo(3, topics=["web"]),
    ]
    profile = build_preference_profile(repos)
    assert "machine-learning" in profile.topics
    # machine-learning: 2/3 ≈ 0.6667, web: 1/3 ≈ 0.3333
    assert profile.topics["machine-learning"] == round(2 / 3, 4)
    assert profile.topics.get("web", 0) < profile.topics["machine-learning"]


def test_build_preference_keywords():
    repos = [
        _make_repo(1, description="async HTTP client library"),
        _make_repo(2, description="HTTP server framework"),
    ]
    profile = build_preference_profile(repos)
    assert "http" in profile.keywords or "client" in profile.keywords
