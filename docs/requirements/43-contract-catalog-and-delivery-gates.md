# Executable contract catalogue and integrated delivery gates

Date: 2026-11-09. Status: **implementation specification; artifacts/tests not created**.
Owner: engineering/evidence/API/security/operator. Authority: ADR-008.
This ADR-008 pass refines 158 requirements (70 V0 / 88 later), adding EWP-53–60
and SYS-ACC-01–10 for task/scenario totals of 60/56. ADR-009/document 49 later add
12 future IAM IDs and technical detail: current totals 170 requirements, 72 tasks
and 68 scenarios. Named roles are assignment slots, not fabricated individuals or approvals.

## Materialization order and contract ownership

Machine-readable artifacts are future EWP-02/42 outputs. The planned Evidence
Contracts component stays 0.0.0 until real owned files/checks exist. Do not create
empty schema stubs or a second hand-maintained API/client authority just to fill
this table. New contracts record exact version, fingerprint, producer/consumers,
examples, invalid inputs, compatibility policy and owning requirement references.

| Catalogue ID | Contract/artifact to materialize | Authority / first consumers / gate |
| --- | --- | --- |
| CTR-01 | Capture/export/legacy profile inventories, canonical bytes and independent verifier examples | Document 15/17; finalizer/export/migration; EWP-02 before corresponding writes |
| CTR-02 | CaptureEngine request/result, job/attempt/error and durable event schemas | Document 14; controller/isolated runner/SSE; EWP-02/07/09 |
| CTR-03 | Cookie API DTO/OpenAPI, revisions/idempotency/errors and negative access examples | Documents 08/16; SSR/web routes; EWP-02/06, no public token expansion |
| CTR-04 | Purpose/profile/eligibility decision and safe reason registry | Document 40; application services/worker/read paths; EWP-53 |
| CTR-05 | Dependency edges, removal fence/pin and reservation descriptors | Documents 41/42; DB/finalizer/reconciler; EWP-54/55 |
| CTR-06 | Feature descriptor/compatibility and migration/restore report | Document 42; startup/operator/capability endpoints; EWP-56 |
| CTR-07 | C1/C2 representations/analysis key/profile/attention; C3 watch/epoch; C4 event/outbox/payload | Documents 21–25; only their enabled stages; EWP-19–29 |
| CTR-08 | H1 annotation/task/view; H2 cue/hit/search coverage and input snapshot | Documents 28–30; H1/H2 services and UI; EWP-32–35 |
| CTR-09 | H3 reference/evidence reports and H4 native transfer/quarantine/mapping | Documents 31/32; renderer/verifier/import; EWP-36–39 |
| CTR-10 | Companion pairing/scopes/capabilities/chunks/receipt/profile/export | Documents 35/36; server and generated TypeScript client; EWP-42/43/47/48 |
| CTR-11 | B2 acquisition observation/session epoch and separate upload-consent snapshot | Documents 34/35/37/40; local journal/server intake; EWP-50 |
| CTR-12 | Fixture manifest, test-result evidence record and enabled-feature compatibility report | This document; qualification/operator handoff; EWP-58–60 |

Freeze identifiers and required inventory before writing producers. Generate DTO/
TypeScript/collection representations from one authoritative version where useful;
verify generated files match the recorded schema fingerprint. An API collection
may add runnable assertions but cannot redefine schema fields silently. Do not
publish contracts or connect an external workspace as part of this documentation.

Keep negative examples for unknown profile/version/fields, null versus unknown time,
duplicate keys/inventory, stale revisions, omitted required outputs, authority
confusion and over-limit data. Contract parsing proves shape only; real browser,
DB/filesystem, provider and deployed network tests remain separate gates.

## Bounded synthetic fixture catalogue

