# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import asyncio
from functools import partial
from io import BytesIO

from PIL import Image

from project.components.object_storage.s3 import BucketNotFound
from project.dependencies.s3 import S3Client
from project.logger import logger


class LogoUploader:
    """Perform image conversion and upload to S3 bucket."""

    def __init__(self, s3_client: S3Client, s3_bucket_name: str) -> None:
        self.s3_client = s3_client
        self.s3_bucket_name = s3_bucket_name

    def convert_sync(self, image: bytes, resize_size: tuple[int, int] = (200, 200), output_type: str = 'PNG') -> bytes:
        """Convert and resize image synchronously."""

        buffer = BytesIO()

        try:
            img = Image.open(BytesIO(image))
            img = img.resize(resize_size, Image.Resampling.LANCZOS)
            img.save(buffer, output_type)
        except Exception:
            logger.exception('Unable to convert image.')
            raise

        return buffer.getvalue()

    async def convert(self, image: bytes) -> bytes:
        """Convert and resize image."""

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, partial(self.convert_sync, image))

    async def upload(self, image: bytes, filename: str) -> None:
        """Upload image to S3 bucket."""

        try:
            logger.info(f'Trying to upload file "{filename}" into the "{self.s3_bucket_name}" bucket')
            await self.s3_client.put_object(bucket=self.s3_bucket_name, key=filename, file=image)
            logger.info(f'File "{filename}" has been uploaded to the "{self.s3_bucket_name}" bucket.')
        except BucketNotFound:
            raise
        except Exception:
            logger.exception(f'Unable to upload file "{filename}" into the "{self.s3_bucket_name}" bucket.')
            raise

    async def create_bucket(self) -> None:
        """Create new S3 bucket."""
        try:
            logger.info(f'Trying to create bucket "{self.s3_bucket_name}".')
            await self.s3_client.create_bucket(self.s3_bucket_name)
        except Exception:
            logger.exception(f'Unable to create bucket "{self.s3_bucket_name}".')
            raise

    async def convert_and_upload(self, image: bytes, filename: str) -> None:
        """Convert image and upload to S3 bucket.

        Create bucket if it does not exist.
        """

        converted_image = await self.convert(image)

        try:
            await self.upload(converted_image, filename)
        except BucketNotFound:
            logger.exception(f'Bucket "{self.s3_bucket_name}" does not exist.')
            await self.create_bucket()
            await self.upload(converted_image, filename)
