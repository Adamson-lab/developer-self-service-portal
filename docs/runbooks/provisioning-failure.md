# Runbook: provisioning failure

**Symptom.** Requests move to `failed`, or the ProvisioningFailureRateHigh alert fires.

**First checks (5 minutes).**
1. `GET /requests?status=failed` and read `failure` on each record. Group by error text.
2. Check the landing-zone health dashboard for the affected subscription.
3. Confirm the Terraform state lease is not held by a stale run.

**Containment.**
- If one template fails everywhere, pause that template in `catalog/templates.yaml` by removing its environment entry, and announce it in the platform channel.
- If one subscription fails, pause new requests for that business unit only.
- Do not re-run an apply by hand. Re-submit through the portal so the audit trail stays complete.

**Escalation.** Platform on-call within 15 minutes for a single template; Security on-call if an error mentions authorisation or policy.

**Recovery.** Once the cause is fixed, retry failed requests through the approval path. Record the incident reference against each affected request ID.
