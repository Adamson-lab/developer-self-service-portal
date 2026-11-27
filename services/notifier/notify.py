"""Builds notification messages and records them. Production posts to Teams or Slack webhooks
and email via the enterprise relay. Messages never include secrets or full cost breakdowns."""
from datetime import datetime, timezone

OUTBOX: list[dict] = []

SUBJECTS = {
    "request.submitted": "Environment request submitted",
    "request.approved": "Environment request approved",
    "request.declined": "Environment request declined",
    "request.ready": "Environment is ready",
    "request.failed": "Environment provisioning failed",
}


def notify(event: str, rec) -> dict:
    msg = {
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "to": [rec.request.requester] + ([rec.approver] if rec.approver else []),
        "subject": f"{SUBJECTS.get(event, event)}: {rec.request.template} ({rec.request.environment.value})",
        "request_id": rec.id,
    }
    OUTBOX.append(msg)
    return msg
