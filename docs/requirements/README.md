# Evidence Workspace requirements package

Date: 2026-11-09. Revision: 0.5. Status: **selected engineering design baseline;
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
The user subsequently adopted the upstream-inspired direction through ADR-005:
document 20 routes to staged requirements 21–26. Source history is explicit V0
scope; comparison/filter/watch/delivery are selected later stages, not V0 gates.
ADR-006 adopts investigation/handoff ideas from Hunchly: explicit submission context
and independent importance join V0; annotations, search/cues, reports and native
transfer have separate later-stage gates in documents 28–33.

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
| [20 Adopted roadmap](20-change-monitoring-proposal.md) | Stage boundary, adoption authority and former candidate mapping |
| [21 History and comparison](21-source-history-and-comparison.md) | V0 Source history and C1 reproducible offline comparison |
| [22 Profiles and attention](22-profiles-and-editorial-attention.md) | C2 focus/noise revisions, previews and personal acknowledgement |
| [23 Watches and scheduling](23-watches-and-scheduling.md) | C3 due slots, windows/DST, quotas, epoch/baseline and recovery |
| [24 Notifications and delivery](24-notifications-and-delivery.md) | C4 disclosure permission, minimal payload, outbox/retry/uncertainty |
| [25 Extension contracts/operations](25-extension-contracts-and-operations.md) | APIs, resource limits, dependencies, migrations and restore |
| [26 Adoption acceptance/roadmap](26-adoption-roadmap-and-acceptance.md) | 40 new requirement mappings, MON scenarios and EWP-19–30 |
| [27 Later boundaries](27-advanced-format-and-reuse-boundaries.md) | Deferred visual/native-format/selector/inheritance/transport evaluations |
| [28 Investigation context](28-investigation-context.md) | V0 request context/importance; later tasks and saved views |
| [29 Evidence annotations](29-evidence-annotations.md) | Exact quote/pixel anchors, revisions, assertions and dependency lifecycle |
| [30 Evidence search/cues](30-evidence-search-and-research-cues.md) | Private corpus coverage, literal matching and tentative observations |
| [31 Investigation reports](31-investigation-reports.md) | Frozen selections, citation/disclosure profiles and bounded rendering |
| [32 Transfer/acquisition](32-transfer-and-acquisition-boundaries.md) | Own-native export, quarantined import and deferred acquisition boundaries |
| [33 Investigation acceptance/roadmap](33-investigation-roadmap-and-acceptance.md) | 27 new requirement mappings, HUN scenarios and EWP-31–40 |

Related source research: [changedetection.io review](../reference/changedetection-io-review.md).
The [Hunchly comparison](../reference/hunchly-comparison.md) distinguishes public
documentation from hands-on verification and edition-dependent functionality.

## Sources and interpretation

Each requirement document names concept sections and relevant current files.
New numeric defaults, admin-only publishing, simplified review, V0 deferrals and
API details are engineering choices, not quotations from the concept. Decision IDs
`DEC-*` track those choices and qualification. ADR-002–004 record selected dispositions;
ADR-001 remains governance; ADR-005 records staged adoption. Deferred items in
document 27 remain evaluations. ADR-006 records investigation/handoff adoption.
The registry now has 134 selected requirements: 70 V0 (67 original, history and two
context/triage requirements), 64 later-stage, all with explicit acceptance coverage.

Core invariants apply to V0 as well as production: private by default, explicit
publication, immutable captured bytes, editable editorial context, durable job state,
bounded hostile-content processing and truthful completeness/error reporting.

The written design/traceability pass now supports assigning bounded foundation
work. [Review/gate disposition](19-documentation-review.md) distinguishes selected
choices from pending empirical feasibility, individual assignment and runtime gates.
No sensitive pilot/hostile capture/production readiness is implied by documentation.
