"""Create conversations table.

Revision ID: 001
Revises:
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "conversations",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("phone_number", sa.String(), nullable=False),
        sa.Column("incoming_message", sa.String(), nullable=False),
        sa.Column("llm_response", sa.String(), nullable=False),
        sa.Column("provider_message_id", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("provider_message_id"),
    )
    op.create_index(
        "ix_conversations_phone_number",
        "conversations",
        ["phone_number"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_conversations_phone_number", table_name="conversations")
    op.drop_table("conversations")