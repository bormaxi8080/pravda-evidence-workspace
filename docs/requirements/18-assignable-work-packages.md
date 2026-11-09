# Assignable implementation work packages

Date: 2026-11-09. Status: **planned tasks, none implemented by this documentation pass**.
Owner: engineering lead. Roles below are assignment slots, not invented people or
completed reviews. Source: original requirements 01–10, selected design 13–17,
ADRs 002–004. All code tasks update affected versions/docs and record real evidence.

## Task catalogue

Each row is a bounded ticket: scope/result, prerequisites, responsible role and
completion evidence. Estimates require a real team and EWP-01 results; no calendar
or throughput commitment is inferred from this table.

| Ticket | Dependencies / owner | Concrete deliverable | Completion gate |
| --- | --- | --- | --- |
| EWP-01 Build and runner feasibility | EWP-61/62; backend + security/operations | Reproducible package/build plan fixing backend/COPY-order defects; pinned versions; one isolated Playwright runner prototype and capability/network proof | Synthetic capture + blocked private/DNS/redirect/subresource paths; show browser has no DB/secrets/final volume; fail closed/reopen ADR if infeasible |
| EWP-02 Machine-readable contracts | Selected 13–16; evidence/API | Real JSON profile/request/result/OpenAPI schemas and synthetic success/error examples; activate Evidence Contracts at 0.1.0 with ownership | Parse/validate examples and negative cases, unknown-version/required-inventory/self-hash tests; no new runtime dependency on planned metadata |
| EWP-03 Schema and migration framework | EWP-02/63; domain/backend | Ordered PostgreSQL migrations, entity constraints/indexes/roles, compatibility check replacing create_all upgrade authority | Fresh DB and rollback/forward-failure rehearsal; real FK/unique/audit privilege tests |
| EWP-04 Legacy import and compatibility | EWP-03; backend/operator | Source inspection report, byte-preserving Snapshot import, legacy profile, ID/tag/public-route mappings and anomaly handling | ACC-10 fixture counts/digests/unknowns/public suspension; bad path/symlink/missing-byte cases cannot broaden access |
| EWP-05 Identity and admission | EWP-03; security/backend | Browser-bound OAuth state, verified allowlist logic, durable sessions, operator bootstrap, user disablement/role lifecycle | ACC-11 org-only/empty lists, expiry/replay/provider error, session revocation and last-admin recovery; live provider result separately recorded |
| EWP-06 Shared services and audit | EWP-03/05; backend | Uniform authorization/CSRF, transactional safe audit, structured errors, idempotency service | Denied route/file/job mutation tests, audit write failure rollback, idempotency replay/conflict and no secret outputs |
| EWP-07 Durable queue and events | EWP-03/06; backend | Admission/slot locking, leases/generations, attempts, cancel/retry/recovery, durable SSE sequence | ACC-03/04 real competing/late workers, lost NOTIFY, cancel race and bounded recovery; no false exactly-once claim |
| EWP-08 Trusted artifact finalization | EWP-02/03/07; evidence/backend | Safe runner-output import, staged hashing/manifest/promotion, fenced DB commit and reconciliation | ACC-04/07/09 at each crash point; symlink/traversal/bounds/tamper tests, no evidence overwrite |
| EWP-09 Isolated capture vertical slice | EWP-01/05/06/07/08/53; capture/security | Actual engine contract, readiness options/provenance and private submit -> complete capture detail flow | ACC-01/04/08 synthetic real browser + DB; limits/partial/HTTP404 outcomes, no browser execution in web lifespan |
| EWP-10 Editorial UI and revision service | EWP-06/08/09; UX/backend | Archive/detail/dashboard/Source history (REQ-HIS-001), bounded filters, notes/tags/collections, revision-aware review, accessible themes/errors | ACC-01/06/10/11 and MON-ACC-07 real browser; identical/partial history retained, conflicts/edits preserve hashes; group deletion preserves evidence |
| EWP-11 CSV preview-confirm | EWP-06/07/10; backend/UX | Strict grammar/limits, actor-bound preview, dedupe choices, atomic capacity/idempotent confirmation and mixed batch progress | ACC-02/04/11 malformed/oversize/stale/duplicate/queue-full cases; no preview jobs/silent truncation/partial admission |
| EWP-12 Publication and safe public viewer | EWP-05/06/08/10/77; publication/security/UX | Exact admin preview, pinned projection, new slug, revoke, no-store asset authorization and legacy mapping | ACC-05/06/10 anonymous/private/old slug/proxy asset tests, no raw evidence/notes/usernames; no GET state mutations |
| EWP-13 Private export and verifier | EWP-02/06/08/10/54/77; evidence | Bounded ZIP/HTML/export job, independent verifier, explicit profile/PDF/metadata options, expiry | ACC-07 real package independent verification, empty/damaged/duplicate/path cases; safe receipt and required-PDF failure |
| EWP-14 Install/backup/restore/upgrade | EWP-01/04/05/07/08/12/13/65/66; operations | Implement target workspace-admin interfaces from 17; maintenance boundary, coherent backup, isolated restore, emergency purge ledger and upgrade runbooks | ACC-09/10 clean install/restore with matching IDs/bytes/audit; old sessions/egress/publication disabled in rehearsal; no untested shell-command claim |
| EWP-15 Integrated V0 qualification | EWP-09–14/31/55/56/57/58/64/67/68; engineering + security/operations/UX | Full 70-requirement V0 dossier including HUN-ACC-01/02, applicable ACC-01–11 and core SYS scenarios, measured environment/limits, browser/accessibility review and defect triage | All mandatory gates pass, no skipped required evidence; explicit optional PDF/monitoring gaps and no unresolved critical privacy/loss/isolation defect |
| EWP-16 V0 operator handoff | EWP-15; product/operator | Known limitations, editor/operator onboarding, support/incident path and reproducible pilot package manifest | Named operator can execute core/recovery runbooks on test environment; separate release decision, no automatic push/tag/deploy |
| EWP-17 Production format/monitoring delta | EWP-16/75/76/78; evidence/operations | Explicit WARC fidelity profile/validator, safe required PDF, availability probes and automated monitored backups/upgrade | ACC-12 format/interoperability/security/restore evidence; old V0 profiles retain historical identity |
| EWP-18 Production review and pilots | EWP-17; product/security/operations | Security/dependency review, measured supported limits/RPO/RTO, concept-target pilot evidence and release-candidate dossier | All concept section 33 conditions and critical defects closed; release/version/tag/publication separately authorized |

