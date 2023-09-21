# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from datetime import datetime
from typing import Any
from typing import Union
from uuid import UUID

import pytest

from project.components import ResourceRequest
from project.components.models import ModelList
from project.components.resource_request.crud import ResourceRequestCRUD
from project.components.resource_request.schemas import ResourceRequestSchema
from tests.fixtures.components._base_factory import BaseFactory


class ResourceRequestFactory(BaseFactory):
    """Create resource request related entries for testing purposes."""

    def generate(
        self,
        project_id: UUID = ...,
        user_id: str = ...,
        username: str = ...,
        email: str = ...,
        requested_for: str = ...,
        completed_at: datetime = ...,
        vm_connections: Union[dict[str, Any], None] = ...,
        message: Union[str, None] = ...,
    ) -> ResourceRequestSchema:
        if project_id is ...:
            project_id = self.fake.uuid4(cast_to=None)

        if user_id is ...:
            user_id = self.fake.uuid4()

        if username is ...:
            username = self.fake.simple_profile()['username']

        if email is ...:
            email = self.fake.email()

        if requested_for is ...:
            requested_for = self.fake.slug()

        if completed_at is ...:
            completed_at = self.fake.past_datetime()

        if vm_connections is ...:
            vm_connections = {self.fake.text(max_nb_chars=25): ['READ']}

        if message is ...:
            message = self.fake.text(max_nb_chars=100)

        return ResourceRequestSchema(
            project_id=project_id,
            user_id=user_id,
            email=email,
            username=username,
            requested_for=requested_for,
            completed_at=completed_at,
            vm_connections=vm_connections,
            message=message,
        )

    async def create(
        self,
        project_id: UUID = ...,
        user_id: str = ...,
        username: str = ...,
        email: str = ...,
        requested_for: str = ...,
        completed_at: datetime = ...,
    ) -> ResourceRequest:
        entry = self.generate(project_id, user_id, username, email, requested_for, completed_at)

        async with self.crud:
            return await self.crud.create(entry)

    async def bulk_create(
        self,
        number: int,
        project_id: UUID = ...,
        user_id: str = ...,
        requested_for: str = ...,
        completed_at: datetime = ...,
        **kwds: Any,
    ) -> ModelList[ResourceRequest]:
        return ModelList(
            [await self.create(project_id, user_id, requested_for, completed_at, **kwds) for _ in range(number)]
        )


@pytest.fixture
def resource_request_crud(db_session) -> ResourceRequestCRUD:
    yield ResourceRequestCRUD(db_session)


@pytest.fixture
def resource_request_factory(resource_request_crud, fake) -> ResourceRequestFactory:
    yield ResourceRequestFactory(resource_request_crud, fake)
