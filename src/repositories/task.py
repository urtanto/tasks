import sqlalchemy.exc
from pydantic import UUID4
from sqlalchemy import Result, select, update
from sqlalchemy.orm import selectinload

from src.models import TaskModel
from src.schemas.tasks import CreateTaskRequest, FilterTaskRequest, UpdateTaskRequest
from src.utils.repository import SqlAlchemyRepository


class TaskError(Exception):
    """Custom exception for task data manipulating errors."""


class NoTaskError(Exception):
    """Custom exception for task not found error."""


class TaskRepository(SqlAlchemyRepository[TaskModel]):
    _model = TaskModel

    async def create_task(self, user: CreateTaskRequest) -> TaskModel:
        """Create a new user in the database.

        :param user: User attributes to be set.
        :return: The created UserModel instance.
        :raises CreateUserException: If user creation fails.
        """
        try:
            return await self.add_one_and_get_obj(**user.model_dump())
        except SqlAlchemyRepository.IntegrityError as e:
            raise TaskError(e) from e

    async def get_all(self, task_filter: FilterTaskRequest) -> list[TaskModel]:
        """Get tasks with filtering.

        :param task_filter: Filter attributes to be applied.
        :return: List of TaskModel instances matching the filter.
        """
        query = select(self._model)

        if task_filter.title:
            query = query.where(self._model.title.ilike(f'%{task_filter.title}%'))

        if task_filter.status:
            query = query.where(self._model.status == task_filter.status)

        if task_filter.author_id:
            query = query.where(self._model.author_id == task_filter.author_id)

        query = query.options(
            selectinload(self._model.watchers),
            selectinload(self._model.executors),
        )

        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def update(self, task_id: UUID4, update_data: UpdateTaskRequest) -> TaskModel:
        """Update task by ID.

        :param task_id: ID of the task to be updated.
        :param update_data: New data for the task.
        :return: The updated TaskModel instance.
        """
        query = update(self._model).where(self._model.id == task_id)

        if 'title' in update_data.model_fields_set:
            query = query.values(title=update_data.title)

        if 'description' in update_data.model_fields_set:
            query = query.values(description=update_data.description)

        if 'status' in update_data.model_fields_set:
            query = query.values(status=update_data.status)

        if 'author_id' in update_data.model_fields_set:
            query = query.values(author_id=update_data.author_id)

        if 'assignee_id' in update_data.model_fields_set:
            query = query.values(assignee_id=update_data.assignee_id)

        query = query.returning(self._model)

        try:
            result: Result = await self._session.execute(query)
            task: TaskModel = result.scalar_one()
        except sqlalchemy.exc.NoResultFound:
            raise NoTaskError
        except sqlalchemy.exc.IntegrityError:
            raise TaskError
        return task
