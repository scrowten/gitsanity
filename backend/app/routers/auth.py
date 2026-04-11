import secrets

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.limiter import limiter
from app.models.user import User
from app.services import auth as auth_service

router = APIRouter(prefix="/auth", tags=["auth"])

GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"

# Short TTL for the OAuth state cookie — must outlive the GitHub redirect round-trip
_STATE_COOKIE_MAX_AGE = 600  # 10 minutes


@router.get("/login")
@limiter.limit("10/minute")
async def login(request: Request) -> RedirectResponse:
    # C-2: Generate unpredictable state to prevent session fixation / CSRF on OAuth flow
    state = secrets.token_urlsafe(32)
    params = (
        f"client_id={settings.github_client_id}"
        f"&redirect_uri={settings.github_redirect_uri}"
        f"&scope=read:user+user:email"
        f"&state={state}"
    )
    response = RedirectResponse(f"{GITHUB_AUTH_URL}?{params}")
    response.set_cookie(
        key="oauth_state",
        value=state,
        httponly=True,
        secure=settings.production,
        samesite="lax",  # Must be lax — GitHub redirect is cross-site GET
        max_age=_STATE_COOKIE_MAX_AGE,
    )
    return response


@router.get("/callback")
@limiter.limit("10/minute")
async def callback(
    request: Request,
    code: str,
    state: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
) -> RedirectResponse:
    # C-2: Validate OAuth state to prevent session fixation
    stored_state = request.cookies.get("oauth_state")
    if not stored_state or not secrets.compare_digest(stored_state, state):
        raise HTTPException(status_code=400, detail="Invalid OAuth state")

    if len(code) > 256:
        raise HTTPException(status_code=400, detail="Invalid code")

    access_token = await auth_service.exchange_code_for_token(code)
    if not access_token:
        raise HTTPException(status_code=400, detail="GitHub OAuth failed")

    user = await auth_service.get_or_create_user(db, access_token)
    session_token = auth_service.create_session_token(str(user.id))

    background_tasks.add_task(auth_service.sync_starred_repos, str(user.id), access_token)

    redirect = RedirectResponse(url=f"{settings.frontend_url}/feed")
    redirect.delete_cookie("oauth_state")  # Clear state cookie after successful auth
    # In production the frontend (Vercel) and backend (Railway) are on different domains.
    # samesite=none allows the browser to send the cookie on cross-site requests while
    # secure=True (enforced by production flag) keeps it HTTPS-only.
    # In dev (same origin) we keep samesite=strict for maximum CSRF protection.
    session_samesite = "none" if settings.production else "strict"
    redirect.set_cookie(
        key="session",
        value=session_token,
        httponly=True,
        secure=settings.production,
        samesite=session_samesite,
        max_age=settings.access_token_expire_minutes * 60,
    )
    return redirect


@router.get("/me")
async def me(current_user: User = Depends(get_current_user)) -> dict:
    return {
        "id": str(current_user.id),
        "github_username": current_user.github_username,
        "display_name": current_user.display_name,
        "avatar_url": current_user.avatar_url,
        "email": current_user.email,
    }


@router.post("/logout")
async def logout(response: Response) -> dict:
    response.delete_cookie("session")
    return {"message": "Logged out"}
