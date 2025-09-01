from uuid import UUID

from pydantic import BaseModel, ConfigDict


class TaskBase(BaseModel):
    title: str
    description: str
    status: str


class TaskCreate(TaskBase):
    pass


class Task(TaskBase):
    uuid: UUID

    model_config = ConfigDict(
        from_attributes=True
    )

