# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

"""Add Project model.

Revision ID: 0001
Revises:
Create Date: 2022-04-04 18:58:48.883313
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'projects',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('code', sa.VARCHAR(length=32), nullable=False),
        sa.Column('name', sa.VARCHAR(length=256), nullable=False),
        sa.Column('description', sa.VARCHAR(length=256), nullable=False),
        sa.Column('image_url', sa.VARCHAR(length=2083), nullable=True),
        sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('tags', postgresql.ARRAY(sa.VARCHAR(length=256)), nullable=False),
        sa.Column('system_tags', postgresql.ARRAY(sa.VARCHAR(length=256)), nullable=False),
        sa.Column('is_discoverable', sa.BOOLEAN(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema='project',
    )
    op.create_index(op.f('ix_project_projects_code'), 'projects', ['code'], unique=True, schema='project')


def downgrade():
    op.drop_index(op.f('ix_project_projects_code'), table_name='projects', schema='project')
    op.drop_table('projects', schema='project')
