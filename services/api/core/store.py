"""Request storage. First build is in memory; production swaps this for Postgres
behind the same get/put/all interface (see docs/adr/0002)."""
from core.models import RequestRecord

_REQUESTS: dict[str, RequestRecord] = {}


def put(rec: RequestRecord) -> RequestRecord:
    _REQUESTS[rec.id] = rec
    return rec


def get(request_id: str) -> RequestRecord | None:
    return _REQUESTS.get(request_id)


def all_requests() -> list[RequestRecord]:
    return list(_REQUESTS.values())


def clear() -> None:
    _REQUESTS.clear()
