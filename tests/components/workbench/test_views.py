# Copyright (C) 2022-Present Indoc Systems
#
# Licensed under the GNU AFFERO GENERAL PUBLIC LICENSE,
# Version 3.0 (the "License") available at https://www.gnu.org/licenses/agpl-3.0.en.html.
# You may not use this file except in compliance with the License.

import pytest

from project.components.exceptions import NotFound


class TestWorkbenchViews:
    async def test_list_workbenches_returns_list_of_existing_workbenches(
        self, client, jq, project_factory, workbench_factory
    ):
        created_project = await project_factory.create()
        created_workbench = await workbench_factory.create(project_id=created_project.id)

        response = await client.get('/v1/workbenches/')

        assert response.status_code == 200

        body = jq(response)
        received_workbench_id = body('.result[].id').first()
        received_total = body('.total').first()

        assert received_workbench_id == str(created_workbench.id)
        assert received_total == 1

    async def test_get_workbench_returns_workbench_by_id(self, client, project_factory, workbench_factory):
        created_project = await project_factory.create()
        created_workbench = await workbench_factory.create(project_id=created_project.id)

        response = await client.get(f'/v1/workbenches/{created_workbench.id}')

        assert response.status_code == 200

        received_workbench = response.json()

        assert received_workbench['id'] == str(created_workbench.id)

    async def test_list_workbenches_returns_list_of_workbenches_filtered_by_project_id(
        self, client, jq, project_factory, workbench_factory
    ):
        created_project1 = await project_factory.create()
        created_project2 = await project_factory.create()
        created_workbench1 = await workbench_factory.create(project_id=created_project1.id)
        await workbench_factory.create(project_id=created_project2.id)

        response = await client.get('/v1/workbenches/', params={'project_id': created_project1.id})

        assert response.status_code == 200

        body = jq(response)
        received_workbench_id = body('.result[].id').first()
        received_total = body('.total').first()
        assert received_workbench_id == str(created_workbench1.id)
        assert received_total == 1

    async def test_create_workbench_creates_new_workbench(
        self, client, jq, project_factory, workbench_factory, workbench_crud
    ):
        created_project = await project_factory.create()
        workbench = workbench_factory.generate(project_id=created_project.id)

        payload = workbench.to_payload()
        response = await client.post('/v1/workbenches/', json=payload)

        assert response.status_code == 200

        body = jq(response)
        received_workbench_id = body('.id').first()
        received_workbench = await workbench_crud.retrieve_by_id(received_workbench_id)

        assert received_workbench.resource == workbench.resource
        assert received_workbench.deployed_at

    async def test_update_workbench_updates_workbench_field_by_id(
        self, client, jq, project_factory, workbench_factory, workbench_crud
    ):
        created_project = await project_factory.create()
        created_workbench = await workbench_factory.create(project_id=created_project.id)
        workbench = workbench_factory.generate()

        payload = {'deployed_by_user_id': workbench.deployed_by_user_id}
        response = await client.patch(f'/v1/workbenches/{created_workbench.id}', json=payload)

        assert response.status_code == 200

        body = jq(response)
        received_workbench_id = body('.id').first()
        received_workbench = await workbench_crud.retrieve_by_id(received_workbench_id)

        assert received_workbench.deployed_by_user_id == workbench.deployed_by_user_id

    async def test_delete_workbench(self, client, project_factory, workbench_factory, workbench_crud):
        created_project = await project_factory.create()
        created_workbench = await workbench_factory.create(project_id=created_project.id)

        response = await client.delete(f'/v1/workbenches/{created_workbench.id}')

        assert response.status_code == 204

        with pytest.raises(NotFound):
            await workbench_crud.retrieve_by_id(created_workbench.id)
