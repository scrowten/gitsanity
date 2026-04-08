"""Shared pytest fixtures for API tests.

The database and GitHub HTTP calls are mocked so tests run without
a real PostgreSQL instance or network access.
"""
import uuid
from collections.abc import AsyncGenerator
from unittest.mock import AsyncMock, MagicMock

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.main import app
from app.models.user import User


@pytest.fixture
def mock_user() -> User:
    return User(
        id=uuid.uuid4(),
        github_id=12345,
        github_username="testuser",
        display_name="Test User",
        avatar_url="https://avatars.githubusercontent.com/u/12345",
        email="test@example.com",
        github_access_token="gho_test_token",
    )


@pytest.fixture
def mock_db() -> AsyncMock:
    session = AsyncMock(spec=AsyncSession)
    # execute().scalar_one_or_none() pattern
    session.execute.return_value = MagicMock(
        scalar_one_or_none=MagicMock(return_value=None),
        scalars=MagicMock(return_value=MagicMock(all=MagicMock(return_value=[]))),
        all=MagicMock(return_value=[]),
    )
    return session


@pytest.fixture
async def client(mock_user: User, mock_db: AsyncMock) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield mock_db

    async def override_get_current_user() -> User:
        return mock_user

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def unauthenticated_client(mock_db: AsyncMock) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield mock_db

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides.clear()
