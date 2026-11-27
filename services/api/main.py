"""Developer Self-Service Portal API.

Run from services/api:  uvicorn main:app --reload
"""
import sys
from pathlib import Path

# Make sibling packages (worker, notifier) importable when running from services/api.
SERVICES_DIR = Path(__file__).resolve().parents[1]
if str(SERVICES_DIR) not in sys.path:
    sys.path.insert(0, str(SERVICES_DIR))

from fastapi import FastAPI  # noqa: E402

from routes import audit as audit_routes  # noqa: E402
from routes import catalog as catalog_routes  # noqa: E402
from routes import requests as request_routes  # noqa: E402

app = FastAPI(
    title="Developer Self-Service Portal",
    version="0.2.0",
    description="Policy-gated golden-path environments with approvals and a tamper-evident audit trail.",
)
app.include_router(catalog_routes.router)
app.include_router(request_routes.router)
app.include_router(audit_routes.router)


@app.get("/healthz", tags=["ops"])
def healthz():
    return {"status": "ok", "version": app.version}