EWP-13 intentionally precedes EWP-14 and depends only on the private evidence flow;
it can run alongside publication work after shared contracts settle. No ticket
depends on its own future qualification. EWP-01 is a bounded engineering investigation,
not permission to enable hostile capture or production deployment.

## Contract and consumer checkpoints

- EWP-02/03: application package compatibility, schema/profile versions and migration
  consumers; the future incompatible runtime increment uses the selected major version.
- EWP-07/09: runner/controller generation, state/error/timing and event clients tested together.
- EWP-08/13: capture/export manifest paths, exact bytes and independent verifier agree.
- EWP-10/12: editorial approval revision and pinned public metadata cannot diverge.
- EWP-04/12/14: legacy public ID mapping, safe suspension and restore policy agree.
- EWP-14/15: operational commands verified against real behavior before docs say they work.

## Standard ticket body and evidence

```text
ID / title / assigned person / responsible role:
Source requirement IDs and detailed contract sections:
Prerequisite tickets / decision references:
Affected components and consumer compatibility:
Bounded deliverables and explicit exclusions:
Data migration / rollback / privacy consequences:
Synthetic fixtures and exact test environment:
Happy / denied / boundary / race / crash / recovery checks:
Required commands and observable completion evidence:
Unavailable checks / remaining defects / handoff:
```

Scope is reviewable without waiting for names/estimates. Before starting a ticket,
assign a person and validate its prerequisites; do not invent approvals or claim
tests that have not run. The adopted C1–C4 continuation is defined as EWP-19–30 in
[document 26](26-adoption-roadmap-and-acceptance.md); these later tickets are not
silent V0 prerequisites. C0 Source history explicitly refines EWP-10/15.

## Investigation continuation and V0 refinement

[Document 33](33-investigation-roadmap-and-acceptance.md) adds EWP-31–40; together
with EWP-19–30 in document 26, that pass has 40 assignable tasks. EWP-10/11 supply
editorial and CSV foundations for EWP-31's explicit context/importance refinement.
EWP-15 depends on EWP-31 so those two new V0 requirements cannot be skipped.
EWP-31 does not depend on V0 qualification. H1–H4 tasks remain later-stage gates.

## Browser companion continuation

[Document 38](38-companion-roadmap-and-acceptance.md) adds EWP-41–52. The current
browser-stage pass has 52 tasks across documents 18/26/33/38. All browser tasks depend on
qualified V0, never the reverse. B0 and B1 qualify independently of B2 and H/C
adapters; these additions do not alter the 70 V0 requirements or EWP-15 gates.

## Integrated refinement tasks

[Document 43](43-contract-catalog-and-delivery-gates.md) adds EWP-53–60; current
refinement pass total is 60. EWP-53/54 supply shared eligibility/dependency authority for
core capture/export; EWP-55–58 refine existing V0 capacity/preflight/removal/fixture
proof before EWP-15. They implement only actual core paths in V0. No C/H/B feature
or adapter becomes a baseline prerequisite. EWP-59/60 add enabled-stage rehearsal/
handoff after EWP-16; they are not prerequisites of their own earlier qualification.

## Infrastructure and future identity detail

[Document 49](49-infrastructure-and-identity-delivery.md) extends the registry to
72 tasks. EWP-61/62 decompose the existing build/runner feasibility milestone;
EWP-63 provides the schema/role bootstrap, EWP-65/66 the actual installation/backup/
upgrade subwork and EWP-64/67/68 core DB/maintenance/recovery qualification.
Parent prerequisites are updated without duplicating implementation deliverables.
EWP-69–71 are U1/U2/U3 later identity stages and never prerequisites of V0 or the
baseline production release. EWP-72 hands off the actual supported technical scope.

## Preservation and protected-read refinement

[Document 53](53-preservation-delivery-and-production-gates.md) adds EWP-73–78;
current total is 78 tasks. EWP-77 implements existing core pre-header integrity/
authorization/resource rules before EWP-12/13, without depending on WARC/PDF.
EWP-73–76/78 refine the already mandatory production format gate EWP-17; none
requires C/H/B/U implementation. EWP-17 retains availability/automated-operations
scope and EWP-18 retains independent production/security/pilot release conditions.
