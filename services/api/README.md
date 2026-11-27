# API service

FastAPI application that exposes the catalogue, request lifecycle, approvals and audit reads.

## Run

```powershell
cd services\api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000/docs for the interactive API.

## Endpoints

| Method | Path | Purpose | Guardrails |
|---|---|---|---|
| GET | `/healthz` | Liveness | — |
| GET | `/catalog` | List golden-path templates | Catalog scope |
| GET | `/catalog/{name}` | One template | Catalog scope |
| POST | `/requests` | Submit a request; policy runs in the same call | G-01, G-02, G-03 |
| GET | `/requests` | List requests | — |
| GET | `/requests/{id}` | One request | — |
| POST | `/requests/{id}/approve` | Approve or decline | G-05, G-06 |
| GET | `/audit` | Export the audit chain | G-04 |
| GET | `/audit/verify` | Verify the chain | G-07 |

## Layout

- `main.py` wires routers and sets up the import path for sibling services.
- `routes/` holds thin HTTP handlers.
- `core/` holds domain logic with no HTTP imports, so it is unit-testable on its own.
- `requirements.txt` pins every dependency to an exact version.

## Known limits (first build)
The store is in memory and the approver identity comes from the request body. Both are fixed before production; see `docs/security/threat-model.md`.
