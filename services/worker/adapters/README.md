# Adapters

An adapter takes a plan and returns `{ok, error, mode}`. The API does not know which adapter is in use.

| Adapter | Executes cloud changes | Used in |
|---|---|---|
| `dry_run` | No | Tests, demos, CI |
| `terraform` | Only with `execute=True` on the landing-zone runner | Staging and production pipelines |

New adapters (Bicep, CloudFormation, Deployment Manager) must keep the same return shape and be idempotent on `request_id`.
