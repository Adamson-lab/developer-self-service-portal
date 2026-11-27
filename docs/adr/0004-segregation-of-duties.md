# 0004: Segregation of duties enforced in the API

**Context.** A single engineer who can both request and approve production capacity defeats the purpose of approval. Hiding the approve button in the web UI does not stop a direct API call.

**Decision.** `core/policy.can_approve` rejects any approval where the approver matches the requester, after case and whitespace normalisation. The denial is recorded in the audit log as `request.approval_denied`. Approver groups come from Entra ID through `identity/group-map.json`.

**Consequences.** Emergency break-glass procedures are out of scope for this build and need their own ADR, with a second approver and an automatic alert.

**Guardrails affected.** G-01, G-06.
