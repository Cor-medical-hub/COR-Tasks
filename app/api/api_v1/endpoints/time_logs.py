from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user_dep
from app.crud.crud_time_log import time_log
from app.schemas.time_log import TimeLogRead, TimeLogCreate
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=TimeLogRead)
def create_time_log(
    *,
    db: Session = Depends(get_db),
    time_log_in: TimeLogCreate,
    current_user: User = get_current_active_user_dep,
) -> Any:
    return time_log.create_with_user(db, obj_in=time_log_in, user_id=current_user.id)

@router.get("/task/{task_id}", response_model=List[TimeLogRead])
def read_time_logs_by_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = get_current_active_user_dep,
) -> Any:
    return time_log.get_multi_by_task(db, task_id=task_id)

@router.get("/subtask/{subtask_id}", response_model=List[TimeLogRead])
def read_time_logs_by_subtask(
    *,
    db: Session = Depends(get_db),
    subtask_id: int,
    current_user: User = get_current_active_user_dep,
) -> Any:
    return time_log.get_multi_by_subtask(db, subtask_id=subtask_id)