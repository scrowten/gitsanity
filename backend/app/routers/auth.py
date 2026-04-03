from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"


@router.get("/login")
async def login() -> RedirectResponse:
    params = (
        f"client_id={settings.github_client_id}"
        f"&redirect_uri={settings.github_redirect_uri}"
        f"&scope=read:user+user:email"
    )
    return RedirectResponse(f"{GITHUB_AUTH_URL}?{params}")


@router.get("/callback")
async def callback(
    code: str,
    response: Response,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    access_token = await auth_service.exchange_code_for_token(code)
    if not access_token:
        raise HTTPException(status_code=400, detail="GitHub OAuth failed")

    user = await auth_service.get_or_create_user(db, access_token)
    session_token = auth_service.create_session_token(str(user.id))

    background_tasks.add_task(auth_service.sync_starred_repos, db, user, access_token)

    redirect = RedirectResponse(url="http://localhost:3000/feed")
    redirect.set_cookie(
        key="session",
        value=session_token,
        httponly=True,
        secure=False,  # set True in production
        samesite="lax",
        max_age=settings.access_token_expire_minutes * 60,
    )
    return redirect


@router.post("/logout")
async def logout(response: Response) -> dict:
    response.delete_cookie("session")
    return {"message": "Logged out"}
