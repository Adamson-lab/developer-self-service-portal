from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class Environment(str, Enum):
    dev = "dev"
    staging = "staging"
    prod = "prod"


class EnvRequest(BaseModel):
    template: str = Field(min_length=3, max_length=64)
    team: str = Field(min_length=2, max_length=64)
    requester: str = Field(min_length=5, max_length=128)
    environment: Environment
    estimated_monthly_usd: float = Field(ge=0)
    justification: Optional[str] = Field(default=None, max_length=500)


class Decision(BaseModel):
    allowed: bool
    needs_approval: bool
    reasons: list[str] = []


class RequestStatus(str, Enum):
    rejected = "rejected"
    pending_approval = "pending_approval"
    approved = "approved"
    provisioning = "provisioning"
    ready = "ready"
    failed = "failed"


class RequestRecord(BaseModel):
    id: str
    request: EnvRequest
    decision: Decision
    status: RequestStatus
    approver: Optional[str] = None
    plan: Optional[dict] = None
    failure: Optional[str] = None


class ApprovalBody(BaseModel):
    approver: str = Field(min_length=5, max_length=128)
    accept: bool
