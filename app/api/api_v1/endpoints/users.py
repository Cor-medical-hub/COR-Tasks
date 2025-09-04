from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user_dep, get_current_active_superuser_dep
from app.core.errors import NotFoundError, ForbiddenError
from app.crud.crud_user import user
from app.models.user import User
from app.schemas.user import User as UserSchema, UserCreate, UserUpdate

router = APIRouter()


@router.get("/", response_model=List[UserSchema])
async def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_active_superuser_dep,
) -> Any:
    """Retrieve users. Only superusers can access this endpoint."""
    users = user.get_multi(db, skip=skip, limit=limit)
    return users


@router.post("/", response_model=UserSchema)
async def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
    current_user: User = get_current_active_superuser_dep,
) -> Any:
    """Create new user. Only superusers can access this endpoint."""
    user_by_email = user.get_by_email(db, email=user_in.email)
    if user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    user_by_username = user.get_by_username(db, username=user_in.username)
    if user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken",
        )
    return user.create(db, obj_in=user_in)


@router.get("/me", response_model=UserSchema)
async def read_user_me(current_user: User = get_current_active_user_dep) -> Any:
    """Get current user."""
    return current_user


@router.put("/me", response_model=UserSchema)
async def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Update current user."""
    return user.update(db, db_obj=current_user, obj_in=user_in)


@router.get("/{user_id}", response_model=UserSchema)
async def read_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Get a specific user by id."""
    user_obj = user.get(db, id=user_id)
    if not user_obj:
        raise NotFoundError(detail="User not found")
    
    # Only allow superusers to access other users' data
    if user_obj.id != current_user.id and not current_user.is_superuser:
        raise ForbiddenError(detail="Not enough permissions")
    
    return user_obj


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = get_current_active_superuser_dep,
) -> Any:
    """Update a user. Only superusers can access this endpoint."""
    user_obj = user.get(db, id=user_id)
    if not user_obj:
        raise NotFoundError(detail="User not found")
    
    return user.update(db, db_obj=user_obj, obj_in=user_in)


@router.delete("/{user_id}", response_model=UserSchema)
async def delete_user(
    *,
    db: Session = Depends(get_db),
    user_id: int,
    current_user: User = get_current_active_superuser_dep,
) -> Any:
    """Delete a user. Only superusers can access this endpoint."""
    user_obj = user.get(db, id=user_id)
    if not user_obj:
        raise NotFoundError(detail="User not found")
    
    return user.delete(db, id=user_id)