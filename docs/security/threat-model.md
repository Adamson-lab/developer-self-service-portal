# Threat model (STRIDE)

## Trust boundaries
1. Browser or CLI to portal API (through the gateway with mTLS and Entra ID tokens).
2. Portal API to queue and database.
3. Worker to cloud control plane (managed identity, scoped role assignment).
4. Portal to outbound notifications (relay only).

## Threats and mitigations

| Category | Threat | Mitigation | Guardrail |
|---|---|---|---|
| Spoofing | Caller impersonates an approver | Entra ID token validated at gateway; approver identity taken from token, not body (v0.3 target) | G-06 |
| Tampering | Audit entries altered | Hash chain, append-only table, hourly SIEM export | G-07 |
| Repudiation | Approver denies approving | Approval record stores approver, time and request hash | G-04 |
| Information disclosure | Credentials leak through plan files | Plans hold no secrets; workers use managed identity | — |
| Denial of service | Request flood fills queue | Gateway rate limits per identity; queue depth alarm | — |
| Elevation of privilege | Engineer provisions prod directly | Prod requires independent approver; provisioning gate | G-01, G-05 |
| Elevation of privilege | Request for an unentitled template | Entitlement from directory group, checked on every request | G-03 |
| Shadow IT | Free-form resource creation | Only catalogued templates can be requested | Catalog |

## Known gaps (tracked)
- Approver identity is currently accepted from the request body. The gateway must bind it to the token before production (issue to be opened).
- The in-memory store has no durability. Blocked until Postgres lands.
- Break-glass access is not yet designed (see ADR 0004).
