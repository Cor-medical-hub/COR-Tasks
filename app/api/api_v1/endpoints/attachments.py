from typing import Any, List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.deps import get_db, get_current_active_user_dep
from app.crud.crud_attachment import attachment
from app.schemas.attachment import AttachmentRead, AttachmentCreate
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=AttachmentRead)
def create_attachment(
    *,
    db: Session = Depends(get_db),
    attachment_in: AttachmentCreate,
    current_user: User = get_current_active_user_dep,
) -> Any:
    return attachment.create_with_owner(db, obj_in=attachment_in, uploaded_by_id=current_user.id)

@router.get("/task/{task_id}", response_model=List[AttachmentRead])
def read_attachments_by_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = get_current_active_user_dep,
) -> Any:
    return attachment.get_multi_by_task(db, task_id=task_id)

@router.get("/subtask/{subtask_id}", response_model=List[AttachmentRead])
def read_attachments_by_subtask(
    *,
    db: Session = Depends(get_db),
    subtask_id: int,
    current_user: User = get_current_active_user_dep,
) -> Any:
    return attachment.get_multi_by_subtask(db, subtask_id=subtask_id)