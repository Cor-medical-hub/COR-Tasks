from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_current_user, get_current_active_user, get_current_active_superuser
from app.db.session import SessionLocal
from app.models.user import User


def get_db() -> Generator[Session, None, None]:
    """Dependency for getting DB session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Reusable dependencies
get_current_user_dep = Depends(get_current_user)
get_current_active_user_dep = Depends(get_current_active_user)
get_current_active_superuser_dep = Depends(get_current_active_superuser)