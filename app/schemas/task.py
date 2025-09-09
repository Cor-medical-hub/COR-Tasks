from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.models.task import TaskStatus


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.TODO
    project_id: Optional[int] = None
    assignee_ids: list[int] = None
    due_date: Optional[datetime] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    project_id: Optional[int] = None
    assignee_ids: Optional[List[int]] = None
    due_date: Optional[datetime] = None


class TaskInDBBase(TaskBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    due_date: Optional[datetime] = None

    class Config:
        from_attributes = True


class Task(TaskInDBBase):
    pass


class TaskInDB(TaskInDBBase):
    pass


class TaskList(BaseModel):
    tasks: List[Task]
    total: int