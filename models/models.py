import uuid

from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import UUID
import enum

from db import Base


class StatusEnum(str, enum.Enum):
    created = "создано"
    in_progress = "в работе"
    completed = "завершено"


class Task(Base):
    __tablename__ = "Tasks"
    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(255), nullable=False)
    description = Column(String(1024), nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.created, nullable=False)
