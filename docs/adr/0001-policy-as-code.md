# 0001: Policy as code

**Context.** Auditors need to read the rules and see that they run. Rules hidden in a web form or a spreadsheet cannot be tested or versioned.

**Decision.** Express admission rules in Python (`core/policy.py`) for the running service, and mirror them in Rego (`policies/rego/portal.rego`). CI runs both engines on the same cases (`policies/examples/requests.json`) and fails on any difference.

**Consequences.** Two implementations to maintain, which is a cost we accept. In return, Security can review Rego without reading Python, and drift cannot reach production unnoticed. Every guardrail in `policies/guardrails.yaml` names its test.

**Guardrails affected.** G-01, G-02, G-03.
