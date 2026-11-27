# Services

The portal runs as three cooperating services plus a notifier. The first build packages them in one repository, and each keeps its own deployable boundary in production.

| Service | Folder | Responsibility | Scale profile |
|---|---|---|---|
| API | `api/` | Requests, decisions, approvals, audit reads | Stateless, horizontal |
| Worker | `worker/` | Turns approved requests into infrastructure changes | Queue-driven, per-subscription concurrency |
| Notifier | `notifier/` | Messages to requesters and approvers | Low volume, retried |

Services talk through the API and the queue only. No service reads another service's storage.
