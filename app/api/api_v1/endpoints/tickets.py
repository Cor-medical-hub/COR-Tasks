from typing import Any, List, Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_active_user_dep, get_current_active_superuser_dep
from app.core.errors import NotFoundError, ForbiddenError
from app.crud.crud_ticket import ticket
from app.crud.crud_user import user
from app.models.user import User
from app.models.ticket import TicketStatus, TicketPriority
from app.schemas.ticket import Ticket as TicketSchema, TicketCreate, TicketUpdate, TicketList

router = APIRouter()


@router.get("/", response_model=List[TicketSchema])
async def read_tickets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    status: Optional[TicketStatus] = None,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Retrieve tickets with optional filtering by status."""
    if status:
        tickets = ticket.get_multi_by_status(db, status=status, skip=skip, limit=limit)
    else:
        tickets = ticket.get_multi(db, skip=skip, limit=limit)
    return tickets


@router.post("/", response_model=TicketSchema)
async def create_ticket(
    *,
    db: Session = Depends(get_db),
    ticket_in: TicketCreate,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Create new ticket."""
    # Validate assigned_to_id if provided
    if ticket_in.assigned_to_id:
        assigned_user = user.get(db, id=ticket_in.assigned_to_id)
        if not assigned_user:
            raise NotFoundError(detail="Assigned user not found")
    
    return ticket.create_with_owner(db, obj_in=ticket_in, created_by_id=current_user.id)


@router.get("/me", response_model=List[TicketSchema])
async def read_my_tickets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Get tickets created by current user."""
    return ticket.get_multi_by_owner(db, created_by_id=current_user.id, skip=skip, limit=limit)


@router.get("/assigned", response_model=List[TicketSchema])
async def read_assigned_tickets(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Get tickets assigned to current user."""
    return ticket.get_multi_by_assignee(db, assigned_to_id=current_user.id, skip=skip, limit=limit)


@router.get("/search", response_model=List[TicketSchema])
async def search_tickets(
    *,
    db: Session = Depends(get_db),
    query: str = Query(..., min_length=3),
    skip: int = 0,
    limit: int = 100,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Search tickets by title or description."""
    return ticket.search_tickets(db, query=query, skip=skip, limit=limit)


@router.get("/{ticket_id}", response_model=TicketSchema)
async def read_ticket(
    *,
    db: Session = Depends(get_db),
    ticket_id: int,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Get ticket by ID."""
    ticket_obj = ticket.get(db, id=ticket_id)
    if not ticket_obj:
        raise NotFoundError(detail="Ticket not found")
    return ticket_obj


@router.put("/{ticket_id}", response_model=TicketSchema)
async def update_ticket(
    *,
    db: Session = Depends(get_db),
    ticket_id: int,
    ticket_in: TicketUpdate,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Update a ticket."""
    ticket_obj = ticket.get(db, id=ticket_id)
    if not ticket_obj:
        raise NotFoundError(detail="Ticket not found")
    
    # Only ticket creator, assigned user, or superuser can update
    if not (ticket_obj.created_by_id == current_user.id or 
            ticket_obj.assigned_to_id == current_user.id or 
            current_user.is_superuser):
        raise ForbiddenError(detail="Not enough permissions")
    
    # Validate assigned_to_id if provided
    if ticket_in.assigned_to_id and ticket_in.assigned_to_id != ticket_obj.assigned_to_id:
        assigned_user = user.get(db, id=ticket_in.assigned_to_id)
        if not assigned_user:
            raise NotFoundError(detail="Assigned user not found")
    
    return ticket.update(db, db_obj=ticket_obj, obj_in=ticket_in)


@router.delete("/{ticket_id}", response_model=TicketSchema)
async def delete_ticket(
    *,
    db: Session = Depends(get_db),
    ticket_id: int,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Delete a ticket."""
    ticket_obj = ticket.get(db, id=ticket_id)
    if not ticket_obj:
        raise NotFoundError(detail="Ticket not found")
    
    # Only ticket creator or superuser can delete
    if not (ticket_obj.created_by_id == current_user.id or current_user.is_superuser):
        raise ForbiddenError(detail="Not enough permissions")
    
    return ticket.remove(db, id=ticket_id)


@router.post("/{ticket_id}/close", response_model=TicketSchema)
async def close_ticket(
    *,
    db: Session = Depends(get_db),
    ticket_id: int,
    current_user: User = get_current_active_user_dep,
) -> Any:
    """Close a ticket."""
    ticket_obj = ticket.get(db, id=ticket_id)
    if not ticket_obj:
        raise NotFoundError(detail="Ticket not found")
    
    # Only ticket creator, assigned user, or superuser can close
    if not (ticket_obj.created_by_id == current_user.id or 
            ticket_obj.assigned_to_id == current_user.id or 
            current_user.is_superuser):
        raise ForbiddenError(detail="Not enough permissions")
    
    return ticket.close_ticket(db, ticket_id=ticket_id)