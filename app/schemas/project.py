from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel


# Shared properties
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


# Create
class ProjectCreate(ProjectBase):
    pass


# Update
class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


# In DB
class ProjectInDBBase(ProjectBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Out
class Project(ProjectInDBBase):
    pass


# Stored in DB
class ProjectInDB(ProjectInDBBase):
    pass


# List
class ProjectList(BaseModel):
    projects: List[Project]
    total: int