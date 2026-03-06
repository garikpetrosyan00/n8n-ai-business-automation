from datetime import datetime, timezone
from typing import Any

from fastapi import FastAPI


app = FastAPI(title="n8n Helper API", version="0.1.0")


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/normalize-lead")
def normalize_lead(payload: dict[str, Any]) -> dict[str, Any]:
    name = _clean_text(payload.get("name") or payload.get("contact_name"))
    email = _clean_text(payload.get("email") or payload.get("contact_email")).lower()
    company = _clean_text(payload.get("company"))
    role = _clean_text(payload.get("role") or payload.get("job_title"))
    message = _clean_text(payload.get("message") or payload.get("inquiry_summary"))

    normalized = {
        "contact_name": name,
        "contact_email": email,
        "company": company,
        "role": role,
        "inquiry_summary": message,
        "budget_estimate_usd": payload.get("budget_estimate_usd")
        or payload.get("estimated_budget_usd"),
        "source": _clean_text(payload.get("source") or "helper-api"),
        "normalized_at": datetime.now(timezone.utc).isoformat(),
    }

    return {"status": "ok", "normalized_lead": normalized}


@app.post("/score-lead")
def score_lead(payload: dict[str, Any]) -> dict[str, Any]:
    summary = _clean_text(payload.get("message") or payload.get("inquiry_summary")).lower()
    budget = payload.get("budget_estimate_usd") or payload.get("estimated_budget_usd") or 0

    try:
        budget_value = float(budget)
    except (TypeError, ValueError):
        budget_value = 0.0

    lead_score = 40
    if "automation" in summary:
        lead_score += 20
    if "crm" in summary or "integration" in summary:
        lead_score += 15
    if "urgent" in summary or "asap" in summary:
        lead_score += 10
    if budget_value >= 10000:
        lead_score += 10

    lead_score = max(0, min(100, lead_score))

    if lead_score >= 80:
        priority = "high"
        lead_category = "high-fit"
    elif lead_score >= 60:
        priority = "medium"
        lead_category = "qualified"
    else:
        priority = "low"
        lead_category = "early-stage"

    contact_name = _clean_text(payload.get("name") or payload.get("contact_name") or "Lead")
    company = _clean_text(payload.get("company") or "Unknown company")

    return {
        "status": "ok",
        "lead_score": lead_score,
        "priority": priority,
        "lead_category": lead_category,
        "summary": f"{contact_name} from {company} scored {lead_score} ({priority}).",
        "scored_at": datetime.now(timezone.utc).isoformat(),
    }
