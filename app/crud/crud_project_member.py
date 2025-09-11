from typing import List, Optional

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.project_member import ProjectMember, ProjectRole
from app.schemas.project_member import ProjectMemberCreate, ProjectMemberUpdate
from app.crud.crud_activity import activity
from app.models.activity import ActivityType


class CRUDProjectMember(CRUDBase[ProjectMember, ProjectMemberCreate, ProjectMemberUpdate]):
    def add_member(
        self, db: Session, *, project_id: int, user_id: int, role: ProjectRole = ProjectRole.VIEWER
    ) -> ProjectMember:
        db_obj = ProjectMember(
            project_id=project_id,
            user_id=user_id,
            role_in_project=role,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_members(
        self, db: Session, *, project_id: int, skip: int = 0, limit: int = 100
    ) -> List[ProjectMember]:
        return (
            db.query(self.model)
            .filter(ProjectMember.project_id == project_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_member(
        self, db: Session, *, project_id: int, user_id: int
    ) -> Optional[ProjectMember]:
        return (
            db.query(self.model)
            .filter(
                ProjectMember.project_id == project_id,
                ProjectMember.user_id == user_id,
            )
            .first()
        )
    def get_by_project(self, db: Session, project_id: int) -> List[ProjectMember]:
        return db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()


project_member = CRUDProjectMember(ProjectMember)