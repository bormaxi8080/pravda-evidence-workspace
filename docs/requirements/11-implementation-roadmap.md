# Derived implementation roadmap

Date: 2026-11-09. Status: **selected delivery sequence; implementation pending**.
Owner: engineering lead. Source: documents 01–10 and concept sections 30–35.
This is the dependency-ordered software roadmap. The separate
[documentation plan](00-documentation-plan.md) describes how to qualify its inputs.
No runtime stage is implemented or authorized merely by this document.

## Sequencing principles

Work in verifiable vertical increments. Establish authorization, isolation and
recovery before exposing hostile capture/public access. Add regression tests with
the behavior they protect; do not postpone security/testing until the final phase.
Respect legacy package/data compatibility and use synthetic fixtures throughout.

```text
IMP-00 decisions and fixtures
  -> IMP-01 contracts, schema and migration foundation
  -> IMP-02 identity, permissions and audit
  -> IMP-03 durable jobs + isolated capture boundary
  -> IMP-04 evidence finalization and private capture slice
  -> IMP-05 editorial UI + bounded batch import
  -> IMP-06 publication and private export
  -> IMP-07 operator recovery + V0 qualification
  -> IMP-08 production formats, monitoring and operations
  -> IMP-09 security/operational review + pilots + release candidate
```

API/UX work can overlap later stages after common contracts stabilize. Operations
design starts in IMP-00/01; IMP-07 qualifies it rather than introducing backups for
the first time. No stage needs separate infrastructure for every logical module.

## IMP-00 Decision and prototype audit foundation

Dependencies: DOC-12 written design review in document 19. EWP-01 supplies
empirical feasibility before dependent runtime work; it does not depend on a
full product runtime gate that it is meant to help establish. Owner: engineering/product/security leads.
Components: Specification; Governance only if actual workflow tooling changes.

Inventory current behavior, package/build defects, route/DB/file mappings and
threats. Close V0-blocking DEC entries; write architecture ADRs starting at 002.
Create controlled page/CSV/legacy DB/filesystem fixture designs and an evidence
recording convention. Decide package/release migration before a breaking refactor.

Exit: accepted V0 boundary, schema/engine/network direction, resource defaults,
permission/publication policy and migration/verification plan. No calendar promise
until owners and implementation investigations are known.

## IMP-01 Contracts, schema and migration foundation

Dependencies: IMP-00. Owner: domain/backend lead.
Components: Application; Evidence Contracts starts at 0.1.0 only when real contracts
are added; Deployment if schema startup behavior changes.

Implement reviewed evidence/API schema contracts and DTO validation; introduce
Source/Capture/Attempt/Artifact/Editorial/Publication and durable execution entities.
Add ordered migrations, constraints/indexes and prototype fixture migration with
ID/file mappings. Define staging/final storage namespace and lease/audit transaction
interfaces. Remove `create_all` as upgrade authority.

Verification: actual PostgreSQL migrations, invalid constraints, fixture counts,
digests, unknown provenance, incompatible version and migration-failure tests.
Exit: a fresh install and synthetic prototype migration produce compatible state
without evidence loss or unintended publication. Do not claim capture works yet.

## IMP-02 Identity, permissions, sessions and audit

Dependencies: IMP-01. Owner: backend/security lead.
Components: Application; relevant contracts and deployment secret/network settings.

Implement fail-closed GitHub admission, durable revocable sessions, admin bootstrap,
role checks, CSRF and service-level authorization. Establish transactional append-only
audit and safe error/log patterns. Implement disablement/role-change handling for
requests, streams and queued work before asynchronous user actions depend on it.

Verification: ACC-11 identity/role boundaries on real services/DB, denied raw access,
session replay/revocation/CSRF, audit write failure and last-admin recovery.
Exit: no protected mutation/file route bypasses the shared authorization layer.
Live provider integration remains a separately recorded check if unavailable locally.

## IMP-03 Durable jobs and isolated browser boundary

Dependencies: IMP-01/02. Owner: capture/backend/security lead.
Components: Application, Deployment, affected contract definitions.

Implement claim/lease/fencing/heartbeat, bounded retries/cancel/recovery, durable
events and polling. Run one engine implementation behind the CaptureEngine contract.
Separate runner credentials/network/temp storage and enforce URL/DNS/redirect/
subrequest egress and browser limits. Do not keep browser execution in web lifespan.

