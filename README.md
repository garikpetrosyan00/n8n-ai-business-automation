# n8n AI Business Automation Portfolio Project

![Automation Architecture](docs/architecture-diagram.png)

A simulation-based automation portfolio project showing how inbound leads can be validated, qualified, routed, and prepared for CRM + internal notifications using n8n.

## Project Summary

This repository demonstrates a practical automation pattern for small service businesses and agencies:
- Receive leads via webhook
- Validate and normalize input
- Score and route leads by priority
- Prepare CRM-ready records
- Generate internal follow-up notifications

The focus is demo reliability and architecture clarity, not vendor-specific production integrations.

## Business Problem Solved

Teams handling inbound leads often face:
- inconsistent form payloads
- manual qualification and routing
- delayed follow-up
- duplicated CRM entry

This project models a clean workflow architecture that reduces those bottlenecks and makes handoff logic explicit.

## Architecture Summary

Main components:
- `workflows/lead-intake-workflow.json`: intake, validation, normalization, scoring simulation
- `workflows/ai-qualification-routing-workflow.json`: qualification + routing to CRM-ready format
- `workflows/crm-sync-notifications-workflow.json`: CRM sync payload prep, audit log, internal notification
- `services/helper-api/`: reusable FastAPI utility service (`/normalize-lead`, `/score-lead`)

Data flow (demo path):
1. `POST /lead-intake`
2. Lead is validated and normalized
3. Scoring simulation produces priority and summary
4. Output becomes input for qualification/CRM workflows in chained demos

## Workflow List

1. **Lead Intake Workflow** (`/lead-intake`)
   - Accepts flat or nested lead payloads
   - Returns normalized lead + AI-style scoring output

2. **AI Qualification & Routing Workflow** (`/ai-qualification`)
   - Produces qualification details
   - Routes into high/medium/low buckets and CRM-ready record

3. **CRM Sync & Notifications Workflow** (`/crm-sync`)
   - Validates CRM-required fields
   - Builds CRM sync record, audit event, internal notification

## Helper API Role

The helper API is included as a reusable companion service for expansion.
- Current workflows run standalone for reliability and simpler demo setup.
- The API shows how shared normalization/scoring logic can be centralized when workflow logic grows.

## Fast Local Setup

### Prerequisites
- Docker + Docker Compose

### Start

```bash
cp .env.example .env
docker compose up --build
```

### Open services
- n8n: `http://localhost:5678`
- helper API: `http://localhost:8000`

## Demo Steps

1. Open n8n and import workflows from `workflows/`.
2. Open **Lead Intake Workflow** and click **Execute workflow** (test mode).
3. Send the sample lead payload (command below).
4. Confirm response shape matches `samples/sample-ai-output.json`.
5. Repeat for `ai-qualification` and `crm-sync` if you want full pipeline walkthrough.

## Sample API Call

Use the test webhook while running from the editor:

```bash
curl -X POST "http://localhost:5678/webhook-test/lead-intake" \
  -H "Content-Type: application/json" \
  -d @samples/sample-lead.json
```

Optional (nested form-style payload now supported too):

```bash
curl -X POST "http://localhost:5678/webhook-test/lead-intake" \
  -H "Content-Type: application/json" \
  -d @samples/sample-lead-nested.json
```

If the workflow is active (not test mode), use:

```bash
curl -X POST "http://localhost:5678/webhook/lead-intake" \
  -H "Content-Type: application/json" \
  -d @samples/sample-lead.json
```

## Expected Result

The response includes:
- `lead_id`
- normalized `lead` object
- `ai_output` (`lead_score`, `lead_category`, `priority`, `summary`)
- `internal_notification`

Reference output: `samples/sample-ai-output.json`

## Limitations (Simulation Notes)

- AI scoring is deterministic simulation logic, not an LLM call.
- CRM sync is payload preparation only; no real CRM API writes.
- Notification output is generated JSON, not a live Slack/email integration.
- No production auth, retries, queueing, or observability stack is included.

## Why This Is Relevant for Clients

This repo demonstrates client-relevant skills:
- n8n workflow decomposition by business stage
- robust input handling and validation
- practical webhook contracts
- CRM-ready transformation patterns
- clear demo documentation and reproducible local setup

## Repository Structure

```text
.
├── README.md
├── docker-compose.yml
├── docs/
├── samples/
├── services/helper-api/
└── workflows/
```

## License

MIT (`LICENSE`)
