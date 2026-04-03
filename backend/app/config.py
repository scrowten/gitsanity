from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

    # Database
    database_url: str

    # GitHub OAuth
    github_client_id: str
    github_client_secret: str
    github_redirect_uri: str = "http://localhost:8000/auth/callback"

    # GitHub API token for ingestion
    github_token: str = ""

    # Auth
    secret_key: str
    access_token_expire_minutes: int = 10080  # 7 days

    # App
    app_name: str = "GitSanity"
    debug: bool = False


settings = Settings()
