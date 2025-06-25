from typing import TYPE_CHECKING

from fastapi import HTTPException
from pydantic import UUID4
from starlette.status import HTTP_400_BAD_REQUEST

from src.repositories.user import CreateUserError
from src.schemas.user import CreateUserRequest, UserDB
from src.utils.service import BaseService, transaction_mode

if TYPE_CHECKING:
    from src.models import UserModel


class UserService(BaseService):
    _repo: str = 'user'

    @transaction_mode
    async def create_user(self, user: CreateUserRequest) -> UserDB:
        """Create user."""
        try:
            created_user: UserModel = await self.uow.user.create_user(user)
        except CreateUserError:
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail='Email already exists or invalid data provided.',
            )
        return created_user.to_schema()

    @transaction_mode
    async def delete_user(self, user_id: UUID4) -> None:
        """Delete user by ID."""
        await self.uow.user.delete_by_filter(id=user_id)
