# Verification policy

## Governance baseline

Run the commands in [CONTRIBUTING.md](../../CONTRIBUTING.md). Governance tests must
exercise failures as well as a valid fixture: ambiguous ownership, dependency cycles,
stale ledger, missing version bump, history/release changes and invalid skill/docs.
These checks use synthetic temporary repositories and no application credentials.

## Runtime changes

Choose tests for observable behavior and material invariants. A prose-only change
needs local-link/version validation, not a browser/container build. A runtime change
needs relevant regression, negative, boundary and recovery evidence. Keep real
investigations out of fixtures and development indexes.

| Behavior | Required evidence when implemented/changed |
| --- | --- |
| Permissions and publication | Allowed/denied requests for private/public pages, files, exports and SSE; withdrawal/cache behavior |
| Jobs | Real disposable PostgreSQL concurrency, restart, lost wake-up, retries and orphan recovery |
| Captures | Isolated browser with synthetic controlled pages, redirect/DNS/URL boundaries and partial failures |
| Evidence/export | Real output bytes, completeness, tampering/missing-file failures, manifest/checksum verification and receipt escaping |
| Migrations | Prototype fixtures to target schema, data/hash preservation and rollback limits |
| Backup/restore | Restore into a clean environment, verify records and artifact hashes, then complete core workflow |
| UI | Browser evidence of implemented screens, error states and access behavior; mockup screenshots stay labeled mockups |

Mocks are useful for unit boundaries; they do not establish database locking,
network/browser isolation, OAuth integration or restore correctness. Required gates
fail on empty/skipped suites. Report commands, environment, results and unavailable
checks precisely; do not label planned tests as passed. Current runtime evidence
is absent at this baseline; see [source review](../04-current-state.md).

## Platform lanes

[ADR-012](../decisions/0012-macos-development-and-linux-qualification.md) and
[document 56](../requirements/56-macos-development-and-linux-qualification.md)
select MAC-DEV for current implementation. Execute required real local PG/browser/
container/byte/recovery checks on this topology. Label host/guest/tool/image identity;
keep local failure/blocked evidence distinct from deferred-linux cases. Empty,
skipped or mock-only required local tests do not pass. Native Linux support,
server-kernel enforcement and clean-host target qualification are later Linux
iteration obligations; they do not hold all Mac coding/reviews. No arbitrary public
capture or production release is enabled by reclassifying its unproven checks.
