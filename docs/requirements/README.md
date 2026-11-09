# Evidence Workspace requirements package

Date: 2026-11-09. Revision: 0.2. Status: **proposed specification baseline**.
Owner: product/engineering roles; individual assignees are not yet designated.
Versioned component: Specification. No runtime feature, accepted architecture ADR,
product release or measured capacity is created by this package.

## Purpose and authority

Translate the [English concept](../../concept/CONCEPT.en.md) and
[Russian concept](../../concept/CONCEPT.ru.md) into bounded, testable requirements,
an explicit first-prototype scope and a dependency-ordered documentation plan.
The [current-state review](../04-current-state.md) remains the source baseline;
the [HTML mockup](../../index.html) supplies visual/navigation intent only.

This package proposes a **V0 controlled pilot prototype**, distinct from existing
prototype code and the concept's production v1.0. V0 is a scope label, not a SemVer
release, and does not reset the inherited Python package version 1.1.0.
Deferring a capability from V0 does not remove its production requirement.

`shall` means a proposed mandatory requirement for the stated target. `should`
means a recommendation requiring a documented alternative if changed. Requirements
are proposed until adopted; source presence, implementation and verification are
separate statuses. The user's request authorizes drafting these documents, not
declaring every recommendation accepted or implementing runtime changes.

## Reading order and deliverables

| Document | Responsibility |
| --- | --- |
| [00 Documentation delivery plan](00-documentation-plan.md) | Work packages, dependencies, completion gates and detailed specification outputs |
| [01 Product and prototype scope](01-product-and-prototype.md) | Users, outcomes, included/deferred capabilities and bounded V0 limits |
| [02 Architecture](02-architecture.md) | Processes, logical modules, trust boundaries, data flow and deployment choices |
| [03 Domain and data](03-domain-and-data.md) | Entities, state separation, consistency, retention and legacy mapping |
| [04 Capture and jobs](04-capture-and-jobs.md) | URL capture, durable execution, retries, cancellation, batch preview and monitoring |
| [05 Evidence and export](05-evidence-and-export.md) | Artifact profiles, provenance, manifests, hash rules, export and WARC fidelity |
| [06 Editorial workflow and UX](06-editorial-and-ux.md) | Screens, organization, review, accessibility and user-visible failure states |
| [07 Security and publication](07-security-and-publication.md) | Roles, sessions, SSRF, disclosure, publication/revocation and audit |
| [08 API and events](08-api-and-events.md) | Proposed HTTP/SSE interfaces, error, idempotency and compatibility contracts |
| [09 Operations and migration](09-operations-and-migration.md) | Install, health, backup, restore, upgrade, migration and support |
| [10 Acceptance and traceability](10-acceptance-and-traceability.md) | Requirement coverage, scenarios, evidence and prototype/production exit gates |
| [11 Implementation roadmap](11-implementation-roadmap.md) | Runtime milestones derived from specifications; not an implementation authorization |
| [12 Decisions and risks](12-decisions-and-risks.md) | Explicit recommendations, unresolved alternatives, blockers and risk ownership |

## Sources and interpretation

Each requirement document names concept sections and relevant current files.
New numeric defaults, admin-only publishing, simplified review, V0 deferrals and
API details are engineering proposals, not quotations from the concept. Decision
IDs `DEC-*` track those choices. Existing governance ADR-001 is already occupied;
future architecture ADRs start at ADR-002, despite the concept's illustrative list.

Core invariants apply to V0 as well as production: private by default, explicit
publication, immutable captured bytes, editable editorial context, durable job state,
bounded hostile-content processing and truthful completeness/error reporting.

Documentation is ready for implementation planning only when unresolved blocking
choices are closed, requirement/contract/state definitions agree, and every mandatory
requirement has an owner and acceptance scenario. That gate has not yet been passed.
