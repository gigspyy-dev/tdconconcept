# Thrudark Customer Experience Agent

A Claude-powered customer service dashboard for Thrudark — UK high-performance outerwear with special forces heritage.

## Setup

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set your Anthropic API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your key
   ```

3. **Run the app**
   ```bash
   uvicorn backend.main:app --reload
   ```

4. **Open the dashboard**

   Navigate to [http://localhost:8000](http://localhost:8000)

## Features

- 12 realistic mock tickets loaded on startup (orders, returns, complaints, feedback, warranty)
- Click **Process with AI** on any ticket to run the Claude agent
- Use **⚡ Process All with AI** in the sidebar to classify and draft replies for all tickets at once
- Filter by rep, status, or priority
- Edit draft replies and update ticket status directly in the dashboard
- Escalation warnings displayed prominently for flagged tickets
- Stats bar shows live counts of open / urgent / escalations

## Architecture

```
backend/
  models.py      — Pydantic models (Ticket, AgentResult, Rep, TicketUpdateRequest)
  mock_data.py   — 12 mock tickets + 2 reps (Sarah, James)
  agent.py       — Claude claude-sonnet-4-6 agent with tool use
  main.py        — FastAPI app, in-memory state, REST API
frontend/
  index.html     — Single-page dashboard (vanilla JS, dark theme)
```
