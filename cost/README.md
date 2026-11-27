# Cost controls

`budgets.json` holds the monthly ceilings used in policy and the alert thresholds used in Azure budgets.

- Ceilings must match `catalog/templates.yaml`. CI fails on drift (`scripts/catalog_lint.py`).
- Alerts fire at 50%, 80% and 100% of ceiling, and go to FinOps and the platform approvers.
- Estimated cost is the requester's figure at submission. Actual spend is reconciled monthly from the cost-management export, and variances above 20% trigger a review of the template.
