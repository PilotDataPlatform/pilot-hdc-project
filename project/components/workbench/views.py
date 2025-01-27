# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from typing import Union
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response

from project.components.parameters import PageParameters
from project.components.workbench.crud import WorkbenchCRUD
from project.components.workbench.dependencies import get_workbench_crud
from project.components.workbench.parameters import WorkbenchFilterParameters
from project.components.workbench.schemas import WorkbenchCreateSchema
from project.components.workbench.schemas import WorkbenchListResponseSchema
from project.components.workbench.schemas import WorkbenchResponseSchema
from project.components.workbench.schemas import WorkbenchUpdateSchema

router = APIRouter(prefix='/workbenches', tags=['Workbenches'])


@router.get('/', summary='List all workbenches.', response_model=WorkbenchListResponseSchema)
async def list_workbenches(
    filter_parameters: WorkbenchFilterParameters = Depends(),
    page_parameters: PageParameters = Depends(),
    workbench_crud: WorkbenchCRUD = Depends(get_workbench_crud),
) -> WorkbenchListResponseSchema:
    """List all workbenches."""
    filtering = filter_parameters.to_filtering()
    pagination = page_parameters.to_pagination()

    page = await workbench_crud.paginate(pagination, filtering=filtering)

    response = WorkbenchListResponseSchema.from_page(page)

    return response


@router.get('/{workbench_id}', summary='Get a workbench by id.', response_model=WorkbenchResponseSchema)
async def get_workbench(
    workbench_id: Union[UUID, str], workbench_crud: WorkbenchCRUD = Depends(get_workbench_crud)
) -> WorkbenchResponseSchema:
    """Get a workbench by id."""

    workbench = await workbench_crud.retrieve_by_id(workbench_id)

    return workbench


@router.post('/', summary='Create a new workbench.', response_model=WorkbenchResponseSchema)
async def create_workbench(
    body: WorkbenchCreateSchema, workbench_crud: WorkbenchCRUD = Depends(get_workbench_crud)
) -> WorkbenchResponseSchema:
    """Create a new workbench."""

    async with workbench_crud:
        workbench = await workbench_crud.create(body)

    return workbench


@router.patch('/{workbench_id}', summary='Update a workbench.', response_model=WorkbenchResponseSchema)
async def update_workbench(
    workbench_id: UUID, body: WorkbenchUpdateSchema, workbench_crud: WorkbenchCRUD = Depends(get_workbench_crud)
) -> WorkbenchResponseSchema:
    """Update a workbench."""

    async with workbench_crud:
        workbench = await workbench_crud.update(workbench_id, body)

    return workbench


@router.delete('/{workbench_id}', summary='Delete a workbench.')
async def delete_workbench(workbench_id: UUID, workbench_crud: WorkbenchCRUD = Depends(get_workbench_crud)) -> Response:
    """Delete a workbench."""

    async with workbench_crud:
        await workbench_crud.delete(workbench_id)

    response = Response(status_code=204)

    return response
