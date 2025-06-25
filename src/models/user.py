import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel
from src.schemas.user import UserDB

if TYPE_CHECKING:
    from src.models.task import TaskModel


class UserModel(BaseModel):
    __tablename__ = 'users'

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=False)

    watching_tasks: Mapped[list['TaskModel']] = relationship(
        secondary='watchers',
        back_populates='watchers',
    )
    execute_tasks: Mapped[list['TaskModel']] = relationship(
        secondary='executors',
        back_populates='executors',
    )

    def to_schema(self) -> UserDB:
        return UserDB(**self.__dict__)
