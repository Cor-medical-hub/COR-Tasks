from typing import Optional, List
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.core.errors import NotFoundError
from app.crud.base import CRUDBase
from app.models.task import Task, TaskStatus
from app.models.user import User
from app.schemas.task import TaskCreate, TaskUpdate
from app.crud.crud_activity import activity
from app.models.activity import ActivityType


class CRUDTask(CRUDBase[Task, TaskCreate, TaskUpdate]):
    def create_with_owner(self, db: Session, *, obj_in: TaskCreate, created_by_id: int) -> Task:
        db_obj = Task(
            title=obj_in.title,
            description=obj_in.description,
            status=obj_in.status,
            priority=obj_in.priority,
            due_date=obj_in.due_date,
            project_id=obj_in.project_id,
            created_by_id=created_by_id,
        )
        if obj_in.assignee_ids:
            users = db.query(User).filter(User.id.in_(obj_in.assignee_ids)).all()
            if not users:
                raise NotFoundError(detail="Assigned users not found")
            db_obj.assignees = users
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        activity.log(
            db,
            user_id=created_by_id,
            action_type=ActivityType.CREATED,
            task_id=db_obj.id,
            new_value={"title": db_obj.title, "description": db_obj.description},
        )
        return db_obj

    def get_multi_by_project(self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100) -> List[Task]:
        return (
            db.query(self.model)
            .filter(Task.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_assignee(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Task]:
        return (
            db.query(self.model)
            .join(Task.assignees)  
            .filter(User.id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_status(self, db: Session, *, status: TaskStatus, skip: int = 0, limit: int = 100) -> List[Task]:
        return (
            db.query(self.model)
            .filter(Task.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def search_tasks(self, db: Session, *, query: str, skip: int = 0, limit: int = 100) -> List[Task]:
        search = f"%{query}%"
        return (
            db.query(self.model)
            .filter(or_(Task.title.ilike(search), Task.description.ilike(search)))
            .offset(skip)
            .limit(limit)
            .all()
        )

    def complete_task(self, db: Session, *, task_id: int) -> Optional[Task]:
        task = self.get(db, id=task_id)
        if not task:
            return None
        task.status = TaskStatus.DONE
        task.completed_at = datetime.now()
        db.add(task)
        db.commit()
        db.refresh(task)
        activity.log(
            db,
            user_id=task.created_by_id,
            action_type=ActivityType.STATUS_CHANGED,
            task_id=task.id,
            new_value={"title": task.title, "description": task.description},
        )
        return task


task = CRUDTask(Task)