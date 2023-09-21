# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

"""Add Workbench model.

Revision ID: 0003
Revises: 0002
Create Date: 2022-04-05 19:27:02.257066
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = '0002'


def upgrade():
    op.create_table(
        'workbenches',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('project_id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('resource', sa.VARCHAR(length=256), nullable=False),
        sa.Column('deployed_at', postgresql.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('deployed_by_user_id', sa.VARCHAR(length=256), nullable=False),
        sa.ForeignKeyConstraint(
            ['project_id'],
            ['project.projects.id'],
        ),
        sa.PrimaryKeyConstraint('id'),
        schema='project',
    )


def downgrade():
    op.drop_table('workbenches', schema='project')
