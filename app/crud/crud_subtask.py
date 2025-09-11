from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.errors import NotFoundError
from app.crud.base import CRUDBase
from app.models.subtask import Subtask
from app.models.user import User
from app.schemas.subtask import SubtaskCreate, SubtaskUpdate
from app.models.task import TaskStatus
from app.crud.crud_activity import activity
from app.models.activity import ActivityType

class CRUDSubtask(CRUDBase[Subtask, SubtaskCreate, SubtaskUpdate]):
    def create_with_task(self, db: Session, *, obj_in: SubtaskCreate, created_by_id: int) -> Subtask:
        db_obj = Subtask(
            title=obj_in.title,
            description=obj_in.description,
            status=obj_in.status,
            priority=obj_in.priority,
            due_date=obj_in.due_date,
            task_id=obj_in.task_id,
            parent_id=obj_in.parent_id,
        )
        if obj_in.assignee_ids:
            users = db.query(User).filter(User.id.in_(obj_in.assignee_ids)).all()
            if not users or len(users) != len(obj_in.assignee_ids):
                raise NotFoundError(detail="One or more assigned users not found")
            db_obj.assignees = users

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        activity.log(
            db,
            user_id=created_by_id,
            action_type=ActivityType.CREATED,
            subtask_id=db_obj.id,
            new_value={"title": db_obj.title, "description": db_obj.description},
        )
        return db_obj

    def get_multi_by_task(self, db: Session, *, task_id: int, skip: int = 0, limit: int = 100) -> List[Subtask]:
        return (
            db.query(self.model)
            .filter(Subtask.task_id == task_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_assignee(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Subtask]:
        return (
            db.query(self.model)
            .join(Subtask.assignees)
            .filter(User.id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def complete_subtask(self, db: Session, *, subtask_id: int) -> Optional[Subtask]:
        subtask = self.get(db, id=subtask_id)
        if not subtask:
            return None
        subtask.status = TaskStatus.DONE
        subtask.completed_at = datetime.now()
        db.add(subtask)
        db.commit()
        db.refresh(subtask)
        activity.log(
            db,
            user_id=subtask.assignees,
            action_type=ActivityType.STATUS_CHANGED,
            subtask_id=subtask.id,
            new_value={"title": subtask.title, "description": subtask.description, "status": subtask.status},
        )
        return subtask


subtask = CRUDSubtask(Subtask)