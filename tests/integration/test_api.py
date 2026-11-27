import pytest
from fastapi.testclient import TestClient

from core import audit, store
from main import app

client = TestClient(app)

SANDBOX = {"template": "sandbox-web", "team": "web", "requester": "dev1@bank.example",
           "environment": "dev", "estimated_monthly_usd": 50}
PROD = {"template": "payments-prod", "team": "payments", "requester": "eng1@bank.example",
        "environment": "prod", "estimated_monthly_usd": 9000,
        "justification": "Q1 card-processing capacity"}


@pytest.fixture(autouse=True)
def clean_state():
    store.clear()
    audit.reset()
    yield


def test_healthz():
    assert client.get("/healthz").json()["status"] == "ok"


def test_sandbox_is_auto_provisioned():
    r = client.post("/requests", json=SANDBOX)
    assert r.status_code == 201
    body = r.json()
    assert body["status"] == "ready"
    assert body["plan"]["module"] == "sandbox-web"


def test_prod_waits_for_approval():  # G-01
    r = client.post("/requests", json=PROD)
    assert r.json()["status"] == "pending_approval"
    assert r.json()["plan"] is None


def test_self_approval_is_blocked():  # G-06
    rec = client.post("/requests", json=PROD).json()
    r = client.post(f"/requests/{rec['id']}/approve",
                    json={"approver": PROD["requester"], "accept": True})
    assert r.status_code == 403
    events = [e["event"] for e in client.get("/audit").json()]
    assert "request.approval_denied" in events


def test_independent_approval_provisions():  # G-05
    rec = client.post("/requests", json=PROD).json()
    r = client.post(f"/requests/{rec['id']}/approve",
                    json={"approver": "cto@bank.example", "accept": True})
    assert r.json()["status"] == "ready"
    assert r.json()["approver"] == "cto@bank.example"


def test_provision_refuses_rejected_state():  # G-05
    from core.models import RequestStatus
    from routes.requests import _provision
    rec = client.post("/requests", json={**SANDBOX, "estimated_monthly_usd": 999}).json()
    stored = store.get(rec["id"])
    assert stored.status == RequestStatus.rejected
    with pytest.raises(RuntimeError, match="G-05"):
        _provision(stored)


def test_cost_ceiling_is_rejected_not_queued():  # G-02
    r = client.post("/requests", json={**SANDBOX, "estimated_monthly_usd": 999})
    assert r.json()["status"] == "rejected"


def test_audit_trail_is_recorded():  # G-04
    client.post("/requests", json=SANDBOX)
    events = [e["event"] for e in client.get("/audit").json()]
    assert events[:2] == ["request.submitted", "request.provisioning"]
    assert client.get("/audit/verify").json()["intact"] is True  # G-07


def test_unknown_template_is_404():
    r = client.post("/requests", json={**SANDBOX, "template": "shadow-it-vm"})
    assert r.status_code == 404
