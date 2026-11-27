# Policies

Policy is code. Two engines express the same rules so Security can review either one:

| Path | Engine | Used by |
|---|---|---|
| `core/policy.py` (in `services/api`) | Python | The running API on every request |
| `rego/portal.rego` | OPA / Rego | CI cross-check and external policy review |

`examples/requests.json` holds cases with expected decisions. CI runs both engines against
them, so drift between the two implementations fails the build.

`guardrails.yaml` maps every rule ID (G-01 to G-07) to the code that enforces it and the test
that proves it. This file is the first thing an auditor should ask for.
