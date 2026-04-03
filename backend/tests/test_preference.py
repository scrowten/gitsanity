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
    assert profile.languages["python"] > profile.languages["typescript"]
    assert profile.languages["python"] == 1.0  # normalized to max


def test_build_preference_topics():
    repos = [
        _make_repo(1, topics=["machine-learning", "python"]),
        _make_repo(2, topics=["machine-learning"]),
        _make_repo(3, topics=["web"]),
    ]
    profile = build_preference_profile(repos)
    assert "machine-learning" in profile.topics
    assert profile.topics["machine-learning"] == 1.0
    assert profile.topics.get("web", 0) < profile.topics["machine-learning"]


def test_build_preference_keywords():
    repos = [
        _make_repo(1, description="async HTTP client library"),
        _make_repo(2, description="HTTP server framework"),
    ]
    profile = build_preference_profile(repos)
    assert "http" in profile.keywords or "client" in profile.keywords
