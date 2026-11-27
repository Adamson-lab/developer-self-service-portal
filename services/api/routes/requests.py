from uuid import uuid4

from fastapi import APIRouter, HTTPException

from core import audit, store
from core.catalog import load_catalog
from core.models import ApprovalBody, EnvRequest, RequestRecord, RequestStatus
from core.policy import can_approve, evaluate
from notifier.notify import notify
from worker.adapters import dry_run
from worker.provisioner import build_plan

router = APIRouter(prefix="/requests", tags=["requests"])
CATALOG = load_catalog()


@router.post("", status_code=201, response_model=RequestRecord)
def submit(req: EnvRequest):
    if req.template not in CATALOG:
        raise HTTPException(404, f"unknown template '{req.template}'")

    decision = evaluate(req, CATALOG[req.template])
    if not decision.allowed:
        status = RequestStatus.rejected
    elif decision.needs_approval:
        status = RequestStatus.pending_approval
    else:
        status = RequestStatus.approved

    rec = store.put(RequestRecord(id=str(uuid4()), request=req, decision=decision, status=status))
    audit.record("request.submitted", request_id=rec.id, requester=req.requester,
                 template=req.template, status=status.value, reasons=decision.reasons)
    notify("request.submitted", rec)

    if status == RequestStatus.approved:
        rec = _provision(rec)
    return rec


@router.get("", response_model=list[RequestRecord])
def list_requests():
    return store.all_requests()


@router.get("/{request_id}", response_model=RequestRecord)
def get_request(request_id: str):
    rec = store.get(request_id)
    if rec is None:
        raise HTTPException(404, "request not found")
    return rec


@router.post("/{request_id}/approve", response_model=RequestRecord)
def approve(request_id: str, body: ApprovalBody):
    rec = store.get(request_id)
    if rec is None:
        raise HTTPException(404, "request not found")
    if rec.status != RequestStatus.pending_approval:
        raise HTTPException(409, f"request is {rec.status.value}, not pending_approval")

    ok, why = can_approve(body.approver, rec.request.requester)
    if not ok:
        audit.record("request.approval_denied", request_id=rec.id, approver=body.approver, reason=why)
        raise HTTPException(403, why)

    rec.approver = body.approver
    if not body.accept:
        rec.status = RequestStatus.rejected
        store.put(rec)
        audit.record("request.declined", request_id=rec.id, approver=body.approver)
        notify("request.declined", rec)
        return rec

    audit.record("request.approved", request_id=rec.id, approver=body.approver)
    notify("request.approved", rec)
    return _provision(rec)


def _provision(rec: RequestRecord) -> RequestRecord:
    """Gate: only approved requests reach the worker (G-05)."""
    if rec.status not in (RequestStatus.approved, RequestStatus.pending_approval):
        raise RuntimeError(f"refusing to provision from state {rec.status.value} (G-05)")

    rec.status = RequestStatus.provisioning
    audit.record("request.provisioning", request_id=rec.id)
    plan = build_plan(rec.id, rec.request, CATALOG[rec.request.template])
    rec.plan = plan
    result = dry_run.apply(plan)  # production: enqueue to Service Bus, worker applies Terraform

    if result["ok"]:
        rec.status = RequestStatus.ready
        audit.record("request.ready", request_id=rec.id, module=plan["module"])
        notify("request.ready", rec)
    else:
        rec.status = RequestStatus.failed
        rec.failure = result["error"]
        audit.record("request.failed", request_id=rec.id, error=result["error"])
        notify("request.failed", rec)
    store.put(rec)
    return rec
