"""Policy evaluation. Mirrors policies/rego/portal.rego so both engines can be cross-checked.

Each rule carries the guardrail ID from policies/guardrails.yaml.
"""
from core.models import Decision, EnvRequest


def evaluate(req: EnvRequest, tpl: dict) -> Decision:
    reasons: list[str] = []

    # G-03 / catalog scoping: template must be offered in the requested environment
    if req.environment.value not in tpl["environments"]:
        reasons.append(f"template '{req.template}' is not offered in {req.environment.value}")

    # G-03: team entitlement
    allowed_teams = tpl.get("allowed_teams", ["any"])
    if "any" not in allowed_teams and req.team not in allowed_teams:
        reasons.append(f"team '{req.team}' is not entitled to this template")

    # G-02: cost ceiling is a hard reject, never a queue
    ceiling = tpl["max_monthly_usd"]
    if req.estimated_monthly_usd > ceiling:
        reasons.append(
            f"estimated ${req.estimated_monthly_usd:,.0f}/mo exceeds ceiling ${ceiling:,.0f}/mo"
        )

    if reasons:
        return Decision(allowed=False, needs_approval=False, reasons=reasons)

    # G-01: production always needs a named human; templates can also opt in
    needs = bool(tpl.get("approval_required")) or req.environment.value == "prod"
    return Decision(allowed=True, needs_approval=needs, reasons=[])


def can_approve(approver: str, requester: str) -> tuple[bool, str]:
    # G-06: segregation of duties. Nobody approves their own request.
    if approver.strip().lower() == requester.strip().lower():
        return False, "requester cannot approve their own request (G-06)"
    return True, ""
