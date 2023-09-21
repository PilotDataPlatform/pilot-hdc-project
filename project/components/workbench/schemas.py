# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from uuid import UUID

from project.components.schemas import BaseSchema
from project.components.schemas import ListResponseSchema
from project.components.schemas import ParentOptionalFields


class WorkbenchSchema(BaseSchema):
    """General workbench schema."""

    project_id: UUID
    resource: str = ''
    deployed_by_user_id: str = ''


class WorkbenchCreateSchema(WorkbenchSchema):
    """Workbench schema used for creation."""


class WorkbenchUpdateSchema(WorkbenchSchema, metaclass=ParentOptionalFields):
    """Workbench schema used for update."""


class WorkbenchResponseSchema(WorkbenchSchema):
    """Default schema for single workbench in response."""

    id: UUID
    deployed_at: datetime

    class Config:
        orm_mode = True


class WorkbenchListResponseSchema(ListResponseSchema):
    """Default schema for multiple workbenches in response."""

    result: list[WorkbenchResponseSchema]
