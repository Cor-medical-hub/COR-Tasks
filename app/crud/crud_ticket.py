from typing import Any, Dict, Optional, Union, List
from datetime import datetime

from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.crud.base import CRUDBase
from app.models.ticket import Ticket, TicketStatus
from app.schemas.ticket import TicketCreate, TicketUpdate


class CRUDTicket(CRUDBase[Ticket, TicketCreate, TicketUpdate]):
    def create_with_owner(self, db: Session, *, obj_in: TicketCreate, created_by_id: int) -> Ticket:
        """Create a new ticket with owner ID."""
        db_obj = Ticket(
            title=obj_in.title,
            description=obj_in.description,
            status=obj_in.status,
            priority=obj_in.priority,
            created_by_id=created_by_id,
            assigned_to_id=obj_in.assigned_to_id,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_multi_by_owner(
        self, db: Session, *, created_by_id: int, skip: int = 0, limit: int = 100
    ) -> List[Ticket]:
        """Get tickets created by a specific user."""
        return (
            db.query(self.model)
            .filter(Ticket.created_by_id == created_by_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_by_assignee(
        self, db: Session, *, assigned_to_id: int, skip: int = 0, limit: int = 100
    ) -> List[Ticket]:
        """Get tickets assigned to a specific user."""
        return (
            db.query(self.model)
            .filter(Ticket.assigned_to_id == assigned_to_id)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_multi_by_status(
        self, db: Session, *, status: TicketStatus, skip: int = 0, limit: int = 100
    ) -> List[Ticket]:
        """Get tickets by status."""
        return (
            db.query(self.model)
            .filter(Ticket.status == status)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def search_tickets(
        self, db: Session, *, query: str, skip: int = 0, limit: int = 100
    ) -> List[Ticket]:
        """Search tickets by title or description."""
        search = f"%{query}%"
        return (
            db.query(self.model)
            .filter(or_(Ticket.title.ilike(search), Ticket.description.ilike(search)))
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def close_ticket(self, db: Session, *, ticket_id: int) -> Optional[Ticket]:
        """Close a ticket by setting its status to closed and recording the closed time."""
        ticket = self.get(db, id=ticket_id)
        if not ticket:
            return None
        
        ticket.status = TicketStatus.CLOSED
        ticket.closed_at = datetime.now()
        db.add(ticket)
        db.commit()
        db.refresh(ticket)
        return ticket


ticket = CRUDTicket(Ticket)