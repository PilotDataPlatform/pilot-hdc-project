# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from uuid import uuid4

from sqlalchemy import VARCHAR
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from project.components.db_model import DBModel


class Workbench(DBModel):
    """Workbench database model."""

    __tablename__ = 'workbenches'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    project_id = Column(UUID(as_uuid=True), ForeignKey('projects.id'), nullable=False)
    resource = Column(VARCHAR(length=256), nullable=False)
    deployed_at = Column(TIMESTAMP(timezone=True), default=datetime.utcnow, nullable=False)
    deployed_by_user_id = Column(VARCHAR(length=256), nullable=False)

    project = relationship('Project', back_populates='workbenches')
