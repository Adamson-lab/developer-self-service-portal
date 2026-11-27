from fastapi import APIRouter

from core import audit

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("")
def export_audit():
    return audit.export()


@router.get("/verify")
def verify_chain():
    intact, broken_at = audit.verify()
    return {"intact": intact, "first_broken_seq": broken_at, "events": len(audit.export())}
