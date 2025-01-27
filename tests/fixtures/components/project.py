# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Any

import pytest

from project.components import ModelList
from project.components import Project
from project.components.project.crud import ProjectCRUD
from project.components.project.schemas import ProjectSchema
from tests.fixtures.components._base_factory import BaseFactory


class ProjectFactory(BaseFactory):
    """Create project related entries for testing purposes."""

    def generate(
        self,
        code: str = ...,
        name: str = ...,
        description: str = ...,
        logo_name: str = ...,
        tags: list[str] = ...,
        system_tags: list[str] = ...,
        is_discoverable: bool = ...,
    ) -> ProjectSchema:
        if code is ...:
            code = self.fake.pystr_format('?#' * 10).lower()

        if name is ...:
            name = code

        if description is ...:
            description = self.fake.sentence()

        if logo_name is ...:
            logo_name = self.fake.file_name(extension='png')

        if tags is ...:
            tags = self.fake.words(3, unique=True)

        if system_tags is ...:
            system_tags = self.fake.words(2, unique=True)

        if is_discoverable is ...:
            is_discoverable = True

        return ProjectSchema(
            code=code,
            name=name,
            description=description,
            logo_name=logo_name,
            tags=tags,
            system_tags=system_tags,
            is_discoverable=is_discoverable,
        )

    async def create(
        self,
        code: str = ...,
        name: str = ...,
        description: str = ...,
        logo_name: str = ...,
        tags: list[str] = ...,
        system_tags: list[str] = ...,
        is_discoverable: bool = ...,
        **kwds: Any,
    ) -> Project:
        entry = self.generate(code, name, description, logo_name, tags, system_tags, is_discoverable)

        async with self.crud:
            return await self.crud.create(entry, **kwds)

    async def bulk_create(
        self,
        number: int,
        code: str = ...,
        name: str = ...,
        description: str = ...,
        logo_name: str = ...,
        tags: list[str] = ...,
        system_tags: list[str] = ...,
        is_discoverable: bool = ...,
        **kwds: Any,
    ) -> ModelList[Project]:
        return ModelList(
            [
                await self.create(code, name, description, logo_name, tags, system_tags, is_discoverable, **kwds)
                for _ in range(number)
            ]
        )


@pytest.fixture
def project_crud(db_session) -> ProjectCRUD:
    yield ProjectCRUD(db_session)


@pytest.fixture
def project_factory(project_crud, fake) -> ProjectFactory:
    yield ProjectFactory(project_crud, fake)
