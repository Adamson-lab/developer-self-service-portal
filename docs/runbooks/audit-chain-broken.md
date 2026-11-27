# Runbook: audit chain broken

**Symptom.** `GET /audit/verify` returns `intact: false`, or AuditChainBroken fires. This is a security incident until proven otherwise.

**First checks.**
1. Note `first_broken_seq`. Entries before it are unaffected.
2. Compare the chain head with the hourly export in the SIEM. A mismatch means the in-service copy changed.
3. Check database audit logs for `UPDATE` or `DELETE` against the audit table, and the identities that ran them.

**Containment.**
- Freeze provisioning: set the feature flag `portal.provisioning.enabled` to false.
- Preserve the database snapshot before any other action.
- Do not repair the chain by rewriting hashes. A rewritten chain is not evidence.

**Escalation.** CISO office and Internal Audit within one hour. Notify the regulator liaison if restricted data classes are in scope.
