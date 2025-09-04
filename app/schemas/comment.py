from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


class CommentBase(BaseModel):
    content: str


class CommentCreate(CommentBase):
    user_id: int
    ticket_id: Optional[int] = None
    task_id: Optional[int] = None


class CommentUpdate(BaseModel):
    content: Optional[str] = None


class CommentInDBBase(CommentBase):
    id: int
    user_id: int
    ticket_id: Optional[int]
    task_id: Optional[int]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Comment(CommentInDBBase):
    pass


class CommentInDB(CommentInDBBase):
    pass


class CommentList(BaseModel):
    comments: List[Comment]
    total: int