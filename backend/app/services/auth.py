import uuid
from datetime import UTC, datetime, timedelta

import httpx
from jose import jwt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.recommendation import StarredRepo, UserPreference
from app.models.user import User
from app.services.github import GitHubClient
from app.services.preference import build_preference_profile


async def exchange_code_for_token(code: str) -> str | None:
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            "https://github.com/login/oauth/access_token",
            data={
                "client_id": settings.github_client_id,
                "client_secret": settings.github_client_secret,
                "code": code,
            },
            headers={"Accept": "application/json"},
        )
        data = resp.json()
        return data.get("access_token")


async def get_or_create_user(db: AsyncSession, access_token: str) -> User:
    gh = GitHubClient(access_token)
    gh_user = await gh.get_user()

    result = await db.execute(
        select(User).where(User.github_id == gh_user["id"])
    )
    user = result.scalar_one_or_none()

    if user:
        user.github_access_token = access_token
        user.last_login_at = datetime.now(UTC)
        user.display_name = gh_user.get("name") or gh_user["login"]
        user.avatar_url = gh_user.get("avatar_url")
    else:
        user = User(
            github_id=gh_user["id"],
            github_username=gh_user["login"],
            display_name=gh_user.get("name") or gh_user["login"],
            avatar_url=gh_user.get("avatar_url"),
            email=gh_user.get("email"),
            github_access_token=access_token,
        )
        db.add(user)

    await db.commit()
    await db.refresh(user)
    return user


def create_session_token(user_id: str) -> str:
    expire = datetime.now(UTC) + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    return jwt.encode(
        {"sub": user_id, "exp": expire},
        settings.secret_key,
        algorithm="HS256",
    )


def decode_session_token(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        return payload.get("sub")
    except Exception:
        return None


async def sync_starred_repos(
    db: AsyncSession, user: User, access_token: str
) -> None:
    gh = GitHubClient(access_token)
    starred = await gh.get_starred_repos(max_pages=5)  # up to 500 repos

    # Store starred repos
    for repo in starred:
        existing = await db.execute(
            select(StarredRepo).where(
                StarredRepo.user_id == user.id,
                StarredRepo.repo_github_id == repo.github_id,
            )
        )
        if not existing.scalar_one_or_none():
            db.add(
                StarredRepo(
                    user_id=user.id,
                    repo_github_id=repo.github_id,
                    repo_full_name=repo.full_name,
                )
            )

    await db.commit()

    # Build and store preference profile
    profile = build_preference_profile(starred)

    # Clear old preferences
    old_prefs = await db.execute(
        select(UserPreference).where(UserPreference.user_id == user.id)
    )
    for pref in old_prefs.scalars():
        await db.delete(pref)

    # Insert updated preferences
    for lang, weight in profile.languages.items():
        db.add(UserPreference(
            user_id=user.id,
            preference_type="language",
            preference_value=lang,
            weight=weight,
        ))
    for topic, weight in profile.topics.items():
        db.add(UserPreference(
            user_id=user.id,
            preference_type="topic",
            preference_value=topic,
            weight=weight,
        ))

    await db.commit()
