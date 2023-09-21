# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import json
from typing import Any
from typing import Optional
from typing import get_type_hints

from pydantic import BaseModel
from pydantic import main

from project.components.pagination import Page


class ParentOptionalFields(main.ModelMetaclass):
    """Annotate as optional all fields of parent classes."""

    def __new__(
        mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any], **kwds: Any
    ) -> 'ParentOptionalFields':
        annotations = namespace.get('__annotations__', {})

        for base in bases:
            fields = get_type_hints(base)
            for name, field in fields.items():
                if name in annotations:
                    continue

                if not name.startswith('__'):
                    field = Optional[field]

                annotations[name] = field

        namespace['__annotations__'] = annotations

        return super().__new__(mcs, name, bases, namespace, **kwds)


class BaseSchema(BaseModel):
    """Base class for all available schemas."""

    def to_payload(self) -> dict[str, str]:
        return json.loads(self.json())


class ListResponseSchema(BaseSchema):
    """Default schema for multiple base schemas in response."""

    num_of_pages: int
    page: int
    total: int
    result: list[BaseSchema]

    @classmethod
    def from_page(cls, page: Page):
        return cls(num_of_pages=page.total_pages, page=page.number, total=page.count, result=page.entries)
