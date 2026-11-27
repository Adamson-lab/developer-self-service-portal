# Catalog schemas

`template.schema.json` is the contract every catalog entry must satisfy. It rejects unknown keys (`additionalProperties: false`), so a typo such as `max_monthy_usd` fails the build instead of silently removing a cost ceiling. The CI job `catalog-lint` validates every template against it on each pull request.

Changing the schema is itself a reviewed change, because loosening it can weaken G-02.
