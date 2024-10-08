# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Any

from common import get_boto3_admin_client
from common import get_boto3_client
from common.object_storage_adaptor.boto3_admin_client import Boto3AdminClient
from common.object_storage_adaptor.boto3_client import Boto3Client


class BucketNotFound(Exception):
    """Raised when specified bucket is not found."""


class S3Client:
    """Class that combines two boto3 clients from common package for better usability."""

    boto_client: Boto3Client
    boto_admin_client: Boto3AdminClient

    @classmethod
    async def initialize(cls, endpoint: str, access_key: str, secret_key: str, https: bool = False) -> 'S3Client':
        """Create an instance of S3Client with initialized boto3 clients."""
        s3_client = cls()
        s3_client.boto_client = await get_boto3_client(
            endpoint=endpoint, access_key=access_key, secret_key=secret_key, https=https
        )
        s3_client.boto_admin_client = await get_boto3_admin_client(
            endpoint=endpoint,
            access_key=access_key,
            secret_key=secret_key,
        )
        return s3_client

    async def create_bucket(self, bucket: str) -> dict[str, Any]:
        """Create a bucket in S3."""
        return await self.boto_admin_client.create_bucket(bucket)

    async def set_bucket_versioning(self, bucket: str) -> dict[str, Any]:
        """Set versioning for a bucket."""
        return await self.boto_admin_client.set_bucket_versioning(bucket)

    async def create_bucket_encryption(self, bucket: str) -> dict[str, Any]:
        """Create encryption for a bucket."""
        return await self.boto_admin_client.create_bucket_encryption(bucket)

    async def put_object(self, bucket: str, key: str, file: bytes) -> dict[str, Any]:
        """Upload a single file to S3."""
        async with self.boto_client._session.client(
            's3', endpoint_url=self.boto_client.endpoint, config=self.boto_client._config
        ) as s3:
            try:
                res = await s3.put_object(Bucket=bucket, Key=key, Body=file)
                return res
            except s3.exceptions.NoSuchBucket:
                raise BucketNotFound

    async def remove_bucket(self, bucket: str) -> dict[str, Any]:
        """Delete a bucket from S3."""
        async with self.boto_admin_client._session.client(
            's3', endpoint_url=self.boto_admin_client.endpoint, config=self.boto_admin_client._config
        ) as s3:
            try:
                res = await s3.delete_bucket(Bucket=bucket)
                return res
            except s3.exceptions.NoSuchBucket:
                raise BucketNotFound
