# Module: sandbox-web

Creates one resource group and one monthly budget for a single approved request.

- Inputs: see `variables.tf`. Every input is required except `tags`.
- Outputs: resource group name, consumed by the root composition.
- Budget notification: 80% of `monthly_budget_usd`, sent to the request owner.

Change this module through a reviewed pull request. A change here affects every future request for the template, so it needs Platform approval.
