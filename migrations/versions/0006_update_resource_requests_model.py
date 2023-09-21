# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

"""update Resource requests model.

Revision ID: 0006
Revises: 0005
Create Date: 2022-07-06 10:41:50.362568
"""

import sqlalchemy as sa
from alembic import op

revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = '0005'


def upgrade():
    op.alter_column('resource_requests', 'requested_by_user_id', new_column_name='user_id', schema='project')
    op.add_column('resource_requests', sa.Column('username', sa.VARCHAR(length=256), nullable=False), schema='project')
    op.add_column('resource_requests', sa.Column('email', sa.VARCHAR(length=256), nullable=False), schema='project')
    op.create_index('user_id', 'resource_requests', ['project_id', 'requested_for'], unique=True, schema='project')


def downgrade():
    op.alter_column('resource_requests', 'user_id', new_column_name='requested_by_user_id', schema='project')
    op.drop_index('user_id', table_name='resource_requests', schema='project')
    op.drop_column('resource_requests', 'email', schema='project')
    op.drop_column('resource_requests', 'username', schema='project')
