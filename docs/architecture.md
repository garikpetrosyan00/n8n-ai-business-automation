# Architecture Overview

This project follows a modular n8n architecture for business automation. It receives inbound leads, enriches and qualifies them with AI, synchronizes records to CRM systems, and sends internal notifications for fast follow-up.

## Main Workflow Modules

1. Intake Module
   - Accepts lead data from webhooks or form integrations.
   - Performs initial validation and normalization.

2. AI Qualification Module
   - Sends lead context to an AI service for scoring and classification.
   - Produces structured output for downstream automation.

3. CRM Sync Module
   - Maps qualified lead fields into CRM-ready payloads.
   - Creates or updates records through REST API calls.

4. Notification Module
   - Sends internal alerts (for example Slack or email).
   - Includes priority, score, and recommended next actions.

5. Storage and Audit Module
   - Persists workflow events and key payload snapshots.
   - Supports traceability and troubleshooting.

6. Helper Service Module
   - Provides reusable API endpoints for normalization and scoring support.
   - Keeps logic centralized when workflows need shared utility behavior.

## Data Flow

1. A lead enters through an intake webhook.
2. n8n validates and standardizes the payload.
3. Optional helper API calls (`/normalize-lead`, `/score-lead`) can be used when shared utility logic is needed.
4. The normalized lead is passed to the AI qualification step.
5. Structured AI output is used to determine routing and priority.
6. Qualified data is synchronized to CRM through API endpoints.
7. Internal notifications are sent to the relevant team.
8. Key events and outputs are stored for audit and reporting.

## Lead Intake Workflow Data Flow

This repository now includes an implemented lead intake workflow at `workflows/lead-intake-workflow.json`.

1. `Webhook Trigger` receives a new lead through `POST /lead-intake`.
2. `Validate Required Fields` checks for `name`, `email`, `company`, and `message`.
3. `Check Validation Result` routes invalid payloads to a validation error response path.
4. `Normalize Lead Data` trims text fields, lowercases email, and adds `received_at`.
5. `AI Qualification Simulation` generates `lead_score`, `lead_category`, `priority`, and `summary`.
6. `Prepare Storage Record` structures lead and qualification data into a storage-ready payload.
7. `Build Notification Message` prepares an internal alert message for operations or sales teams.
8. `Respond Success` or `Respond Validation Error` returns the final JSON response to the caller.

## AI Qualification & Routing Workflow

This repository also includes `workflows/ai-qualification-routing-workflow.json` for AI-style qualification and routing after intake normalization.

1. `Webhook Trigger` receives structured lead data through `POST /ai-qualification`.
2. `Prepare AI Input` compacts lead context (company, role, inquiry summary, and budget estimate) into an analysis-ready payload.
3. `AI Qualification Simulation` produces qualification fields such as `lead_score`, `lead_category`, `priority`, `confidence`, `recommended_action`, and `crm_stage`.
4. `Route High Priority` and `Route Medium Priority` apply conditional branching for high, medium, and low-priority outcomes.
5. Branch-specific `Prepare CRM Record` nodes build a normalized CRM-ready object (`contact_name`, `contact_email`, `company`, `score`, `priority`, `stage`, `owner_hint`, `notes`).
6. `Prepare Follow-up Recommendation` outputs a concise internal next step based on routing outcome.
7. `Respond Final JSON` returns a structured response suitable for downstream storage, sync, or notification workflows.

In the overall architecture, normalized lead data from intake can be passed into this workflow to determine business priority, CRM readiness, and team follow-up actions.

## CRM Sync & Notifications Workflow

This repository also includes `workflows/crm-sync-notifications-workflow.json` to represent downstream operations after a lead is qualified.

1. `Webhook Trigger` receives qualified lead payloads through `POST /crm-sync`.
2. `Validate CRM Payload` checks required fields: `contact_name`, `contact_email`, `company`, `priority`, and `stage`.
3. `Route Validation` sends valid payloads through success processing and invalid payloads to an error response path.
4. `Prepare CRM Sync Record` converts lead data into a normalized CRM sync object with `external_id`, business fields, and `synced_at`.
5. `Prepare Audit Log` builds a lightweight event record for traceability (`event_type`, `timestamp`, `company`, `contact_email`, `sync_status`).
6. `Prepare Internal Notification` formats an operational alert message for internal channels.
7. `Build Success Response` returns `crm_sync_record`, `audit_log`, `internal_notification`, and `status: success`.
8. `Build Error Response` returns `status: error`, `missing_fields`, and a concise validation message.

In the full architecture, this workflow acts as the execution layer that translates qualification outcomes into CRM-ready records, audit entries, and team notifications.

## Helper API in Architecture

The helper API (`services/helper-api`) sits alongside n8n as a lightweight utility service.

1. In this portfolio version, workflows run without a hard dependency on helper endpoints to keep demos reliable.
2. n8n can call helper endpoints when repeated transformation logic should be centralized in code.
3. `/normalize-lead` can be used before routing to enforce a consistent lead contract.
4. `/score-lead` can be used when deterministic scoring should be shared across workflows.
5. `/health` supports quick local checks during development and demos.

Helper services are useful in automation systems because they keep workflow graphs readable while allowing reusable business logic to be maintained in one place.

## Demo and Samples Reference

- Walkthrough guide: `docs/demo-walkthrough.md`
- Project summary: `docs/project-summary.md`
- Lead sample: `samples/sample-lead.json`
- Alternate nested lead sample: `samples/sample-lead-nested.json`
- Qualification sample: `samples/sample-qualified-lead.json`
- CRM sync sample: `samples/sample-crm-sync-output.json`
- Notification sample: `samples/sample-notification-message.json`
