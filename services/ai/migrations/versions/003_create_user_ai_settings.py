"""Create ai_providers and user_provider_keys tables

Revision ID: 003_create_user_ai_settings
Revises: 002_create_ai_prompts
Create Date: 2026-06-25 00:00:00.000000

"""

from typing import Sequence, Union
import uuid

from alembic import op
import sqlalchemy as sa
import shared

revision: str = "003_create_user_ai_settings"
down_revision: Union[str, Sequence[str], None] = "002_create_ai_prompts"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "ai_providers",
        sa.Column("id", shared.db.type_decorators.GUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("display_name", sa.String(), nullable=False),
        sa.Column("key_prefix", sa.String(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name", name="uq_ai_providers_name"),
    )
    op.create_index("ix_ai_providers_name", "ai_providers", ["name"], unique=True)

    op.create_table(
        "user_provider_keys",
        sa.Column("id", shared.db.type_decorators.GUID(), nullable=False),
        sa.Column("user_id", shared.db.type_decorators.GUID(), nullable=False),
        sa.Column("provider_id", shared.db.type_decorators.GUID(), nullable=False),
        sa.Column("encrypted_key", sa.Text(), nullable=True),
        sa.Column("model_name", sa.String(), nullable=True),
        sa.Column("base_url", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["provider_id"], ["ai_providers.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "user_id", "provider_id", name="uq_user_provider_keys_user_provider"
        ),
    )
    op.create_index(
        "ix_user_provider_keys_user_id", "user_provider_keys", ["user_id"], unique=False
    )

    op.execute(
        sa.text(
            """
            INSERT INTO ai_providers (id, name, display_name, key_prefix, is_active)
            VALUES
                (:anthropic_id, 'anthropic', 'Anthropic', 'sk-ant-', TRUE),
                (:ollama_id,    'ollama',    'Ollama (Local)', NULL,   TRUE)
            """
        ).bindparams(
            anthropic_id=str(uuid.uuid4()),
            ollama_id=str(uuid.uuid4()),
        )
    )


def downgrade() -> None:
    op.drop_index("ix_user_provider_keys_user_id", table_name="user_provider_keys")
    op.drop_table("user_provider_keys")
    op.drop_index("ix_ai_providers_name", table_name="ai_providers")
    op.drop_table("ai_providers")