Verification: ACC-03/04/08 with real competing DB workers, killed/late workers,
lost notifications and deployed runner network controls. Exit: bounded capture
attempts recover safely; incomplete output cannot be finalized as success.

## IMP-04 Private evidence vertical slice

Dependencies: IMP-03. Owner: evidence/backend lead.
Components: Application, Evidence Contracts; Deployment for filesystem permissions.

Implement bounded artifact writes, provenance, profile validation, deterministic
manifest/checksums, atomic promotion/fenced DB completion and reconciliation.
Expose an authorized capture detail with original artifact inspection/verification.
Wire a minimal submit -> job -> complete/private evidence flow before broad UI work.

Verification: ACC-01/04/07/09 for bytes/hashes, missing/corrupt artifacts, every
finalization crash point and full disk. Exit: complete means the exact V0 profile
exists and verifies; retries preserve prior finalized evidence.

## IMP-05 Editorial workflow and batch import

Dependencies: IMP-04. Owner: product/UX/backend lead.
Components: Application; UI Prototype only if the design reference itself changes.

Implement dashboard/archive/filter/detail, notes/tags/collections, revision conflicts,
review, queue controls, CSV parse-preview-confirm and idempotent batch admission.
Reuse the mockup's visual language and responsive themes, replace simulated states
with authoritative service responses and provide accessible failure/empty states.

Verification: ACC-02/06/11 with real browser interactions and mixed batch results.
Exit: editors complete the private workflow without CLI; oversize/duplicate/stale
actions fail predictably and changing context never rewrites original bytes.

## IMP-06 Publication and private export

Dependencies: IMP-02/04/05. Owner: publication/evidence/backend lead.
Components: Application, Evidence Contracts, Deployment for cache/security headers.

Implement pinned reviewed publication, admin preview/publish/revoke, no-store public
asset routes and safe metadata projection. Implement bounded private export jobs,
HTML receipt, export inventory and independent verification; optional PDF behavior
must be explicit. Implement legacy public-link compatibility according to DEC-10.

Verification: ACC-05/07/10 through actual proxy/anonymous browser, all asset routes,
receipt injection/resource fetch, stale review/idempotency and package tampering.
Exit: private content stays private, revoked links deny new server reads and complete
exports verify outside the installation. WARC/PDF production delta remains visible.

## IMP-07 Recovery, installation and V0 qualification

Dependencies: IMP-01 through IMP-06. Owner: operations/engineering lead.
Components: Application, Deployment, relevant documentation.

Finish reproducible packaging/Compose commands, health/degraded-mode behavior,
resource/admission limits, operator install/admin/drain/backup/restore/upgrade/incident
runbooks and support diagnostics. Rehearse migration and isolated clean restore.
Run the full applicable ACC-01–11 matrix, record failures/limits and fix blockers.

Exit: tested controlled prototype package, known omissions, supported measured
environment and trained pilot operator. Product release number remains a separate
release decision. No sensitive pilot use while privacy/isolation/recovery blockers remain.

## IMP-08 Production artifact and operational delta

Dependencies: qualified V0 and decisions DEC-04/09/12. Owner: engineering/operations.
Components: Application, Evidence Contracts, Deployment and Specification.

Implement WARC fidelity contract and interoperable validation, required safe PDF,
bounded availability monitoring, automatic monitored backups and tested upgrade
support. Improve operational/performance evidence under representative permitted
loads. Preserve old V0 profiles as historical profiles; do not synthesize absent
network history or relabel incomplete historical evidence as production-complete.

Exit: all production feature requirements and profile/migration compatibility tests
pass on documented environment; unsupported sources and legacy profiles remain explicit.

## IMP-09 Review, pilots and release qualification

Dependencies: IMP-08 and full concept section 33 acceptance. Owner: product,
security and operations leads.

Complete security review, dependency/container review, disaster/onboarding docs,
pilot training and release-candidate evidence. Pilot in the concept's target
3–5 newsrooms where feasible, recording capture/queue/storage/recovery/usability
results and support incidents. Resolve critical defects and decide supported limits.

Exit: reviewed component/source/artifact snapshot, migrations, recovery plan and
known limitations justify a separately authorized release/tag/publication.

## Per-stage task record

Each implementation ticket shall reference requirement IDs/scenarios, affected
components/contracts, deliverables, dependency/decision IDs, migration/rollback
effects, exact checks/environment and exit evidence. Record what is unavailable.
Keep a stage incomplete when its required real DB/browser/isolation/restore gate
has not run; neither source presence nor mock-only green tests close it.
