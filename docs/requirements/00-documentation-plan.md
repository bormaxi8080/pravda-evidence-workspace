# Documentation delivery plan

Date: 2026-11-09. Status: **written design pass completed; runtime qualification pending**. Owner: engineering lead with product,
security and operations reviewers. Affected component: Specification.
Sources: concept sections 2, 29–35; [design brief](../05-next-design-phase.md).

## Objective

Create an implementation-ready specification set before expanding prototype code.
The first baseline is documents 01–12. The continuation in documents 13–20 and
ADRs 002–004 completes/refines the written design; [review results](19-documentation-review.md)
and [assignable tickets](18-assignable-work-packages.md) record actual handoff limits.
The work below remains the reusable method for completing and qualifying the baseline.
It is a documentation work breakdown, distinct from the later runtime roadmap.
No dates or team estimates are asserted without named owners and availability.

Revision 0.4 further adopts changedetection.io ideas through ADR-005/documents
20–27, formal requirements and EWP-19–30. This extends the same review/traceability
method with a precise C0/V0 boundary and later-stage acceptance, not a runtime rewrite.

## Definition of a complete document

Every specification needs stable requirement IDs, source rationale, target stage,
clear inputs/outputs and states, permissions/trust boundaries, failure and recovery,
compatibility/migration effects, acceptance scenarios, dependencies and unresolved
choices. Reviewers record decisions; authors do not promote proposals to accepted
merely because prose has been written. Examples remain synthetic.

## Work packages and dependencies

| Package | Depends on | Outputs to finish/review | Completion evidence |
| --- | --- | --- | --- |
| DOC-00 Source reconciliation | None | Source inventory, README/code conflicts, missing deck caveat, terminology, prototype-data assumptions | Every inherited feature is marked present/proposed/deferred/unverified; current source paths cited |
| DOC-01 Product boundary | DOC-00 | Personas, core journeys, V0/production matrix, exclusions, deployment and capacity assumptions | Product reviewer can classify every screen/action and explain V0 limits |
| DOC-02 Architecture choices | DOC-01 | Context/process/data-flow views, module ownership, engine and network boundaries, topology alternatives | DEC-01/02/03 resolved or bounded; no unexplained external dependency |
| DOC-03 Domain and consistency | DOC-02 | ERD-ready entity/field dictionary, constraints/indexes, transition tables, transaction/reconciliation rules | Capture, job, review and publication states cannot contradict one another; legacy mapping reviewed |
| DOC-04 Capture and execution | DOC-02/03 | Engine request/result contract, job lease/retry/cancel model, batch grammar/preview, timeout/error catalogue | Crash, duplicate, partial output, lost notification and stale-worker scenarios have deterministic outcomes |
| DOC-05 Evidence contract | DOC-03/04 | Artifact profiles, byte/JSON canonicalization rules, manifest/checksum relationships, integrity verifier behavior, WARC fidelity | Synthetic package can be specified without self-hash cycles or unstated missing artifacts |
| DOC-06 Access and threat model | DOC-01/02/03 | Role/action matrix, session/admission design, SSRF/egress policy, public allowlist, cache/revocation and audit rules | Threats map to controls/tests; content/network disclosure boundaries have owners |
| DOC-07 Editorial UX | DOC-01/03/04/06 | Screen/state inventory, forms/filters, review, batch preview, publication confirmation, empty/error/accessibility behavior | Each primary journey has steps, permissions, results and failure messages |
| DOC-08 API and events | DOC-03/04/05/06/07 | Endpoint/request/response tables, draft OpenAPI design, pagination, errors, CSRF/idempotency, SSE reconnect/event retention | Each UI command maps to an authorized service; producer/consumer states and errors agree |
| DOC-09 Operations and migration | DOC-02/03/05/06 | Environment matrix, install/upgrade runbooks, prototype migration map, backup consistency/restore, health and incident paths | Clean install and restore procedures include independently checkable expected outputs |
| DOC-10 Acceptance and traceability | DOC-01 through DOC-09 | Requirement-scenario-source matrix, synthetic fixtures, failure injection, V0/production exit gates | Every mandatory requirement covered; no mock-only proof for real DB/browser/recovery guarantees |
| DOC-11 Delivery roadmap | DOC-10 and blocking decisions | Vertical implementation stages, dependency graph, component/contract impacts, migration and evidence gates | A stage can be assigned and reviewed without inventing scope or prerequisites |
| DOC-12 Baseline review | All preceding packages | Cross-document consistency review, open decision dispositions, version/changelog update, accepted ADR set | Implementation-ready gate below passes; product readiness is still unclaimed |

## Detailed execution sequence

### Wave A: establish the bounded product

Complete DOC-00 and DOC-01 first. Walk an editor through one URL capture and one
CSV batch, then through internal review and a reader's public link. Agree what
counts as a successful capture and what the prototype may omit. Record non-goals
and defaults centrally in document 01, so other documents reference them.

Review DOC-02 and DOC-03 next. Choose the capture boundary using a small controlled
technical investigation when implementation work is later authorized. Document
credential separation and storage authority. Define immutable and mutable fields,
identifiers, time semantics and transaction boundaries before designing endpoints.

