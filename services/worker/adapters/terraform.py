"""Terraform adapter. Writes a tfvars file per request and returns the exact commands.

It does not execute by default. Enable execution only in the landing-zone runner, with a
scoped service principal and remote state locking.
"""
import json
import subprocess
from pathlib import Path

INFRA_ROOT = Path(__file__).resolve().parents[3] / "infra" / "terraform"


def commands(plan: dict, workdir: Path = INFRA_ROOT) -> list[list[str]]:
    tfvars = workdir / f"{plan['request_id']}.auto.tfvars.json"
    return [
        ["terraform", "-chdir=" + str(workdir), "init", "-input=false"],
        ["terraform", "-chdir=" + str(workdir), "plan", "-input=false",
         f"-var-file={tfvars.name}", "-out=tfplan"],
        ["terraform", "-chdir=" + str(workdir), "apply", "-input=false", "tfplan"],
    ]


def render_tfvars(plan: dict, workdir: Path = INFRA_ROOT) -> Path:
    payload = {
        "template": plan["module"],
        "request_id": plan["request_id"],
        **plan["variables"],
        "tags": plan["tags"],
    }
    path = workdir / f"{plan['request_id']}.auto.tfvars.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return path


def apply(plan: dict, execute: bool = False) -> dict:
    render_tfvars(plan)
    cmds = commands(plan)
    if not execute:
        return {"ok": True, "error": None, "mode": "plan_only", "commands": cmds}
    for cmd in cmds:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if proc.returncode != 0:
            return {"ok": False, "error": proc.stderr.strip()[:500], "mode": "terraform"}
    return {"ok": True, "error": None, "mode": "terraform"}
