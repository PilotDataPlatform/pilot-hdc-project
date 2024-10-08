# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import hashlib
from enum import Enum

import httpx
from common import get_minio_policy_client
from common.object_storage_adaptor.minio_policy_client import MinioPolicyClient
from common.object_storage_adaptor.minio_policy_client import NotFoundError
from fastapi import Depends
from minio.helpers import url_replace
from minio.signer import sign_v4_s3

from project.components.object_storage.policy_templates import TEMPLATES_LIBRARY
from project.config import Settings
from project.config import get_settings


class Roles(Enum):
    ADMIN = 'admin'
    CONTRIBUTOR = 'contributor'
    COLLABORATOR = 'collaborator'


class PolicyManager:
    """Manager for project policies."""

    def __init__(self, minio_policy_client: MinioPolicyClient):
        self.minio_policy_client = minio_policy_client
        self.roles = Roles
        self.templates = TEMPLATES_LIBRARY

    async def create_policies_for_project(self, project_code: str) -> None:
        """Add MinIO policies for respective project buckets users."""
        for role in self.roles:
            policy_content = self.templates[role.value](project_code)
            await self.minio_policy_client.create_IAM_policy(project_code + '-' + role.value, policy_content)

    async def remove_IAM_policy(self, policy_name: str, region: str = 'us-east-1') -> str:
        """
        Summary:
            The function will delete the IAM policy in minio server.

        Parameter:
            - policy_name(str): the policy name to get
            - region(str): the region of service (default is us-east-1)
        """
        self.minio_policy_client.logger.info('Remove policy: %s', policy_name)

        # fetch the credential to generate headers
        creds = self.minio_policy_client._provider.retrieve() if self.minio_policy_client._provider else None

        # use native BaseURL class to follow the pattern
        params = {'name': policy_name}
        url = self.minio_policy_client._base_url.build('DELETE', region, query_params=params)
        url = url_replace(url, path='/minio/admin/v3/remove-canned-policy')

        headers = None
        headers, date = self.minio_policy_client._build_headers(url.netloc, headers, '', creds)
        # make the signiture of request
        content_hash = hashlib.sha256(''.encode()).hexdigest()
        headers = sign_v4_s3('DELETE', url, region, headers, creds, content_hash, date)

        # sending to minio server to remove IAM policy
        str_endpoint = url.scheme + '://' + url.netloc
        async with httpx.AsyncClient() as client:
            response = await client.delete(
                str_endpoint + url.path,
                params=params,
                headers=headers,
            )

        if response.status_code == 404:
            error_msg = f'Policy {policy_name} does not exist'
            self.minio_policy_client.logger.error(error_msg)
            raise NotFoundError(error_msg)
        elif response.status_code != 200:
            error_msg = f'Fail to remove minio policy: {response.text}'
            self.minio_policy_client.logger.error(error_msg)
            raise Exception(error_msg)

        return 'success'

    async def rollback_policies_for_project(self, project_code: str) -> None:
        """Remove MinIO policies for respective project buckets users."""
        for role in self.roles:
            await self.remove_IAM_policy(project_code + '-' + role.value)


async def get_policy_manager(settings: Settings = Depends(get_settings)) -> PolicyManager:
    s3_endpoint = settings.S3_HOST + ':' + str(settings.S3_PORT)
    minio_client = await get_minio_policy_client(
        s3_endpoint, settings.S3_ACCESS_KEY, settings.S3_SECRET_KEY, https=settings.S3_HTTPS_ENABLED
    )
    return PolicyManager(minio_client)
