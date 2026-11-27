"""Records the intended change without touching cloud resources. Used by tests and demos."""


def apply(plan: dict) -> dict:
    if not plan.get("module"):
        return {"ok": False, "error": "plan has no module"}
    return {"ok": True, "error": None, "mode": "dry_run", "module": plan["module"]}
