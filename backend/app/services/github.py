from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

import httpx


@dataclass
class GitHubRepo:
    github_id: int
    full_name: str
    description: str | None
    primary_language: str | None
    topics: list[str]
    star_count: int
    fork_count: int
    html_url: str
    homepage: str | None
    created_at: str | None
    updated_at: str | None


class GitHubClient:
    BASE_URL = "https://api.github.com"

    def __init__(self, token: str) -> None:
        self._token = token
        self._headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    async def get_user(self) -> dict:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{self.BASE_URL}/user", headers=self._headers
            )
            resp.raise_for_status()
            return resp.json()

    async def get_starred_repos(self, max_pages: int = 10) -> list[GitHubRepo]:
        repos: list[GitHubRepo] = []
        async with httpx.AsyncClient(timeout=10.0) as client:
            for page in range(1, max_pages + 1):
                resp = await client.get(
                    f"{self.BASE_URL}/user/starred",
                    headers=self._headers,
                    params={"per_page": 100, "page": page},
                )
                resp.raise_for_status()
                data = resp.json()
                if not data:
                    break
                for r in data:
                    repos.append(_parse_repo(r))
        return repos

    async def search_repos(
        self,
        query: str,
        sort: str = "stars",
        per_page: int = 30,
    ) -> list[GitHubRepo]:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{self.BASE_URL}/search/repositories",
                headers=self._headers,
                params={"q": query, "sort": sort, "per_page": per_page},
            )
            resp.raise_for_status()
            return [_parse_repo(r) for r in resp.json().get("items", [])]

    async def get_trending_repos(
        self, language: str = "", time_range: str = "weekly"
    ) -> list[GitHubRepo]:
        # GitHub has no official trending API; use search as a proxy
        query = "stars:>100"
        if language:
            query += f" language:{language}"
        if time_range == "daily":
            since = (datetime.now(UTC) - timedelta(days=1)).strftime("%Y-%m-%d")
            query += f" created:>{since}"
        elif time_range == "weekly":
            since = (datetime.now(UTC) - timedelta(days=7)).strftime("%Y-%m-%d")
            query += f" created:>{since}"
        return await self.search_repos(query, sort="stars", per_page=30)


def _parse_repo(data: dict) -> GitHubRepo:
    return GitHubRepo(
        github_id=data["id"],
        full_name=data["full_name"],
        description=data.get("description"),
        primary_language=data.get("language"),
        topics=data.get("topics", []),
        star_count=data.get("stargazers_count", 0),
        fork_count=data.get("forks_count", 0),
        html_url=data["html_url"],
        homepage=data.get("homepage"),
        created_at=data.get("created_at"),
        updated_at=data.get("updated_at"),
    )
