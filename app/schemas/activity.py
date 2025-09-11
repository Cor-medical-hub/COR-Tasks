from datetime import datetime
from pydantic import BaseModel
from typing import Optional, Any
from app.models.activity import ActivityType


class ActivityBase(BaseModel):
    task_id: Optional[int] = None
    subtask_id: Optional[int] = None
    action_type: ActivityType
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None


class ActivityCreate(ActivityBase):
    pass


class ActivityRead(ActivityBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True