# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from project.components.object_storage.s3 import S3Client
from project.components.project.crud import ProjectCRUD
from project.components.project.logo_uploader import LogoUploader
from project.components.project.object_storage_manager import ObjectStorageManager
from project.config import Settings
from project.config import get_settings
from project.dependencies import get_db_session
from project.dependencies import get_s3_client


def get_project_crud(db_session: AsyncSession = Depends(get_db_session)) -> ProjectCRUD:
    """Return an instance of ProjectCRUD as a dependency."""

    return ProjectCRUD(db_session)


def get_logo_uploader(
    s3_client: S3Client = Depends(get_s3_client), settings: Settings = Depends(get_settings)
) -> LogoUploader:
    """Return an instance of LogoUploader as a dependency."""

    return LogoUploader(s3_client, settings.S3_BUCKET_FOR_PROJECT_LOGOS)


def get_object_storage_manager(
    s3_client: S3Client = Depends(get_s3_client), settings: Settings = Depends(get_settings)
) -> ObjectStorageManager:
    """Returns an instance of ObjectStorageManager as a dependency."""
    return ObjectStorageManager(s3_client, settings)
