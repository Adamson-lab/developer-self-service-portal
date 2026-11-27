# Routes

HTTP handlers only. Each file owns one resource.

| File | Resource | Notes |
|---|---|---|
| `requests.py` | Environment requests and approvals | Holds the provisioning gate `_provision`, the only path to the worker (G-05) |
| `catalog.py` | Golden-path templates | Read-only; the catalogue changes through reviewed pull requests |
| `audit.py` | Audit export and verification | Read-only; no write endpoint exists by design |

Handlers do three things: validate input with Pydantic, call `core`, and shape the response. Business rules do not belong here. If a rule is in a route, it cannot be unit-tested without HTTP.
