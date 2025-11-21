# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Optional

from fastapi import Query
from pydantic import BaseModel
from pydantic import create_model

from project.components.filtering import Filtering
from project.components.pagination import Pagination
from project.components.sorting import Sorting
from project.components.sorting import SortingOrder
from project.components.types import StrEnum


class QueryParameters(BaseModel):
    """Base class for class-based query parameters definition."""


class PageParameters(QueryParameters):
    """Base query parameters for pagination."""

    page: int = Query(default=0, ge=0)
    page_size: int = Query(default=20, ge=1)

    def to_pagination(self) -> Pagination:
        return Pagination(page=self.page, page_size=self.page_size)


class SortByFields(StrEnum):
    """Base class for defining sort by fields."""


class SortParameters(QueryParameters):
    """Base query parameters for sorting."""

    sort_by: str | None = Query(default=None)
    sort_order: SortingOrder | None = Query(default=SortingOrder.ASC)

    @classmethod
    def with_sort_by_fields(cls, fields: type[SortByFields]) -> type['SortParameters']:
        """Limit sort_by field with values specified in fields argument."""

        return create_model(cls.__name__, __base__=cls, sort_by=(Optional[fields], Query(default=None)))

    def to_sorting(self) -> Sorting:
        field = self.sort_by

        if isinstance(field, SortByFields):
            field = field.value

        return Sorting(field=field, order=self.sort_order)


class FilterParameters(QueryParameters):
    """Base query parameters for filtering."""

    def to_filtering(self) -> Filtering:
        raise NotImplementedError
