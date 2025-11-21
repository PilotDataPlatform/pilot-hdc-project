# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.
"""Adding unique constaint for project_id, user_id and requested_for.

Revision ID: 0007
Revises: 0006
Create Date: 2022-09-14 14:55:28.345686
"""

from alembic import op

revision = '0007'
down_revision = '0006'
branch_labels = None
depends_on = '0006'


def upgrade():
    op.drop_index('user_id', table_name='resource_requests', schema='project')
    op.create_unique_constraint(
        'user_id_project_id_requested_for',
        'resource_requests',
        ['user_id', 'project_id', 'requested_for'],
        schema='project',
    )


def downgrade():
    op.drop_constraint('user_id_project_id_requested_for', 'resource_requests', schema='project', type_='unique')
    op.create_index('user_id', 'resource_requests', ['project_id', 'requested_for'], unique=False, schema='project')
