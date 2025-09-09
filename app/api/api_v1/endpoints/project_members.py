from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.api.deps import get_db
from app.crud.crud_project_member import project_member
from app.crud.crud_project import project as project_crud
from app.crud.crud_user import user as user_crud
from app.schemas.project_member import ProjectMemberCreate, ProjectMember, ProjectMemberUpdate
from app.models.project_member import ProjectMember as db_ProjectMember

router = APIRouter()


@router.post("/", response_model=ProjectMember)
def add_project_member(
    member_in: ProjectMemberCreate,
    db: Session = Depends(get_db),
):

    project = project_crud.get(db, id=member_in.project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")


    user = user_crud.get(db, id=member_in.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_member = (
        db.query(db_ProjectMember)
        .filter(
            db_ProjectMember.project_id == member_in.project_id,
            db_ProjectMember.user_id == member_in.user_id,
        )
        .first()
    )
    if existing_member:
        raise HTTPException(
            status_code=400,
            detail="User is already a member of this project"
        )

    return project_member.create(db=db, obj_in=member_in)


@router.get("/{project_id}", response_model=List[ProjectMember])
def get_project_members(
    project_id: int,
    db: Session = Depends(get_db),
):
    members = project_member.get_by_project(db=db, project_id=project_id)
    return members


@router.put("/{member_id}", response_model=ProjectMember)
def update_project_member(
    member_id: int,
    member_in: ProjectMemberUpdate,
    db: Session = Depends(get_db),
):
    db_member = project_member.get(db=db, id=member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Project member not found")

    return project_member.update(db=db, db_obj=db_member, obj_in=member_in)


@router.delete("/{member_id}", response_model=ProjectMember)
def delete_project_member(
    member_id: int,
    db: Session = Depends(get_db),
):
    db_member = project_member.get(db=db, id=member_id)
    if not db_member:
        raise HTTPException(status_code=404, detail="Project member not found")

    return project_member.remove(db=db, id=member_id)