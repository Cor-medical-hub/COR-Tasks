from datetime import datetime
import enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, Table, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class ActivityType(str, enum.Enum):
    CREATED = "created"
    UPDATED = "updated"
    STATUS_CHANGED = "status_changed"
    COMMENTED = "commented"
    ASSIGNED = "assigned"
    UNASSIGNED = "unassigned"
    ATTACHMENT_ADDED = "attachment_added"
    TIME_LOGGED = "time_logged"


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True)
    subtask_id = Column(Integer, ForeignKey("subtasks.id", ondelete="CASCADE"), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")

    action_type = Column(Enum(ActivityType), nullable=False)
    old_value = Column(JSONB, nullable=True)
    new_value = Column(JSONB, nullable=True)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # связи
    task = relationship("Task", back_populates="activities")
    subtask = relationship("Subtask", back_populates="activities")