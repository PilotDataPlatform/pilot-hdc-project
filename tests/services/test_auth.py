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
from project.services.auth import AuthClient


@pytest.fixture
def auth_client(settings: Settings) -> AuthClient:
    return AuthClient(settings.AUTH_SERVICE, settings.SERVICE_CLIENT_TIMEOUT)


class TestAuthClient:
    async def test_create_user_group_send_correct_payload(self, httpx_mock, auth_client):
        httpx_mock.add_response(method='POST', url=auth_client.service_url + 'user/group', status_code=200)
        await auth_client.create_user_groups('test_code', 'some description')
        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body.get('group_name') == 'test_code'
        assert body.get('description') == 'some description'

    async def test_create_user_roles_send_correct_payload(self, httpx_mock, auth_client):
        httpx_mock.add_response(method='POST', url=auth_client.service_url + 'admin/users/realm-roles', status_code=200)
        await auth_client.create_user_roles('test_code')
        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body.get('project_code') == 'test_code'
        assert set(body.get('project_roles')) == {'admin', 'collaborator', 'contributor'}

    async def test_get_platform_admins_return_correct_result(self, httpx_mock, auth_client):
        httpx_mock.add_response(
            method='POST',
            url=auth_client.service_url + 'admin/roles/users',
            status_code=200,
            json={'result': [{'name': 'test'}, {'name': 'user'}]},
        )
        res = await auth_client.get_platform_admins()
        assert len(res) == 2
        assert {'name': 'test'} in res
        assert {'name': 'user'} in res

    async def test_create_user_groups_raises_exception_on_wrong_status_code_from_auth(self, httpx_mock, auth_client):
        httpx_mock.add_response(method='POST', url=auth_client.service_url + 'user/group', status_code=500)
        with pytest.raises(UnhandledException):
            await auth_client.create_user_groups('test_code', 'some description')

    async def test_create_user_roles_raises_exception_on_wrong_status_code_from_auth(self, httpx_mock, auth_client):
        httpx_mock.add_response(method='POST', url=auth_client.service_url + 'admin/users/realm-roles', status_code=500)
        with pytest.raises(UnhandledException):
            await auth_client.create_user_roles('test_code')

    async def test_get_platform_admins_raises_exception_on_wrong_status_code_from_auth(self, httpx_mock, auth_client):
        httpx_mock.add_response(method='POST', url=auth_client.service_url + 'admin/roles/users', status_code=500)
        with pytest.raises(UnhandledException):
            await auth_client.get_platform_admins()

    async def test_create_user_groups_raises_exception_on_timeout_from_auth(self, auth_client):
        with pytest.raises(ServiceNotAvailable):
            await auth_client.create_user_groups('test_code', 'some description')

    async def test_create_user_roles_raises_exception_on_timeout_from_auth(self, auth_client):
        with pytest.raises(ServiceNotAvailable):
            await auth_client.create_user_roles('test_code')

    async def test_get_platform_admins_raises_exception_on_timeout_from_auth(self, auth_client):
        with pytest.raises(ServiceNotAvailable):
            await auth_client.get_platform_admins()

    async def test_create_default_permissions_send_correct_payload_200(self, httpx_mock, auth_client):
        project_code = 'test_project'
        httpx_mock.add_response(method='POST', url=auth_client.service_url + 'defaultroles', status_code=200)
        await auth_client.create_default_permissions(project_code)
        request = httpx_mock.get_request()
        body = json.loads(request.content)
        assert body.get('project_code') == project_code

    async def test_create_default_permissions_raises_exception_on_wrong_status_code_from_auth_500(
        self, httpx_mock, auth_client
    ):
        project_code = 'test_project'
        httpx_mock.add_response(method='POST', url=auth_client.service_url + 'defaultroles', status_code=500)
        with pytest.raises(UnhandledException):
            await auth_client.create_default_permissions(project_code)

    async def test_create_default_permissions_raises_exception_on_timeout_from_auth(self, httpx_mock, auth_client):
        project_code = 'test_project'
        with pytest.raises(ServiceNotAvailable):
            await auth_client.create_default_permissions(project_code)
