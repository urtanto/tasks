import uuid

from src.utils.enums import Status
from tests.fixtures.db_mocks.users import USERS

TASKS = (
    {
        'id': uuid.uuid4(),
        'title': 'First',
        'description': None,
        'status': Status.TODO,
        'author_id': USERS[0]['id'],
        'assignee_id': USERS[1]['id'],
    },
    {
        'id': uuid.uuid4(),
        'title': 'Second',
        'description': None,
        'status': Status.IN_PROGRESS,
        'author_id': USERS[0]['id'],
        'assignee_id': USERS[2]['id'],
    },
)
