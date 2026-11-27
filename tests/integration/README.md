# Integration tests

These drive the real API and verify the controls as an outsider would see them.

- Sandbox provisioning end to end (G-04 audit events recorded).
- Production waits for approval (G-01).
- Self-approval is refused and the refusal is audited (G-06).
- A rejected request cannot reach the worker (G-05).
- Cost overruns are rejected, not queued (G-02).
- Unknown templates return 404, so shadow IT fails closed.

Each test resets the store and audit log first, so order does not matter.
