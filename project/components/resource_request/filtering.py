# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Optional
from typing import Type

from sqlalchemy.sql import Select

from project.components.filtering import Filtering
from project.components.resource_request.models import ResourceRequest


class ResourceRequestFiltering(Filtering):
    """Resource Request filter params."""

    username: Optional[str] = None
    email: Optional[str] = None
    project_code: Optional[str] = None

    def apply(self, statement: Select, model: Type[ResourceRequest]) -> Select:
        """Apply filter to SQL query."""
        if self.username:
            statement = statement.where(model.username.ilike(self.username))
        if self.email:
            statement = statement.where(model.email.ilike(self.email))
        if self.project_code:
            statement = statement.filter(model.project.has(code=self.project_code))
        return statement
