# Helper API

Lightweight FastAPI service that complements n8n workflows with reusable lead normalization and scoring utilities.

## Purpose

The helper API provides small transformation endpoints that can be called from n8n when workflow logic is better kept in code.

## Endpoints

- `GET /health`
  - Returns service health status.

- `POST /normalize-lead`
  - Accepts lead-like JSON and returns cleaned, normalized fields.

- `POST /score-lead`
  - Accepts lead-like JSON and returns a simulated lead qualification result (`lead_score`, `priority`, `lead_category`, `summary`).

## Quick Usage Examples

```bash
curl -X GET http://localhost:8000/health
```

```bash
curl -X POST http://localhost:8000/normalize-lead \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Elena Martinez",
    "email": "  Elena.Martinez@NorthStarLogistics.Example  ",
    "company": " NorthStar Logistics ",
    "job_title": "Operations Manager",
    "message": "Need automation for lead intake and CRM sync",
    "estimated_budget_usd": 18000
  }'
```

```bash
curl -X POST http://localhost:8000/score-lead \
  -H "Content-Type: application/json" \
  -d '{
    "contact_name": "Elena Martinez",
    "company": "NorthStar Logistics",
    "inquiry_summary": "Urgent automation and CRM integration support",
    "budget_estimate_usd": 18000
  }'
```

## How It Complements n8n

- Keeps reusable data transformation logic centralized.
- Reduces duplication across multiple workflows.
- Provides deterministic helper behavior for portfolio demonstrations.

## Run Locally

```bash
cd services/helper-api
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
