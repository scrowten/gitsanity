import pytest
import respx
import httpx
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health(client: AsyncClient) -> None:
    resp = await client.get("/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"


@pytest.mark.asyncio
async def test_login_redirects_to_github(unauthenticated_client: AsyncClient) -> None:
    resp = await unauthenticated_client.get("/auth/login", follow_redirects=False)
    assert resp.status_code in (302, 307)
    assert "github.com/login/oauth/authorize" in resp.headers["location"]


@pytest.mark.asyncio
async def test_me_authenticated(client: AsyncClient) -> None:
    resp = await client.get("/auth/me")
    assert resp.status_code == 200
    data = resp.json()
    assert data["github_username"] == "testuser"
    assert data["display_name"] == "Test User"
    assert "id" in data


@pytest.mark.asyncio
async def test_me_unauthenticated(unauthenticated_client: AsyncClient) -> None:
    resp = await unauthenticated_client.get("/auth/me")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_logout(client: AsyncClient) -> None:
    resp = await client.post("/auth/logout")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Logged out"


@pytest.mark.asyncio
@respx.mock
async def test_callback_invalid_code(unauthenticated_client: AsyncClient) -> None:
    # GitHub returns no access_token for invalid code
    respx.post("https://github.com/login/oauth/access_token").mock(
        return_value=httpx.Response(200, json={"error": "bad_verification_code"})
    )
    resp = await unauthenticated_client.get("/auth/callback?code=badcode", follow_redirects=False)
    assert resp.status_code == 400
