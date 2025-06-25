import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Index, String, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models import BaseModel
from src.schemas.tasks import TaskDB
from src.utils.enums import Status

if TYPE_CHECKING:
    from src.models.user import UserModel


class TaskModel(BaseModel):
    __tablename__ = 'tasks'
    __table_args__ = (
        Index('title_index', 'title'),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4, unique=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)
    status: Mapped[Status] = mapped_column(Enum(Status, name='task_status'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), nullable=False)
    author_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
    )
    assignee_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=True,
    )

    watchers: Mapped[list['UserModel']] = relationship(
        back_populates='watching_tasks',
        secondary='watchers',
    )
    executors: Mapped[list['UserModel']] = relationship(
        back_populates='execute_tasks',
        secondary='executors',
    )

    def to_schema(self) -> TaskDB:
        return TaskDB(**self.__dict__)
