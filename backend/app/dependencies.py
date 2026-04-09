import uuid

from fastapi import Cookie, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.user import User
from app.services.auth import decode_session_token


async def get_current_user(
    session: str | None = Cookie(default=None),
    db: AsyncSession = Depends(get_db),
) -> User:
    if not session:
        raise HTTPException(status_code=401, detail="Not authenticated")
    user_id = decode_session_token(session)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid session")
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        # L-2: malformed sub claim in JWT (corrupted or old token) → clean 401, not 500
        raise HTTPException(status_code=401, detail="Invalid session")
    result = await db.execute(select(User).where(User.id == user_uuid))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
