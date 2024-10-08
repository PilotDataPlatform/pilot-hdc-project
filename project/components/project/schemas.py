# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from base64 import urlsafe_b64decode
from datetime import datetime
from typing import Any
from typing import Optional
from uuid import UUID

import magic
from pydantic import HttpUrl
from pydantic import constr
from pydantic import validator

from project.components.schemas import BaseSchema
from project.components.schemas import ListResponseSchema
from project.components.schemas import ParentOptionalFields
from project.config import get_settings


class ProjectSchema(BaseSchema):
    """General project schema."""

    code: constr(min_length=3, max_length=32, regex=r'^[a-z][a-z0-9]*$', strip_whitespace=True)  # noqa: F722
    name: constr(min_length=3, max_length=256, strip_whitespace=True)
    description: constr(max_length=256, strip_whitespace=True) = ''
    logo_name: Optional[constr(max_length=40, strip_whitespace=True)] = None
    tags: list[constr(max_length=256, strip_whitespace=True)] = []
    system_tags: list[constr(max_length=256)] = []
    is_discoverable: bool = False


class ProjectCreateSchema(ProjectSchema):
    """Project schema used for creation."""


class ProjectUpdateSchema(ProjectSchema, metaclass=ParentOptionalFields):
    """Project schema used for update."""


class ProjectResponseSchema(ProjectSchema):
    """Default schema for single project in response."""

    id: UUID
    created_at: datetime
    image_url: Optional[HttpUrl] = None

    class Config:
        orm_mode = True

    @validator('image_url', always=True)
    def set_image_url(cls, _: Any, values: dict[str, Any]) -> Optional[str]:
        if logo_name := values['logo_name']:
            prefix = get_settings().S3_PREFIX_FOR_PROJECT_IMAGE_URLS.rstrip('/')
            return f'{prefix}/{logo_name}'

        return None


class ProjectListResponseSchema(ListResponseSchema):
    """Default schema for multiple projects in response."""

    result: list[ProjectResponseSchema]


class ProjectLogoUploadSchema(BaseSchema):
    """Project logo schema used for image upload."""

    base64: constr(min_length=32, max_length=get_settings().ICON_SIZE_LIMIT)

    @validator('base64')
    def is_valid_image_format_in_base64_string(cls, value: str) -> str:
        try:
            image = urlsafe_b64decode(value)
        except Exception:
            raise ValueError('invalid base64 string')

        mime_type = magic.from_buffer(image, mime=True)
        if mime_type not in ('image/png',):
            raise ValueError('unsupported image format')

        return value

    def get_image(self) -> bytes:
        return urlsafe_b64decode(self.base64)
