import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_saved_unauthenticated(unauthenticated_client: AsyncClient) -> None:
    resp = await unauthenticated_client.get("/saved")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_saved_returns_list(client: AsyncClient) -> None:
    # mock_db.execute returns empty rows by default (conftest)
    resp = await client.get("/saved")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
