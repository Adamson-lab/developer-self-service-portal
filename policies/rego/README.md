# Rego policy

`portal.rego` is the declarative form of the portal's admission rules.

- `allow` is true only when `violations` is empty.
- `needs_approval` is true for any production request, or when the template opts in (G-01).
- Violations carry human-readable reasons that the API returns to the requester unchanged.

Run with OPA: `opa eval -d portal.rego -i input.json "data.portal.decision"`.
