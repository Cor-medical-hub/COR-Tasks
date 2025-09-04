from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate


class CRUDComment(CRUDBase[Comment, CommentCreate, CommentUpdate]):
    def create_with_owner(self, db: Session, *, obj_in: CommentCreate, created_by_id: int) -> Comment:
        db_obj = Comment(
            content=obj_in.content,
            ticket_id=obj_in.ticket_id,
            task_id=obj_in.task_id,
            created_by_id=created_by_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_ticket(self, db: Session, *, ticket_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
        return (
            db.query(self.model)
            .filter(Comment.ticket_id == ticket_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_task(self, db: Session, *, task_id: int, skip: int = 0, limit: int = 100) -> List[Comment]:
        return (
            db.query(self.model)
            .filter(Comment.task_id == task_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


comment = CRUDComment(Comment)