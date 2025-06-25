"""The module contains base routes for working with tasks."""

from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from src.api.v1.services.task import TaskService
from src.schemas.response import BaseErrorResponse
from src.schemas.tasks import (
    CreateTaskRequest,
    FilterTaskRequest,
    MultiTaskResponse,
    TaskDB,
    TaskResponse,
    UpdateTaskRequest,
)
from src.utils.constans import Tags

router = APIRouter(prefix='/tasks', tags=[Tags.TASKS_V1])


@router.post(
    path='/',
    status_code=HTTP_201_CREATED,
    responses={
        HTTP_201_CREATED: {
            'model': TaskResponse,
            'description': 'Task created successfully.',
        },
        HTTP_400_BAD_REQUEST: {
            'model': BaseErrorResponse,
            'description': 'Invalid input data.',
        },
    },
)
async def create_task(
        task: CreateTaskRequest,
        service: TaskService = Depends(),
) -> TaskResponse:
    """Create task."""
    created_task: TaskDB = await service.create(task)
    return TaskResponse(payload=created_task)


@router.get(
    path='/',
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {
            'model': MultiTaskResponse,
            'description': 'Tasks got successfully.',
        },
    },
)
async def get_tasks(
        task_filter: FilterTaskRequest = Depends(FilterTaskRequest),
        service: TaskService = Depends(),
) -> MultiTaskResponse:
    """Get tasks with filtering."""
    tasks: list[TaskDB] = await service.get_all(task_filter)
    return MultiTaskResponse(payload=tasks)


@router.get(
    path='/{task_id}',
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {
            'model': TaskResponse,
            'description': 'Task got successfully.',
        },
        HTTP_404_NOT_FOUND: {
            'model': BaseErrorResponse,
            'description': 'Task not found.',
        },
    },
)
async def get_task(
        task_id: UUID4,
        service: TaskService = Depends(),
) -> TaskResponse:
    """Delete user."""
    task: TaskDB = await service.get_by_id(task_id)
    return TaskResponse(payload=task)


@router.patch(
    path='/{task_id}',
    status_code=HTTP_200_OK,
    responses={
        HTTP_200_OK: {
            'model': TaskResponse,
            'description': 'Task updated successfully.',
        },
        HTTP_404_NOT_FOUND: {
            'model': BaseErrorResponse,
            'description': 'Task not found.',
        },
        HTTP_400_BAD_REQUEST: {
            'model': BaseErrorResponse,
            'description': 'Invalid input data.',
        },
    },
)
async def update_task(
        task_id: UUID4,
        task: UpdateTaskRequest,
        service: TaskService = Depends(),
) -> TaskResponse:
    """Update task."""
    updated_task: TaskDB = await service.update(task_id, task)
    return TaskResponse(payload=updated_task)


@router.delete(
    path='/{task_id}',
    status_code=HTTP_204_NO_CONTENT,
    responses={
        HTTP_204_NO_CONTENT: {
            'description': 'Task deleted successfully.',
        },
    },
)
async def delete_task(
        task_id: UUID4,
        service: TaskService = Depends(),
) -> None:
    """Delete task."""
    await service.delete(task_id)
