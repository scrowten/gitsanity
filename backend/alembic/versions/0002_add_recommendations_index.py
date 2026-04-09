"""add composite index on recommendations(user_id, action)

Revision ID: 0002
Revises: 0001
Create Date: 2026-04-09

M-8: The saved-repos query filters by user_id + action='saved'. Without a
composite index, every lookup does a full table scan on the user_id index and
then filters in Postgres. This index makes that query O(log n) for both columns.
"""
from collections.abc import Sequence

from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_index(
        "ix_recommendations_user_action",
        "recommendations",
        ["user_id", "action"],
    )


def downgrade() -> None:
    op.drop_index("ix_recommendations_user_action", table_name="recommendations")
