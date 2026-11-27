# Observability

Everything an operator or auditor needs to know whether the controls are working.

| File | Purpose |
|---|---|
| `audit-event.schema.json` | Contract for each audit entry, checked in tests |
| `slo.yaml` | Proposed service-level objectives |
| `alerts.yaml` | Alert rules tied to runbooks and owners |

Alerts name an owner and a runbook. An alert without either is removed during review.
