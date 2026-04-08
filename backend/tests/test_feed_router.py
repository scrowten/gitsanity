import uuid
from unittest.mock import MagicMock, patch

import pytest
import respx
import httpx
from httpx import AsyncClient

from app.services.github import GitHubRepo


def _make_gh_repo(github_id: int, language: str = "Python") -> GitHubRepo:
    return GitHubRepo(
        github_id=github_id,
        full_name=f"owner/repo-{github_id}",
        description="A great repo",
        primary_language=language,
        topics=["testing"],
        star_count=500,
        fork_count=50,
        html_url=f"https://github.com/owner/repo-{github_id}",
        homepage=None,
        created_at=None,
        updated_at="2025-06-01T00:00:00Z",
    )


@pytest.mark.asyncio
async def test_feed_unauthenticated(unauthenticated_client: AsyncClient) -> None:
    resp = await unauthenticated_client.get("/feed")
    assert resp.status_code == 401


@pytest.mark.asyncio
@respx.mock
async def test_feed_returns_items_from_github_fallback(client: AsyncClient) -> None:
    # Catalog is empty → falls back to GitHub trending search
    gh_items = [
        {
            "id": i,
            "full_name": f"owner/repo-{i}",
            "description": "test",
            "language": "Python",
            "topics": [],
            "stargazers_count": 500,
            "forks_count": 10,
            "html_url": f"https://github.com/owner/repo-{i}",
            "homepage": None,
            "created_at": None,
            "updated_at": "2025-06-01T00:00:00Z",
        }
        for i in range(1, 6)
    ]
    respx.get("https://api.github.com/search/repositories").mock(
        return_value=httpx.Response(200, json={"items": gh_items})
    )

    resp = await client.get("/feed")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)


@pytest.mark.asyncio
async def test_feed_invalid_action(client: AsyncClient, mock_db: MagicMock) -> None:
    # Repo not found → 404
    resp = await client.post("/feed/99999/action?action=saved")
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_feed_bad_action_value(client: AsyncClient) -> None:
    resp = await client.post("/feed/1/action?action=invalid")
    assert resp.status_code == 400
