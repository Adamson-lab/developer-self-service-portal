"""Translate an approved request into IaC module inputs.

The plan is deterministic and contains no secrets, so it can be stored in the audit trail
and replayed. Tags carry the portal request ID so every cloud resource traces back to an
approved request (a control auditors check first).
"""


def build_plan(request_id: str, req, tpl: dict) -> dict:
    return {
        "request_id": request_id,
        "module": tpl["iac_module"],
        "variables": {
            "team": req.team,
            "environment": req.environment.value,
            "owner": req.requester,
            "monthly_budget_usd": tpl["max_monthly_usd"],
            "justification": req.justification or "",
        },
        "tags": {
            "portal_request": request_id,
            "managed_by": "self-service-portal",
            "environment": req.environment.value,
        },
    }
