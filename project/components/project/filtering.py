# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from uuid import UUID

from sqlalchemy.sql import Select

from project.components.filtering import Filtering
from project.components.project import Project


class ProjectFiltering(Filtering):
    """Projects filtering control parameters."""

    name: str | None = None
    code: str | None = None
    codes: list[str] | None = None
    description: str | None = None
    created_at: tuple[datetime, datetime] | None = None
    tags: list[str] | None = None
    is_discoverable: bool | None = None
    ids: list[UUID] | None = None

    def apply(self, statement: Select, model: type[Project]) -> Select:
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
