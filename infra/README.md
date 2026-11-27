# Infrastructure

Infrastructure-as-code for the landing zones the portal provisions into, and for the portal's own platform (not included in this first build).

| Folder | Contents |
|---|---|
| `terraform/` | Root composition plus one module per golden-path template |

The portal's own platform (AKS, Postgres, Service Bus, Key Vault) is owned by the platform team and lives in a separate repository, so that the thing being governed does not also govern itself.
