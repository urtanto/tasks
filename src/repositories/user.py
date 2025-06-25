from src.models import UserModel
from src.schemas.user import CreateUserRequest
from src.utils.repository import SqlAlchemyRepository


class CreateUserError(Exception):
    """Custom exception for user creation errors."""


class UserRepository(SqlAlchemyRepository[UserModel]):
    _model = UserModel

    async def create_user(self, user: CreateUserRequest) -> UserModel:
        """Create a new user in the database.

        :param user: User attributes to be set.
        :return: The created UserModel instance.
        :raises CreateUserException: If user creation fails.
        """
        try:
            return await self.add_one_and_get_obj(**user.model_dump())
        except SqlAlchemyRepository.IntegrityError as e:
            raise CreateUserError(e) from e
