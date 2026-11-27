# Notifier

Builds messages for four events: submitted, approved, declined, ready and failed. Each message names the template and environment and carries the request ID, never the full cost breakdown or any secret.

In the first build messages collect in an outbox list. Production posts to Teams channel webhooks for platform approvers and sends email through the enterprise relay for requesters. Delivery failures retry with backoff and raise an alert after three attempts.
