from src.utils.constans import Tags

TAG_METADATA = [
    {
        'name': Tags.HEALTHZ,
        'description': 'Standard health check.',
    },
    {
        'name': Tags.USER_V1,
        'description': 'Operation with user v1.',
    },
    {
        'name': Tags.TASKS_V1,
        'description': 'Operation with tasks v1.',
    },
]

TITLE = 'Task 1 - CRUD Task'
DESCRIPTION = (
    'Implemented on FastAPI.\n\n'
    'Examples taken from the book - https://www.cosmicpython.com/book/chapter_06_uow.html.\n\n'
    'For contact - https://t.me/kalyukov_ns'
)
VERSION = '0.0.1'

ERRORS_MAP = {
    'mongo': 'Mongo connection failed',
    'postgres': 'PostgreSQL connection failed',
    'redis': 'Redis connection failed',
    'rabbit': 'RabbitMQ connection failed',
}
