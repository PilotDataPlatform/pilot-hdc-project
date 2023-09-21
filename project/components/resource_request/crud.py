# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from sqlalchemy.future import select
from sqlalchemy.orm import contains_eager
from sqlalchemy.sql import Select

from project.components.crud import CRUD
from project.components.project.models import Project
from project.components.resource_request.models import ResourceRequest


class ResourceRequestCRUD(CRUD):
    """CRUD for managing resource request database models."""

    model = ResourceRequest

    @property
    def select_query(self) -> Select:
        """Return base select including join with Project model."""
        return select(self.model).join(Project).options(contains_eager(self.model.project))
