# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from uuid import uuid4

from sqlalchemy import VARCHAR
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from project.components.db_model import DBModel


class ResourceRequest(DBModel):
    """Resource request database model."""

    __tablename__ = 'resource_requests'
    __table_args__ = (
        UniqueConstraint(
            'user_id',
            'project_id',
            'requested_for',
            name='user_id_project_id_requested_for',
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
    user_id = Column(VARCHAR(length=256), nullable=False)
    username = Column(VARCHAR(length=256), nullable=False)
    email = Column(VARCHAR(length=256), nullable=False)
    requested_for = Column(VARCHAR(length=256), nullable=False)
    requested_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    completed_at = Column(TIMESTAMP(timezone=True), nullable=True)
    message = Column(VARCHAR(length=100), nullable=True)
    vm_connections = Column(JSONB(), nullable=True)

    project = relationship('Project', back_populates='resource_requests')
