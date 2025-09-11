import logging
from sqlalchemy.orm import Session

from app.db.session import Base, engine
from app.core.config import settings
from app.schemas.user import UserCreate
from app.crud.crud_user import user as user_crud

# Import all models to ensure they are registered with SQLAlchemy
# from app.models.user import User
# from app.models.project import Project
# from app.models.task import Task
# from app.models.ticket import Ticket, TicketStatus, TicketPriority
# from app.models.comment import Comment
# from app.models.project_member import ProjectMember, ProjectRole
# from app.models.subtask import Subtask

# from app.models.activity import Activity, ActivityType
# from app.models.attachment import Attachment
# from app.models.time_log import TimeLog
from app.models import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create initial superuser if it doesn't exist
    superuser = user_crud.get_by_email(db, email="admin@example.com")
    if not superuser:
        user_in = UserCreate(
            email="admin@example.com",
            username="admin",
            password="admin",  # Change this in production!
            is_superuser=True,
            full_name="Initial Admin",
        )
        superuser = user_crud.create(db, obj_in=user_in)
        logger.info(f"Superuser created: {superuser.email}")
    else:
        logger.info(f"Superuser already exists: {superuser.email}")


def main() -> None:
    from app.db.session import SessionLocal
    
    logger.info("Creating initial data")
    db = SessionLocal()
    init_db(db)
    logger.info("Initial data created")


if __name__ == "__main__":
    main()