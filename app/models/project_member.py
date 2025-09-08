from datetime import datetime
import enum
from sqlalchemy import Column, Enum, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base

class ProjectRole(enum.Enum):
    OWNER = "owner"
    EDITOR = "editor"
    VIEWER = "viewer"


class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    role_in_project = Column(Enum(ProjectRole), default=ProjectRole.EDITOR)
    joined_at = Column(DateTime, default=datetime.utcnow)

    # связи
    user = relationship("User", back_populates="projects_member")
    project = relationship("Project", back_populates="members")