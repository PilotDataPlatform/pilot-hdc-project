# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from enum import IntEnum
from typing import Any

import httpx
from common import LoggerFactory
from fastapi import Depends

from project.components.exceptions import ServiceNotAvailable
from project.components.exceptions import UnhandledException
from project.components.types import StrEnum
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


class Zones(IntEnum):
    GREENROOM = 0
    CORE = 1


class ItemStatus(StrEnum):
    """Available statuses a file can have in the metadata service."""

    REGISTERED = 'REGISTERED'  # file created but uploading is not complete yet, either in progress or failed
    ACTIVE = 'ACTIVE'  # file uploading is complete.
    ARCHIVED = 'ARCHIVED'  # file has been deleted

    def __str__(self) -> str:
        return str(self.name)


class MetadataClient:
    """Client to connect with metadata service."""

    def __init__(self, metadata_service_url: str) -> None:
        self.service_url = metadata_service_url + '/v1/'
        self.zones = Zones

    def generate_user_folder_payload(self, users: list[dict[str, Any]], project_code: str):
        folders = []
        for zone in self.zones:
            for user in users:
                folders.append(
                    {
                        'name': user['name'],
                        'zone': zone.value,
                        'type': 'name_folder',
                        'status': ItemStatus.ACTIVE,
                        'owner': user['name'],
                        'container_code': project_code,
                        'container_type': 'project',
                        'size': 0,
                        'location_uri': '',
                        'version': '',
                    }
                )
        return folders

    async def create_users_name_folders(self, users: list[dict[str, Any]], project_code: str) -> None:
        """Bulk create folders for project through metadata service."""
        try:
            folders = self.generate_user_folder_payload(users, project_code)
            async with httpx.AsyncClient() as client:
                response = await client.post(self.service_url + 'items/batch/', json={'items': folders})
                response.raise_for_status()

        except httpx.HTTPStatusError:
            logger.error(
                f'Metadata service could not create folders for project "{project_code}", error {response.text}'
            )
            raise UnhandledException()

        except httpx.RequestError:
            logger.exception(f'Unable to connect to the metadata service to create folder for project "{project_code}"')
            raise ServiceNotAvailable()

        except Exception:
            logger.exception(f'Unable to to create folders for project "{project_code}"')
            raise UnhandledException()


def get_metadata_client(settings: Settings = Depends(get_settings)) -> MetadataClient:
    """Create a callable dependency for MetadataClient."""
    return MetadataClient(settings.METADATA_SERVICE)
