# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import pytest
from common import NotFoundError

from project.components.object_storage.policy import get_policy_manager
from project.dependencies import get_s3_client


class TestPolicyManager:
    async def test_policy_manager_creates_policies(self, minio_container, minio_client, settings):
        project_code = 'test-code'
        s3_client = await get_s3_client(settings)
        await s3_client.create_bucket(project_code)
        policy_manager = await get_policy_manager(settings)
        await policy_manager.create_policies_for_project(project_code)
        for role in policy_manager.roles:
            assert await minio_client.get_IAM_policy(project_code + '-' + role.value)

    async def test_policy_manager_rolls_back_created_policies(self, minio_container, minio_client, settings):
        project_code = 'another-test-code'
        s3_client = await get_s3_client(settings)
        await s3_client.create_bucket(project_code)
        policy_manager = await get_policy_manager(settings)
        await policy_manager.create_policies_for_project(project_code)

        await policy_manager.rollback_policies_for_project(project_code)
        for role in policy_manager.roles:
            with pytest.raises(NotFoundError):
                await minio_client.get_IAM_policy(project_code + '-' + role.value)
