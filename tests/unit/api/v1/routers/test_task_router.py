"""Contains tests for user routes."""

import pytest
from httpx import AsyncClient

from tests.fixtures import testing_cases
from tests.utils import RequestTestCase, prepare_payload


class TestTaskRouter:

    @staticmethod
    @pytest.mark.usefixtures('setup_users', 'setup_tasks')
    @pytest.mark.parametrize('case', testing_cases.TEST_TASK_ROUTE_CREATE_PARAMS)
    async def test_create(
            case: RequestTestCase,
            async_client: AsyncClient,
    ) -> None:
        with case.expected_error:
            response = await async_client.post(case.url, json=case.data, headers=case.headers)
            assert response.status_code == case.expected_status

            if 'id' in case.expected_data:
                case.expected_data.pop('id')

            actual = prepare_payload(response, exclude=['id', 'created_at', 'watchers', 'executors'])
            assert actual == case.expected_data

    @staticmethod
    @pytest.mark.usefixtures('setup_users', 'setup_tasks')
    @pytest.mark.parametrize('case', testing_cases.TEST_TASK_ROUTE_GET_TASK_PARAMS)
    async def test_get_task(
            case: RequestTestCase,
            async_client: AsyncClient,
    ) -> None:
        with case.expected_error:
            response = await async_client.get(case.url, headers=case.headers)
            assert response.status_code == case.expected_status

            if 'id' in case.expected_data:
                case.expected_data.pop('id')

            actual = prepare_payload(response, exclude=['id', 'created_at', 'watchers', 'executors'])
            assert actual == case.expected_data

    @staticmethod
    @pytest.mark.usefixtures('setup_users', 'setup_tasks')
    @pytest.mark.parametrize('case', testing_cases.TEST_TASK_ROUTE_GET_TASKS_PARAMS)
    async def test_get_tasks(
            case: RequestTestCase,
            async_client: AsyncClient,
    ) -> None:
        with case.expected_error:
            response = await async_client.get(case.url, headers=case.headers)
            actual = response.json()['payload']
            assert response.status_code == case.expected_status

            for data in case.expected_data:
                if 'id' in data:
                    data.pop('id')

            for data in actual:
                if 'id' in data:
                    data.pop('id')
                if 'created_at' in data:
                    data.pop('created_at')
                if 'watchers' in data:
                    data.pop('watchers')
                if 'executors' in data:
                    data.pop('executors')

            assert actual == case.expected_data

    @staticmethod
    @pytest.mark.usefixtures('setup_users', 'setup_tasks')
    @pytest.mark.parametrize('case', testing_cases.TEST_TASK_ROUTE_UPDATE_PARAMS)
    async def test_update(
            case: RequestTestCase,
            async_client: AsyncClient,
    ) -> None:
        with case.expected_error:
            response = await async_client.patch(case.url, json=case.data, headers=case.headers)
            assert response.status_code == case.expected_status

            if 'id' in case.expected_data:
                case.expected_data.pop('id')

            actual = prepare_payload(response, exclude=['id', 'created_at', 'watchers', 'executors'])
            assert actual == case.expected_data

    @staticmethod
    @pytest.mark.usefixtures('setup_users', 'setup_tasks')
    @pytest.mark.parametrize('case', testing_cases.TEST_TASK_ROUTE_DELETE_PARAMS)
    async def test_delete(
            case: RequestTestCase,
            async_client: AsyncClient,
    ) -> None:
        with case.expected_error:
            response = await async_client.delete(case.url, headers=case.headers)
            assert response.status_code == case.expected_status
