# Evidence Workspace requirements package

Date: 2026-11-09. Revision: 0.3. Status: **selected engineering design baseline;
runtime qualification pending**.
Owner: product/engineering roles; individual assignees are not yet designated.
Versioned component: Specification. No runtime feature, independent review sign-off,
product release or measured capacity is created by this package.

## Purpose and authority

Translate the [English concept](../../concept/CONCEPT.en.md) and
[Russian concept](../../concept/CONCEPT.ru.md) into bounded, testable requirements,
an explicit first-prototype scope and a dependency-ordered documentation plan.
The [current-state review](../04-current-state.md) remains the source baseline;
the [HTML mockup](../../index.html) supplies visual/navigation intent only.

This package selects a **V0 controlled pilot prototype** design, distinct from existing
prototype code and the concept's production v1.0. V0 is a scope label, not a SemVer
release, and does not reset the inherited Python package version 1.1.0.
Deferring a capability from V0 does not remove its production requirement.

`shall` means a mandatory design requirement for the stated target. `should`
means a recommendation requiring a documented alternative if changed. Source presence,
design selection, implementation and verification are separate statuses. The continuation request
authorizes concrete engineering choices documented in ADR-002–004 and documents
13–19, without inventing reviewer approval or implementing runtime changes.
Document 20 is separately proposed optional scope, not part of V0 requirements.

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
| [12 Decisions and risks](12-decisions-and-risks.md) | Decision context, selected dispositions, qualification and risk ownership |
| [13 Selected V0 baseline](13-selected-v0-baseline.md) | Decision dispositions, exact starting limits and terminology |
| [14 Domain and execution contracts](14-domain-and-execution-contracts.md) | Typed entity/constraint dictionary, transitions, engine/network, CSV and SSE |
| [15 Evidence and publication contracts](15-evidence-and-publication-contracts.md) | Exact profiles/bytes/inventories, finalization crash cases and safe publication/export |
| [16 Screen and API contracts](16-screen-and-api-contracts.md) | Field/error/permission/HTTP examples, screen actions and identity/legacy behavior |
| [17 Migration/operations playbook](17-migration-and-operations-playbook.md) | Target procedures, mappings and observable operator outcomes |
| [18 Assignable work packages](18-assignable-work-packages.md) | EWP-01–18 dependencies, role assignments, deliverables and gates |
| [19 Documentation review](19-documentation-review.md) | Four-wave results, requirement refinement and honest handoff limits |
| [20 Change-monitoring proposal](20-change-monitoring-proposal.md) | Optional post-V0 comparison/filter/schedule/notification candidates |

Related source research: [changedetection.io review](../reference/changedetection-io-review.md).

## Sources and interpretation

Each requirement document names concept sections and relevant current files.
New numeric defaults, admin-only publishing, simplified review, V0 deferrals and
API details are engineering choices, not quotations from the concept. Decision IDs
`DEC-*` track those choices and qualification. ADR-002–004 record selected dispositions;
ADR-001 remains governance. Optional upstream-inspired suggestions remain candidates.

Core invariants apply to V0 as well as production: private by default, explicit
publication, immutable captured bytes, editable editorial context, durable job state,
bounded hostile-content processing and truthful completeness/error reporting.

The written design/traceability pass now supports assigning bounded foundation
work. [Review/gate disposition](19-documentation-review.md) distinguishes selected
choices from pending empirical feasibility, individual assignment and runtime gates.
No sensitive pilot/hostile capture/production readiness is implied by documentation.
