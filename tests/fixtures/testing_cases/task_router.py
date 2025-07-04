import uuid

from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from tests.constants import BASE_ENDPOINT_URL
from tests.fixtures.db_mocks import TASKS
from tests.utils import RequestTestCase, json_serializable

TEST_TASK_ROUTE_CREATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/',
        headers={},
        data=json_serializable(
            {
                'title': TASKS[0]['title'],
                'status': TASKS[0]['status'],
                'author_id': TASKS[0]['author_id'],
                'assignee_id': TASKS[0]['assignee_id'],
            },
        ),
        expected_status=HTTP_201_CREATED,
        expected_data=json_serializable(TASKS[0]),
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/',
        headers={},
        data={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/',
        headers={},
        data=json_serializable(
            {
                'title': TASKS[0]['title'],
                'status': TASKS[0]['status'],
                'author_id': uuid.uuid4(),
                'assignee_id': TASKS[0]['assignee_id'],
            },
        ),
        expected_status=HTTP_400_BAD_REQUEST,
        expected_data={},
        description='Invalid input data',
    ),
]

TEST_TASK_ROUTE_GET_TASK_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/{TASKS[0]["id"]}',
        headers={},
        data={},
        expected_status=HTTP_200_OK,
        expected_data=json_serializable(TASKS[0]),
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/{uuid.uuid4()}',
        headers={},
        data={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Not existing task ID',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/sdfasd',
        headers={},
        data={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Positive case',
    ),
]

TEST_TASK_ROUTE_GET_TASKS_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/',
        headers={},
        data={},
        expected_status=HTTP_200_OK,
        expected_data=json_serializable(TASKS),
        description='Positive case',
    ),
]

TEST_TASK_ROUTE_UPDATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/{TASKS[0]["id"]}',
        headers={},
        data={
            'title': 'test',
        },
        expected_status=HTTP_200_OK,
        expected_data=json_serializable(
            {
                'title': 'test',
                'status': TASKS[0]['status'],
                'description': TASKS[0]['description'],
                'author_id': TASKS[0]['author_id'],
                'assignee_id': TASKS[0]['assignee_id'],
            },
        ),
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/{uuid.uuid4()}',
        headers={},
        data={
            'title': 'test',
        },
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Not existing task ID',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/asdfasdf',
        headers={},
        data={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid id',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/{TASKS[0]["id"]}',
        headers={},
        data={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid body',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/{TASKS[0]["id"]}',
        headers={},
        data={
            'author_id': str(uuid.uuid4()),
        },
        expected_status=HTTP_400_BAD_REQUEST,
        expected_data={},
        description='Invalid input data',
    ),
]

TEST_TASK_ROUTE_DELETE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/{TASKS[0]["id"]}',
        headers={},
        data={},
        expected_status=HTTP_204_NO_CONTENT,
        description='Positive case',
    ),
]
