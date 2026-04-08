"""Repository ingestion service.

Searches GitHub for repos matching a user's preference profile and upserts
them into the `repositories` table so the recommendation engine has a catalog
to score against.
"""
import logging
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.repository import Repository
from app.services.github import GitHubClient, GitHubRepo
from app.services.preference import UserPreferenceProfile

logger = logging.getLogger(__name__)


async def ingest_repos_for_user(
    db: AsyncSession,
    profile: UserPreferenceProfile,
    access_token: str,
    max_per_query: int = 30,
) -> int:
    """Fetch repos from GitHub matching the user's preference profile and
    upsert them into the repositories table.

    Returns the number of repos upserted.
    """
    gh = GitHubClient(access_token)
    repos: list[GitHubRepo] = []

    # Build queries from top languages and topics
    top_languages = sorted(profile.languages, key=lambda k: profile.languages[k], reverse=True)[:3]
    top_topics = sorted(profile.topics, key=lambda k: profile.topics[k], reverse=True)[:3]

    queries: list[str] = []
    for lang in top_languages:
        queries.append(f"language:{lang} stars:>50")
    for topic in top_topics:
        queries.append(f"topic:{topic} stars:>50")

    # Fallback if no preferences yet
    if not queries:
        queries = ["stars:>500"]

    for query in queries:
        try:
            results = await gh.search_repos(query, sort="stars", per_page=max_per_query)
            repos.extend(results)
        except Exception:
            logger.exception("GitHub search failed for query: %s", query)

    if not repos:
        logger.warning("No repos fetched from GitHub during ingestion")
        return 0

    # Deduplicate by github_id
    seen: set[int] = set()
    unique_repos = [r for r in repos if not (r.github_id in seen or seen.add(r.github_id))]  # type: ignore[func-returns-value]

    upserted = 0
    for repo in unique_repos:
        result = await db.execute(
            select(Repository).where(Repository.github_id == repo.github_id)
        )
        existing = result.scalar_one_or_none()

        repo_updated_at: datetime | None = None
        if repo.updated_at:
            try:
                repo_updated_at = datetime.fromisoformat(repo.updated_at.replace("Z", "+00:00"))
            except ValueError:
                pass

        repo_created_at: datetime | None = None
        if repo.created_at:
            try:
                repo_created_at = datetime.fromisoformat(repo.created_at.replace("Z", "+00:00"))
            except ValueError:
                pass

        if existing:
            existing.star_count = repo.star_count
            existing.fork_count = repo.fork_count
            existing.description = repo.description
            existing.topics = repo.topics
            existing.primary_language = repo.primary_language
            existing.repo_updated_at = repo_updated_at
            existing.last_indexed_at = datetime.now(UTC)
        else:
            db.add(Repository(
                github_id=repo.github_id,
                full_name=repo.full_name,
                description=repo.description,
                primary_language=repo.primary_language,
                topics=repo.topics,
                star_count=repo.star_count,
                fork_count=repo.fork_count,
                html_url=repo.html_url,
                homepage=repo.homepage,
                repo_created_at=repo_created_at,
                repo_updated_at=repo_updated_at,
            ))
        upserted += 1

    await db.commit()
    logger.info("Ingested %d repos into catalog", upserted)
    return upserted
