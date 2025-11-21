# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from sqlalchemy.sql import Select

from project.components.filtering import Filtering
from project.components.workbench import Workbench


class WorkbenchFiltering(Filtering):
    """Workbenches filtering control parameters."""

    project_id: str | None = None

    def apply(self, statement: Select, model: type[Workbench]) -> Select:
        """Return statement with applied filtering."""

        if self.project_id:
            statement = statement.where(model.project_id == self.project_id)

        return statement
