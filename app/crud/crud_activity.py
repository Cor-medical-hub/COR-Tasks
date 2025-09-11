from sqlalchemy.orm import Session
from app.models.activity import Activity
from app.schemas.activity import ActivityCreate
from app.crud.base import CRUDBase


class CRUDActivity(CRUDBase[Activity, ActivityCreate, None]):
    def log(
        self,
        db: Session,
        *,
        user_id: int,
        action_type: str,
        task_id: int = None,
        subtask_id: int = None,
        old_value: dict = None,
        new_value: dict = None,
    ) -> Activity:
        db_obj = Activity(
            user_id=user_id,
            action_type=action_type,
            task_id=task_id,
            subtask_id=subtask_id,
            old_value=old_value,
            new_value=new_value,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


activity = CRUDActivity(Activity)