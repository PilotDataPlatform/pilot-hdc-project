# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Union
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response

from project.components.exceptions import UnhandledException
from project.components.object_storage.policy import PolicyManager
from project.components.object_storage.policy import get_policy_manager
from project.components.parameters import PageParameters
from project.components.parameters import SortParameters
from project.components.project.crud import ProjectCRUD
from project.components.project.dependencies import get_logo_uploader
from project.components.project.dependencies import get_object_storage_manager
from project.components.project.dependencies import get_project_crud
from project.components.project.logo_uploader import LogoUploader
from project.components.project.object_storage_manager import ObjectStorageManager
from project.components.project.parameters import ProjectFilterParameters
from project.components.project.parameters import ProjectSortByFields
from project.components.project.schemas import ProjectCreateSchema
from project.components.project.schemas import ProjectListResponseSchema
from project.components.project.schemas import ProjectLogoUploadSchema
from project.components.project.schemas import ProjectResponseSchema
from project.components.project.schemas import ProjectUpdateSchema
from project.services.auth import AuthClient
from project.services.auth import get_auth_client
from project.services.metadata import MetadataClient
from project.services.metadata import get_metadata_client

router = APIRouter(prefix='/projects', tags=['Projects'])


@router.get('/', summary='List all projects.', response_model=ProjectListResponseSchema)
async def list_projects(
    filter_parameters: ProjectFilterParameters = Depends(),
    sort_parameters: SortParameters.with_sort_by_fields(ProjectSortByFields) = Depends(),
    page_parameters: PageParameters = Depends(),
    project_crud: ProjectCRUD = Depends(get_project_crud),
) -> ProjectListResponseSchema:
    """List all projects."""

    filtering = filter_parameters.to_filtering()
    sorting = sort_parameters.to_sorting()
    pagination = page_parameters.to_pagination()

    async with project_crud:
        page = await project_crud.paginate(pagination, sorting, filtering)

    response = ProjectListResponseSchema.from_page(page)

    return response


@router.get('/{project_id}', summary='Get a project by id or code.', response_model=ProjectResponseSchema)
async def get_project(
    project_id: Union[UUID, str], project_crud: ProjectCRUD = Depends(get_project_crud)
) -> ProjectResponseSchema:
    """Get a project by id or code."""

    async with project_crud:
        project = await project_crud.retrieve_by_id_or_code(project_id)

    return project


@router.post('/', summary='Create a new project.', response_model=ProjectResponseSchema)
async def create_project(
    body: ProjectCreateSchema,
    project_crud: ProjectCRUD = Depends(get_project_crud),
    object_storage_manager: ObjectStorageManager = Depends(get_object_storage_manager),
    policy_manager: PolicyManager = Depends(get_policy_manager),
    auth_client: AuthClient = Depends(get_auth_client),
    metadata_client: MetadataClient = Depends(get_metadata_client),
) -> ProjectResponseSchema:
    """Create a new project."""

    async with project_crud:
        project = await project_crud.create(body)

    try:
        await object_storage_manager.create_buckets_for_project(project_code=project.code)
        await policy_manager.create_policies_for_project(project_code=project.code)
        await auth_client.create_user_groups(project_code=project.code, description=project.description)
        await auth_client.create_user_roles(project_code=project.code)
        await auth_client.create_default_permissions(project_code=project.code)
        platform_admins = await auth_client.get_platform_admins()
        await metadata_client.create_users_name_folders(project_code=project.code, users=platform_admins)
    except Exception:
        await policy_manager.rollback_policies_for_project(project_code=project.code)
        await object_storage_manager.remove_buckets_for_project(project_code=project.code)
        await project_crud.delete(project.id)
        raise UnhandledException()

    return project


@router.patch('/{project_id}', summary='Update a project.', response_model=ProjectResponseSchema)
async def update_project(
    project_id: UUID, body: ProjectUpdateSchema, project_crud: ProjectCRUD = Depends(get_project_crud)
) -> ProjectResponseSchema:
    """Update a project."""

    async with project_crud:
        project = await project_crud.update(project_id, body)

    return project


@router.delete('/{project_id}', summary='Delete a project.')
async def delete_project(project_id: UUID, project_crud: ProjectCRUD = Depends(get_project_crud)) -> Response:
    """Delete a project."""

    async with project_crud:
        await project_crud.delete(project_id)

    response = Response(status_code=204)

    return response


@router.post('/{project_id}/logo', summary='Upload a logo for a project.', response_model=ProjectResponseSchema)
async def upload_project_logo(
    project_id: UUID,
    body: ProjectLogoUploadSchema,
    project_crud: ProjectCRUD = Depends(get_project_crud),
    logo_uploader: LogoUploader = Depends(get_logo_uploader),
) -> ProjectResponseSchema:
    """Upload a logo for a project."""

    async with project_crud:
        await project_crud.retrieve_by_id(project_id)

    image = body.get_image()
    logo_name = f'{project_id}.png'

    await logo_uploader.convert_and_upload(image, logo_name)

    async with project_crud:
        project_update = ProjectUpdateSchema(logo_name=logo_name)
        project = await project_crud.update(project_id, project_update)

    return project
