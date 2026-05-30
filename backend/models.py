from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ChannelEnum(str, Enum):
    email = "email"
    ticket = "ticket"


class StatusEnum(str, Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"


class PriorityEnum(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    urgent = "urgent"


class CategoryEnum(str, Enum):
    order_status = "order_status"
    return_exchange = "return_exchange"
    product_query = "product_query"
    complaint = "complaint"
    feedback = "feedback"
    warranty = "warranty"
    shipping_issue = "shipping_issue"
    other = "other"


class Ticket(BaseModel):
    id: str
    subject: str
    body: str
    customer_name: str
    customer_email: str
    channel: ChannelEnum
    created_at: datetime
    status: StatusEnum = StatusEnum.open
    priority: PriorityEnum = PriorityEnum.medium
    category: Optional[CategoryEnum] = None
    assigned_to: Optional[str] = None
    escalation_flag: bool = False
    draft_reply: Optional[str] = None


class AgentResult(BaseModel):
    ticket_id: str
    category: CategoryEnum
    priority: PriorityEnum
    assigned_to: Optional[str]
    escalation_flag: bool
    escalation_reason: Optional[str]
    draft_reply: str
    confidence_score: float


class Rep(BaseModel):
    id: str
    name: str
    email: str
    active_tickets: List[str] = []


class TicketUpdateRequest(BaseModel):
    status: Optional[StatusEnum] = None
    priority: Optional[PriorityEnum] = None
    category: Optional[CategoryEnum] = None
    assigned_to: Optional[str] = None
    escalation_flag: Optional[bool] = None
    draft_reply: Optional[str] = None
