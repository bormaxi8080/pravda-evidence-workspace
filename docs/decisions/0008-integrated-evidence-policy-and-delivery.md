# ADR-008: Consolidate evidence policy and implementation gates

Date: 2026-11-09. Status: **selected design refinement; not implemented/qualified**.
Authority: user requested further documentation improvements based on ADR-002–007.
Sources: requirements 01–38 and their local consistency review in document 39.
No new external product/API assertion or independent review is implied.

## Decision

Keep the 158 requirement IDs and 70 V0 / 88 later-stage scope unchanged. Refine
their implementation through documents 39–43: one purpose-specific evidence
eligibility policy, dependency/invalidation authority, shared resource accounting,
feature/migration/restore gates and an executable-contract delivery catalogue.

Differentiate profile completeness, byte integrity, acquisition channel, asserted
provenance, editorial approval and operation eligibility. A verified upload cannot
inherit local server witnessing, a comparison cannot approve evidence, and a public
projection cannot grant permission to export private originals or annotations.

Use bounded dependency closure with an immediate root deny fence before asynchronous
cleanup. Retraction, cache eviction, corruption and emergency purge have different
effects. A pin prevents ordinary cache eviction, not authorized emergency removal.
No legal-hold service, general hard-delete UI or automatic original retention is added.

Preserve each operation's resource ceilings, add one installation-wide heavy-task
permit initially, and reserve 100 of the existing 1,000 pending positions for small
interactive work. Bulk/automatic/derived work is limited to the remaining 900;
finite fair claiming prevents a new feature from monopolizing the host. These are
selected limits requiring measurement, not latency/capacity guarantees.

Select effective feature state from implemented contracts, compatible schema,
qualification evidence, operator enablement, dependencies, quotas and restore hold.
Unknown contracts fail; disabling admission does not rewrite accepted evidence or
implicitly withdraw existing publications. Record rollback limits before migration.

Resolve B2 stop semantics: no new observation may use a stopped/expired acquisition
epoch; descriptors registered while active may receive explicit upload approval
after stop and finish under current upload/actor authority unless cancelled/revoked. Stored historical
session linkage is not a requirement that recording still be active at finalize.

## Consequences

Add EWP-53–60 and SYS-ACC-01–10 as refinements/verification of existing requirements,
not new product capabilities. Registry: 60 tasks, 56 scenario definitions; all prior
IDs remain stable. V0 implements only applicable server/core portions, leaving
C/H/B adapters and flags disabled. Later modules do not become V0 prerequisites.

Specification alone advances for this prose iteration. Application/Deployment and
planned Browser Extension/Evidence Contracts versions do not change. Actual schemas,
policy code, migrations, fixture harness, runtime tests and operator qualification
remain implementation deliverables. A local commit is not a release/deployment.
