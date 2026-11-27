# Core domain

Pure Python with no HTTP or cloud imports.

| Module | Responsibility | Guardrails |
|---|---|---|
| `models.py` | Request, decision, status and approval types | — |
| `catalog.py` | Loads and validates `catalog/templates.yaml` at startup | Catalog scope |
| `policy.py` | Admission rules and segregation of duties | G-01, G-02, G-03, G-06 |
| `audit.py` | Hash-chained audit log and verification | G-04, G-07 |
| `store.py` | Request storage behind a small interface | — |

Because this layer has no framework dependency, the unit tests in `tests/unit` run in under a second and the policy logic can be reviewed as plain Python.
