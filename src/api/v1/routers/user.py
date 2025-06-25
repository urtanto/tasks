"""The module contains base routes for working with user."""

from fastapi import APIRouter, Depends
from pydantic import UUID4
from starlette.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from src.api.v1.services.user import UserService
from src.schemas.response import BaseErrorResponse
from src.schemas.user import (
    CreateUserRequest,
    CreateUserResponse,
    UserDB,
)
from src.utils.constans import Tags

router = APIRouter(prefix='/user', tags=[Tags.USER_V1])


@router.post(
    path='/',
    status_code=HTTP_201_CREATED,
    responses={
        HTTP_201_CREATED: {
            'model': CreateUserResponse,
            'description': 'User created successfully.',
        },
        HTTP_400_BAD_REQUEST: {
            'model': BaseErrorResponse,
            'description': 'Invalid input data.',
        },
    },
)
async def create_user(
        user: CreateUserRequest,
        service: UserService = Depends(UserService),
) -> CreateUserResponse:
    """Create user."""
    created_user: UserDB = await service.create_user(user)
    return CreateUserResponse(payload=created_user)


@router.delete(
    path='/{user_id}',
    status_code=HTTP_204_NO_CONTENT,
)
async def delete_user(
        user_id: UUID4,
        service: UserService = Depends(),
) -> None:
    """Delete user."""
    await service.delete_user(user_id)
