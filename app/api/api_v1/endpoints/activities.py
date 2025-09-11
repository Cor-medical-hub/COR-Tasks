from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user_dep
from app.crud.crud_attachment import attachment
from app.schemas.activity import ActivityRead
from app.models.user import User
from app.models.activity import Activity

router = APIRouter()


@router.get("/task/{task_id}", response_model=List[ActivityRead])
async def get_task_activities(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = get_current_active_user_dep,
):
    return db.query(Activity).filter(Activity.task_id == task_id).order_by(Activity.created_at.desc()).all()