# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from sqlalchemy.sql import Select

from project.components.filtering import Filtering
from project.components.resource_request.models import ResourceRequest


class ResourceRequestFiltering(Filtering):
    """Resource Request filter params."""

    username: str | None = None
    email: str | None = None
    project_code: str | None = None

    def apply(self, statement: Select, model: type[ResourceRequest]) -> Select:
        """Apply filter to SQL query."""
        if self.username:
            statement = statement.where(model.username.ilike(self.username))
        if self.email:
            statement = statement.where(model.email.ilike(self.email))
        if self.project_code:
            statement = statement.filter(model.project.has(code=self.project_code))
        return statement
