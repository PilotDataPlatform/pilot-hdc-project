# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import magic
import pytest

from project.components.project.logo_uploader import LogoUploader
from project.dependencies import get_s3_client


@pytest.fixture(scope='session')
async def logo_uploader(settings) -> LogoUploader:
    s3_client = await get_s3_client(settings)
    yield LogoUploader(s3_client, settings.S3_BUCKET_FOR_PROJECT_LOGOS)


class TestLogoUploader:
    def test_convert_sync_returns_converted_png_image(self, logo_uploader, fake):
        image = fake.image()

        converted_image = logo_uploader.convert_sync(image)
        received_mime_type = magic.from_buffer(converted_image, mime=True)

        assert received_mime_type == 'image/png'

    async def test_convert_returns_converted_png_image(self, logo_uploader, fake):
        image = fake.image()

        converted_image = await logo_uploader.convert(image)
        received_mime_type = magic.from_buffer(converted_image, mime=True)

        assert received_mime_type == 'image/png'

    async def test_convert_and_upload_uploads_image_after_bucket_creation(
        self, logo_uploader, fake, s3_test_client, minio_container
    ):
        image = fake.image()
        filename = fake.file_name(extension='png')

        logo_uploader.s3_bucket_name = fake.word()

        await logo_uploader.convert_and_upload(image, filename)
        assert s3_test_client.check_if_bucket_exists(logo_uploader.s3_bucket_name)
        assert s3_test_client.check_if_file_exists(logo_uploader.s3_bucket_name, filename)
