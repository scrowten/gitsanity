"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-04-08

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("github_id", sa.Integer(), nullable=False, unique=True),
        sa.Column("github_username", sa.String(255), nullable=False),
        sa.Column("display_name", sa.String(255), nullable=True),
        sa.Column("avatar_url", sa.Text(), nullable=True),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("github_access_token", sa.Text(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "last_login_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_table(
        "repositories",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column("github_id", sa.Integer(), nullable=False, unique=True),
        sa.Column("full_name", sa.String(512), nullable=False, index=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("primary_language", sa.String(100), nullable=True),
        sa.Column(
            "topics",
            postgresql.ARRAY(sa.String()),
            nullable=True,
            server_default="{}",
        ),
        sa.Column("star_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("fork_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("readme_summary", sa.Text(), nullable=True),
        sa.Column("html_url", sa.Text(), nullable=False),
        sa.Column("homepage", sa.Text(), nullable=True),
        sa.Column("repo_created_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("repo_updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "last_indexed_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("quality_score", sa.Float(), nullable=True),
    )

    op.create_table(
        "starred_repos",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("repo_github_id", sa.Integer(), nullable=False),
        sa.Column("repo_full_name", sa.String(512), nullable=False),
        sa.Column(
            "synced_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_table(
        "user_preferences",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column("preference_type", sa.String(50), nullable=False),
        sa.Column("preference_value", sa.String(255), nullable=False),
        sa.Column("weight", sa.Float(), nullable=False, server_default="1.0"),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
    )

    op.create_table(
        "recommendations",
        sa.Column("id", postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column(
            "user_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("users.id", ondelete="CASCADE"),
            nullable=False,
            index=True,
        ),
        sa.Column(
            "repo_id",
            postgresql.UUID(as_uuid=True),
            sa.ForeignKey("repositories.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("reason", sa.Text(), nullable=True),
        sa.Column(
            "generated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column("seen", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("action", sa.String(50), nullable=True),
    )


def downgrade() -> None:
    op.drop_table("recommendations")
    op.drop_table("user_preferences")
    op.drop_table("starred_repos")
    op.drop_table("repositories")
    op.drop_table("users")
