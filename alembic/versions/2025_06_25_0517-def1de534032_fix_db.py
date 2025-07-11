"""fix db

Revision ID: def1de534032
Revises: c2ca7016ecab
Create Date: 2025-06-25 05:17:23.936926

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "def1de534032"
down_revision: Union[str, None] = "c2ca7016ecab"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "executors",
        sa.Column("task_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"], ["tasks.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("task_id", "user_id"),
    )
    op.create_table(
        "watchers",
        sa.Column("task_id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(
            ["task_id"], ["tasks.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("task_id", "user_id"),
    )
    op.create_unique_constraint(None, "tasks", ["id"])
    op.create_unique_constraint(None, "users", ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "users", type_="unique")
    op.drop_constraint(None, "tasks", type_="unique")
    op.drop_table("watchers")
    op.drop_table("executors")
    # ### end Alembic commands ###
