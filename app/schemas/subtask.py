from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel
from app.models.task import TaskPriority, TaskStatus




class SubtaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TaskStatus] = TaskStatus.TODO
    priority: Optional[TaskPriority] = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    parent_id: Optional[int] = None


class SubtaskCreate(SubtaskBase):
    assignee_ids: Optional[List[int]] = None
    task_id: int


class SubtaskUpdate(SubtaskBase):
    assignee_ids: Optional[List[int]] = None


class Subtask(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
    parent_id: Optional[int]
    assignee_ids: List[int] = []
    children: List["Subtask"] = []

    class Config:
        orm_mode = True
