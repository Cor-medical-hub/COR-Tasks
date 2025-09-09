from sqlalchemy import Column, Integer, String, Table, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.session import Base
from app.models.task import TaskPriority, TaskStatus


subtask_assignees = Table(
    "subtask_assignees",
    Base.metadata,
    Column("subtask_id", Integer, ForeignKey("subtasks.id", ondelete="CASCADE"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
)

class Subtask(Base):
    __tablename__ = "subtasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.MEDIUM, nullable=False)

    # Связь с задачей верхнего уровня
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True)
    task = relationship("Task", back_populates="subtasks")

    # Self-reference (иерархия подзадач)
    parent_id = Column(Integer, ForeignKey("subtasks.id", ondelete="CASCADE"), nullable=True)
    parent = relationship("Subtask", remote_side="Subtask.id", back_populates="children")
    children = relationship("Subtask", back_populates="parent", cascade="all, delete-orphan")

    # исполнители
    assignees = relationship(
        "User",
        secondary="subtask_assignees",
        back_populates="assigned_subtasks",
    )

    due_date = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())