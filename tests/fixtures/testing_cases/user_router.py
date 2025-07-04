import uuid

from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_422_UNPROCESSABLE_ENTITY

from tests.constants import BASE_ENDPOINT_URL
from tests.fixtures.db_mocks import USERS
from tests.utils import RequestTestCase

TEST_USER_ROUTE_CREATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/',
        headers={},
        data={
            'full_name': 'Test User',
            'email': 'test@test.com',
        },
        expected_status=HTTP_201_CREATED,
        expected_data={
            'full_name': 'Test User',
            'email': 'test@test.com',
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/',
        headers={},
        data={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/',
        headers={},
        data={
            'full_name': 'Test User',
            'email': USERS[0]['email'],
        },
        expected_status=HTTP_400_BAD_REQUEST,
        expected_data={},
        description='Already exists user with this email',
    ),
]

TEST_USER_ROUTE_DELETE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/{USERS[0]["id"]}',
        headers={},
        data={},
        expected_status=HTTP_204_NO_CONTENT,
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/user/{uuid.uuid4()}',
        headers={},
        data={},
        expected_status=HTTP_204_NO_CONTENT,
        expected_data={},
        description='Not valid request body',
    ),
]
