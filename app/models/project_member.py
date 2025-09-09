from datetime import datetime
import enum
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.db.session import Base
from sqlalchemy import Enum as SQLEnum
from enum import Enum

class ProjectRole(str, Enum):
    OWNER = "OWNER"
    EDITOR = "EDITOR"
    VIEWER = "VIEWER"

    @classmethod
    def _missing_(cls, value: object):
        if isinstance(value, str):
            value = value.upper()
            for member in cls:
                if member.value == value:
                    return member
        return None


class ProjectMember(Base):
    __tablename__ = "project_members"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    project_id = Column(Integer, ForeignKey("projects.id"))
    role_in_project = Column(
        SQLEnum(ProjectRole, name="projectrole", native_enum=False),  
        default=ProjectRole.EDITOR,
        nullable=False,
    )
    joined_at = Column(DateTime, default=datetime.utcnow)

    # связи
    user = relationship("User", back_populates="projects_member")
    project = relationship("Project", back_populates="members")

    __table_args__ = (
        UniqueConstraint("user_id", "project_id", name="uq_project_user"),
    )