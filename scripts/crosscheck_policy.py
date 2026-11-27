"""Runs every case in policies/examples/requests.json through the Python engine and, when the
`opa` binary is available, through the Rego policy. Fails if either disagrees with the expectation.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "api"))

from core.models import EnvRequest  # noqa: E402
from core.policy import evaluate  # noqa: E402

CASES = json.loads((ROOT / "policies" / "examples" / "requests.json").read_text())
REGO = ROOT / "policies" / "rego" / "portal.rego"


def python_decision(case: dict) -> dict:
    req = EnvRequest(template=case["template"]["name"], requester="x@bank.example", **case["request"])
    d = evaluate(req, case["template"])
    return {"allowed": d.allowed, "needs_approval": d.needs_approval}


def rego_decision(case: dict) -> dict | None:
    if not shutil.which("opa"):
        return None
    payload = {"template": case["template"], "request": {"requester": "x@bank.example", **case["request"]}}
    out = subprocess.run(
        ["opa", "eval", "-d", str(REGO), "-I", "data.portal.decision", "--format", "json"],
        input=json.dumps(payload), capture_output=True, text=True, check=True,
    )
    value = json.loads(out.stdout)["result"][0]["expressions"][0]["value"]
    return {"allowed": value["allowed"], "needs_approval": value["needs_approval"]}


def main() -> int:
    failures = 0
    for case in CASES:
        expected = case["expect"]
        py = python_decision(case)
        rg = rego_decision(case)
        ok = py == expected and (rg is None or rg == expected)
        status = "PASS" if ok else "FAIL"
        rego_note = "rego skipped" if rg is None else f"rego={rg}"
        print(f"{status}  {case['name']}: python={py} {rego_note} expected={expected}")
        failures += 0 if ok else 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
