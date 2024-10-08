# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from sqlalchemy.sql import Select

from project.components.project.models import Project
from project.components.resource_request.models import ResourceRequest
from project.components.sorting import Sorting


class ResourceRequestSorting(Sorting):
    """Resource request sorting control parameters."""

    def apply(self, statement: Select, model: ResourceRequest) -> Select:
        """Return statement with applied ordering.

        This is necessary to allow sorting by fields from the relationship model.
        """
        try:
            _, relationship_field = self.field.split('.', 1)
            self.field = relationship_field
            model = Project
        except ValueError:
            pass
        return super().apply(statement, model)
