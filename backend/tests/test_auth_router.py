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
    location = resp.headers["location"]
    assert "github.com/login/oauth/authorize" in location
    # C-2: state parameter must be present to prevent session fixation
    assert "state=" in location
    assert "oauth_state" in resp.cookies


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
async def test_callback_rejects_missing_state(unauthenticated_client: AsyncClient) -> None:
    # C-2: callback without state param should be rejected (422 missing field)
    resp = await unauthenticated_client.get("/auth/callback?code=somecode", follow_redirects=False)
    assert resp.status_code == 422


@pytest.mark.asyncio
async def test_callback_rejects_mismatched_state(unauthenticated_client: AsyncClient) -> None:
    # C-2: mismatched state cookie vs query param should be rejected
    unauthenticated_client.cookies.set("oauth_state", "legit-state")
    resp = await unauthenticated_client.get(
        "/auth/callback?code=somecode&state=attacker-state", follow_redirects=False
    )
    assert resp.status_code == 400


@pytest.mark.asyncio
@respx.mock
async def test_callback_invalid_code(unauthenticated_client: AsyncClient) -> None:
    # GitHub returns no access_token for invalid code — state cookie must match
    state = "test-state-value"
    unauthenticated_client.cookies.set("oauth_state", state)
    respx.post("https://github.com/login/oauth/access_token").mock(
        return_value=httpx.Response(200, json={"error": "bad_verification_code"})
    )
    resp = await unauthenticated_client.get(
        f"/auth/callback?code=badcode&state={state}", follow_redirects=False
    )
    assert resp.status_code == 400
