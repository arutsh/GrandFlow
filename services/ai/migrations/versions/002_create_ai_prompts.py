"""Create ai_prompts table and seed parse_budget v1

Revision ID: 002_create_ai_prompts
Revises: 001_create_ai_audit_logs
Create Date: 2026-06-16 00:00:00.000000

"""

from typing import Sequence, Union
from datetime import datetime, timezone

from alembic import op
import sqlalchemy as sa
from shared.db.type_decorators import GUID

revision: str = "002_create_ai_prompts"
down_revision: Union[str, Sequence[str], None] = "001_create_ai_audit_logs"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

PARSE_BUDGET_SYSTEM_PROMPT = """You are a structured data extractor for nonprofit grant budgets.
Return ONLY valid JSON matching the schema below. No prose, no markdown.
If a value is unknown or cannot be inferred, use JSON null — never the string "null".

Schema:
{
  "budget_name": "string",
  "external_funder_name": "string or null",
  "duration_months": integer or null,
  "lines": [
    {
      "category_name": "string",
      "description": "string",
      "amount": number,
      "extra_fields": object or null
    }
  ]
}"""

PARSE_BUDGET_USER_TEMPLATE = "{{ text }}"


def upgrade() -> None:
    op.create_table(
        "ai_prompts",
        sa.Column("id", GUID(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("version", sa.String(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("system_prompt", sa.Text(), nullable=False),
        sa.Column("user_template", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_ai_prompts_name"), "ai_prompts", ["name"], unique=False)

    op.execute(
        sa.text("""
            INSERT INTO ai_prompts
                (id, name, version, is_active, system_prompt, user_template, created_at)
            VALUES (
                gen_random_uuid(),
                'parse_budget',
                'v1',
                true,
                :system_prompt,
                :user_template,
                :created_at
            )
            """).bindparams(
            system_prompt=PARSE_BUDGET_SYSTEM_PROMPT,
            user_template=PARSE_BUDGET_USER_TEMPLATE,
            created_at=datetime.now(timezone.utc),
        )
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_ai_prompts_name"), table_name="ai_prompts")
    op.drop_table("ai_prompts")
