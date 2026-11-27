# Golden-path modules

One module per catalogued template. Modules share a variable contract (`request_id`, `team`, `environment`, `owner`, `monthly_budget_usd`, `location`, `tags`) so the root composition can select any of them.

| Module | Template | Environment | Notable controls |
|---|---|---|---|
| `sandbox-web` | Web application sandbox | dev | Budget alert at 80%, owner tagging |
| `app-staging` | Application staging | staging | Expiry tag for the reaper, budget alert |
| `payments-prod` | Payments production landing zone | prod | Restricted data class tag, change ticket tag, private networking intent |

Every module creates a resource group named from team, environment and the first eight characters of the request ID, so names stay unique and traceable.
