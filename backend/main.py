import os
from contextlib import asynccontextmanager
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.models import Ticket, AgentResult, Rep, TicketUpdateRequest, StatusEnum
from backend.mock_data import get_mock_tickets, get_mock_reps
from backend import agent

load_dotenv()

# In-memory state
tickets: dict[str, Ticket] = {}
reps: dict[str, Rep] = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load mock data on startup
    for t in get_mock_tickets():
        tickets[t.id] = t
    for r in get_mock_reps():
        reps[r.id] = r
    yield


app = FastAPI(title="Thrudark Customer Experience API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ── Helper ────────────────────────────────────────────────────────────────────

def _rep_active_counts() -> dict[str, int]:
    return {rep_id: len(r.active_tickets) for rep_id, r in reps.items()}


def _apply_agent_result(ticket: Ticket, result: AgentResult) -> None:
    """Mutate ticket in-place with agent result and update rep assignments."""
    # Remove from previous rep's active list
    if ticket.assigned_to and ticket.assigned_to in reps:
        prev = reps[ticket.assigned_to]
        if ticket.id in prev.active_tickets:
            prev.active_tickets.remove(ticket.id)

    ticket.category = result.category
    ticket.priority = result.priority
    ticket.assigned_to = result.assigned_to
    ticket.escalation_flag = result.escalation_flag
    ticket.draft_reply = result.draft_reply
    ticket.status = StatusEnum.in_progress

    # Add to new rep's active list
    if result.assigned_to and result.assigned_to in reps:
        new_rep = reps[result.assigned_to]
        if ticket.id not in new_rep.active_tickets:
            new_rep.active_tickets.append(ticket.id)


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/api/tickets", response_model=list[Ticket])
def list_tickets(
    status: Optional[str] = Query(None),
    assigned_to: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
):
    result = list(tickets.values())
    if status:
        result = [t for t in result if t.status.value == status]
    if assigned_to:
        result = [t for t in result if t.assigned_to == assigned_to]
    if priority:
        result = [t for t in result if t.priority.value == priority]
    # Most recent first
    result.sort(key=lambda t: t.created_at, reverse=True)
    return result


@app.get("/api/tickets/{ticket_id}", response_model=Ticket)
def get_ticket(ticket_id: str):
    if ticket_id not in tickets:
        raise HTTPException(status_code=404, detail="Ticket not found")
    return tickets[ticket_id]


@app.post("/api/tickets/{ticket_id}/process", response_model=AgentResult)
def process_ticket(ticket_id: str):
    if ticket_id not in tickets:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket = tickets[ticket_id]
    try:
        result = agent.process_ticket(ticket, _rep_active_counts())
    except EnvironmentError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")
    _apply_agent_result(ticket, result)
    return result


@app.post("/api/tickets/process-all")
def process_all_tickets():
    """Process all tickets that have not yet been classified (no category set)."""
    processed = []
    errors = []
    for ticket_id, ticket in tickets.items():
        if ticket.category is not None:
            continue  # already processed
        try:
            result = agent.process_ticket(ticket, _rep_active_counts())
            _apply_agent_result(ticket, result)
            processed.append(ticket_id)
        except Exception as e:
            errors.append({"ticket_id": ticket_id, "error": str(e)})
    return {"processed": processed, "errors": errors}


@app.patch("/api/tickets/{ticket_id}", response_model=Ticket)
def update_ticket(ticket_id: str, update: TicketUpdateRequest):
    if ticket_id not in tickets:
        raise HTTPException(status_code=404, detail="Ticket not found")
    ticket = tickets[ticket_id]

    # Handle rep reassignment
    if update.assigned_to is not None and update.assigned_to != ticket.assigned_to:
        if ticket.assigned_to and ticket.assigned_to in reps:
            old_rep = reps[ticket.assigned_to]
            if ticket_id in old_rep.active_tickets:
                old_rep.active_tickets.remove(ticket_id)
        if update.assigned_to in reps:
            new_rep = reps[update.assigned_to]
            if ticket_id not in new_rep.active_tickets:
                new_rep.active_tickets.append(ticket_id)

    update_data = update.model_dump(exclude_none=True)
    for field, value in update_data.items():
        setattr(ticket, field, value)

    # If resolved, remove from rep's active list
    if ticket.status == StatusEnum.resolved and ticket.assigned_to in reps:
        rep = reps[ticket.assigned_to]
        if ticket_id in rep.active_tickets:
            rep.active_tickets.remove(ticket_id)

    return ticket


@app.get("/api/reps", response_model=list[Rep])
def list_reps():
    return list(reps.values())


@app.get("/api/stats")
def get_stats():
    all_tickets = list(tickets.values())
    by_status: dict[str, int] = {}
    by_priority: dict[str, int] = {}
    by_category: dict[str, int] = {}
    escalations = 0

    for t in all_tickets:
        by_status[t.status.value] = by_status.get(t.status.value, 0) + 1
        by_priority[t.priority.value] = by_priority.get(t.priority.value, 0) + 1
        if t.category:
            by_category[t.category.value] = by_category.get(t.category.value, 0) + 1
        if t.escalation_flag:
            escalations += 1

    return {
        "total": len(all_tickets),
        "by_status": by_status,
        "by_priority": by_priority,
        "by_category": by_category,
        "escalations": escalations,
    }


# ── Static frontend ───────────────────────────────────────────────────────────

frontend_dir = os.path.join(os.path.dirname(__file__), "..", "frontend")

@app.get("/")
def serve_index():
    return FileResponse(os.path.join(frontend_dir, "index.html"))

app.mount("/static", StaticFiles(directory=frontend_dir), name="static")
