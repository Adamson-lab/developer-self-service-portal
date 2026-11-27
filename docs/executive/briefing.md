# Executive briefing: developer self-service environments

## The problem
Engineers wait days to weeks for environments. Each wait is handled by a ticket, a manual approval and a hand-built configuration. The result is slow delivery, inconsistent controls, and no reliable answer to "who approved this, and what does it cost?"

## What the portal does
Engineers choose from a catalogue of reviewed golden paths. Each request is checked against policy in the same request: entitlement, cost ceiling and environment scope. Production always needs an independent approver. Every decision is recorded in an audit chain that cannot be changed without detection.

## Controls at a glance
- Only catalogued templates can be provisioned (no shadow IT).
- Cost ceilings are hard limits; over-ceiling requests are refused, not queued.
- Production requires a second person, enforced by the API.
- Non-production environments expire automatically unless extended.
- Audit evidence is exportable and verifiable on demand.

## Decisions requested
1. Endorse the golden-path catalogue as the only route to new environments, starting with three templates.
2. Mandate production approval through the portal from the next quarter.
3. Fund the production build: Postgres, Service Bus, identity binding and the landing-zone runner.

## Measures we propose to report quarterly
- Median time from request to ready, by template (target set with Platform).
- Share of environments created through the portal versus outside it.
- Non-production spend against ceilings, and count of expired environments.
- Audit verification status and count of denied self-approval attempts.

Figures are targets for sign-off, not measured results. The first measured report follows the production pilot.
