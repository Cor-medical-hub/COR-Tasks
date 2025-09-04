from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase

from app.models.project import Project

from app.schemas.project import ProjectCreate, ProjectUpdate



class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def create_with_owner(self, db: Session, *, obj_in: ProjectCreate, created_by_id: int) -> Project:
        db_obj = Project(
            name=obj_in.name,
            description=obj_in.description,
            created_by_id=created_by_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(self, db: Session, *, created_by_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        return (
            db.query(self.model)
            .filter(Project.created_by_id == created_by_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


project = CRUDProject(Project)