from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user_dep
from app.core.errors import NotFoundError, ForbiddenError
from app.crud.crud_subtask import subtask
from app.models.user import User
from app.schemas.subtask import Subtask as SubtaskSchema, SubtaskCreate, SubtaskUpdate

router = APIRouter()


@router.get("/", response_model=List[SubtaskSchema])
async def read_subtasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Retrieve all subtasks (paginated)."""
    return subtask.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=SubtaskSchema)
async def create_subtask(
    *,
    db: Session = Depends(get_db),
    subtask_in: SubtaskCreate,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Create new subtask for a task."""
    return subtask.create_with_task(db, obj_in=subtask_in, created_by_id=current_user.id)


@router.get("/task/{task_id}", response_model=List[SubtaskSchema])
async def read_subtasks_by_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Get subtasks belonging to a task."""
    return subtask.get_multi_by_task(db, task_id=task_id, skip=skip, limit=limit)


@router.get("/assigned", response_model=List[SubtaskSchema])
async def read_assigned_subtasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Get subtasks assigned to current user (Many-to-Many)."""
    return subtask.get_multi_by_assignee(db, user_id=current_user.id, skip=skip, limit=limit)


@router.put("/{subtask_id}", response_model=SubtaskSchema)
async def update_subtask(
    *,
    db: Session = Depends(get_db),
    subtask_id: int,
    subtask_in: SubtaskUpdate,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Update a subtask."""
    subtask_obj = subtask.get(db, id=subtask_id)
    if not subtask_obj:
        raise NotFoundError(detail="Subtask not found")

    if not (
        current_user in subtask_obj.assignees or
        current_user.is_superuser
    ):
        raise ForbiddenError(detail="Not enough permissions")

    return subtask.update(db, db_obj=subtask_obj, obj_in=subtask_in)


@router.delete("/{subtask_id}", response_model=SubtaskSchema)
async def delete_subtask(
    *,
    db: Session = Depends(get_db),
    subtask_id: int,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Delete a subtask."""
    subtask_obj = subtask.get(db, id=subtask_id)
    if not subtask_obj:
        raise NotFoundError(detail="Subtask not found")

    if not (
        current_user in subtask_obj.assignees or
        current_user.is_superuser
    ):
        raise ForbiddenError(detail="Not enough permissions")

    return subtask.remove(db, id=subtask_id)


@router.post("/{subtask_id}/complete", response_model=SubtaskSchema)
async def complete_subtask(
    *,
    db: Session = Depends(get_db),
    subtask_id: int,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Mark a subtask as completed."""
    subtask_obj = subtask.get(db, id=subtask_id)
    if not subtask_obj:
        raise NotFoundError(detail="Subtask not found")

    if not (
        current_user in subtask_obj.assignees or
        current_user.is_superuser
    ):
        raise ForbiddenError(detail="Not enough permissions")

    return subtask.complete_subtask(db, subtask_id=subtask_id)