from typing import Optional
from datetime import datetime
from pydantic import BaseModel
from app.models.project_member import ProjectRole


# Shared properties
class ProjectMemberBase(BaseModel):
    user_id: int
    role_in_project: ProjectRole = ProjectRole.VIEWER


# Create
class ProjectMemberCreate(ProjectMemberBase):
    project_id: int


# Update
class ProjectMemberUpdate(BaseModel):
    role_in_project: Optional[ProjectRole] = None


# In DB
class ProjectMemberInDBBase(ProjectMemberBase):
    id: int
    project_id: int
    joined_at: datetime

    class Config:
        orm_mode = True


# For response
class ProjectMember(ProjectMemberInDBBase):
    pass

