from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base
from app.models.task import task_assignees


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    avatar_url = Column(String(255), nullable=True)

    # Связи
    created_tasks = relationship("Task", foreign_keys="Task.created_by_id", back_populates="created_by")
    assigned_tasks = relationship(
        "Task",
        secondary=task_assignees,
        back_populates="assignees",
    )
    assigned_subtasks = relationship(
        "Subtask",
        secondary="subtask_assignees",
        back_populates="assignees",
    )
    projects = relationship("Project", back_populates="created_by", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    projects_member = relationship("ProjectMember", back_populates="user")