# Lifecycle

Non-production environments expire so forgotten sandboxes do not accumulate spend.

`reaper-schedule.json` defines the time to live per template and the action taken:

| Template | Time to live | Action |
|---|---|---|
| sandbox-web | 14 days | Notify 3 days ahead, then destroy |
| app-staging | 30 days | Notify 5 days ahead, then destroy |
| payments-prod | None | Never auto-expires; decommissioned by change request |

Owners can extend a non-production environment once by submitting a new request with a justification. Production is never reaped automatically.
