from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user_dep
from app.core.errors import NotFoundError, ForbiddenError
from app.crud.crud_task import task
from app.crud.crud_user import user
from app.models.user import User
from app.models.task import TaskStatus
from app.schemas.task import Task as TaskSchema, TaskCreate, TaskUpdate

router = APIRouter()


@router.get("/", response_model=List[TaskSchema])
async def read_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[TaskStatus] = None,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Retrieve tasks with optional filtering by status."""
    if status:
        tasks = task.get_multi_by_status(db, status=status, skip=skip, limit=limit)
    else:
        tasks = task.get_multi(db, skip=skip, limit=limit)
    return tasks


@router.post("/", response_model=TaskSchema)
async def create_task(
    *,
    db: Session = Depends(get_db),
    task_in: TaskCreate,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Create new task."""
    if task_in.assignee_ids:
        users = db.query(User).filter(User.id.in_(task_in.assignee_ids)).all()
        if not users or len(users) != len(task_in.assignee_ids):
            raise NotFoundError(detail="One or more assigned users not found")

    return task.create_with_owner(db, obj_in=task_in, created_by_id=current_user.id)


@router.get("/project/{project_id}", response_model=List[TaskSchema])
async def read_tasks_by_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Get tasks belonging to a project."""
    return task.get_multi_by_project(db, project_id=project_id, skip=skip, limit=limit)


@router.get("/assigned", response_model=List[TaskSchema])
async def read_assigned_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Get tasks assigned to current user (Many-to-Many)."""
    return task.get_multi_by_assignee(db, user_id=current_user.id, skip=skip, limit=limit)


@router.get("/search", response_model=List[TaskSchema])
async def search_tasks(
    *,
    db: Session = Depends(get_db),
    query: str = Query(..., min_length=3),
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Search tasks by title or description."""
    return task.search_tasks(db, query=query, skip=skip, limit=limit)


@router.put("/{task_id}", response_model=TaskSchema)
async def update_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    task_in: TaskUpdate,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Update a task."""
    task_obj = task.get(db, id=task_id)
    if not task_obj:
        raise NotFoundError(detail="Task not found")

    if not (
        task_obj.created_by_id == current_user.id or
        current_user in task_obj.assignees or
        current_user.is_superuser
    ):
        raise ForbiddenError(detail="Not enough permissions")

    return task.update(db, db_obj=task_obj, obj_in=task_in)


@router.delete("/{task_id}", response_model=TaskSchema)
async def delete_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Delete a task."""
    task_obj = task.get(db, id=task_id)
    if not task_obj:
        raise NotFoundError(detail="Task not found")

    if not (
        task_obj.created_by_id == current_user.id or
        current_user in task_obj.assignees or
        current_user.is_superuser
    ):
        raise ForbiddenError(detail="Not enough permissions")

    return task.remove(db, id=task_id)


@router.post("/{task_id}/complete", response_model=TaskSchema)
async def complete_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Mark a task as completed."""
    task_obj = task.get(db, id=task_id)
    if not task_obj:
        raise NotFoundError(detail="Task not found")

    if not (
        task_obj.created_by_id == current_user.id or
        current_user in task_obj.assignees or
        current_user.is_superuser
    ):
        raise ForbiddenError(detail="Not enough permissions")

    return task.complete_task(db, task_id=task_id)