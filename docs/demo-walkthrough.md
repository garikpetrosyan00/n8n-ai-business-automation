# Demo Walkthrough

This walkthrough shows how a sample lead moves through the automation hub from intake to CRM-ready output and internal notification.

## Narrative Flow

1. A new lead is submitted to the intake webhook.
2. Lead data is validated and normalized for consistency.
3. Qualification logic simulates AI-style scoring and categorization.
4. Qualified leads are routed by priority for next actions.
5. CRM sync payloads are prepared with audit metadata.
6. Internal notification content is generated for fast team follow-up.

## Workflow-to-Step Mapping

1. Intake and Validation
   - Workflow: `workflows/lead-intake-workflow.json`
   - Value: catches incomplete payloads early and standardizes incoming data.

2. Qualification and Routing
   - Workflow: `workflows/ai-qualification-routing-workflow.json`
   - Value: prioritizes leads and recommends actionable follow-up.

3. CRM Sync and Notifications
   - Workflow: `workflows/crm-sync-notifications-workflow.json`
   - Value: prepares CRM-ready records, creates audit logs, and informs internal teams.

## Sample Outputs

- Incoming lead example: `samples/sample-lead.json`
- Qualification output example: `samples/sample-qualified-lead.json`
- CRM sync output example: `samples/sample-crm-sync-output.json`
- Internal notification example: `samples/sample-notification-message.json`

## Business Value by Step

- Intake: improves reliability by validating required business data.
- Normalization: ensures consistent records across downstream systems.
- Qualification: helps teams focus on higher-value opportunities first.
- Routing: aligns follow-up urgency with lead quality.
- CRM Sync: reduces manual entry and supports pipeline visibility.
- Notification: shortens response time through automated internal alerts.
