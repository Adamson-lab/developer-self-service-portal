"""Queue contract between the API and the worker.

First build calls the adapter synchronously. Production uses Azure Service Bus (or SQS /
Pub/Sub) with at-least-once delivery, so every adapter must be idempotent on request_id.
"""
from typing import Protocol


class ProvisionQueue(Protocol):
    def enqueue(self, plan: dict) -> None: ...
    def dequeue(self) -> dict | None: ...
