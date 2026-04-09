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

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.main import app
from app.models.user import User
from app.security import encrypt_token

# C-3: Store token as Fernet ciphertext, matching production behaviour.
# Tests that call decrypt_token(user.github_access_token, settings.secret_key)
# will now get the correct plaintext back instead of raising a decryption error.
_TEST_GITHUB_TOKEN = "gho_test_token"


@pytest.fixture
def mock_user() -> User:
    return User(
        id=uuid.uuid4(),
        github_id=12345,
        github_username="testuser",
        display_name="Test User",
        avatar_url="https://avatars.githubusercontent.com/u/12345",
        email="test@example.com",
        github_access_token=encrypt_token(_TEST_GITHUB_TOKEN, settings.secret_key),
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

    # H-9: Save and restore overrides instead of clearing all, to avoid clobbering
    # overrides set by other fixtures that may be in scope simultaneously.
    saved = dict(app.dependency_overrides)
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides = saved


@pytest.fixture
async def unauthenticated_client(mock_db: AsyncMock) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield mock_db

    saved = dict(app.dependency_overrides)
    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    app.dependency_overrides = saved
