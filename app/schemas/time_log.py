from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel



class TimeLogBase(BaseModel):
    task_id: Optional[int] = None
    subtask_id: Optional[int] = None
    minutes_spent: int
    description: Optional[str] = None


class TimeLogCreate(TimeLogBase):
    pass


class TimeLogUpdate(BaseModel):
    minutes_spent: Optional[int] = None
    description: Optional[str] = None


class TimeLogRead(TimeLogBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True

