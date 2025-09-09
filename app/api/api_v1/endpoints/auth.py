from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.core.config import settings
from app.core.security import create_access_token, verify_password
from app.core.errors import AuthenticationError, BadRequestError
from app.crud.crud_user import user

from app.schemas.token import Token
from app.schemas.user import User as UserSchema, UserCreate

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_access_token(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """OAuth2 compatible token login, get an access token for future requests."""
    # Try to authenticate with email
    user_obj = user.authenticate(db, email=form_data.username, password=form_data.password)
    # If not found, try with username
    if not user_obj:
        user_obj = user.get_by_username(db, username=form_data.username)
        if user_obj and verify_password(form_data.password, user_obj.hashed_password):
            pass
        else:
            raise AuthenticationError(detail="Incorrect email/username or password")
    elif not user.is_active(user_obj):
        raise AuthenticationError(detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user_obj.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/register", response_model=UserSchema)
async def register_user(*, db: Session = Depends(get_db), user_in: UserCreate) -> Any:
    """Register a new user."""
    # Check if user with this email exists
    user_by_email = user.get_by_email(db, email=user_in.email)
    if user_by_email:
        raise BadRequestError(detail="Email already registered")
    
    # Check if user with this username exists
    user_by_username = user.get_by_username(db, username=user_in.username)
    if user_by_username:
        raise BadRequestError(detail="Username already taken")
    
    # Create new user
    return user.create(db, obj_in=user_in)