# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

"""Add index on created_at in project model.

Revision ID: 0009
Revises: 0008
Create Date: 2023-02-15 23:04:51.034401
"""

from alembic import op

revision = '0009'
down_revision = '0008'
branch_labels = None
depends_on = '0008'


def upgrade():
    op.create_index(op.f('ix_project_projects_created_at'), 'projects', ['created_at'], unique=False, schema='project')


def downgrade():
    op.drop_index(op.f('ix_project_projects_created_at'), table_name='projects', schema='project')
