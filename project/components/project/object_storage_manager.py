# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from common import LoggerFactory

from project.components.object_storage.s3 import BucketNotFound
from project.components.object_storage.s3 import S3Client
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


class ObjectStorageManager:
    def __init__(self, s3_client: S3Client, settings: Settings) -> None:
        self.s3_client = s3_client
        self.settings = settings

    async def create_bucket(self, bucket_name: str) -> None:
        """Create a bucket and set versioning for it."""
        logger.info(f'Creating bucket {bucket_name}')
        await self.s3_client.create_bucket(bucket_name)

        if self.settings.S3_GATEWAY_ENABLED is False:
            logger.info(f'S3 Gateway is disabled, add versioning for {bucket_name}')
            await self.s3_client.set_bucket_versioning(bucket_name)
        else:
            logger.warning(f'S3 Gateway is enabled, versioning for {bucket_name} will not be enabled by API')

        if self.settings.S3_BUCKET_ENCRYPTION_ENABLED:
            logger.info(f'Bucket encryption enabled, encrypting {bucket_name}')
            await self.s3_client.create_bucket_encryption(bucket_name)
        else:
            logger.warning(f'Bucket encryption is not enabled, not encrypting {bucket_name}')

    async def create_buckets_for_project(self, project_code: str) -> None:
        """Create all the required buckets for the project."""
        logger.info(f'Creating buckets for project {project_code}')
        for bucket_prefix in self.settings.S3_BUCKET_ZONE_PREFIXES:
            bucket_name = bucket_prefix + '-' + project_code
            await self.create_bucket(bucket_name)

    async def remove_bucket(self, bucket_name: str) -> None:
        """Remove a bucket."""
        logger.info(f'Removing bucket {bucket_name}')
        await self.s3_client.remove_bucket(bucket_name)

    async def remove_buckets_for_project(self, project_code: str) -> None:
        """Remove all the created buckets for the project."""
        logger.info(f'Removing all buckets for project {project_code}')
        try:
            for bucket_prefix in self.settings.S3_BUCKET_ZONE_PREFIXES:
                bucket_name = bucket_prefix + '-' + project_code
                await self.remove_bucket(bucket_name)
        except BucketNotFound:
            pass
