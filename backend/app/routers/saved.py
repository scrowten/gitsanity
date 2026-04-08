from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies import get_current_user
from app.models.recommendation import Recommendation
from app.models.repository import Repository
from app.models.user import User
from app.schemas.recommendation import RepoCard

router = APIRouter(prefix="/saved", tags=["saved"])


@router.get("", response_model=list[RepoCard])
async def get_saved(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[RepoCard]:
    result = await db.execute(
        select(Recommendation, Repository)
        .join(Repository, Recommendation.repo_id == Repository.id)
        .where(
            Recommendation.user_id == current_user.id,
            Recommendation.action == "saved",
        )
        .order_by(Recommendation.generated_at.desc())
    )
    rows = result.all()

    return [
        RepoCard(
            github_id=repo.github_id,
            full_name=repo.full_name,
            description=repo.description,
            primary_language=repo.primary_language,
            topics=repo.topics or [],
            star_count=repo.star_count,
            html_url=repo.html_url,
            score=rec.score,
            reason=rec.reason or "",
        )
        for rec, repo in rows
    ]
