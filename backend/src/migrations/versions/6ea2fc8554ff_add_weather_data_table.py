"""add weather_data table

Revision ID: 6ea2fc8554ff
Revises: 6920d1d16fc2
Create Date: 2025-09-17 10:18:13.974888

"""

import sqlalchemy as sa
import sqlmodel
from alembic import op


# revision identifiers, used by Alembic.
revision = "6ea2fc8554ff"
down_revision = "6920d1d16fc2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create weather_data table
    op.create_table(
        "weather_data",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ref_id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("TIMEZONE('utc', CURRENT_TIMESTAMP)"),
            nullable=True,
        ),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("temperature", sa.Float(), nullable=False),
        sa.Column("timestamp", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("ref_id"),
    )
    # Create indexes
    op.create_index(op.f("ix_weather_data_id"), "weather_data", ["id"], unique=False)
    op.create_index(op.f("ix_weather_data_ref_id"), "weather_data", ["ref_id"], unique=False)
    op.create_index(op.f("ix_weather_data_latitude"), "weather_data", ["latitude"], unique=False)
    op.create_index(op.f("ix_weather_data_longitude"), "weather_data", ["longitude"], unique=False)
    op.create_index(op.f("ix_weather_data_timestamp"), "weather_data", ["timestamp"], unique=False)


def downgrade() -> None:
    # Drop indexes
    op.drop_index(op.f("ix_weather_data_timestamp"), table_name="weather_data")
    op.drop_index(op.f("ix_weather_data_longitude"), table_name="weather_data")
    op.drop_index(op.f("ix_weather_data_latitude"), table_name="weather_data")
    op.drop_index(op.f("ix_weather_data_ref_id"), table_name="weather_data")
    op.drop_index(op.f("ix_weather_data_id"), table_name="weather_data")
    # Drop table
    op.drop_table("weather_data")
