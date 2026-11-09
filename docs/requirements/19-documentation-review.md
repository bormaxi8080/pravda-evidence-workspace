# Four-wave documentation review and handoff

Date: 2026-11-09. Revision: 0.3. Status: **engineering documentation pass completed;
implementation and qualification pending**. Owner: engineering lead.
This is a self-review, not an independent human review or a runtime test report.

This revision-0.3 review records the preceding pass. The subsequent revision 0.4
adoption is ADR-005 and documents 20–27: 107 selected requirements, including 68 V0
and 39 later-stage, plus EWP-19–30. Original requirement IDs and prior source/test
observations remain stable; C0 history now explicitly refines the V0 handoff.

## Four-wave results

| Wave | Result produced | Evidence and remaining limits |
| --- | --- | --- |
| A Product/terminology/architecture/domain | V0 boundary retained, vocabulary fixed, direct Playwright/PG16/process topology selected, entity/constraint dictionary and package migration direction | ADR-002, documents 13/14; actual build/engine/isolation qualification EWP-01 pending |
| B Execution/evidence/security | Exact lease/retry/cancel/partial states, engine result, staged/fenced finalization, profile/hash serialization, role/session/publication boundaries | ADR-003/004, documents 14/15/16; real DB/browser/security/byte verifier tests not executed |
| C UX/API/migration/operations | Screen actions/errors, DTO/HTTP/idempotency/SSE contract, legacy route/data map, install/admin/backup/restore/incident target procedures | Documents 16/17; OpenAPI/schemas/CLI implementation and operational evidence pending |
| D Consistency/decisions/assignable work | Decision dispositions, requirement-to-detail/task mapping, 18 bounded work packages, optional upstream-inspired extension separated | This review, document 18/20; individual assignees, estimates and external review remain unset |

## Requirement-family refinement map

Original requirement IDs and scenario assignments in document 10 remain stable.
These documents resolve their details without duplicating or renumbering requirements.

| Existing requirements | Detailed contract | Work packages |
| --- | --- | --- |
| REQ-SCP-001–006 | 13 scope/defaults, ADR-002/003 | EWP-01/09/10/11/12/13/15/16 |
| REQ-ARC-001–008 | 13 topology, 14 engine/network, 15 finalization | EWP-01/02/03/06/07/08/09/14 |
| REQ-DAT-001–008 | 14 dictionary/state, 15 bytes, 17 migration | EWP-03/04/08/10/12/14 |
| REQ-JOB-001–007 | 13 timings, 14 queue/engine/batch/events | EWP-07/09/11/15 |
| REQ-JOB-008 | 17 operational boundaries; availability implementation remains production | EWP-17/18; content monitoring in 20 is separately optional |
| REQ-EVD-001–008 | 15 profiles/finalization/export; historical meaning in 17 | EWP-02/08/13/14/17 |
| REQ-UX-001–007 | 16 screen/actions/errors and safe configuration | EWP-10/11/12/13/15/16 |
| REQ-SEC-001–008 | 14 isolation/output, 15 disclosure, 16 auth/API, 17 operator trust | EWP-01/05/06/09/12/13/14/15 |
| REQ-API-001–006 | 14 events, 16 operations/examples/errors/compatibility | EWP-02/06/07/10/11/12/13 |
| REQ-OPS-001–008 | 13 environment/caps, 17 procedures/health/restore/purge | EWP-01/04/14/15/16/17/18 |

## Contradictions resolved in this pass

1. The concept favors Pravda while source uses direct Playwright: select one bounded
   Playwright runner for V0 behind an adapter, keep Pravda as a later evaluated option.
2. README/concept mention PostgreSQL 15 while Compose has 16: qualify 16 first.
3. Package 1.1.0 versus future production v1.0: do not reset package; use explicit
   future major migration when contracts break; product release remains null.
4. Capture versus export manifest: define separate byte inventories and no self-hashes.
5. Capture outcome versus corruption: preserve historical provenance, track integrity
   observations separately and block unsafe serving/complete export when invalid.
6. Mutable public toggle versus review/publication: pin explicit projection/revision,
   use no-store and never reactivate revoked slugs implicitly.
7. Collection/tag changes versus approval: all capture-affecting editorial changes
   share revision/audit rules; no side route leaves stale approval valid.
8. Legacy public flags versus conservative disclosure: review mappings, report/suspend
   unreviewed links and make the compatibility change explicit before cutover.
9. Queue state versus runner concurrency: lease fencing prevents stale accepted output;
   actual runner termination/slot policy prevents concurrent zombie browser growth.
10. Monitoring versus evidence: availability, comparison, schedule, attention and
    publication stay independent; changedetection ideas do not expand V0 by implication.

## Gate disposition

The design is concrete enough to assign EWP-01 (qualification investigation) and
EWP-02 (schema/OpenAPI materialization), then progress through dependent foundation
work with recorded evidence. No empirical feasibility, hostile Internet capture,
sensitive pilot, deployment or production gate is declared passed here.

The original DOC-12 implementation-ready gate has its written design/traceability
portion satisfied by this pass. Named review/assignment, exact build/engine pins
and feasibility tests remain actual work; they are not ceremonial approval requests
that block reversible documentation. Any failed feasibility reopens its specific
ADR and downstream tickets, not the entire product concept.

## Verification of this documentation change

Run repository validator, the existing governance regression suite, local Markdown
link checks, requirement/scenario coverage and work-package dependency/reference
checks. Inspect staged diff and versions. These establish documentation/tooling
consistency only. Record actual command results in delivery; never infer runtime
ACC results from them. Upstream review was source-only and imports no code/assets.

## Revision 0.5 investigation/handoff refinement

Official Hunchly documentation was compared in
[the source register](../reference/hunchly-comparison.md); the product was not installed
or tested. ADR-006/documents 28–33 add 27 requirements with HUN-ACC-01–10 and
EWP-31–40. That pass totals 134 requirements (70 V0, 64 later-stage), 40 tasks.
The earlier review/counts above record their historical pass, not current scope.

Consistency refinements: keep Collection rather than duplicate Case; pin explicit
submission context without worker overwrites; isolate importance from editorial
approval; distinguish cue matching from CSS extraction; preserve exact quote/crop
anchors; freeze report revisions/disclosure; quarantine native imports without
foreign authority. The core V0 matrix/API/domain/qualification dependency includes
H0. H1–H4 remain later-stage work. All new runtime scenarios are unexecuted; no
independent review or implementation claim follows from this documentation pass.

## Revision 0.6 companion refinement

ADR-007/documents 34–38 select the optional browser channel with a primary-platform
source register and explicit B0/B1/B2 boundary. Current totals: 158 requirements
(70 V0, 88 later), 52 tasks and 46 named acceptance scenarios across four registries.
New 24 requirements map to B-ACC-01–12; no previous ID is removed/renumbered.

Cross-document decisions: distinguish B0 server handoff from B1 local observation;
use narrow expiring grants instead of web cookies; keep collector claims separate
from server byte verification; fence target/consent/upload generations; quarantine
before acceptance; keep private browser profile publication/baselines disabled;
rotate epoch on restore. MV3 permission/native-memory/timing behavior remains a
real feasibility/qualification gate, not a tested property of this prose.
