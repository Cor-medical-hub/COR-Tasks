from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.time_log import TimeLog
from app.schemas.time_log import TimeLogCreate, TimeLogUpdate
from app.crud.crud_activity import activity
from app.models.activity import ActivityType

class CRUDTimeLog(CRUDBase[TimeLog, TimeLogCreate, TimeLogUpdate]):
    def create_with_user(
        self, db: Session, *, obj_in: TimeLogCreate, user_id: int
    ) -> TimeLog:
        db_obj = TimeLog(
            task_id=obj_in.task_id,
            subtask_id=obj_in.subtask_id,
            minutes_spent=obj_in.minutes_spent,
            description=obj_in.description,
            user_id=user_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        activity.log(
            db,
            user_id=user_id,
            action_type=ActivityType.TIME_LOGGED,
            task_id=db_obj.task_id,
            new_value={"task_id": obj_in.task_id, "minutes_spent": obj_in.minutes_spent},
        )
        return db_obj

    def get_multi_by_task(
        self, db: Session, *, task_id: int, skip: int = 0, limit: int = 100
    ) -> List[TimeLog]:
        return (
            db.query(self.model)
            .filter(TimeLog.task_id == task_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_subtask(
        self, db: Session, *, subtask_id: int, skip: int = 0, limit: int = 100
    ) -> List[TimeLog]:
        return (
            db.query(self.model)
            .filter(TimeLog.subtask_id == subtask_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


time_log = CRUDTimeLog(TimeLog)