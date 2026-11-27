# Unit tests

Fast, no HTTP. Each test names the guardrail it proves in a comment.

- `test_policy.py` covers G-01, G-02, G-03 and G-06, including the normalisation case where `A@Bank.example ` must not bypass self-approval.
- `test_audit_chain.py` covers G-07: intact chains verify, edited entries are detected, deleted entries are detected.

When a new rule is added to `core/policy.py`, it needs a test here and a line in `policies/guardrails.yaml`.