| Fixture family | Inputs / expected distinction |
| --- | --- |
| FX-01 Server profiles | Controlled 200/404, partial/no MHTML, repeated same bytes; completeness differs from baseline/publication eligibility |
| FX-02 Foreign/legacy | Unknown times/actors, claimed valid IDs, profile collision; no role/publication/source-witness inheritance |
| FX-03 Browser | Separate client/server clocks, viewport-only/page, wrong-tab generation, stopped session with approved bytes; exact channel/consent preserved |
| FX-04 Anchors/search | Multibyte/repeated/casefold text and scaled image regions; original spans/pixels, partial corpus and no-index versus no-hit |
| FX-05 Dependency closure | Original -> representation -> quote/crop -> report/index plus safe citation; corruption/eviction/retract/purge take different paths |
| FX-06 Capacity | Concurrent CSV/manual/watch/upload/export, expired/reclaimed lease and full pinned pool; one accounting authority, no double release |
| FX-07 Migration/restore | Old/new writer, unsupported reader, missing quarantine, ledger newer than backup; restore hold/epoch and no automatic replay |
| FX-08 Adversarial bytes | Path/link/duplicate/MIME/JSON/archive/decode/image limits, unsafe markup and output size failure; explicit denial without network fetch |

Fixture manifests record deterministic seed/version, expected byte hashes, synthetic
origin/environment and which gates they support. Tiny grammar fixtures and real
controlled-browser outputs are separate classes; a hand-written MHTML sample does
not establish live capture fidelity. Use generated synthetic accounts/content only.
Keep approved small fixtures in the future owning test/contract component; large
browser outputs, logs and secrets stay out of Git/indexes. A malicious string is
test data, never an instruction for an agent or tool.

## Assignable refinement tasks

| Ticket | Dependencies / owner | Bounded deliverable | Completion evidence |
| --- | --- | --- | --- |
| EWP-53 Shared eligibility/profile service | EWP-02/03/06; evidence/security | Materialized CTR-04, known profile registry and one purpose-specific decision service reused by core paths | SYS-ACC-01/07; unknown/partial/foreign/browser decisions, denied diagnostics, no new V0 feature adapter |
| EWP-54 Dependency/pin and invalidation authority | EWP-03/06/08; evidence/backend | Transactional exact dependencies/reverse lookup, root fence/epoch, pin accounting, bounded closure/reconciliation | SYS-ACC-02/03/04; real concurrent ready/read/remove/crash cases; V0 only actual core edges |
| EWP-55 Shared reservations and fair claiming | EWP-07/08/53; backend/deployment | Global pending/heavy/temp/cache counters and generations, core admission/claim classes, overload diagnostics | SYS-ACC-05/06; real concurrent DB/process/full-disk proof, no duplicate release or client priority override |
| EWP-56 Feature/schema compatibility preflight | EWP-03/05/06/53; backend/operator | CTR-06 descriptors, safe effective states, implemented-core startup/migration checks and default-disabled later features | SYS-ACC-07/08; compatible reader/writer/permission/flag/restore-hold cases |
| EWP-57 Emergency removal and restore fences | EWP-14/54/56; operator/security | Actual operator dry-run/containment/ledger/closure/reconcile workflow for existing removal policy | SYS-ACC-03/04/08 and core ACC-09; real protected ledger/DB/filesystem crash/clean-restore evidence |
| EWP-58 Synthetic fixture and evidence harness | EWP-09/12/13/14/31/55/56/57; QA/evidence | FX/CTR-12 core fixture generators, independent verifier runner and structured evidence records; add enabled-stage cases later | Applicable core SYS scenarios alongside existing ACC/HUN V0 cases; no empty/skipped/mock-only required success |
| EWP-59 Compatibility rehearsal framework | EWP-16/56/58; engineering/operator | Core framework plus per-stage candidate fixtures supplied by owning C/H/B tickets, safe disable/upgrade/rollback/restore and mixed archive semantics | Applicable SYS-ACC-01–10 and owning stage cases; unsupported stages explicitly excluded, no all-feature prerequisite |
| EWP-60 Integrated implementation/operator handoff | EWP-16/59; product/operator | Current contract/support matrix, workflow/incident guide and implementation-evidence index for actual enabled artifacts | Named assignee can run core/relevant feature and recovery procedures on synthetic deployment; release/store/deploy separately authorized |

