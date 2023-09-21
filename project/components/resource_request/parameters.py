# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Optional

from fastapi import Query

from project.components.parameters import FilterParameters
from project.components.parameters import SortByFields
from project.components.parameters import SortParameters
from project.components.resource_request.filtering import ResourceRequestFiltering
from project.components.resource_request.sorting import ResourceRequestSorting


class ResourceRequestSortByFields(SortByFields):
    """Fields by which resource requests can be sorted."""

    PROJECT_ID = 'project_id'
    USER_ID = 'user_id'
    USERNAME = 'username'
    EMAIL = 'email'
    REQUESTED_FOR = 'requested_for'
    COMPLETED_AT = 'completed_at'
    REQUESTED_AT = 'requested_at'
    PROJECT_NAME = 'project.name'
    PROJECT_CODE = 'project.code'


class ResourceRequestSortParameters(SortParameters):
    """Base query parameters for sorting."""

    def to_sorting(self) -> ResourceRequestSorting:
        field = self.sort_by

        if isinstance(field, SortByFields):
            field = field.value

        return ResourceRequestSorting(field=field, order=self.sort_order)


class ResourceRequestFilterParameters(FilterParameters):
    """Query parameters for resource request filtering."""

    username: Optional[str] = Query(default=None)
    email: Optional[str] = Query(default=None)
    project_code: Optional[str] = Query(default=None)

    def to_filtering(self) -> ResourceRequestFiltering:
        return ResourceRequestFiltering(
            username=self.username,
            email=self.email,
            project_code=self.project_code,
        )
