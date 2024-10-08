# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import json

import pytest

from project.components.exceptions import ServiceNotAvailable
from project.components.exceptions import UnhandledException
from project.config import Settings
from project.services.metadata import MetadataClient


@pytest.fixture
def metadata_client(settings: Settings) -> MetadataClient:
    return MetadataClient(settings.METADATA_SERVICE)


class TestMetadataClient:
    async def test_create_users_name_folders_sends_folders_to_create(self, httpx_mock, metadata_client):
        httpx_mock.add_response(method='POST', url=metadata_client.service_url + 'items/batch/', status_code=200)
        await metadata_client.create_users_name_folders([{'name': 'test'}], 'test_code')
        request = httpx_mock.get_request()
        assert b'test_code' in request.content
        body = json.loads(request.content)
        assert len(body['items']) == len(metadata_client.zones)

    async def test_create_users_name_folders_raises_exception_on_wrong_status_code_from_metadata(
        self, httpx_mock, metadata_client
    ):
        httpx_mock.add_response(method='POST', url=metadata_client.service_url + 'items/batch/', status_code=500)
        with pytest.raises(UnhandledException):
            await metadata_client.create_users_name_folders([{'name': 'test'}], 'test_code')

    async def test_create_users_name_folders_raises_exception_on_timeout_from_metadata(self, metadata_client):
        with pytest.raises(ServiceNotAvailable):
            await metadata_client.create_users_name_folders([{'name': 'test'}], 'test_code')