EWP-53 precedes the core vertical slice; EWP-54 precedes export. EWP-55/56/57/58
refine existing V0 admission/operations/verification before EWP-15, without making
later C/H/B implementations prerequisites. EWP-57 follows operational foundations,
not EWP-15, so the dependency graph remains acyclic. EWP-59/60 are later handoff
refinements. Each later stage qualification and EWP-30/40/52 depends on EWP-59's
core framework; its owning stage ticket supplies/runs that stage's cases. EWP-59
never waits for a completed C/H/B qualification or every future adapter, so this
framework dependency is not a cycle or an all-feature prerequisite.

EWP-58's first gate is the actual V0 subset: no need for future browser/monitoring/
report fixtures to declare V0 qualification. Future fixture cases are delivered
with their own stage implementation; recorded not_applicable means the stage is
explicitly disabled, not that a mandatory implemented feature can skip tests.

## Integrated scenario catalogue

### SYS-ACC-01 Purpose-specific evidence eligibility

Run FX-01/02/03 through every enabled inspect/export/compare/anchor/search/report/
baseline/publication path. Same profile facts produce consistent purpose decisions;
complete error pages are not article baselines, foreign/client claims do not become
local witnessing, and unknown/denied resources do not leak descriptive metadata.

### SYS-ACC-02 Dependency/pin integrity and cache expiry

Create FX-05 chains, pin exact revisions, expire unpinned cache and change extractor.
Rebuild only matching supported computations; old anchors/report refs do not float.
Physical bytes are charged once while each logical pin is accountable. Missing
or pinned-full cache is unavailable/capacity, never silent evidence deletion.

### SYS-ACC-03 Root fence versus late readers/writers

Serve/export/index/crop while a selected root is fenced; kill cleanup after its
first 500-edge page and attempt new dependent promotion. No affected bytes/snippets/
ready output can bypass the root fence while closure is incomplete. Independent
unaffected data retains its own access decision. Closure progress is not completeness.

### SYS-ACC-04 Retraction, revocation and purge distinctions

Edit/retract an annotation, revoke a public slug, disable an actor, corrupt original
bytes and perform synthetic operator removal separately. Assert each documented
effect; no original rewrite, blanket shared-evidence deletion or promised recall of
external copies. Ledger/DB split failures keep containment until reconciled.

### SYS-ACC-05 Atomic admission and reservation conservation

Race manual URL/export, selected 500-row CSV, watch, intake and derived work at
global/bulk/byte/temp/cache bounds. Reservation -> job conversion does not double
charge; aborted batches create no subset. Queue reserve and artifact disk reserve
cannot be spent twice by independent processes; retries do not invent extra quota.

### SYS-ACC-06 Fairness, worker death and aggregate resource bounds

Fill each enabled class, delay active work, lose lease/notification and restart
claimers/reconciler. One aggregate heavy permit and per-type limits hold; no second
process starts while the old one may execute. Persisted class rotation gives
runnable classes opportunities without promising an unmeasured latency SLA.

### SYS-ACC-07 Feature readiness and version compatibility

Toggle operator config with unsupported profiles, missing migration, unqualified
environment, failed dependency/resource setup and changed security policy. Capability
is enabled only when all predicates pass; descriptor data cannot execute code or
expand credentials/permissions. A documentation-only commit does not itself void
unaffected runtime evidence or qualify a changed parser.

### SYS-ACC-08 Removal-aware clean restore and downgrade

Restore FX-07 with ledger newer than backup, missing temporary upload bytes, stale
reservations, tokens and unsettled outbox. Hold serving/actions, rotate epoch and
reconcile before deliberate resume. Test unsupported old reader and forward-fix/
backup rollback, recording lost post-backup writes instead of claiming generic
zero-loss rollback. Required ledger unavailable means restore cannot open serving.

### SYS-ACC-09 Stopped browser session and frozen upload consent

