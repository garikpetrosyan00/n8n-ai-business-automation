# AI Business Automation Hub with n8n

AI-powered business automation project built with n8n to orchestrate lead intake, AI qualification, CRM synchronization, and internal notifications through modular workflows.

## Overview

This repository is a portfolio-grade foundation for designing and documenting practical business automation systems. It focuses on clean workflow organization, realistic payload examples, and a scalable architecture that can be extended with implementation-specific workflows.

## Core Features

- Lead intake via webhooks and API-driven integrations
- AI-based lead qualification with structured decision outputs
- CRM synchronization using REST APIs
- Internal notification routing for faster response times
- Modular workflow design for maintainability and reuse

## Proposed Architecture

- Intake workflows receive and normalize inbound lead data
- AI qualification workflows score, classify, and recommend actions
- CRM sync workflows create or update records in target systems
- Notification workflows deliver internal alerts by channel
- Storage/audit layer preserves key event and payload history

Detailed notes: see `docs/architecture.md`.

## Implemented Workflows

Lead Intake Workflow (`workflows/lead-intake-workflow.json`)
- Webhook trigger accepts `POST /lead-intake` lead submissions
- Validation checks required fields (`name`, `email`, `company`, `message`)
- Normalization standardizes whitespace, email casing, and timestamps
- AI qualification simulation assigns score, category, priority, and summary
- Storage preparation builds a structured record for downstream persistence
- Notification formatting creates an internal alert message for the team

AI Qualification & Routing Workflow (`workflows/ai-qualification-routing-workflow.json`)
- Webhook trigger accepts `POST /ai-qualification` structured lead payloads
- AI input preparation builds a compact analysis payload for scoring context
- Qualification simulation generates score, category, priority, confidence, and action hints
- Conditional routing separates high, medium, and low-priority processing paths
- CRM preparation outputs normalized `crm_record` fields with ownership hints
- Follow-up preparation outputs concise internal next-step recommendations

Together, the two workflows represent a clear progression from lead intake to qualification and routing.

## Folder Structure

```text
.
├── docs/
│   └── architecture.md
├── samples/
│   ├── sample-ai-output.json
│   ├── sample-qualified-lead.json
│   └── sample-lead.json
├── services/
│   └── helper-api/
│       └── .gitkeep
└── workflows/
    ├── .gitkeep
    ├── ai-qualification-routing-workflow.json
    └── lead-intake-workflow.json
```

## Tech Stack

- n8n for workflow orchestration
- REST APIs for system integrations
- JSON payload contracts for workflow interfaces
- Optional helper services (Node.js/Python) for custom extensions

## Future Improvements

- Add additional n8n workflows (qualification routing, CRM sync, notifications)
- Add environment configuration examples (`.env.example`)
- Add validation schemas for lead and AI payloads
- Add test harnesses for webhook and API contract testing
- Add deployment notes for self-hosted and cloud n8n setups

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
