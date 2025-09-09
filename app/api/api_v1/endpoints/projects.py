from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user_dep
from app.core.errors import NotFoundError, ForbiddenError
from app.crud.crud_project import project
from app.models.user import User
from app.schemas.project import Project as ProjectSchema, ProjectCreate, ProjectUpdate

router = APIRouter()


@router.get("/", response_model=List[ProjectSchema])
async def read_projects(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Retrieve all projects."""
    return project.get_multi(db, skip=skip, limit=limit)


@router.post("/", response_model=ProjectSchema)
async def create_project(
    *,
    db: Session = Depends(get_db),
    project_in: ProjectCreate,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Create new project."""
    return project.create_with_owner(db, obj_in=project_in, created_by_id=current_user.id)


@router.get("/me", response_model=List[ProjectSchema])
async def read_my_projects(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Get projects created by current user."""
    return project.get_multi_by_owner(db, created_by_id=current_user.id, skip=skip, limit=limit)


@router.put("/{project_id}", response_model=ProjectSchema)
async def update_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    project_in: ProjectUpdate,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Update a project."""
    project_obj = project.get(db, id=project_id)
    if not project_obj:
        raise NotFoundError(detail="Project not found")

    if not (project_obj.created_by_id == current_user.id or current_user.is_superuser):
        raise ForbiddenError(detail="Not enough permissions")

    return project.update(db, db_obj=project_obj, obj_in=project_in)


@router.delete("/{project_id}", response_model=ProjectSchema)
async def delete_project(
    *,
    db: Session = Depends(get_db),
    project_id: int,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Delete a project."""
    project_obj = project.get(db, id=project_id)
    if not project_obj:
        raise NotFoundError(detail="Project not found")

    if not (project_obj.created_by_id == current_user.id or current_user.is_superuser):
        raise ForbiddenError(detail="Not enough permissions")

    return project.remove(db, id=project_id)