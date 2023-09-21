# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

"""Add Resource Request model.

Revision ID: 0002
Revises: 0001
Create Date: 2022-04-05 15:50:47.603266
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = '0001'


def upgrade():
    op.create_table(
        'resource_requests',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('requested_by_user_id', sa.VARCHAR(length=256), nullable=False),
        sa.Column('requested_for', sa.VARCHAR(length=256), nullable=False),
        sa.Column('requested_at', postgresql.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('completed_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ['project_id'],
            ['project.projects.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        schema='project',
    )


def downgrade():
    op.drop_table('resource_requests', schema='project')
