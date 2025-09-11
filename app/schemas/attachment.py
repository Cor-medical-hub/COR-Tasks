from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel



class AttachmentBase(BaseModel):
    filename: str
    file_url: str
    task_id: Optional[int] = None
    subtask_id: Optional[int] = None


class AttachmentCreate(AttachmentBase):
    pass


class AttachmentUpdate(BaseModel):
    filename: Optional[str] = None
    file_url: Optional[str] = None


class AttachmentRead(AttachmentBase):
    id: int
    uploaded_by_id: int
    uploaded_at: datetime

    class Config:
        orm_mode = True

