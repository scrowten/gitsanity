from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.dependencies import get_current_user
from app.limiter import limiter
from app.security import decrypt_token
from app.models.recommendation import Recommendation, UserPreference
from app.models.repository import Repository
from app.models.user import User
from app.schemas.recommendation import FeedResponse, RepoCard
from app.services.github import GitHubClient, GitHubRepo
from app.services.preference import UserPreferenceProfile
from app.services.recommender import score_repos

router = APIRouter(prefix="/feed", tags=["feed"])


@router.get("", response_model=FeedResponse)
@limiter.limit("30/minute")
async def get_feed(
    request: Request,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> FeedResponse:
    # Load user preferences
    prefs_result = await db.execute(
        select(UserPreference).where(UserPreference.user_id == current_user.id)
    )
    prefs = prefs_result.scalars().all()

    profile = _prefs_to_profile(prefs)

    # Fetch candidates from our repo catalog
    repos_result = await db.execute(
        select(Repository)
        .where(Repository.star_count >= 10)
        .order_by(Repository.star_count.desc())
        .limit(500)
    )
    candidate_repos = repos_result.scalars().all()

    # If catalog is empty, fetch from GitHub trending directly
    if not candidate_repos:
        access_token = decrypt_token(current_user.github_access_token, settings.secret_key)
        gh = GitHubClient(access_token)
        top_lang = _top_language(profile)
        gh_repos = await gh.get_trending_repos(language=top_lang)
        scored = score_repos(gh_repos, profile)
    else:
        gh_repos = [_db_to_github_repo(r) for r in candidate_repos]
        scored = score_repos(gh_repos, profile)

    offset = (page - 1) * limit
    page_items = scored[offset: offset + limit]

    return FeedResponse(
        items=[
            RepoCard(
                github_id=item.repo.github_id,
                full_name=item.repo.full_name,
                description=item.repo.description,
                primary_language=item.repo.primary_language,
                topics=item.repo.topics,
                star_count=item.repo.star_count,
                html_url=item.repo.html_url,
                score=item.score,
                reason=item.reason,
            )
            for item in page_items
        ],
        total=len(scored),
        page=page,
        has_more=offset + limit < len(scored),
    )


@router.post("/{github_id}/action")
@limiter.limit("60/minute")
async def repo_action(
    request: Request,
    github_id: int,
    action: Literal["saved", "dismissed", "clicked"],
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:

    result = await db.execute(
        select(Repository).where(Repository.github_id == github_id)
    )
    repo = result.scalar_one_or_none()
    if not repo:
        raise HTTPException(status_code=404, detail="Repo not found")

    existing = await db.execute(
        select(Recommendation).where(
            Recommendation.user_id == current_user.id,
            Recommendation.repo_id == repo.id,
        )
    )
    rec = existing.scalar_one_or_none()
    if rec:
        rec.action = action
        rec.seen = True
    else:
        db.add(Recommendation(
            user_id=current_user.id,
            repo_id=repo.id,
            score=0.0,
            action=action,
            seen=True,
        ))

    await db.commit()
    return {"status": "ok", "action": action}


def _prefs_to_profile(prefs: list[UserPreference]) -> UserPreferenceProfile:
    languages: dict[str, float] = {}
    topics: dict[str, float] = {}
    for p in prefs:
        if p.preference_type == "language":
            languages[p.preference_value] = p.weight
        elif p.preference_type == "topic":
            topics[p.preference_value] = p.weight
    return UserPreferenceProfile(
        languages=languages,
        topics=topics,
        keywords={},
        total_stars_analyzed=0,
    )


def _top_language(profile: UserPreferenceProfile) -> str:
    if not profile.languages:
        return ""
    return max(profile.languages, key=lambda k: profile.languages[k])


def _db_to_github_repo(r: Repository) -> GitHubRepo:
    from app.services.github import GitHubRepo
    return GitHubRepo(
        github_id=r.github_id,
        full_name=r.full_name,
        description=r.description,
        primary_language=r.primary_language,
        topics=r.topics or [],
        star_count=r.star_count,
        fork_count=r.fork_count,
        html_url=r.html_url,
        homepage=r.homepage,
        created_at=None,
        updated_at=r.repo_updated_at.isoformat() if r.repo_updated_at else None,
    )