Freeze/register an observation while active, stop/expire its acquisition epoch,
then explicitly approve/review upload and keep approved intents. Unchanged registered
bytes can finalize under current upload/actor authority; unregistered offline items
need explicit manual B1 review without a fabricated B2 registration. Changed/missing
consent, new observation registration under stopped epoch,
grant revoke or upload cancellation fails. No expired recording scope is revived.
This scenario applies only when B2 is implemented, never as a V0 prerequisite.

### SYS-ACC-10 Mixed time/profile adapters and truthful handoff

Use future/unknown client times and foreign IDs, change date basis/cursor version,
and render/export enabled H/C/B results. Server-controlled archive order and exact
channel labels remain stable; claimed times stay claims. Contract/fixture/command/
environment/source identities in the handoff match actual executed results, with
disabled/unavailable stages and remaining defects explicit.

## Refinement traceability and evidence record

| Existing requirement IDs | Detailed refinement | Planned integration evidence |
| --- | --- | --- |
| REQ-DAT-001, REQ-DAT-003, REQ-EVD-001, REQ-EVD-002, REQ-EVD-005, REQ-MON-006, REQ-BAE-003, REQ-BAE-005 | 40 purpose/channel/time policy | SYS-ACC-01, SYS-ACC-10 |
| REQ-DAT-004, REQ-DAT-006, REQ-DAT-008, REQ-EXT-002, REQ-EXT-005, REQ-ANN-005, REQ-ANN-006, REQ-RPT-006 | 41 dependencies/pins/removal | SYS-ACC-02, SYS-ACC-03, SYS-ACC-04, SYS-ACC-08 |
| REQ-SCP-004, REQ-JOB-001, REQ-JOB-002, REQ-JOB-006, REQ-EXT-003, REQ-BCP-004, REQ-BCP-005 | 42 shared resource accounting | SYS-ACC-05, SYS-ACC-06 |
| REQ-API-001, REQ-API-006, REQ-OPS-002, REQ-OPS-004, REQ-OPS-005, REQ-EXT-004, REQ-BLC-005, REQ-BLC-006 | 42/43 contracts/migration/restore | SYS-ACC-07, SYS-ACC-08, SYS-ACC-10 |
| REQ-BRW-003, REQ-BCP-005, REQ-BAE-002, REQ-BLC-002, REQ-BLC-003 | 40 frozen observation/consent boundary | SYS-ACC-09 |

This is a refinement matrix, not a replacement complete requirement registry.
The complete 158-ID coverage remains in documents 10/26/33/38. Existing ACC/MON/
HUN/B scenarios retain their definitions; SYS adds system interaction checks only.

Actual evidence records need scenario and requirement IDs, supported feature set,
source/artifact/contract/fixture hashes, exact command/steps, real environment,
start/end/outcome, safe failure artifact reference, reviewer/assignee when real,
and limitations. Status is pending/passed/failed/blocked/not_applicable with explicit
scope. Never mark a gate passed from prose, empty/skipped suites, metadata-only
checks or unrelated model/mocked results. No runtime result is recorded in this pass.

## Technical/IAM contract catalogue continuation

ADR-009/documents 44–49 extend materialization with CTR-13 fixed job-launcher/1
request/lifecycle/resource templates; CTR-14 validated settings/redacted effective
config and deployment/backup manifest; CTR-15 DB migration/role/pool/maintenance
report; CTR-16 U1–U3 user/bundle/space/invitation/link/workload schemas. These are
future versioned data/tool contracts, not implemented files or working commands.

Application owns authorization/state/migration bindings; Deployment owns image/
network/host enforcement; Evidence Contracts owns actual shared DTO/schema examples
when activated. U contracts cannot make V0 depend on planned schemas/runtime. Use
existing fixture/evidence rules and OPS scenarios, with actual role/host/DB/process
proof. The added IAM complete matrix is in 49; the original 158 IDs keep their
existing owning coverage, with no duplicated definitions.
