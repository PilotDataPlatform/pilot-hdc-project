# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from uuid import uuid4

from sqlalchemy import BOOLEAN
from sqlalchemy import VARCHAR
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from project.components.db_model import DBModel


class Project(DBModel):
    """Project database model."""

    __tablename__ = 'projects'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    code = Column(VARCHAR(length=32), unique=True, index=True, nullable=False)
    name = Column(VARCHAR(length=256), nullable=False)
    description = Column(VARCHAR(length=2048), nullable=False)
    logo_name = Column(VARCHAR(length=40), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, index=True, nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    tags = Column(ARRAY(VARCHAR(256)), default=[], nullable=False)
    system_tags = Column(ARRAY(VARCHAR(256)), default=[], nullable=False)
    is_discoverable = Column(BOOLEAN(), default=True, nullable=False)

    resource_requests = relationship('ResourceRequest', back_populates='project', cascade='all, delete-orphan')
    workbenches = relationship('Workbench', back_populates='project', cascade='all, delete-orphan')
