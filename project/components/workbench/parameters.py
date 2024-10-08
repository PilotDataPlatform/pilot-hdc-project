# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Optional

from fastapi import Query

from project.components.parameters import FilterParameters
from project.components.workbench.filtering import WorkbenchFiltering


class WorkbenchFilterParameters(FilterParameters):
    """Query parameters for workbench filtering."""

    project_id: Optional[str] = Query(default=None)

    def to_filtering(self) -> WorkbenchFiltering:
        return WorkbenchFiltering(
            project_id=self.project_id,
        )
