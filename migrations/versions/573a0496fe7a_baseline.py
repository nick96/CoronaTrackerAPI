"""baseline

Revision ID: 573a0496fe7a
Revises: 
Create Date: 2020-04-10 12:42:52.398967

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "573a0496fe7a"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "positive",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("key", sa.String(), unique=True, nullable=False),
        sa.Column("checksum", sa.String(), unique=True),
        sa.Column("hash", sa.String(), unique=True),
    )

    op.create_table(
        "contact",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("key", sa.String(), unique=True, nullable=False),
        sa.Column("checksum", sa.String(), unique=True),
        sa.Column("hash", sa.String(), unique=True),
    )


def downgrade():
    op.drop_table("positive")
    op.drop_table("contact")
