from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

from app.models.ticket import TicketStatus, TicketPriority


# Shared properties
class TicketBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[TicketStatus] = TicketStatus.OPEN
    priority: Optional[TicketPriority] = TicketPriority.MEDIUM
    assigned_to_id: Optional[int] = None


# Properties to receive via API on creation
class TicketCreate(TicketBase):
    pass


# Properties to receive via API on update
class TicketUpdate(TicketBase):
    title: Optional[str] = None
    status: Optional[TicketStatus] = None
    priority: Optional[TicketPriority] = None


# Properties shared by models stored in DB
class TicketInDBBase(TicketBase):
    id: int
    created_by_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Properties to return via API
class Ticket(TicketInDBBase):
    pass


# Properties stored in DB
class TicketInDB(TicketInDBBase):
    pass


# For listing tickets
class TicketList(BaseModel):
    tickets: List[Ticket]
    total: int