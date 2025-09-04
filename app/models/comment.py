from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)

    # Автор комментария
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", backref="comments")

    # Привязка к тикету или таску
    ticket_id = Column(Integer, ForeignKey("tickets.id"), nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)

    ticket = relationship("Ticket", backref="comments")
    task = relationship("Task", backref="comments")

    # Таймштампы
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())