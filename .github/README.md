# .github

GitHub-specific configuration: CI pipelines, issue forms and ownership rules.

- `workflows/` holds the CI pipeline. Every pull request must pass unit tests, integration tests, the OPA cross-check and the catalog lint before merge.
- `ISSUE_TEMPLATE/` holds the forms teams use to request a new golden-path template, which is how the catalog grows under review.
- `CODEOWNERS` (added with the first branch protection rule) routes policy and catalog changes to Security and Platform. Those reviews are the approvals auditors look for when they test G-01 through G-03.

Branch protection on `main`: no direct pushes, two approvals for changes under `policies/` or `catalog/`, signed commits required.
