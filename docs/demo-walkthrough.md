# Demo Walkthrough

This walkthrough is optimized for reviewers who want to run the project quickly and verify believable outputs.

## 1) Start Services

```bash
cp .env.example .env
docker compose up --build
```

Check containers:

```bash
docker compose ps
```

Expected:
- `n8n` is running on `5678`
- `helper-api` is running on `8000`

Optional helper API health check:

```bash
curl -s http://localhost:8000/health
```

## 2) Import Workflows in n8n

1. Open `http://localhost:5678`
2. Import these files from `workflows/`:
   - `lead-intake-workflow.json`
   - `ai-qualification-routing-workflow.json`
   - `crm-sync-notifications-workflow.json`

## 3) Webhook Usage Guidance (Important)

n8n has two webhook URL modes:
- **Test mode** (when you click **Execute workflow**): `/webhook-test/<path>`
- **Active mode** (workflow toggled active): `/webhook/<path>`

Paths used in this repo:
- `lead-intake`
- `ai-qualification`
- `crm-sync`

## 4) Run Lead Intake Demo

1. Open **Lead Intake Workflow**.
2. Click **Execute workflow**.
3. In a terminal, run:

```bash
curl -X POST "http://localhost:5678/webhook-test/lead-intake" \
  -H "Content-Type: application/json" \
  -d @samples/sample-lead.json
```

Expected response shape:
- `lead_id`
- `status: processed`
- `lead` (normalized fields)
- `ai_output` (`lead_score`, `priority`, `lead_category`, `summary`)
- `internal_notification`

Reference: `samples/sample-ai-output.json`

Optional compatibility check (nested payload):

```bash
curl -X POST "http://localhost:5678/webhook-test/lead-intake" \
  -H "Content-Type: application/json" \
  -d @samples/sample-lead-nested.json
```

## 5) Run AI Qualification Demo

1. Open **AI Qualification & Routing Workflow**.
2. Click **Execute workflow**.
3. Run:

```bash
curl -X POST "http://localhost:5678/webhook-test/ai-qualification" \
  -H "Content-Type: application/json" \
  -d @samples/sample-lead.json
```

Reference: `samples/sample-qualified-lead.json`

## 6) Run CRM Sync Demo

1. Open **CRM Sync & Notifications Workflow**.
2. Click **Execute workflow**.
3. Run:

```bash
curl -X POST "http://localhost:5678/webhook-test/crm-sync" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_name": "Elena Martinez",
    "contact_email": "elena.martinez@northstarlogistics.example",
    "company": "NorthStar Logistics",
    "priority": "high",
    "stage": "Discovery",
    "score": 95,
    "summary": "High-fit lead for automation and CRM support"
  }'
```

Reference: `samples/sample-crm-sync-output.json`

## 7) Short Validation Checklist

- [ ] `samples/sample-lead.json` works directly with `/lead-intake`
- [ ] Intake response includes normalized lead + AI output
- [ ] AI qualification response includes `qualified_lead` and routing bucket
- [ ] CRM sync response includes `crm_sync_record`, `audit_log`, and `internal_notification`
- [ ] Required-field validation returns a clear 400 error when payload is incomplete

## Notes

- This is a simulation portfolio demo: scoring, CRM sync, and notifications are intentionally mocked as deterministic logic.
- Helper API is included as a reusable companion service and can be integrated into workflows when scaling complexity.
