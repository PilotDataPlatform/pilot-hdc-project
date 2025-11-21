# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import EmailStr

from project.components.schemas import BaseSchema
from project.components.schemas import ListResponseSchema
from project.components.schemas import ParentOptionalFields


class ResourceRequestSchema(BaseSchema):
    """General resource request schema."""

    project_id: UUID
    user_id: str
    email: EmailStr
    username: str
    requested_for: str
    completed_at: datetime | None = None
    message: str | None = None
    vm_connections: dict[str, Any] | None = None


class EmbeddedProjectSchema(BaseSchema):
    """Project schema embedded into resource request."""

    code: str
    name: str

    class Config:
        orm_mode = True


class ResourceRequestCreateSchema(ResourceRequestSchema):
    """Resource request schema used for creation."""


class ResourceRequestUpdateSchema(ResourceRequestSchema, metaclass=ParentOptionalFields):
    """Resource request schema used for update."""


class ResourceRequestResponseSchema(ResourceRequestSchema):
    """Default schema for single resource request in response."""

    id: UUID
    project: EmbeddedProjectSchema
    requested_at: datetime

    class Config:
        orm_mode = True


class ResourceRequestListResponseSchema(ListResponseSchema):
    """Default schema for multiple resource requests in response."""

    result: list[ResourceRequestResponseSchema]
