# Workflows

`ci.yml` runs on every pull request and every push to `main`.

| Job | What it proves |
|---|---|
| `unit` | Policy rules G-01 to G-03 and G-06, plus audit chain G-07, behave as documented |
| `integration` | The API enforces G-04, G-05 and G-06 end to end through HTTP |
| `catalog-lint` | Every template in `catalog/templates.yaml` matches the schema and `cost/budgets.json` |
| `rego-crosscheck` | OPA and the Python engine return identical decisions for every case in `policies/examples` |

A failing job blocks merge. Nothing in this pipeline touches cloud subscriptions; deployment is a separate, approval-gated workflow owned by the landing-zone team.
