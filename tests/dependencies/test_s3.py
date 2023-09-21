# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from project.dependencies import get_s3_client


class TestS3Client:
    async def test_s3_client_creates_bucket(self, settings, minio_container, s3_test_client):
        s3_client = await get_s3_client(settings)
        await s3_client.create_bucket('test-bucket')
        assert s3_test_client.check_if_bucket_exists('test-bucket')

    async def test_s3_client_removes_bucket(self, settings, minio_container, s3_test_client):
        s3_client = await get_s3_client(settings)
        await s3_client.create_bucket('another-bucket')
        assert s3_test_client.check_if_bucket_exists('another-bucket')
        await s3_client.remove_bucket('another-bucket')
        assert not s3_test_client.check_if_bucket_exists('another-bucket')

    async def test_s3_client_puts_object(self, settings, minio_container, s3_test_client, fake):
        s3_client = await get_s3_client(settings)
        await s3_client.create_bucket('file-bucket')
        image = fake.image()
        filename = fake.file_name(extension='png')
        await s3_client.put_object('file-bucket', filename, image)
        assert s3_test_client.check_if_file_exists('file-bucket', filename)
