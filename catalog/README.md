# Catalog

The catalog is the only source of what can be provisioned. If a template is not listed in
`templates.yaml`, no request for it can succeed. This is the control against shadow IT.

## Files

| File | Purpose |
|---|---|
| `templates.yaml` | Reviewed golden-path templates, one block per template |
| `schemas/template.schema.json` | JSON Schema used by the CI job to lint each template |

## Template fields

| Field | Meaning | Governs |
|---|---|---|
| `environments` | Where the template may be used | Catalog scoping |
| `allowed_teams` | Which teams are entitled | G-03 |
| `max_monthly_usd` | Hard cost ceiling per environment | G-02 |
| `approval_required` | Forces a human approver even outside prod | G-01 |
| `iac_module` | Terraform module under `infra/terraform/modules` | Provisioning |

## Adding a template

1. Open an issue using the new-template form.
2. Add the block to `templates.yaml`.
3. Add a matching module under `infra/terraform/modules/<iac_module>`.
4. Add a unit test in `tests/unit/test_policy.py`.
5. Platform and Security approve the PR. CODEOWNERS enforces this.
