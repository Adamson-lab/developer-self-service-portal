---
name: New golden-path template
about: Propose a reviewed environment template for the catalog
labels: catalog, needs-triage
---

## Business owner
Name, role, cost centre.

## Purpose
What workload does this environment serve, and what is the expected lifetime?

## Entitled teams
Teams allowed to request this template. Use directory group names.

## Environments
- [ ] dev
- [ ] staging
- [ ] prod

## Cost ceiling
Proposed monthly ceiling in USD and the basis for the number (price calculator export, prior run-rate, or vendor quote).

## Approval
- [ ] Always require a named approver, even outside prod
- [ ] Standard (prod still requires approval by policy)

## Data classification
Public / internal / confidential / restricted. Restricted data needs Security sign-off before the template is merged.

## Implementation
Terraform module name and location under `infra/terraform/modules`.

## Controls checklist
- [ ] Tags include owner, team, template and request ID
- [ ] Budget alert configured at 80%
- [ ] Logs routed to the central SIEM
- [ ] Destruction path defined in `lifecycle/`
