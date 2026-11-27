"""Append-only, hash-chained audit log.

Each entry stores the SHA-256 of the previous entry, so any edit or deletion after the
fact is detectable by verify(). This is the evidence regulators and internal audit ask for.
"""
import hashlib
import json
from datetime import datetime, timezone

_EVENTS: list[dict] = []
GENESIS = "0" * 64


def _digest(body: dict) -> str:
    canonical = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def record(event: str, **data) -> dict:
    prev = _EVENTS[-1]["hash"] if _EVENTS else GENESIS
    body = {
        "seq": len(_EVENTS) + 1,
        "ts": datetime.now(timezone.utc).isoformat(),
        "event": event,
        "prev_hash": prev,
        **data,
    }
    entry = {**body, "hash": _digest(body)}
    _EVENTS.append(entry)
    return entry


def export() -> list[dict]:
    return list(_EVENTS)


def verify() -> tuple[bool, int | None]:
    """Return (intact, first_broken_seq). Recomputes every hash and link."""
    prev = GENESIS
    for entry in _EVENTS:
        body = {k: v for k, v in entry.items() if k != "hash"}
        if entry["prev_hash"] != prev or _digest(body) != entry["hash"]:
            return False, entry["seq"]
        prev = entry["hash"]
    return True, None


def reset() -> None:
    _EVENTS.clear()
