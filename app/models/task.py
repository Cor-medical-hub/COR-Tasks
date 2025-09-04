from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import enum

from app.db.session import Base


class TaskStatus(str, enum.Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    BLOCKED = "blocked"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.TODO, nullable=False)

    # Связь с проектом
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="SET NULL"), nullable=True)
    project = relationship("Project", back_populates="tasks")

    # Связь с пользователем (исполнитель)
    assigned_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    assigned_to = relationship("User", backref="tasks")

    # Таймштампы
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    due_date = Column(DateTime(timezone=True), nullable=True)