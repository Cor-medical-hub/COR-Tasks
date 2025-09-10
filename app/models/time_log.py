from datetime import datetime
import enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, Table, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base



class TimeLog(Base):
    __tablename__ = "time_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True)
    subtask_id = Column(Integer, ForeignKey("subtasks.id", ondelete="CASCADE"), nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")

    minutes_spent = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # связи
    task = relationship("Task", back_populates="time_logs")
    subtask = relationship("Subtask", back_populates="time_logs")