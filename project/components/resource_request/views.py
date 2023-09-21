# Copyright (C) 2022-2023 Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE, Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi.responses import Response

from project.components.parameters import PageParameters
from project.components.resource_request.crud import ResourceRequestCRUD
from project.components.resource_request.dependencies import get_resource_request_crud
from project.components.resource_request.parameters import ResourceRequestFilterParameters
from project.components.resource_request.parameters import ResourceRequestSortByFields
from project.components.resource_request.parameters import ResourceRequestSortParameters
from project.components.resource_request.schemas import ResourceRequestCreateSchema
from project.components.resource_request.schemas import ResourceRequestListResponseSchema
from project.components.resource_request.schemas import ResourceRequestResponseSchema
from project.components.resource_request.schemas import ResourceRequestUpdateSchema

router = APIRouter(prefix='/resource-requests', tags=['Resource Requests'])


@router.get('/', summary='List all resource requests.', response_model=ResourceRequestListResponseSchema)
async def list_resource_requests(
    page_parameters: PageParameters = Depends(),
    sort_parameters: ResourceRequestSortParameters.with_sort_by_fields(ResourceRequestSortByFields) = Depends(),
    filter_params: ResourceRequestFilterParameters = Depends(),
    resource_request_crud: ResourceRequestCRUD = Depends(get_resource_request_crud),
) -> ResourceRequestListResponseSchema:
    """List all resource requests."""

    sorting = sort_parameters.to_sorting()
    pagination = page_parameters.to_pagination()
    filtering = filter_params.to_filtering()

    page = await resource_request_crud.paginate(pagination, sorting, filtering)

    response = ResourceRequestListResponseSchema.from_page(page)

    return response


@router.get(
    '/{resource_request_id}',
    summary='Get a resource request by id.',
    response_model=ResourceRequestResponseSchema,
)
async def get_resource_request(
    resource_request_id: UUID, resource_request_crud: ResourceRequestCRUD = Depends(get_resource_request_crud)
) -> ResourceRequestResponseSchema:
    """Get a resource request by id."""

    resource_request = await resource_request_crud.retrieve_by_id(resource_request_id)
    return resource_request


@router.post('/', summary='Create a new resource request.', response_model=ResourceRequestResponseSchema)
async def create_resource_request(
    body: ResourceRequestCreateSchema, resource_request_crud: ResourceRequestCRUD = Depends(get_resource_request_crud)
) -> ResourceRequestResponseSchema:
    """Create a new resource request."""

    async with resource_request_crud:
        resource_request = await resource_request_crud.create(body)

    return resource_request


@router.patch(
    '/{resource_request_id}', summary='Update a resource request.', response_model=ResourceRequestResponseSchema
)
async def update_resource_request(
    resource_request_id: UUID,
    body: ResourceRequestUpdateSchema,
    resource_request_crud: ResourceRequestCRUD = Depends(get_resource_request_crud),
) -> ResourceRequestResponseSchema:
    """Update a resource request."""

    async with resource_request_crud:
        resource_request = await resource_request_crud.update(resource_request_id, body)

    return resource_request


@router.delete('/{resource_request_id}', summary='Delete a resource request.')
async def delete_resource_request(
    resource_request_id: UUID, resource_request_crud: ResourceRequestCRUD = Depends(get_resource_request_crud)
) -> Response:
    """Delete a resource request."""

    async with resource_request_crud:
        await resource_request_crud.delete(resource_request_id)

    response = Response(status_code=204)

    return response
