from pydantic import BaseModel


class RepoCard(BaseModel):
    github_id: int
    full_name: str
    description: str | None
    primary_language: str | None
    topics: list[str]
    star_count: int
    html_url: str
    score: float
    reason: str


class FeedResponse(BaseModel):
    items: list[RepoCard]
    total: int
    page: int
    has_more: bool
