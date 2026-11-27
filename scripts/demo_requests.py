"""Sends a demo sequence to a running API so stakeholders see every control fire.

Usage (PowerShell):  python scripts\\demo_requests.py --base http://127.0.0.1:8000
Standard library only, so it runs on any corporate laptop without extra installs.
"""
import argparse
import json
import urllib.error
import urllib.request

CASES = [
    ("Sandbox within budget (auto-approved)", {
        "template": "sandbox-web", "team": "web", "requester": "dev1@bank.example",
        "environment": "dev", "estimated_monthly_usd": 60}),
    ("Sandbox over cost ceiling (G-02)", {
        "template": "sandbox-web", "team": "web", "requester": "dev1@bank.example",
        "environment": "dev", "estimated_monthly_usd": 900}),
    ("Prod request by entitled team (needs approval, G-01)", {
        "template": "payments-prod", "team": "payments", "requester": "eng1@bank.example",
        "environment": "prod", "estimated_monthly_usd": 9000,
        "justification": "Card-processing capacity for Q1"}),
    ("Prod request by unentitled team (G-03)", {
        "template": "payments-prod", "team": "marketing", "requester": "mkt1@bank.example",
        "environment": "prod", "estimated_monthly_usd": 500}),
]


def call(method: str, url: str, body: dict | None = None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, json.loads(resp.read())
    except urllib.error.HTTPError as err:
        return err.code, json.loads(err.read() or b"{}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base", default="http://127.0.0.1:8000")
    args = parser.parse_args()

    for label, body in CASES:
        status, rec = call("POST", f"{args.base}/requests", body)
        print(f"\n== {label}\n   HTTP {status}  status={rec.get('status')}  reasons={rec.get('decision', {}).get('reasons', [])}")
        if rec.get("status") == "pending_approval":
            code, out = call("POST", f"{args.base}/requests/{rec['id']}/approve",
                             {"approver": "cto@bank.example", "accept": True})
            print(f"   approval by CTO -> HTTP {code} status={out.get('status')}")

    _, verdict = call("GET", f"{args.base}/audit/verify")
    print(f"\nAudit chain intact: {verdict['intact']} ({verdict['events']} events)")


if __name__ == "__main__":
    main()
