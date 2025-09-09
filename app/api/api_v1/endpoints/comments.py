from typing import Any, List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user_dep
from app.core.errors import NotFoundError, ForbiddenError
from app.crud.crud_comment import comment
from app.models.user import User
from app.schemas.comment import Comment as CommentSchema, CommentCreate, CommentUpdate

router = APIRouter()


@router.post("/", response_model=CommentSchema)
async def create_comment(
    *,
    db: Session = Depends(get_db),
    comment_in: CommentCreate,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Create new comment."""
    return comment.create_with_owner(db, obj_in=comment_in, created_by_id=current_user.id)


@router.get("/ticket/{ticket_id}", response_model=List[CommentSchema])
async def read_comments_by_ticket(
    *,
    db: Session = Depends(get_db),
    ticket_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Get comments for a ticket."""
    return comment.get_multi_by_ticket(db, ticket_id=ticket_id, skip=skip, limit=limit)


@router.get("/task/{task_id}", response_model=List[CommentSchema])
async def read_comments_by_task(
    *,
    db: Session = Depends(get_db),
    task_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Get comments for a task."""
    return comment.get_multi_by_task(db, task_id=task_id, skip=skip, limit=limit)


@router.put("/{comment_id}", response_model=CommentSchema)
async def update_comment(
    *,
    db: Session = Depends(get_db),
    comment_id: int,
    comment_in: CommentUpdate,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Update a comment."""
    comment_obj = comment.get(db, id=comment_id)
    if not comment_obj:
        raise NotFoundError(detail="Comment not found")

    if not (comment_obj.user_id == current_user.id or current_user.is_superuser):
        raise ForbiddenError(detail="Not enough permissions")

    return comment.update(db, db_obj=comment_obj, obj_in=comment_in)


@router.delete("/{comment_id}", response_model=CommentSchema)
async def delete_comment(
    *,
    db: Session = Depends(get_db),
    comment_id: int,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Delete a comment."""
    comment_obj = comment.get(db, id=comment_id)
    if not comment_obj:
        raise NotFoundError(detail="Comment not found")

    if not (comment_obj.user_id == current_user.id or current_user.is_superuser):
        raise ForbiddenError(detail="Not enough permissions")

    return comment.remove(db, id=comment_id)