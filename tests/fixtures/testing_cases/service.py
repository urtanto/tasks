from uuid import uuid4

from src.schemas.user import UserDB
from tests.fixtures.db_mocks import USERS
from tests.utils import BaseTestCase

TEST_BASE_SERVICE_GET_BY_QUERY_ONE_OR_NONE_PARAMS: list[BaseTestCase] = [
    BaseTestCase(
        data={'full_name': USERS[0]['full_name']},
        expected_data=UserDB(
            email=USERS[0]['email'],
            full_name=USERS[0]['full_name'],
            id=USERS[0]['id'],
        ),
        description='Good case',
    ),
    BaseTestCase(
        data={'full_name': 'Liza'},
        expected_data=None,
        description='Not existing user',
    ),
]

TEST_BASE_SERVICE_GET_BY_QUERY_ALL_PARAMS: list[BaseTestCase] = [
    BaseTestCase(
        data={'full_name': USERS[1]['full_name']},
        expected_data=[USERS[1]],
        description='Good case',
    ),
    BaseTestCase(
        data={'full_name': 'Liza'},
        expected_data=[],
        description='Not existing user',
    ),
]

TEST_BASE_SERVICE_UPDATE_ONE_BY_ID_PARAMS: list[BaseTestCase] = [
    BaseTestCase(
        data={
            '_id': USERS[1]['id'],
            'full_name': 'Ivan',
        },
        expected_data=UserDB(
            id=USERS[1]['id'],
            full_name='Ivan',
            email=USERS[1]['email'],
        ),
        description='Good case',
    ),
]

TEST_BASE_SERVICE_DELETE_BY_QUERY_PARAMS: list[BaseTestCase] = [
    BaseTestCase(
        data={
            'id': USERS[0]['id'],
        },
        expected_data=USERS[1:],
        description='Good case',
    ),
    BaseTestCase(
        data={
            'full_name': USERS[1]['full_name'],
        },
        expected_data=[USERS[0], USERS[2]],
    ),
    BaseTestCase(
        data={
            'id': uuid4(),
        },
        expected_data=USERS,
        description='Not existing user, should not change anything',
    ),
    BaseTestCase(
        data={},
        expected_data=[],
        description='Delete all users',
    ),
]
