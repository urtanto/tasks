from typing import TYPE_CHECKING

from fastapi import HTTPException
from pydantic import UUID4
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from src.repositories.task import NoTaskError, TaskError
from src.schemas.tasks import CreateTaskRequest, FilterTaskRequest, TaskDB, UpdateTaskRequest
from src.utils.service import BaseService, transaction_mode

if TYPE_CHECKING:
    from src.models import TaskModel


class TaskService(BaseService):
    _repo: str = 'task'

    @transaction_mode
    async def create(self, user: CreateTaskRequest) -> TaskDB:
        """Create user."""
        try:
            created_task: TaskModel = await self.uow.task.create_task(user)
        except TaskError:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Wrong data provided.')
        return created_task.to_schema()

    @transaction_mode
    async def get_by_id(self, task_id: UUID4) -> TaskDB | None:
        """Get task by ID."""
        task = await self.uow.task.get_by_filter_one_or_none(id=task_id)
        self.check_existence(obj=task, details='Task not found.')
        return task.to_schema()

    @transaction_mode
    async def get_all(self, task_filter: FilterTaskRequest) -> list[TaskDB]:
        """Get tasks with filtering."""
        tasks: list[TaskModel] = await self.uow.task.get_all(task_filter)
        return [task.to_schema() for task in tasks]

    @transaction_mode
    async def update(self, task_id: UUID4, update_data: UpdateTaskRequest) -> TaskDB:
        """Update task."""
        try:
            updated_task = await self.uow.task.update(task_id, update_data)
        except NoTaskError:
            raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail='Task not found.')
        except TaskError:
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST, detail='Wrong data provided.')
        return updated_task.to_schema()

    @transaction_mode
    async def delete(self, task_id: UUID4) -> None:
        """Delete task by ID."""
        await self.uow.task.delete_by_filter(id=task_id)
