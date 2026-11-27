# Worker service

Turns an approved request into a plan and applies it through an adapter.

- `provisioner.py` builds the plan. Plans contain module name, variables and tags, but never secrets.
- `provision_queue.py` defines the queue contract for production (at-least-once delivery, idempotent by request ID).
- `adapters/dry_run.py` records the intent without changing anything. Used in tests and demos.
- `adapters/terraform.py` writes the tfvars file and produces the init, plan and apply commands. It executes only when explicitly enabled on the landing-zone runner.

Every tag on a provisioned resource carries `portal_request`, so any cloud resource can be traced to the approval that created it.
