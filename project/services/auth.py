# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Any
from typing import Optional

import httpx
from common import LoggerFactory
from fastapi import Depends

from project.components.exceptions import ServiceNotAvailable
from project.components.exceptions import UnhandledException
from project.config import Settings
from project.config import get_settings

settings = get_settings()
logger = LoggerFactory(
    __name__,
    level_default=settings.LOG_LEVEL_DEFAULT,
    level_file=settings.LOG_LEVEL_FILE,
    level_stdout=settings.LOG_LEVEL_STDOUT,
    level_stderr=settings.LOG_LEVEL_STDERR,
).get_logger()


class AuthClient:
    """Client to connect with auth service."""

    def __init__(self, auth_service_url: str) -> None:
        self.service_url = auth_service_url + '/v1/'

    async def create_user_groups(self, project_code: str, description: Optional[str] = None) -> None:
        """Creating user groups with auth service."""
        try:
            payload = {'group_name': project_code, 'description': description}
            async with httpx.AsyncClient() as client:
                response = await client.post(self.service_url + 'user/group', json=payload)
                response.raise_for_status()

        except httpx.HTTPStatusError:
            logger.error(
                f'Auth service could not create user groups for project "{project_code}", error {response.text}'
            )
            raise UnhandledException()

        except httpx.RequestError:
            logger.exception(
                f'Unable to connect to the auth service to create user groups for project "{project_code}"'
            )
            raise ServiceNotAvailable()

        except Exception:
            logger.exception(f'Unable to to create user groups for project "{project_code}"')
            raise UnhandledException()

    async def create_user_roles(self, project_code: str) -> None:
        """Creating user roles with auth service."""
        try:
            payload = {'project_roles': ['admin', 'collaborator', 'contributor'], 'project_code': project_code}

            async with httpx.AsyncClient() as client:
                response = await client.post(self.service_url + 'admin/users/realm-roles', json=payload)
                response.raise_for_status()

        except httpx.HTTPStatusError:
            logger.error(
                f'Auth service could not create user roles for project "{project_code}", error {response.text}'
            )
            raise UnhandledException()

        except httpx.RequestError:
            logger.exception(f'Unable to connect to the auth service to create user roles for project "{project_code}"')
            raise ServiceNotAvailable()

        except Exception:
            logger.exception(f'Unable to create user roles for project "{project_code}"')
            raise UnhandledException()

    async def create_default_permissions(self, project_code: str) -> None:
        """Create default RBAC roles for a project."""

        try:
            payload = {'project_code': project_code}

            async with httpx.AsyncClient(timeout=settings.SERVICE_CLIENT_TIMEOUT) as client:
                response = await client.post(self.service_url + 'defaultroles', json=payload)
                response.raise_for_status()
        except httpx.HTTPStatusError:
            logger.error(
                f'Auth service could not create default permissions for project "{project_code}", error {response.text}'
            )
            raise UnhandledException()
        except httpx.RequestError:
            logger.exception(f'Unable to connect to the auth service to create user roles for project "{project_code}"')
            raise ServiceNotAvailable()
        except Exception:
            logger.exception(f'Unable to create default permissions for project "{project_code}"')
            raise UnhandledException()

    async def get_platform_admins(self) -> list[dict[str, Any]]:
        """Getting a list of platform admins from auth service."""
        try:
            payload = {
                'role_names': ['platform-admin'],
                'status': 'active',
                'page_size': 1000,
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(self.service_url + 'admin/roles/users', json=payload)
                response.raise_for_status()

            origin_users = response.json().get('result', [])
            return origin_users

        except httpx.HTTPStatusError:
            logger.error(f'Auth service could not fetch platform admins, error {response.text}')
            raise UnhandledException()

        except httpx.RequestError:
            logger.exception('Unable to connect to the auth service to fetch platform admins')
            raise ServiceNotAvailable()

        except Exception:
            logger.exception('Unable to fetch platform admins')
            raise UnhandledException()


def get_auth_client(settings: Settings = Depends(get_settings)) -> AuthClient:
    """Create a callable dependency for AuthClient."""
    return AuthClient(settings.AUTH_SERVICE)