### Wave B: specify execution, evidence and access together

DOC-04, DOC-05 and DOC-06 may be drafted in parallel as documents, but cannot be
finalized independently. A worker completion must mean that a precise artifact
profile is committed; public access must mean that a permitted publication exists;
retries must not overwrite finalized evidence. Resolve those cross-boundary cases.

Required supporting outputs: transition/error tables, artifact inventory example,
threat/control matrix, role/action table and draft ADRs for blocking decisions.
Machine-readable JSON Schema/OpenAPI artifacts are a later explicit contract task;
the planned Evidence Contracts component stays at 0.0.0 for prose requirements.

### Wave C: make user and operator behavior concrete

Finish DOC-07 with stateful screen specifications rather than decorative mockups.
Finish DOC-08 against the same service/authorization model. Finish DOC-09 with
realistic ordering for drain, backup, migration, restore and verification; do not
assume database and filesystem snapshots are automatically atomic.

Describe both normal use and recovery from missing artifacts, worker termination,
expired sessions, denied publication, full disk and failed migration. Never use
"handled" without specifying user-visible result, persistent state and operator action.

### Wave D: qualify and freeze the specification baseline

For DOC-10, map all requirement IDs to named scenarios and required environments.
For DOC-11, derive stages from dependencies rather than copying the concept's
security/testing phases to the end. In DOC-12 review naming/version migration,
API/manifest semantics, access policy and production deferrals. Preserve dissent
and unknowns as decision entries, not vague TODO statements.

## Implementation-ready documentation gate

- Mandatory V0 requirements are unambiguous, assigned to domain owners and traceable.
- All V0 design choices have recorded dispositions/ADRs; empirical build/isolation gates remain ticket prerequisites.
- State/permission/error tables agree across domain, jobs, API, UI and operations.
- Numeric limits and configuration ownership are defined; no unmeasured SLA is promised.
- Prototype migration, evidence-loss prevention and rollback limits are specified.
- Each stage lists fixtures, required real environments, negative/recovery tests and exit evidence.
- The production checklist retains WARC, PDF, operational/security review and pilot gates.
- Documentation links, component ownership, versions and changelog validate.

## Review and change handling

Use product, domain/backend, security and operations roles as reviewers; one person
may cover several roles, but decisions must name their reasoning and remaining risk.
UI review is required for user-visible state/error changes. Record review status per
document and reopen dependent sections when a contract changes. Do not estimate a
calendar from page count. Estimate runtime tasks only after DOC-12, using a known
team, infrastructure, capture-engine results and migration dataset constraints.

## Revision 0.5 continuation

[ADR-006](../decisions/0006-investigation-context-and-handoff.md) and documents
28–33 apply the same four waves to Hunchly-inspired investigation/handoff. H0
refines V0 context/triage; H1–H4 specify later annotations/search/reports/native
transfer. That pass produced 134 requirements and 40 implementation tasks. The current
source/requirement/scenario/task registry is linked from [the package index](README.md).
A documentation gate remains distinct from measured runtime qualification.

## Revision 0.6 browser-channel design

ADR-007/documents 34–38 specify the previously deferred companion. The same waves
cover mode/scope/architecture; coupled credentials/bytes/consent/finalization;
UI/API/migration/operations; and complete B acceptance/task mapping. Primary Chrome
and RFC sources are recorded separately from unperformed feasibility tests.
Current registry: 158 requirements, 70 V0 / 88 later and 52 assignable tasks.
B0/B1/B2 are later independent gates; V0 and baseline production scope is unchanged.

## Revision 0.7 integration refinement

[The integrated review](39-integration-review-and-refinement.md) identifies gaps
across the already selected branches. Documents 40–43 specify operation eligibility,
dependency/removal authority, shared capacity/feature compatibility and executable
contract/fixture materialization. ADR-008 resolves the named conflicts; this is a
refinement of 158 existing requirements, with 60 tasks and 56 scenario definitions.
V0 implements only its current core subset; later branch adapters remain disabled.

## Revision 0.8 technical and identity detail

ADR-009/documents 44–49 refine the selected Docker/host/process, PostgreSQL role/
schema/query, deployment/settings/upgrade and maintenance/recovery contracts. U1–U3
add 12 explicitly later-stage identity/access definitions. Current totals: 170
requirements (70 V0 / 100 later), 72 tasks and 68 scenario definitions. Complete
IAM coverage and technical refinement gates live in 49; runtime qualification remains
pending. No source config, account, live deployment or backup was changed.

## Revision 0.9 preservation/read-plane refinement

ADR-010/documents 50–53 make the existing production WARC/PDF and core protected-
read obligations concrete: inventories, recording scope, negotiation/limits,
independent replay/verifier, renderer containment and byte snapshot/stream races.
Requirements stay 170 (70 V0/100 later); delivery becomes 78 tasks/76 scenarios.
Core EWP-77 knows only supported V0 reads; WARC/required PDF remain production,
with actual provider qualification rather than an untested dependency adoption.
