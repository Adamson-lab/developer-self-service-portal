# 0003: Hash-chained audit log

**Context.** Internal audit must be able to show that no approval or provisioning event was added, changed or removed after the fact.

**Decision.** Each audit entry stores the SHA-256 of its body and the hash of the previous entry (`core/audit.py`). `GET /audit/verify` recomputes the chain. The production store writes to an append-only Postgres table with database-level `UPDATE` and `DELETE` revoked, and the chain head is exported to the SIEM every hour.

**Consequences.** Verification is O(n) and runs on a schedule, not per request. A hash chain shows tampering but does not prevent it, which is why the database permissions and the SIEM export are part of the control.

**Guardrails affected.** G-04, G-07.
