from datetime import datetime
import enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy import Column, Integer, String, Table, Text, DateTime, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base



class Attachment(Base):
    __tablename__ = "attachments"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_url = Column(Text, nullable=False)

    uploaded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_by = relationship("User")

    task_id = Column(Integer, ForeignKey("tasks.id", ondelete="CASCADE"), nullable=True)
    subtask_id = Column(Integer, ForeignKey("subtasks.id", ondelete="CASCADE"), nullable=True)

    uploaded_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    # связи
    task = relationship("Task", back_populates="attachments")
    subtask = relationship("Subtask", back_populates="attachments")