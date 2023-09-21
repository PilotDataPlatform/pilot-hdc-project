# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

"""Adding vm_connections and message fields.

Revision ID: 0008
Revises: 0007
Create Date: 2022-10-28 13:41:16.864378
"""

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision = '0008'
down_revision = '0007'
branch_labels = None
depends_on = '0007'


def upgrade():
    op.add_column('resource_requests', sa.Column('message', sa.VARCHAR(length=100), nullable=True), schema='project')
    op.add_column(
        'resource_requests',
        sa.Column('vm_connections', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        schema='project',
    )


def downgrade():
    op.drop_column('resource_requests', 'vm_connections', schema='project')
    op.drop_column('resource_requests', 'message', schema='project')
