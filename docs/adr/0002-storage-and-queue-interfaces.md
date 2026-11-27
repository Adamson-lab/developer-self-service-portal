# 0002: Storage and queue behind interfaces

**Context.** The first build must run on a laptop and in CI with no cloud dependencies, but must not lock us into an in-memory design.

**Decision.** `core/store.py` exposes `put`, `get` and `all_requests`. `worker/provision_queue.py` defines a queue protocol. In v0.2 the store is a dictionary and provisioning runs synchronously through `worker/adapters/dry_run.py`. Production uses Postgres and Azure Service Bus with at-least-once delivery.

**Consequences.** Adapters must be idempotent on `request_id`. Swapping storage touches one module. The current in-memory store is not durable and is not used for real environments.

**Guardrails affected.** G-04, G-05.
