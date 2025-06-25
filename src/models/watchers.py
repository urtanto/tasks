import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.models import BaseModel


class Watcher(BaseModel):
    __tablename__ = 'watchers'

    task_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('tasks.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        nullable=False,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE', onupdate='CASCADE'),
        primary_key=True,
        nullable=False,
    )
