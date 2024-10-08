# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import Query
from pydantic import validator

from project.components.parameters import FilterParameters
from project.components.parameters import SortByFields
from project.components.project.filtering import ProjectFiltering


class ProjectSortByFields(SortByFields):
    """Fields by which projects can be sorted."""

    CODE = 'code'
    NAME = 'name'
    CREATED_AT = 'created_at'


class ProjectFilterParameters(FilterParameters):
    """Query parameters for projects filtering."""

    name: Optional[str] = Query(default=None)
    code: Optional[str] = Query(default=None)
    code_any: Optional[str] = Query(default=None)
    description: Optional[str] = Query(default=None)
    created_at_start: Optional[datetime] = Query(default=None)
    created_at_end: Optional[datetime] = Query(default=None)
    tags_all: Optional[str] = Query(default=None)
    is_discoverable: Optional[bool] = Query(default=None)
    ids: Optional[str] = Query(default=None)

    @validator('code_any', 'tags_all')
    def list_split_list_parameters(cls, value: Optional[str]) -> Optional[list[str]]:
        if not value:
            return None

        values = [v.strip() for v in value.split(',')]
        if not all(values):
            raise ValueError('invalid value in the comma-separated list')

        return values

    @validator('ids')
    def list_split_cast_values_to_uuid(cls, value: Optional[str]) -> Optional[list[str]]:
        if not value:
            return None

        values = [UUID(v) for v in value.split(',')]

        return values

    def to_filtering(self) -> ProjectFiltering:
        created_at = None
        if self.created_at_start and self.created_at_end:
            created_at = (self.created_at_start, self.created_at_end)

        return ProjectFiltering(
            name=self.name,
            code=self.code,
            codes=self.code_any,
            description=self.description,
            created_at=created_at,
            tags=self.tags_all,
            is_discoverable=self.is_discoverable,
            ids=self.ids,
        )
