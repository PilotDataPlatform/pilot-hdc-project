# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from typing import Optional
from typing import Type
from uuid import UUID

from sqlalchemy.sql import Select

from project.components.filtering import Filtering
from project.components.project import Project


class ProjectFiltering(Filtering):
    """Projects filtering control parameters."""

    name: Optional[str] = None
    code: Optional[str] = None
    codes: Optional[list[str]] = None
    description: Optional[str] = None
    created_at: Optional[tuple[datetime, datetime]] = None
    tags: Optional[list[str]] = None
    is_discoverable: Optional[bool] = None
    ids: Optional[list[UUID]] = None

    def apply(self, statement: Select, model: Type[Project]) -> Select:
        """Return statement with applied filtering."""

        if self.name:
            statement = statement.where(model.name.ilike(self.name))

        if self.code:
            statement = statement.where(model.code.ilike(self.code))

        if self.codes:
            statement = statement.where(model.code.in_(self.codes))

        if self.description:
            statement = statement.where(model.description.ilike(self.description))

        if self.created_at:
            statement = statement.where(model.created_at.between(*self.created_at))

        if self.tags:
            statement = statement.where(model.tags.contains(self.tags))

        if self.is_discoverable is not None:
            statement = statement.where(model.is_discoverable == self.is_discoverable)

        if self.ids:
            statement = statement.where(model.id.in_(self.ids))

        return statement
