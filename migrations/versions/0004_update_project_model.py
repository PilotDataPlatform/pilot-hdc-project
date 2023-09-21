# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

"""Update Project model.

Revision ID: 0004
Revises: 0003
Create Date: 2022-05-10 19:38:40.132501
"""

import sqlalchemy as sa
from alembic import op

revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = '0003'


def upgrade():
    op.alter_column(
        'projects',
        'description',
        type_=sa.VARCHAR(length=2048),
        schema='project',
    )
    op.alter_column(
        'projects',
        'image_url',
        new_column_name='logo_name',
        type_=sa.VARCHAR(length=40),
        schema='project',
    )


def downgrade():
    op.alter_column(
        'projects',
        'description',
        type_=sa.VARCHAR(length=256),
        schema='project',
    )
    op.alter_column(
        'projects',
        'logo_name',
        new_column_name='image_url',
        type_=sa.VARCHAR(length=2083),
        schema='project',
    )
