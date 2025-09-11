from typing import List, Optional
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.attachment import Attachment
from app.schemas.attachment import AttachmentCreate, AttachmentUpdate
from app.crud.crud_activity import activity
from app.models.activity import ActivityType

class CRUDAttachment(CRUDBase[Attachment, AttachmentCreate, AttachmentUpdate]):
    def create_with_owner(
        self, db: Session, *, obj_in: AttachmentCreate, uploaded_by_id: int
    ) -> Attachment:
        db_obj = Attachment(
            filename=obj_in.filename,
            file_url=obj_in.file_url,
            task_id=obj_in.task_id,
            subtask_id=obj_in.subtask_id,
            uploaded_by_id=uploaded_by_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        activity.log(
            db,
            user_id=uploaded_by_id,
            action_type=ActivityType.CREATED,
            task_id=obj_in.task_id,
            new_value={"filename": obj_in.filename, "file_url": obj_in.file_url},
        )
        return db_obj

    def get_multi_by_task(
        self, db: Session, *, task_id: int, skip: int = 0, limit: int = 100
    ) -> List[Attachment]:
        return (
            db.query(self.model)
            .filter(Attachment.task_id == task_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def get_multi_by_subtask(
        self, db: Session, *, subtask_id: int, skip: int = 0, limit: int = 100
    ) -> List[Attachment]:
        return (
            db.query(self.model)
            .filter(Attachment.subtask_id == subtask_id)
            .offset(skip)
            .limit(limit)
            .all()
        )


attachment = CRUDAttachment(Attachment)