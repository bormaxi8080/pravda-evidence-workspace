# Versioned implementation plan

Date: 2026-11-10. Design revision: 0.11. Status: **selected delivery decomposition;
future release numbers are proposed targets; runtime implementation pending**.
Owners: product/engineering, evidence/security, database/deployment, browser and QA.
Individual assignees, team capacity, estimates, dates and release approval are not
yet assigned. This plan is detailed enough to create bounded implementation tickets;
it does not claim those tickets have started or passed.

## 1. Outcome, inputs and scope

Deliver a self-hosted private newsroom evidence system, then independently enabled
investigation, monitoring, companion and access capabilities. First make a bounded,
recoverable V0 pilot safe to operate; then qualify mandatory production preservation.
Do not turn all later ideas into prerequisites for the first usable system.

This plan follows the [requirements index](README.md), ADR-002–010, the 170 selected
requirements, 78 EWP work packages and 76 named acceptance scenarios. It translates
the [Workspace and companion UI blueprints](54-ui-blueprints-and-interaction-map.md)
into delivery slices. The original implementation registries in documents
[18](18-assignable-work-packages.md), [26](26-adoption-roadmap-and-acceptance.md),
[33](33-investigation-roadmap-and-acceptance.md), [38](38-companion-roadmap-and-acceptance.md),
[43](43-contract-catalog-and-delivery-gates.md), [49](49-infrastructure-and-identity-delivery.md)
and [53](53-preservation-delivery-and-production-gates.md) retain task identities,
prerequisites and acceptance authority. This document assigns each of those tasks
one primary completion milestone and expands its execution steps; it does not
introduce a second competing backlog or additional requirement IDs.

The local HTML design is an implementation input, not application code to deploy.
Preserve private-by-default behavior, immutable evidence, revision-aware context,
explicit disclosure, provenance/time distinctions and bounded hostile processing
when implementing it in the actual application. New routes/forms must conform to
the authoritative API contracts rather than copying mockup hash routes.

## 2. Version semantics and delivery policy

V0 is a scope label. The current Application 1.1.0 is inherited prototype metadata;
it does not mean the target system or a product 1.1 release already exists.
`release/versions.json` product release/date remain null until an actual authorized
release operation. The following product numbers are planning coordinates, not tags,
release declarations or a rewrite of component history.

| Milestone | Proposed future product target | Usable boundary | Primary EWP completions |
| --- | --- | --- | --- |
| F0 | `0.1.0-alpha.1` | Synthetic engineering foundation only; no newsroom pilot | 61, 02, 62, 01, 63, 03, 64 |
| E0 | `0.2.0-alpha.1` | Private synthetic capture vertical slice; no publication or pilot claim | 05, 06, 07, 08, 53, 54, 55, 56, 77, 09, 04 |
| P0 | `0.3.0-beta.1` | Complete controlled V0 pilot after qualification/handoff | 10, 11, 31, 12, 13, 65, 66, 14, 57, 58, 67, 68, 15, 16 |
| R1 | `1.0.0-rc.1` | Production-format candidate; qualified WARC/PDF/replay dossier | 73, 74, 75, 76, 78, 17 |
| G1 | `1.0.0` | Baseline production release candidate approved for actual release | 18 |
| D1 | `1.1.0` | C1 comparison, H1 context, standalone B0 URL companion | 59, 19, 20, 21, 32, 33, 41, 42, 43, 44, 45, 60, 72 |
| D2 | `1.2.0` | C2 profiles/attention, H2 literal corpus/cues, B1 local evidence | 22, 23, 34, 35, 46, 47, 48, 49 |
| D3 | `1.3.0` | H3 frozen reports, H4 native transfer, U1 lifecycle/role bundles | 36, 37, 38, 39, 40, 69, 51 |
| D4 | `1.4.0` | C3 bounded watches, B2 assisted sessions and companion handoff | 24, 25, 26, 50, 52 |
| D5 | `1.5.0` | C4 restricted webhook delivery and U2 AccessSpace closure | 27, 28, 29, 30, 70 |
| D6 | `1.6.0` | U3 configured federation and scoped workload principals | 71 |

The table is a recommended packaging sequence. It does **not** add G1 as a
prerequisite to D1 engineering: optional branches can start after their existing
EWP-16/59 prerequisites on isolated synthetic environments while production formats
are being qualified. Their results cannot waive G1's WARC/PDF/recovery gates.
Similarly, stage grouping does not make an unrelated capability mandatory when
shipping a smaller separately reviewed release. If a bundle is split, update this
plan, enabled-feature matrix and evidence dossier before choosing a new product
number; never relabel an incomplete stage as qualified.

EWP-51 has one primary completion in D3, but incremental C1/H1/H2 adapter subgates
belong in D2 after B1; H3/H4 subgates complete in D3. A subgate needs only its own
qualified stage, not every other adapter. EWP-35's initial H2 gate is literal search/
cues; email/IP observations remain off until their separate maintained extractor
qualification. No unqualified optional extractor blocks the literal-only release.
EWP-60/72 initially complete with the actual enabled D1 scope, then their documents
are maintained with every enabled-stage release. They do not wait for all U stages.

Component versions remain independent:

- Application: use the existing component/package alignment policy; the incompatible
  queue/schema/API replacement needs an explicitly reviewed major component change
  from inherited 1.1.0 (candidate 2.0.0), not a reset to product alpha numbers.
- Evidence Contracts: activate at 0.1.0 only when real authoritative schemas,
  examples and checks exist under owned paths. Version profile/engine protocols
  separately; no historical artifact is relabeled by package version.
- Browser Extension: remain planned 0.0.0 until real MV3 source/build/check ownership
  exists. Candidate component sequence: 0.1.0 B0, 0.2.0 B1, 0.3.0 B2; compatibility
  and stability, not this plan, determine an eventual component 1.0.0.
- Deployment, UI Prototype, Specification and Governance follow their own changes.
  Product packaging pins exact component/image/contract identities rather than
  assigning one shared number to all of them.

## 2.1 Current platform lane and separate Linux iteration

[ADR-012](../decisions/0012-macos-development-and-linux-qualification.md) and
[document 56](56-macos-development-and-linux-qualification.md) select MAC-DEV for
current implementation, local real tests and human acceptance. PC-SETUP-03 prepares
this Mac; native Linux provisioning is not an F0-DEV entry gate. Existing product
milestones above describe eventual usable/release boundaries. Their current Mac
implementation instances are F0-DEV/E0-DEV/P0-DEV and local R1/G1/D1–D6 readiness;
no Mac task acceptance by itself claims a pilot, Linux support or production G1.

LINUX-SETUP-01, LINUX-QUAL-01 and LINUX-QUAL-02 are separate later orchestration
items, not additional EWP/requirement/scenario IDs. Their target evidence remains
mandatory before Linux/production enablement. Current EWP dependencies refer to
accepted MAC-DEV outputs; they do not wait for those deferred Linux items.

## 3. Target architecture and technical workstreams

| Workstream | Target implementation boundary | First delivered / evidence |
| --- | --- | --- |
| Web application | Admitted sessions, CSRF, scoped services, HTML/API/SSE, inert viewers; no browser execution in web lifespan | E0/P0; real allowed/denied HTTP/browser evidence |
| Domain/PostgreSQL | PG16 source of truth for immutable capture identity, revisions, queue, grants, audit, dependencies and reservations | F0/E0; real transactions, constraints, concurrent workers and migration faults |
| Capture execution | Fixed host-trusted launcher, short-lived isolated Playwright runner via engine/1; qualified recording via engine/2 later | F0/E0 then R1; DNS/redirect/subresource/egress and generation proof |
| Artifact authority | Staged import, safe paths/hash/manifest, fenced promotion/commit/reconciliation, purpose eligibility and pins | E0; crash at every durable boundary, no unsafe promotion |
| Protected read plane | Verified snapshot before success headers, owned temp/transfer reservations and reauthorization/revoke checks | E0/P0; substitution, slow reader, timeout/revocation proof |
| Derived/offline work | Offline parser/diff, receipt renderer, report/import validator with bounded input/output and no live repair | P0/R1/D1+; hostile fixtures, no-network/resource proof |
| Browser companion | MV3 popup/options/service worker, then local journal/uploader and side-panel coordinator | D1/D2/D4; actual browser permissions/worker death/target/lease tests |
| Operations | Role-specific images, pinned deployment, config preflight, safe metrics, coherent backup and clean restore | F0–P0 and each new feature; exact environment and measured outcomes |
| Future access | U1 bundles, U2 custody/scoped adapters, U3 federation/workloads through one authorization authority | D3/D5/D6; migration and full installed-surface denial matrix |

Use Python 3.12/PostgreSQL 16 on this macOS arm64 host, with native development
tools and Docker Desktop linux/arm64 role images from documents 44–49/56. The later
native Linux x86_64/Ubuntu 24.04 candidate has a separate measured dossier; its
4 CPU/8 GiB/40 GiB envelope is not a Mac allocation or supported-capacity claim.
Do not retain the historical README's 2 GiB deployment claim as qualification.
Web/worker roles receive only required credentials and mounts. No Docker socket,
DB credential or writable final artifact store goes into browser/decoder containers.
Use a fixed host launcher contract rather than arbitrary container commands.

Implement the existing budgets as actual transactional admission/claim/release
rules: 1,000 pending including 100 interactive positions, one aggregate heavy-work
permit, 1 GiB shared temp, 100 MiB artifact/250 MiB attempt, 40 million screenshot
pixels and 512 MiB export. Enforce disk reserve of max(1 GiB, 10%). Protected reads
add their specified owned 512 MiB spool/2-transfer and deadline accounting within
shared budgets, and release heavy compute before slow transfer. Do not copy these
numbers into independent counters that can collectively exceed the global bound.
More detailed limits in documents 13/14/42/50–52 remain authoritative.

## 4. Entry and completion rules for every ticket

Before starting, assign a human owner/reviewer, exact source revision, scope,
dependencies, affected component paths and evidence environment. Turn each work
item below into a small set of implementation PRs in the written dependency order.
Each PR references its EWP ID, requirement matrix, relevant UI screen IDs and the
specific contract/fixture changes. Avoid a single implementation branch that cannot
be inspected or recovered incrementally.

Every ticket must deliver:

1. The observable behavior and actual files/contracts/migration/tool named in its
   work item, including denied/boundary/error behavior at introduction time.
2. Targeted unit checks where useful, real infrastructure/browser evidence for the
   invariant involved, and a structured record of source/image/tool/fixture identities.
   “Planned”, “present”, “tested” and “qualified for enablement” remain separate.
3. An upgrade/disable/restore disposition. Schema rollback compatibility and backup
   restore are distinct; a flag cannot undo persisted data or recover lost bytes.
4. Changelog/component updates, relevant operating instructions and no sensitive
   captures, credentials, exports or backup contents in Git/index/test logs.
5. Completion evidence reviewed against the named gate. Required empty/skipped/mock-only
   suites are failures, not partial success. Runtime findings reopen the affected
   contract/ADR rather than silently weakening it.

For current tickets, completion means the entire MAC-DEV scope is accepted and
integrated with real applicable local evidence. Native-target-only cases carry
explicit deferred-linux obligations in the separate Linux tickets; they are not
skipped local tests or a production claim. Linux-only assumptions below are read
through document 56. Keep failed local isolation features disabled; independent
implementation may proceed. Accepted upstream commits may be integrated into a
consumer task branch; unaccepted work/main merges remain outside task authority.

Acceptance catalogues: 12 ACC, 12 MON-ACC, 10 HUN-ACC, 12 B-ACC, 10 SYS-ACC,
12 OPS-ACC and 8 PRD-ACC = 76 definitions. Execute only the applicable stage subset
and relevant regressions, with exclusions explicit. This plan creates no duplicate
scenario definitions. The full requirement matrices remain documents 10/26/33/38/49.

## 5. F0 — 0.1.0-alpha.1: establish a measurable foundation

**Outcome:** clean builds, reviewed machine contracts, a proven isolation boundary
and a real schema foundation. Only synthetic engineering use; no pilot evidence
or public exposure. Primary order: EWP-61 + 02 → 62 → 01; 02 + 61 → 63 → 03 → 64.
Build/contracts can proceed independently before their joins. Current execution
is F0-DEV on the Mac after PC-SETUP-03 local readiness, not after Linux provisioning.
Real local gates still apply; native target reruns belong to L1/L2 in document 56.

1. Fix packaging/build ordering from the source review and reproduce a clean wheel
   install. Split web, capture and offline images, lock dependencies and identify
   runtime UID, mounted paths and required capabilities. Record image/source/SBOM.
2. Materialize the core request/result/profile/API examples before coding producers.
   Validate null/unknown distinctions, exact inventory, manifest self-hash exclusion,
   required files and unsupported versions. Activate Evidence Contracts only now.
3. Implement the fixed launcher template/lifecycle interface. Demonstrate sandbox,
   mount, resource and egress policy on real candidate host containers before
   accepting untrusted public destinations. Reap only owned orphan generations.
4. Exercise one controlled browser attempt with blocked private/metadata/DB/daemon
   destinations, DNS/redirect/subresource cases and late output. Record feasibility
   or stop dependent capture work and reopen the engine/launcher choice.
5. Bootstrap PG owner/migrator/runtime roles, migration ledger and schema constraints.
   Replace create_all as upgrade authority. Test failed/duplicate migrations and
   privileges before introducing application writes.
6. Establish query/pool/listener/lock/time/disk budgets and measure representative
   indexes. Keep metrics synthetic and content-free; no unmeasured throughput claim.

**Exit:** EWP-61/62/01 feasibility and OPS-ACC-01–05 applicable evidence, validated
contracts, fresh/failed migration rehearsal and DB budgets. A working image alone
does not pass network or privilege proof. **Recovery:** disposable test volumes;
no legacy data mutation. Rebuild from pinned source; preserve failed evidence.

## 6. E0 — 0.2.0-alpha.1: private evidence vertical slice

**Outcome:** an admitted actor can submit a synthetic public URL and inspect a
private, complete/partial/failed record with verified original bytes. There is no
publication/pilot release claim. Work items below define the complete prerequisite
order; EWP-04 legacy import can proceed after schema work independently of capture.

1. Implement provider-bound OAuth state, admission policy, durable sessions,
   last-admin recovery and disablement. Build one authorization/CSRF/error/audit/
   idempotency service before adding routes. A mocked provider does not establish
   live GitHub qualification; record any remaining integration gap.
2. Implement PG admission, durable sequence/events, leases/generations, retries and
   cancellation. Poll/recover without NOTIFY. Exercise two workers and a stale worker,
   not only unit-level queue mocks.
3. Implement safe runner staging, hashing, profile validation, promotion and fenced
   DB finalization. Inject failures before/after each filesystem/transaction boundary.
   Reconcile orphans without overwriting accepted evidence.
4. Introduce the shared purpose-eligibility authority, exact dependency pins/root
   fences, reservation counters and effective-feature compatibility checks. Only
   core installed edges are required now; future adapters stay disabled.
5. Implement verified reads before exposing byte downloads. Account the snapshot and
   transfer lease, reauthorize, enforce deadlines and deny substitution/tamper. Test
   a slow reader without holding the heavy permit or starving capture finalization.
6. Connect UI-W01/04/06/07 through engine/1 to a controlled source. Preserve original
   URL, readiness policy, HTTP status, server time, immutable artifacts and truthful
   partial/failure. Render only inert previews and escaped strings.
7. Build a dry-run legacy importer: inventory all prototype paths/IDs/tags/public
   links, preserve original hashes and label unknown provenance. Quarantine anomalies;
   suspend public access until deliberate mapping/review. Never migrate live source
   data as part of this planning change.

**Exit:** ACC-01/03/04/07/08/10/11 and relevant SYS/PRD-ACC-07 behavior for this slice,
real PG/browser/filesystem evidence and no unqualified network boundary. **Recovery:**
rebuild from synthetic fixtures; legacy import is dry-run-first with a verified
pre-import backup and explicit forward/restore path. Later features are absent.

## 7. P0 — 0.3.0-beta.1: complete and qualify the V0 pilot

**Outcome:** the complete 70-requirement V0 flow, operation and recovery, with shared
admin/editor roles. It includes Source history and context/importance, not C1/C2,
H1+, B0+, U1+ or required production WARC/PDF.

1. Implement archive/detail/dashboard/Source history and bounded filters/paging.
   Add revision-aware notes/tags/membership, approval, conflicts, theme/focus/empty/
   denied/offline states. Keep worker completion from overwriting editorial changes.
2. Implement strict CSV preview/confirmation and atomic selection admission. Add
   immutable collection/rationale request context and independently revisioned
   importance. Test edits during queued execution and no review/public side effects.
3. Build exact admin publication preview/commit/revoke and safe anonymous viewer.
   Recheck approval and purpose eligibility transactionally. Prove old slugs/assets,
   cache headers, no-store proxy behavior and new-request/ongoing-stream fences.
4. Build private export jobs and independent verifier. Produce actual ZIP/HTML and
   the exact V0 inventory. Keep optional PDF explicit; no silent missing requested
   PDF or inherited production label. Test damaged/path/duplicate/expiry cases.
5. Assemble pinned Compose/network/mount/secret/config preflight, clean install and
   operator bootstrap. Do not launch host control from the web process. Reject
   default secrets, incompatible schema and incomplete egress settings.
6. Implement coherent DB+artifact+config/role backup and upgrade/quiescence/rotation.
   Complete emergency removal ledger/root-fence/reconciliation before claiming
   recovery. Keep destructive filesystem cleanup bounded and owned.
7. Assemble reproducible synthetic core fixtures/evidence harness and safe telemetry.
   Simulate disk full, worker loss, absent backup, SQL/pool exhaustion and unhealthy
   services. Logs must not contain evidence text, URLs with secrets or tokens.
8. Restore into clean volumes/host, apply removal/epoch/session/grant/automation holds,
   verify IDs/hashes and rerun capture → edit → review → publish/revoke → export.
   Measure achieved recoverable point and restore duration; do not invent RPO/RTO.
9. Run EWP-15 across all 70 V0 requirements. Record real browser keyboard/theme/
   layout results and critical privacy/loss/isolation defect disposition. Produce
   a known-limits dossier and named operator handoff in EWP-16.

**Exit:** no skipped mandatory V0 evidence; ACC-01–11 as applicable, MON-ACC-07,
HUN-ACC-01/02, core SYS and OPS-ACC-01–08 plus protected-read cases. Publication
withdrawal/restore/legacy behavior must be real. **Recovery:** preserve compatibility
matrix; gate admission during maintenance, restore a matched backup in isolation,
reconcile removals and keep external/public/automatic work held until review.
A passed P0 is a controlled pilot boundary, not production preservation approval.

## 8. R1 and G1 — production preservation and baseline release

### R1 / 1.0.0-rc.1

1. EWP-73 evaluates recorder-backed current Playwright first using real controlled
   navigation/redirect bodies, subresources, HTTP errors, lost responses and denial
   paths. Pin observation layer, normalization, omissions and candidate versions.
   Browsertrix is an alternative only after measured evaluation, not a selected
   second runtime provider. Infeasibility blocks production, not private V0 history.
2. Materialize engine/2 and workspace-capture-production/1 / production export
   contracts. Correlate PNG/MHTML/WARC/capture and recording metadata to the same
   attempt. Reject wrappers, silent recapture/fallback and unverifiable main bodies.
3. Build one recorder integration, bounded WARC validation and independent offline
   replay. Enforce the 120-second attempt allocation and compressed/decoded/record/
   count ceilings from document 50. Replay receives no app cookies, live fallback,
   DB writes or public app origin authority.
4. In parallel after V0 export, implement the controlled ReceiptModel, local assets,
   offline PDF renderer and validator. Enforce 2 MiB receipt HTML, 16 MiB/100-page PDF,
   512 MiB renderer and deadline bounds. Test Unicode, long strings, escaping,
   resource/filesystem/network attempts and required-PDF failure.
5. Rehearse production-mode migration without relabeling old profiles. Independently
   verify actual production capture/export bytes, restore them cleanly and repeat
   replay/PDF/resource/read checks. Preserve exact producer/reader/tool identities.
6. Complete EWP-78 then EWP-17 format/monitoring delta and ACC-12 evidence. Automation
   for monitored backups/availability is operational hardening, not C3/C4 source
   watches or external editorial notifications.

**Exit:** applicable PRD-ACC-01–08, ACC-12 and OPS/SYS regressions; full same-attempt
format, offline replay, PDF, integrity/read and clean restore evidence. An apparently
readable archive is not proof of source authenticity, trusted time or universal replay.
**Recovery:** keep V0 read compatibility and profile identities; disable new production
admission if unqualified, preserve accepted bytes, use reviewed forward/restore
migration. Never silently downgrade a requested production attempt.

### G1 / 1.0.0

EWP-18 conducts security/dependency review, target newsroom pilots, measured support
limits/RPO/RTO and the concept's section 33 exit assessment. Close critical findings;
produce release candidate manifest, source/image/SBOM/contract identities, operator
sign-off and remaining limitations. Actual release/tag/push/deploy is a distinct
operation. No C/H/B/U expansion is required for this baseline. Future minor release
numbers remain proposals until each bundle is qualified and selected for shipment.

## 9. D1 — 1.1.0: comparison, research context and B0 companion

1. Establish EWP-59's compatibility rehearsal framework after V0 handoff: candidate
   descriptors, disabled/held states, schema/read/write compatibility and enabled-stage
   fixtures. Add only the feature being introduced; no all-feature dependency cycle.
2. Implement deterministic bounded MHTML main-document extraction, ordered pair
   analysis keys, no-network diff/storage/cache, pinned inputs and rebuild/cancel
   authority. C1 UI-W13 shows raw escaped differences, unsupported/identical/error
   separately and exact derivation identity. Qualify real workers/browser/access.
3. Build H1 quote/crop/comment contracts after C1 extraction. Use exact multibyte
   spans, repeated quote disambiguation and original pixel coordinate bounds. Add
   annotation revisions/retraction/dependencies, tasks and personal/shared saved
   queries. Missing anchors do not jump to a new source version.
4. Independently prove MV3 activeTab/pageCapture/worker/target behavior on the actual
   supported browser/OS matrix. Materialize companion/1 and exact profile/receipt
   schemas; generate TypeScript from authoritative contracts if used.
5. Implement pairing service plus UI-W22. Human-entered code/phrase, exact origin,
   digest-only secret storage, expiry/one-consumption, narrow scopes, disable/revoke
   and abuse bounds precede any extension handoff request.
6. Implement popup/options for B0 only: explicit server URL intent with private
   context/importance, own status and visible server-versus-tab warning. Package a
   usable independent B0 build with onboarding, disconnect and upgrade guidance.
7. Run EWP-60/72 initial enabled-scope operator handoff and compatibility records.
   Keep all absent C2+/H2+/B1+/U stages explicitly unsupported/disabled.

**Exit:** C1 MON-ACC-01/02/03/08, H1 HUN-ACC-03/04/05/09, B0 B-ACC-01/02/03/11/12,
applicable SYS and core regressions. Actual MV3/provider/build proof is separate
from the HTML studio. **Migration/recovery:** additive derived/context/grant tables;
originals unchanged; restored grants/sessions invalidated and automatic work held.
A disabled derivation UI cannot bypass pins or private artifact checks.

## 10. D2 — 1.2.0: profiles, personal attention, corpus and B1

1. Add immutable focus/noise profile revisions/fingerprints and bounded raw/filtered
   previews. Reanalysis on the same bytes is reprocessing, not a source-change event.
2. Add internal event/personal acknowledgement. Two users see separate attention;
   GET does not acknowledge, importance/review/publication do not share this state.
3. Build versioned unfiltered text corpus/coverage, exact original spans and literal/
   casefold cue revisions. UI-W17 distinguishes no hit, not indexed, unsupported
   and pending. Qualify literal search first; only add maintained email/IP tentative
   extractors after their separate evidence gate.
4. Implement B1 target consistency, local journal/spool and manual profile selection.
   Coordinate PNG/MHTML intervals with before/after target checks and worker-death
   recovery. Refuse unsupported pages; no silent MHTML downgrade or hidden recapture.
5. Implement owned upload reservations/chunks/offsets/hashes, isolated hostile-byte
   verifier, current-grant/revoke fences and one accepted capture. Test filesystem/
   DB crashes and lost receipt/replay boundaries on real infrastructure.
6. Extend detail/history/export to distinct browser profiles/time claims. Qualify
   independent browser package verification and baseline-publication/watch denials.
7. Complete B1 operations/re-pair/cleanup/restore and EWP-51's C1/H1/H2 adapter subgates
   where qualified. Adapters must not pretend viewport-only evidence has MHTML text.

**Exit:** C2/H2 applicable MON/HUN cases and B1 applicable B-ACC excluding B2-only
recording; real browser+DB+spool/restore proof. **Migration/recovery:** version indexes/
derivations so they can rebuild without rewriting original bytes; pending uploads
remain owned and bounded, restored grants invalid, no unattended upload/resume.

## 11. D3 — 1.3.0: frozen reports, native transfer and U1

1. Define reference-only/original-evidence report inventories and frozen ordered
   capture/annotation/revision selection. Implement explicit disclosure preview,
   bounded safe generation and independent verification. Missing dependencies cannot
   become latest revisions or silently disappear from a “complete” report.
2. Implement native selection export and quarantined import, bounded path/archive/
   nested decoding, foreign namespaces and preserved provenance claims. Admin
   disposition precedes atomic/idempotent acceptance. Never import local authority,
   roles, publication or active watches/delivery; no Hunchly-format compatibility.
3. Exercise import/export crash/recovery/purge and exact dependency closure, then
   complete H3/H4 browser-profile adapters and EWP-51. Publish the supported adapter
   list, not a blanket “browser evidence supports every investigation feature”.
4. Introduce U1 viewer/researcher/reviewer/publisher/workspace_admin bundles and
   lifecycle/invitation/session/offboarding preview. Migrate editor effective rights
   to researcher+reviewer; migrate old admin rights to researcher+reviewer+publisher plus
   workspace administration. workspace_admin alone gains no content/publication right.
5. Test bundle combinations, last-admin recovery, disablement/current grants and
   old-role migration across core and installed stages. V0 remains one shared
   custody scope until U2; role refinement is not historical privacy separation.
6. Complete EWP-40 handoff and update EWP-60/72 operating/support matrices.

**Exit:** HUN-ACC-08/09/10, B adapter cases, OPS-ACC-09/10/12 and affected core/SYS
regressions. **Migration/recovery:** frozen report pins survive compatible upgrades;
quarantine cannot activate automation; bundle migration has effective-rights diff
and clean restore rehearsal before enabled writes. Restore does not revive old sessions.

## 12. D4 — 1.4.0: bounded watches and assisted recording

1. Define watch/epoch/occurrence/quota state after C2. Start new watches paused;
   explicitly configure owner, successful meaningful-text baseline, interval/window/
   time zone and current effective capability. Default 24 hours, minimum 1 hour,
   20 watches, 24 attempts/watch/day, 50 automatic captures/day.
2. Implement PG due-slot admission/fencing, UTC/window/DST rules, coalescing and
   quota transactions. A failed/blocked/empty result never advances baseline; first
   successful baseline emits no change alert. Three qualifying failures pause.
3. Qualify competing schedulers, late epochs, bad-watch isolation, disk/resource
   pressure and restore holds. UI shows actual due/history/quota/reason and explicit
   resume; do not build a backlog storm after downtime.
4. Implement B2 one-tab/origin foreground coordinator and visible side panel/badge.
   Require gesture/grant/lease; apply 30-minute/20-item/5-second/2-second bounds,
   register minimal descriptors only under active lease, and preserve consent.
5. Prove pause/stop/focus/navigation/expiry/restart cases in a real extension. Review
   registered historical pending items separately from unregistered offline claims;
   stopped-epoch retro-registration is denied, manual B1 review remains explicit.
6. Complete companion source/artifact/SBOM/build/privacy/support dossier EWP-52.
   Store submission, signing, publication and installation are separate operations.

**Exit:** C3 MON-ACC-04/09/10/11/12 and full enabled B-stage evidence. **Recovery:**
automation restored held, no spontaneous baseline reset/upload/session restart;
current grants, scopes, budgets and owner reviewed before explicit resumption.

## 13. D5 — 1.5.0: minimal external delivery and access spaces

1. Add admin-approved destinations plus explicit owner opt-in, exact minimal payload
   and transactional deduplicated outbox. Commit intent before any network side effect.
2. Build one restricted HTTPS adapter with protected secret reference, SSRF/redirect/
   timeout/rate controls, at most five attempts and 24-hour lifetime. A remote-accept/
   local-crash result is acceptance uncertain; do not claim exactly-once delivery.
3. Add intent/attempt UI, revocation and deliberate replay. Recheck owner/destination/
   scope at send time; no screenshot/raw diff/query/secret URL in the first payload.
   Complete EWP-30 stage integration, restore/purge and handoff.
4. Introduce U2 one-capture/one-AccessSpace custody, flat groups and scoped grants.
   Migrate all V0 records to shared default; preserve historical access truth. Keep
   collections within their space and prevent them from becoming implicit ACLs.
5. Close every installed read/write/derived/job/export/report/import/browser/search/
   watch/delivery path over space authority. Denied counts/snippets/filenames must
   not reveal another space. Evaluate both human role and scoped grants.
6. Implement controlled move/separation preview with exact dependencies, publication
   revocation and generation fences. Require prescribed authority in both spaces;
   test concurrent moves, stale grants, disabled actors and in-flight work.

**Exit:** C4 MON-ACC-05/11/12 and U2 OPS-ACC-10/11/12 plus all installed-adapter
isolation regressions. **Recovery:** revoke/hold external work first, migrate with
membership/effective-rights preview, keep incompatible writers off, restore only a
matched pre-migration backup and reconcile grants/removals before enablement.

## 14. D6 — 1.6.0: configured federation and workloads

1. Implement configured OIDC issuer/subject trust, authorization code flow/PKCE S256,
   current claim/key validation and explicit account link/unlink. Never auto-link
   by email or treat reconnect as fresh MFA proof.
2. Keep optional provider outage behavior fail-closed without locking out the
   reviewed operator recovery path. Test key rotation, wrong issuer/audience, state/
   nonce/replay, disabled user and link collision across spaces.
3. Implement separate typed service principals and human owner, explicitly scoped
   capture-create/status-own, 7-day credential and 15-minute token bounds. No service
   admin/publication/archive read or implicit browser session. Owner disablement and
   grant rotation/expiry remain effective at every admission/finalizer.
4. Qualify migration and current installed-stage access matrix, update identity/
   incident/runbook/support documents and conduct the enabled-scope operator review.

**Exit:** IAM-011/012, OPS-ACC-09/12 and full installed authority regressions.
**Recovery:** new issuer/workload grants disabled by default during upgrade/restore;
review trust/key/grant mappings before enabling, preserve explicit local recovery.

## 15. Detailed work-item execution catalogue

The catalogue below expands all 78 original work items in primary milestone order.
Dependencies, owner and completion gate are carried from their source registry;
implementation steps are the selected decomposition. Steps within a ticket do not
allow its prerequisite or evidence gate to be bypassed. Every ticket also follows
section 4 and its milestone's migration/recovery rule. Abbreviated dependency IDs
such as `EWP-61/62` mean both complete; ranges mean every work item in the range.
The source table remains authoritative if an empirical finding requires a change.

### F0 work items

#### Work item EWP-61 — Reproducible role-specific images

Primary milestone: **F0**. Prerequisites / owner: None; backend/deployment.
Source: [49 work registry](49-infrastructure-and-identity-delivery.md).

Deliverable: Clean wheel/build correction, locked app/browser/offline targets, source/image/SBOM fingerprints and runtime UID/dependency manifest.

1. Correct clean wheel/build context/order and create locked web/capture/offline image targets with minimal runtime UID/mounts.
2. Record source/image/SBOM and installed dependency identities; demonstrate no compiler/secrets/Chromium in the web runtime.

Completion evidence: OPS-ACC-01; clean install/start, no hidden compiler/secrets/Chromium in web; exact supported versions recorded.

#### Work item EWP-02 — Machine-readable contracts

Primary milestone: **F0**. Prerequisites / owner: Selected 13–16; evidence/API.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Real JSON profile/request/result/OpenAPI schemas and synthetic success/error examples; activate Evidence Contracts at 0.1.0 with ownership.

1. Create authoritative core DTO/profile/engine/API schemas and validated positive/negative examples; generate secondary representations from one source.
2. Implement inventory/digest/self-hash/version fixtures and register real Evidence Contracts ownership/checks before consumers depend on it.

Completion evidence: Parse/validate examples and negative cases, unknown-version/required-inventory/self-hash tests; no new runtime dependency on planned metadata.

#### Work item EWP-62 — Isolated job launcher and network proof

Primary milestone: **F0**. Prerequisites / owner: EWP-61; deployment/security.
Source: [49 work registry](49-infrastructure-and-identity-delivery.md).

Deliverable: Fixed host-trusted lifecycle API/templates, per-job volumes/generations, real sandbox/resource/egress enforcement and owned-orphan reap.

1. Implement fixed host-trusted launcher lifecycle/templates, per-job generation volumes and owned orphan cleanup.
2. Prove actual sandbox/resource/network policy including DNS/IPv4/IPv6/UDP/metadata/DB/daemon denial; no container Docker socket.

Completion evidence: OPS-ACC-02/03; real host/container DNS/IPv4/IPv6/UDP/metadata/DB/daemon denial and late/orphan generation tests.

#### Work item EWP-01 — Build and runner feasibility

Primary milestone: **F0**. Prerequisites / owner: EWP-61/62; backend + security/operations.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Reproducible package/build plan fixing backend/COPY-order defects; pinned versions; one isolated Playwright runner prototype and capability/network proof.

1. Reproduce the known build/runner defects with pinned synthetic inputs; compare the source baseline to the selected launcher interface.
2. Exercise one real isolated navigation plus private/redirect/subresource denial; document unsupported paths and a go/no-go disposition.

Completion evidence: Synthetic capture + blocked private/DNS/redirect/subresource paths; show browser has no DB/secrets/final volume; fail closed/reopen ADR if infeasible.

#### Work item EWP-63 — PostgreSQL schema/role bootstrap

Primary milestone: **F0**. Prerequisites / owner: EWP-02/61; database/backend.
Source: [49 work registry](49-infrastructure-and-identity-delivery.md).

Deliverable: Reviewed owner/runtime/migrator grants, ordered migration framework and core constraints/index foundations from 45.

1. Bootstrap owner/migrator/runtime roles and the migration ledger with explicit grants.
2. Exercise real PG16 DDL/audit denial, failed/duplicate migrations and core integrity fixtures before app schema integration.

Completion evidence: OPS-ACC-04/05; fresh real PG16 roles/DDL/audit denial, failed/duplicate migration and integrity fixtures.

#### Work item EWP-03 — Schema and migration framework

Primary milestone: **F0**. Prerequisites / owner: EWP-02/63; domain/backend.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Ordered PostgreSQL migrations, entity constraints/indexes/roles, compatibility check replacing create_all upgrade authority.

1. Implement ordered migrations for core entities, revisions, attempts and state constraints with reviewed indexes and DB grants.
2. Make startup preflight verify schema compatibility; rehearse fresh, duplicate, failed and forward/restore transitions.

Completion evidence: Fresh DB and rollback/forward-failure rehearsal; real FK/unique/audit privilege tests.

#### Work item EWP-64 — Database budgets and routine maintenance

Primary milestone: **F0**. Prerequisites / owner: EWP-03/63; database/operator.
Source: [49 work registry](49-infrastructure-and-identity-delivery.md).

Deliverable: Bounded pools/listeners/SQL waits, realistic query/index measurements, vacuum/WAL/transaction/disk diagnostics and maintenance runbook.

1. Configure bounded pools/listeners/SQL waits and measure query/index behavior at representative cardinalities.
2. Document vacuum/WAL/lock/transaction/disk diagnostics and test pool exhaustion/competing sessions rather than claiming throughput.

Completion evidence: OPS-ACC-04/05/07; actual competing sessions/pool exhaustion/lock timeout and representative cardinalities.

### E0 work items

#### Work item EWP-05 — Identity and admission

Primary milestone: **E0**. Prerequisites / owner: EWP-03; security/backend.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Browser-bound OAuth state, verified allowlist logic, durable sessions, operator bootstrap, user disablement/role lifecycle.

1. Implement bound OAuth state, verified admission policy and durable session/CSRF lifecycle; include denied/expired/provider-error screens.
2. Add bootstrap, disablement and last-admin recovery; record actual provider integration separately from synthetic identity tests.

Completion evidence: ACC-11 org-only/empty lists, expiry/replay/provider error, session revocation and last-admin recovery; live provider result separately recorded.

#### Work item EWP-06 — Shared services and audit

Primary milestone: **E0**. Prerequisites / owner: EWP-03/05; backend.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Uniform authorization/CSRF, transactional safe audit, structured errors, idempotency service.

1. Route all application actions through one authorization, CSRF, safe audit and idempotency authority.
2. Use typed errors and transaction rollback on required audit failure; exercise allowed/denied private files/jobs/mutations without sensitive logs.

Completion evidence: Denied route/file/job mutation tests, audit write failure rollback, idempotency replay/conflict and no secret outputs.

#### Work item EWP-07 — Durable queue and events

Primary milestone: **E0**. Prerequisites / owner: EWP-03/06; backend.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Admission/slot locking, leases/generations, attempts, cancel/retry/recovery, durable SSE sequence.

1. Implement durable PG claim/lease/generation/attempt/SSE records and atomic admission, cancellation and retry transitions.
2. Test competing workers, lost NOTIFY, process restart and late output; keep terminal attempt history and confirmed UI states.

Completion evidence: ACC-03/04 real competing/late workers, lost NOTIFY, cancel race and bounded recovery; no false exactly-once claim.

#### Work item EWP-08 — Trusted artifact finalization

Primary milestone: **E0**. Prerequisites / owner: EWP-02/03/07; evidence/backend.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Safe runner-output import, staged hashing/manifest/promotion, fenced DB commit and reconciliation.

1. Validate runner stage paths, inventory, quotas and digests; promote under owned generation then commit fenced capture state.
2. Inject crash points across stage/hash/promotion/DB commit; reconcile only owned orphans and never overwrite accepted evidence.

Completion evidence: ACC-04/07/09 at each crash point; symlink/traversal/bounds/tamper tests, no evidence overwrite.

#### Work item EWP-53 — Shared eligibility/profile service

Primary milestone: **E0**. Prerequisites / owner: EWP-02/03/06; evidence/security.
Source: [43 work registry](43-contract-catalog-and-delivery-gates.md).

Deliverable: Materialized CTR-04, known profile registry and one purpose-specific decision service reused by core paths.

1. Implement one known-profile registry and purpose-specific eligibility decision service from CTR-04.
2. Reuse it for all installed capture/view/export/publication/baseline paths; deny unknown/partial/foreign/browser combinations truthfully.

Completion evidence: SYS-ACC-01/07; unknown/partial/foreign/browser decisions, denied diagnostics, no new V0 feature adapter.

#### Work item EWP-54 — Dependency/pin and invalidation authority

Primary milestone: **E0**. Prerequisites / owner: EWP-03/06/08; evidence/backend.
Source: [43 work registry](43-contract-catalog-and-delivery-gates.md).

Deliverable: Transactional exact dependencies/reverse lookup, root fence/epoch, pin accounting, bounded closure/reconciliation.

1. Implement exact transactional dependency/reverse edges, pins, root fence/epoch and bounded closure/reconciliation.
2. Exercise concurrent read/ready/remove/crash and do not invent pins for absent future adapters.

Completion evidence: SYS-ACC-02/03/04; real concurrent ready/read/remove/crash cases; V0 only actual core edges.

#### Work item EWP-55 — Shared reservations and fair claiming

Primary milestone: **E0**. Prerequisites / owner: EWP-07/08/53; backend/deployment.
Source: [43 work registry](43-contract-catalog-and-delivery-gates.md).

Deliverable: Global pending/heavy/temp/cache counters and generations, core admission/claim classes, overload diagnostics.

1. Implement shared pending/heavy/temp/cache accounting, generations and fair core claim classes.
2. Exercise concurrent reservation conversion/release/full disk/worker loss without double accounting or client priority override.

Completion evidence: SYS-ACC-05/06; real concurrent DB/process/full-disk proof, no duplicate release or client priority override.

#### Work item EWP-56 — Feature/schema compatibility preflight

Primary milestone: **E0**. Prerequisites / owner: EWP-03/05/06/53; backend/operator.
Source: [43 work registry](43-contract-catalog-and-delivery-gates.md).

Deliverable: CTR-06 descriptors, safe effective states, implemented-core startup/migration checks and default-disabled later features.

1. Implement schema/reader/writer/permission/flag descriptors and fail-closed startup/migration preflight.
2. Keep later features default-disabled and restored work held; test incompatible and partially available installed-core states.

Completion evidence: SYS-ACC-07/08; compatible reader/writer/permission/flag/restore-hold cases.

#### Work item EWP-77 — Protected read/snapshot authority

Primary milestone: **E0**. Prerequisites / owner: EWP-06/54/55; application/security.
Source: [53 work registry](53-preservation-delivery-and-production-gates.md).

Deliverable: Shared pre-header integrity snapshot, owned read reservations/transfer leases, root/permission/revoke checks and safe whole-file/proxy behavior.

1. Implement shared pre-header verified snapshots, owned read reservations/transfer leases and current authority/root/revoke checks.
2. Prove substitution/tamper/slow-client/timeout/lease/chunk rechecks and release heavy permits before long transfer.

Completion evidence: PRD-ACC-07 plus ACC/SYS access/removal; real file substitution, slow clients, lease/deadline, no heavy-slot deadlock.

#### Work item EWP-09 — Isolated capture vertical slice

Primary milestone: **E0**. Prerequisites / owner: EWP-01/05/06/07/08/53; capture/security.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Actual engine contract, readiness options/provenance and private submit -> complete capture detail flow.

1. Connect admitted capture form to policy, queue, isolated engine/1 and private detail using a controlled fixture source.
2. Expose readiness/status/time/profile and complete/partial/failed outcomes; verify actual browser isolation and no web-lifespan capture.

Completion evidence: ACC-01/04/08 synthetic real browser + DB; limits/partial/HTTP404 outcomes, no browser execution in web lifespan.

#### Work item EWP-04 — Legacy import and compatibility

Primary milestone: **E0**. Prerequisites / owner: EWP-03; backend/operator.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Source inspection report, byte-preserving Snapshot import, legacy profile, ID/tag/public-route mappings and anomaly handling.

1. Inventory prototype DB/files/public routes without mutation and produce a dry-run ID/profile/tag/URL mapping with anomaly totals.
2. Import only verified bounded bytes with foreign/legacy unknowns preserved; suspend publication until explicit disposition and compare counts/digests.

Completion evidence: ACC-10 fixture counts/digests/unknowns/public suspension; bad path/symlink/missing-byte cases cannot broaden access.

### P0 work items

#### Work item EWP-10 — Editorial UI and revision service

Primary milestone: **P0**. Prerequisites / owner: EWP-06/08/09; UX/backend.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Archive/detail/dashboard/Source history (REQ-HIS-001), bounded filters, notes/tags/collections, revision-aware review, accessible themes/errors.

1. Implement UI-W02/03/07/08 with bounded list queries, tabs, Source history and revision-aware context/review.
2. Add expected_revision conflict handling, accessible themes/focus/errors and immutable original-byte checks after every editorial operation.

Completion evidence: ACC-01/06/10/11 and MON-ACC-07 real browser; identical/partial history retained, conflicts/edits preserve hashes; group deletion preserves evidence.

#### Work item EWP-11 — CSV preview-confirm

Primary milestone: **P0**. Prerequisites / owner: EWP-06/07/10; backend/UX.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Strict grammar/limits, actor-bound preview, dedupe choices, atomic capacity/idempotent confirmation and mixed batch progress.

1. Implement strict CSV parser/limits, duplicate dispositions and actor-bound expiring preview with no job side effects.
2. Atomically confirm selected rows under queue reservations/idempotency; render stale/invalid/full-capacity and mixed terminal outcomes.

Completion evidence: ACC-02/04/11 malformed/oversize/stale/duplicate/queue-full cases; no preview jobs/silent truncation/partial admission.

#### Work item EWP-31 — V0 context/importance refinement

Primary milestone: **P0**. Prerequisites / owner: EWP-10/11; UX/backend.
Source: [33 work registry](33-investigation-roadmap-and-acceptance.md).

Deliverable: Pinned collection/rationale submission and CSV context, separate triage revision/filter, migration defaults.

1. Freeze collection/rationale per intent and CSV selection while retaining independently editable current editorial state.
2. Implement CaptureTriage revision/filter with migration defaults; prove pending completion cannot overwrite edits or mutate approval/publication.

Completion evidence: HUN-ACC-01/02, no worker overwrite of pending editorial edits or review/public side effects; prerequisite for EWP-15.

#### Work item EWP-12 — Publication and safe public viewer

Primary milestone: **P0**. Prerequisites / owner: EWP-05/06/08/10/77; publication/security/UX.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Exact admin preview, pinned projection, new slug, revoke, no-store asset authorization and legacy mapping.

1. Create exact approved admin projection preview and transactional publish/revoke with pinned revisions and new slugs.
2. Implement inert anonymous viewer/assets with no-store and protected reads; test revoked/old slugs, caches, streams and excluded private fields.

Completion evidence: ACC-05/06/10 anonymous/private/old slug/proxy asset tests, no raw evidence/notes/usernames; no GET state mutations.

#### Work item EWP-13 — Private export and verifier

Primary milestone: **P0**. Prerequisites / owner: EWP-02/06/08/10/54/77; evidence.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Bounded ZIP/HTML/export job, independent verifier, explicit profile/PDF/metadata options, expiry.

1. Build pinned V0 export inventory, controlled HTML receipt and explicit metadata/PDF options under bounded job reservations.
2. Provide an independent verifier and expiry/download states; reject missing/tampered/duplicate/path/required-output failures.

Completion evidence: ACC-07 real package independent verification, empty/damaged/duplicate/path cases; safe receipt and required-PDF failure.

#### Work item EWP-65 — Deployment config and clean install

Primary milestone: **P0**. Prerequisites / owner: EWP-01/03/05/56; deployment/operator.
Source: [49 work registry](49-infrastructure-and-identity-delivery.md).

Deliverable: Validated redacted settings schema, environment separation, pinned Compose/network/mount/secret bundle, readiness and operator bootstrap.

1. Implement redacted settings validation, separated environments and pinned Compose/network/mount/secret/readiness bundle.
2. Execute clean installation/operator bootstrap and fail startup on default secrets, incompatible schema, unsafe paths or exposure.

Completion evidence: OPS-ACC-03/06; default-secret/empty-policy/wrong-path/schema/exposure failures, clean synthetic installation.

#### Work item EWP-66 — Coherent backup and upgrade procedure

Primary milestone: **P0**. Prerequisites / owner: EWP-65/08/12/13; operator/backend.
Source: [49 work registry](49-infrastructure-and-identity-delivery.md).

Deliverable: Actual quiescence, verified DB+artifact/config/role backup, purpose-specific key rotation and tested upgrade/rollback interfaces.

1. Implement quiesced coherent DB/artifact/config/role backup and verified backup identity.
2. Rehearse interrupted upgrade, compatible/incompatible readers, purpose-specific secret rotation and forward/restore boundaries.

Completion evidence: OPS-ACC-06/08; interrupted upgrade, compatible/incompatible reader and matched backup/byte proof.

#### Work item EWP-14 — Install/backup/restore/upgrade

Primary milestone: **P0**. Prerequisites / owner: EWP-01/04/05/07/08/12/13/65/66; operations.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Implement target workspace-admin interfaces from 17; maintenance boundary, coherent backup, isolated restore, emergency purge ledger and upgrade runbooks.

1. Implement operator install/maintenance/backup/restore/upgrade interfaces from the playbook, using actual pinned deployment inputs.
2. Rehearse clean matched restore and legacy mappings with public/session/egress holds; record exact rollback limits and commands that really ran.

Completion evidence: ACC-09/10 clean install/restore with matching IDs/bytes/audit; old sessions/egress/publication disabled in rehearsal; no untested shell-command claim.

#### Work item EWP-57 — Emergency removal and restore fences

Primary milestone: **P0**. Prerequisites / owner: EWP-14/54/56; operator/security.
Source: [43 work registry](43-contract-catalog-and-delivery-gates.md).

Deliverable: Actual operator dry-run/containment/ledger/closure/reconcile workflow for existing removal policy.

1. Implement operator dry-run containment/removal ledger, exact closure and reconciliation with existing authority.
2. Inject DB/filesystem/ledger/restore failures and prove deny fences precede physical cleanup.

Completion evidence: SYS-ACC-03/04/08 and core ACC-09; real protected ledger/DB/filesystem crash/clean-restore evidence.

#### Work item EWP-58 — Synthetic fixture and evidence harness

Primary milestone: **P0**. Prerequisites / owner: EWP-09/12/13/14/31/55/56/57; QA/evidence.
Source: [43 work registry](43-contract-catalog-and-delivery-gates.md).

Deliverable: FX/CTR-12 core fixture generators, independent verifier runner and structured evidence records; add enabled-stage cases later.

1. Build deterministic FX/CTR-12 core fixture generators, independent verifier runner and structured result records.
2. Exercise real core DB/browser/filesystem/recovery gates; reject empty/skipped/mock-only required qualification evidence.

Completion evidence: Applicable core SYS scenarios alongside existing ACC/HUN V0 cases; no empty/skipped/mock-only required success.

#### Work item EWP-67 — Maintenance telemetry and incident guide

Primary milestone: **P0**. Prerequisites / owner: EWP-65/55/64; operator/security.
Source: [49 work registry](49-infrastructure-and-identity-delivery.md).

Deliverable: Bounded metrics/logs/support bundle, schedule/threshold state, owned temp cleanup, incident escalation/runbooks.

1. Implement bounded content-free metrics/log/support bundle and explicit maintenance schedule/threshold status.
2. Test full disk/unhealthy worker/no backup/quota/DB pressure plus owned temp cleanup without logging source text or secrets.

Completion evidence: OPS-ACC-07; no-content/no-secret telemetry, absent-backup/unhealthy-worker/full-disk and quota diagnostics.

#### Work item EWP-68 — Clean-host recovery and technical qualification

Primary milestone: **P0**. Prerequisites / owner: EWP-14/57/58/66/67; operator/security.
Source: [49 work registry](49-infrastructure-and-identity-delivery.md).

Deliverable: Isolated clean-volume/host restore, removal/epoch/grant/quarantine reconciliation, network/resource rerun and measured support evidence.

1. Restore matched data/config/artifacts into clean isolated volumes/host and verify IDs, hashes and removal/epoch/grant reconciliation.
2. Rerun network/resource/core workflow evidence and record actual recoverable point/time, support envelope and remaining gaps.

Completion evidence: OPS-ACC-01–08 as applicable plus ACC/SYS core gates; actual failure scenario/time/recoverable point, no fake RPO/RTO.

#### Work item EWP-15 — Integrated V0 qualification

Primary milestone: **P0**. Prerequisites / owner: EWP-09–14/31/55/56/57/58/64/67/68; engineering + security/operations/UX.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Full 70-requirement V0 dossier including HUN-ACC-01/02, applicable ACC-01–11 and core SYS scenarios, measured environment/limits, browser/accessibility review and defect triage.

1. Assemble all 70 V0 requirement results and relevant ACC/MON/HUN/SYS/OPS/read cases in an evidence index.
2. Run whole-workflow browser/access/recovery qualification and triage critical defects; publish measured limits and explicit unavailable evidence.

Completion evidence: All mandatory gates pass, no skipped required evidence; explicit optional PDF/monitoring gaps and no unresolved critical privacy/loss/isolation defect.

#### Work item EWP-16 — V0 operator handoff

Primary milestone: **P0**. Prerequisites / owner: EWP-15; product/operator.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Known limitations, editor/operator onboarding, support/incident path and reproducible pilot package manifest.

1. Prepare reproducible pilot manifest, known-limit guide, editor onboarding and incident/recovery instructions.
2. Have a named operator execute synthetic core/recovery procedures; record handoff and keep release/deploy authorization separate.

Completion evidence: Named operator can execute core/recovery runbooks on test environment; separate release decision, no automatic push/tag/deploy.

### R1 work items

#### Work item EWP-73 — Recorder/fidelity feasibility

Primary milestone: **R1**. Prerequisites / owner: EWP-16/62; capture/evidence/security.
Source: [53 work registry](53-preservation-delivery-and-production-gates.md).

Deliverable: Controlled same-attempt recording spike, existing-engine-first evaluation, explicit observation/header/coverage policy, pinned candidate comparison and provider disposition.

1. Compare pinned recorder-backed current engine against controlled same-attempt redirect/body/subresource/failure corpus.
2. Measure observation/normalization/coverage/resource/egress and correlate MHTML/PNG; record one qualified provider or block production.

Completion evidence: PRD-ACC-01/02/04; real browser/recording/egress/resource and MHTML/PNG correlation evidence, or production blocked.

#### Work item EWP-74 — Production profile/engine/verifier contracts

Primary milestone: **R1**. Prerequisites / owner: EWP-73/02/53; evidence/API.
Source: [53 work registry](53-preservation-delivery-and-production-gates.md).

Deliverable: Actual production capture/export and engine/2 schemas, WARC association/byte/inventory checks, structured verifier errors and negative fixtures.

1. Create actual engine/2 and production capture/export/verifier contracts with exact association/inventory/self-hash/parser rules.
2. Validate negative WARC/digest/version/record-association fixtures and preserve historical profile identities.

Completion evidence: PRD-ACC-01/03/08; exact profile/version/self-hash/parser/digest cases, no historical relabel.

#### Work item EWP-75 — Recording adapter and replay qualification

Primary milestone: **R1**. Prerequisites / owner: EWP-74/08/62; capture/deployment.
Source: [53 work registry](53-preservation-delivery-and-production-gates.md).

Deliverable: One qualified recorder-backed engine, bounded recording/validation/finalization, offline independent replay test harness and capability descriptors.

1. Implement one qualified recorder adapter under deadline and stored/decoded/record/count budgets with bounded finalization.
2. Run independent isolated replay and actual same-attempt/timeout/truncation/SSRF/reader evidence without live fallback or second capture.

Completion evidence: PRD-ACC-01–04/08; real same-attempt/timeout/truncation/SSRF/reader proof, no source fallback or unqualified dual provider.

#### Work item EWP-76 — Safe receipt PDF and production export

Primary milestone: **R1**. Prerequisites / owner: EWP-13/61; evidence/rendering/security.
Source: [53 work registry](53-preservation-delivery-and-production-gates.md).

Deliverable: Controlled ReceiptModel/template/font assets, isolated renderer/PDF validator, required-output inventory and independent package verifier.

1. Implement controlled ReceiptModel/template/local assets, offline renderer, PDF validator and required-output package contract.
2. Verify real PDF/ZIP bytes and adversarial Unicode/layout/filesystem/network/attachment/resource failures independently.

Completion evidence: PRD-ACC-03/05/06/08; filesystem/URL/attachment/CPU/memory/layout/Unicode/required-PDF failures and real exported bytes.

#### Work item EWP-78 — Production format/recovery dossier

Primary milestone: **R1**. Prerequisites / owner: EWP-68/75/76/77; evidence/operator.
Source: [53 work registry](53-preservation-delivery-and-production-gates.md).

Deliverable: Versioned producer/independent-reader fixture results, profile-mode migration, exact export verification and clean restore/replay/PDF/resource evidence.

1. Assemble producer/independent-reader/profile migration/export evidence and exact synthetic fixture/tool identities.
2. Clean restore and rerun offline replay/PDF/read/resource gates; record actual supported scope rather than universal fidelity.

Completion evidence: Applicable PRD-ACC-01–08 plus ACC-12 and existing OPS/SYS gates; source/artifact/fixture identities, actual support scope/limitations.

#### Work item EWP-17 — Production format/monitoring delta

Primary milestone: **R1**. Prerequisites / owner: EWP-16/75/76/78; evidence/operations.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Explicit WARC fidelity profile/validator, safe required PDF, availability probes and automated monitored backups/upgrade.

1. Combine qualified production capture/export/replay/read evidence with operational availability and monitored backup/upgrade behavior.
2. Compare every mandatory production delta to ACC-12 and old-profile compatibility; block rather than relabel missing preservation outputs.

Completion evidence: ACC-12 format/interoperability/security/restore evidence; old V0 profiles retain historical identity.

### G1 work items

#### Work item EWP-18 — Production review and pilots

Primary milestone: **G1**. Prerequisites / owner: EWP-17; product/security/operations.
Source: [18 work registry](18-assignable-work-packages.md).

Deliverable: Security/dependency review, measured supported limits/RPO/RTO, concept-target pilot evidence and release-candidate dossier.

1. Perform concept-target pilots plus security/dependency/support review against the actual candidate source/images/contracts.
2. Close critical findings, measure support/RPO/RTO and prepare the release dossier; actual tagging/deployment remains a separate operation.

Completion evidence: All concept section 33 conditions and critical defects closed; release/version/tag/publication separately authorized.

### D1 work items

#### Work item EWP-59 — Compatibility rehearsal framework

Primary milestone: **D1**. Prerequisites / owner: EWP-16/56/58; engineering/operator.
Source: [43 work registry](43-contract-catalog-and-delivery-gates.md).

Deliverable: Core framework plus per-stage candidate fixtures supplied by owning C/H/B tickets, safe disable/upgrade/rollback/restore and mixed archive semantics.

1. Create a reusable candidate descriptor/fixture compatibility rehearsal framework after V0 handoff.
2. Add each owning stage independently for safe disable/upgrade/rollback/restore and mixed archive semantics, without all-feature prerequisites.

Completion evidence: Applicable SYS-ACC-01–10 and owning stage cases; unsupported stages explicitly excluded, no all-feature prerequisite.

#### Work item EWP-19 — Comparison contract/fixtures

Primary milestone: **D1**. Prerequisites / owner: EWP-16; evidence/backend.
Source: [26 work registry](26-adoption-roadmap-and-acceptance.md).

Deliverable: C1 schemas, exact extractor main-document/line rules and synthetic MHTML corpus, identity/failure catalogue.

1. Create deterministic MHTML main-document, line normalization and ordered-pair analysis contracts with synthetic malformed/limit inputs.
2. Record unsupported/ambiguous versus identical/changed outcomes and stable keys before implementing parser workers.

Completion evidence: Known valid/ambiguous/malformed/unsupported/limit fixtures; deterministic analysis-key examples.

#### Work item EWP-20 — Offline analysis and derived storage

Primary milestone: **D1**. Prerequisites / owner: EWP-19; backend/security.
Source: [26 work registry](26-adoption-roadmap-and-acceptance.md).

Deliverable: Bounded no-network parser/diff jobs, input/output digests, cache/dependency/cancel/rebuild authority.

1. Implement offline bounded extraction/diff with exact input/output digests, owned cache/pins and current-authority cancellation/rebuild.
2. Prove no-network parser behavior, worker/temp/cache limits and original-byte immutability under failure and removal races.

Completion evidence: MON-ACC-01/02/08/11/12; no original-byte mutation, real worker/resource/permission evidence.

#### Work item EWP-21 — Comparison UI and C1 qualification

Primary milestone: **D1**. Prerequisites / owner: EWP-20/59; UX/evidence.
Source: [26 work registry](26-adoption-roadmap-and-acceptance.md).

Deliverable: Ordered pair UI, escaped line/word output, provenance/limits/errors, source-history integration.

1. Implement ordered comparison selection and escaped line/word UI with profile/extractor/input identity and explicit unknown states.
2. Qualify real browser/XSS/permissions and Source history integration before enabling C1; retain independent original digest evidence.

Completion evidence: MON-ACC-01/02/03/08 real browser, XSS/denied input checks, independent original integrity.

#### Work item EWP-32 — Annotation contract/derivation

Primary milestone: **D1**. Prerequisites / owner: EWP-16/21; evidence/backend.
Source: [33 work registry](33-investigation-roadmap-and-acceptance.md).

Deliverable: Real quote/crop/comment schemas, exact anchors, bounded derivative jobs and revision/retraction mapping.

1. Implement exact quote/crop/comment schemas, original/derived anchor identity and bounded crop/text derivation.
2. Exercise multibyte/repeated quote, stale/missing input and pixel/scale bounds; define revision/retraction dependency behavior.

Completion evidence: HUN-ACC-03/04/09; multibyte/repeated quote, stale/missing input and pixel/scale/bounds fixtures.

#### Work item EWP-33 — H1 working context/UI

Primary milestone: **D1**. Prerequisites / owner: EWP-32/59; product/UX/backend.
Source: [33 work registry](33-investigation-roadmap-and-acceptance.md).

Deliverable: Annotation detail/history, tasks and personal/shared saved views with explicit context.

1. Build annotation detail/history, assertion edits, tasks and explicit personal/shared saved-query controls.
2. Test concurrent revision/access/GET-no-mutation and preserve evidence/review separation across unavailable/retracted anchors.

Completion evidence: HUN-ACC-03/04/05/09; actual browser conflict/access/GET-no-mutation tests and no changed evidence/review.

#### Work item EWP-41 — Browser feasibility and permission proof

Primary milestone: **D1**. Prerequisites / owner: EWP-16; browser/security.
Source: [38 work registry](38-companion-roadmap-and-acceptance.md).

Deliverable: Minimal synthetic MV3 spike for activeTab, target/document/focus races, pageCapture, quota and worker termination; record package/browser/OS matrix.

1. Build a minimal real MV3 feasibility spike for activeTab, pageCapture, foreground document races and worker termination.
2. Measure current browser/OS/API/quota behavior and record supported profiles; do not replace failed proof with broad permissions.

Completion evidence: B-ACC-04/05/08/09/12 with real browser; exact supported profile decisions, no broad permission workaround.

#### Work item EWP-42 — Companion machine contracts

Primary milestone: **D1**. Prerequisites / owner: EWP-41/02; evidence/API.
Source: [38 work registry](38-companion-roadmap-and-acceptance.md).

Deliverable: Authoritative companion/1 request/error schemas, browser profile/receipt/export schema, state/offset examples and generated TypeScript types.

1. Materialize companion/1, error/receipt/profile/export schemas and generated TypeScript examples from authoritative definitions.
2. Validate chunk/offset/state/inventory/self-hash/ownership cases; activate Browser Extension ownership only with real build source/checks.

Completion evidence: Positive/negative example validation, inventory/self-hash/version/ownership review; activate planned components only with real files/checks.

#### Work item EWP-43 — Pairing, scopes and revoke service

Primary milestone: **D1**. Prerequisites / owner: EWP-42/05/06; security/backend.
Source: [38 work registry](38-companion-roadmap-and-acceptance.md).

Deliverable: Pairing approval UI, opaque token digests, narrow authorization, grant lifecycle, epoch and abuse limits.

1. Implement pending/approved/consumed/denied/expired pairing with human code/phrase, digest-only secrets and narrow grants.
2. Add UI-W22, revoke/epoch/abuse limits and real concurrent exchange/Origin/disabled-user/lost-token tests.

Completion evidence: B-ACC-01/02/07 real DB/HTTP/browser; replay/race/lost token/denied actor/Origin cases.

#### Work item EWP-44 — MV3 B0 shell and URL handoff

Primary milestone: **D1**. Prerequisites / owner: EWP-43/31; browser/UX.
Source: [38 work registry](38-companion-roadmap-and-acceptance.md).

Deliverable: Build/package, options/action UI, exact host permission, pairing/status/context, explicit server capture intent, escaped messages.

1. Build B0 MV3 popup/options and exact host permission with negotiated capabilities, pairing status and explicit URL/context intent.
2. Keep browser content/cookies/archive/publication scopes unavailable; test real gesture/permissions and escaped server errors.

Completion evidence: B-ACC-02/03/12, real gesture/permissions, no cookie/private-read/publication scope; unknown capabilities fail.

#### Work item EWP-45 — B0 qualification and onboarding

Primary milestone: **D1**. Prerequisites / owner: EWP-44/14/59; browser/operator.
Source: [38 work registry](38-companion-roadmap-and-acceptance.md).

Deliverable: Supported B0 package, server feature flag/config/runbook, upgrade/uninstall/revoke guidance.

1. Package a standalone supported B0 build and document config/flags, installation/onboarding, upgrade/disconnect/uninstall.
2. Execute B0 pairing/SSRF/queue/identity/restore regressions; record actual browser/source/package identities.

Completion evidence: B-ACC-01/02/03/11/12 and relevant core identity/SSRF/queue regressions; standalone B0 usable.

#### Work item EWP-60 — Integrated implementation/operator handoff

Primary milestone: **D1**. Prerequisites / owner: EWP-16/59; product/operator.
Source: [43 work registry](43-contract-catalog-and-delivery-gates.md).

Deliverable: Current contract/support matrix, workflow/incident guide and implementation-evidence index for actual enabled artifacts.

1. Build current enabled-contract support matrix and core/relevant-stage workflow/incident guide with evidence links.
2. Have named product/operator reviewers execute synthetic procedures; maintain the matrix with subsequent feature enablement.

Completion evidence: Named assignee can run core/relevant feature and recovery procedures on synthetic deployment; release/store/deploy separately authorized.

#### Work item EWP-72 — Technical/user operations handoff

Primary milestone: **D1**. Prerequisites / owner: EWP-16/68/59; product/operator.
Source: [49 work registry](49-infrastructure-and-identity-delivery.md).

Deliverable: Supported host/image/DB/config/backup matrix, operator and enabled-U-stage guides, access-review/support and evidence index.

1. Compile supported host/image/PG/config/backup and actual enabled-user-stage guides with access-review/support evidence.
2. Execute technical operator handoff at D1, leaving later U cases pending until owning qualification; revise at each enablement.

Completion evidence: Applicable OPS scenarios and actual enabled versions; U cases remain pending until their owning tasks qualify, release/deploy separately authorized.

### D2 work items

#### Work item EWP-22 — Profiles and previews

Primary milestone: **D2**. Prerequisites / owner: EWP-21; evidence/UX.
Source: [26 work registry](26-adoption-roadmap-and-acceptance.md).

Deliverable: Immutable revisions/fingerprint, restricted rules, raw/filtered preview and reanalysis labeling.

1. Implement restricted literal rules and immutable profile revision/fingerprint with raw/filtered preview and validation diagnostics.
2. Reprocess the same bytes under new fingerprints without a false new-source event; retain old results as explicitly versioned derivations.

Completion evidence: MON-ACC-01/02/09; changed rules reprocess same bytes without spurious source-change event.

#### Work item EWP-23 — Personal attention and C2 qualification

Primary milestone: **D2**. Prerequisites / owner: EWP-22/59; backend/UX.
Source: [26 work registry](26-adoption-roadmap-and-acceptance.md).

Deliverable: Internal event/ack model, personal inbox, explicit idempotent acknowledge/reopen.

1. Implement internal change events and actor-specific idempotent acknowledge/reopen transactions.
2. Build personal inbox and two-user tests showing that GET, shared importance, review and publication do not acknowledge for anyone.

Completion evidence: MON-ACC-03/09/11; two users, read-only GET, no review/publication side effects.

#### Work item EWP-34 — H2 corpus/index/cue contracts

Primary milestone: **D2**. Prerequisites / owner: EWP-33/20; search/backend.
Source: [33 work registry](33-investigation-roadmap-and-acceptance.md).

Deliverable: Versioned unfiltered text index/coverage, literal cue revisions and exact source hit records.

1. Create unfiltered versioned text corpus, extraction coverage and exact original-span hit/cue contracts.
2. Separate pending/unsupported/no-index/no-hit, literal/casefold matching and private query/context storage boundaries.

Completion evidence: HUN-ACC-06/07/09; no-index versus no-hit, original-byte spans and query/private-context boundaries.

#### Work item EWP-35 — H2 search and observation qualification

Primary milestone: **D2**. Prerequisites / owner: EWP-34/59; UX/evidence/security.
Source: [33 work registry](33-investigation-roadmap-and-acceptance.md).

Deliverable: First gate: search/literal cues UI; later gate: only qualified maintained email/IP extractors.

1. Implement private search/snippets/literal cues with permission rechecks, reindex/purge and visible corpus coverage.
2. Qualify optional maintained email/IP observations separately; label tentative matches and leave unqualified extractors disabled.

Completion evidence: HUN-ACC-06/07/09/10; coverage/limits/reindex/purge, no identity/truth/graph or automatic notification claims.

#### Work item EWP-46 — B1 capture and local spool

Primary milestone: **D2**. Prerequisites / owner: EWP-45/42; browser/evidence.
Source: [38 work registry](38-companion-roadmap-and-acceptance.md).

Deliverable: Same-target coordinator, viewport/optional MHTML inventory, journal/limits/preview/consent and local migrations.

1. Implement target coordinator, selected viewport/page inventory and bounded durable local spool/journal.
2. Test worker death, target/focus/navigation races, quota/expiry/preview and separate upload consent without hidden recapture.

Completion evidence: B-ACC-04/05/08/12, real worker death/quota/tab race fixtures and no hidden recapture.

#### Work item EWP-47 — B1 intake and durable finalization

Primary milestone: **D2**. Prerequisites / owner: EWP-45/42/08; backend/evidence/security.
Source: [38 work registry](38-companion-roadmap-and-acceptance.md).

Deliverable: Owned reservations/chunks/offset reconciliation, isolated verifier/quarantine, fenced one-capture acceptance, revoke cleanup.

1. Implement owned upload reservations/chunks/offset reconciliation and isolated hostile-byte verifier/quarantine.
2. Fence one accepted capture against revoke/epoch/crash and test exact byte ownership, cleanup and finalization authority.

Completion evidence: B-ACC-05/06/07/11, real DB/filesystem crash points, hostile bytes/resource limits and authority races.

#### Work item EWP-48 — B1 detail/history and independent export

Primary milestone: **D2**. Prerequisites / owner: EWP-46/47/13; evidence/UX.
Source: [38 work registry](38-companion-roadmap-and-acceptance.md).

Deliverable: Channel/time/fidelity labels, private original access, context/editorial integration and browser-export verifier.

1. Extend detail/history/editorial and independent export for browser channel/client time/server receipt/profile fidelity.
2. Deny browser baseline/publication assumptions and verify original submitted bytes with an independent reader.

Completion evidence: B-ACC-03/05/10, external independent digest verification and denied unknown-profile publication/baseline.

#### Work item EWP-49 — B1 qualification and operations

Primary milestone: **D2**. Prerequisites / owner: EWP-48/14/59; security/operator/browser.
Source: [38 work registry](38-companion-roadmap-and-acceptance.md).

Deliverable: Supported profile matrix, bounded cleanup/restore/re-pair, disconnect/incident UX and B1 evidence dossier.

1. Qualify real B1 capture/upload/worker/spool/restore/re-pair on the supported package/browser matrix.
2. Document cleanup/disconnect/incidents and supported profiles; keep B2 recording off until its separate gate.

Completion evidence: All applicable B-ACC cases except B2-only recording; no mock-only DB/browser/restore proof.

### D3 work items

#### Work item EWP-36 — Report profiles/snapshot contracts

Primary milestone: **D3**. Prerequisites / owner: EWP-33/13; evidence/API.
Source: [33 work registry](33-investigation-roadmap-and-acceptance.md).

Deliverable: Reference-only and original-evidence report inventories, frozen selection/preview and citation contracts.

1. Define reference-only/original-evidence report inventories, frozen ordered input revisions and citation/disclosure preview model.
2. Validate purged/retracted/unknown dependencies and changed live collections without silent latest-revision substitution.

Completion evidence: HUN-ACC-08; unknown/purged/retracted dependency and changing live collection fixtures.

#### Work item EWP-37 — H3 report generation/UI

Primary milestone: **D3**. Prerequisites / owner: EWP-36/59; product/evidence/security.
Source: [33 work registry](33-investigation-roadmap-and-acceptance.md).

Deliverable: Ordered report editor/preview, bounded HTML/package job and independent verification.

1. Implement ordered report editor, exact preview and bounded controlled HTML/package generation with dependency pins.
2. Verify actual output independently and test safe rendering, explicit disclosure and missing required outputs.

Completion evidence: HUN-ACC-08/09/10; safe renderer, exact disclosure, no silent missing output/latest-revision substitution.

#### Work item EWP-38 — Transfer profile/quarantine contracts

Primary milestone: **D3**. Prerequisites / owner: EWP-33/13; evidence/security.
Source: [33 work registry](33-investigation-roadmap-and-acceptance.md).

Deliverable: Own native profile, bounded archive validation, foreign namespace/identity mapping and preview.

1. Define native transfer inventory/foreign namespace mapping and quarantined bounded archive validation.
2. Reject unsupported profiles/paths/collisions and imported authority; preview identity/provenance anomalies before acceptance.

Completion evidence: HUN-ACC-09/10; no authority import, unsafe archive/unknown profile/collision/false-trust cases.

#### Work item EWP-39 — H4 acceptance/export/restore

Primary milestone: **D3**. Prerequisites / owner: EWP-38/14/59; backend/operator.
Source: [33 work registry](33-investigation-roadmap-and-acceptance.md).

Deliverable: Idempotent atomic import/selection export, anomaly/quarantine disposition and recovery/purge paths.

1. Implement atomic idempotent native import and explicit selection export with admin anomaly disposition.
2. Exercise DB/filesystem crash, purge and restore while preserving hashes and denying auto-publication/automation/role import.

Completion evidence: HUN-ACC-09/10; real DB/filesystem crash/restore, preserved original hashes and no auto publish/send/watch.

#### Work item EWP-40 — Integrated investigation handoff

Primary milestone: **D3**. Prerequisites / owner: EWP-35/37/39/59; engineering/operator.
Source: [33 work registry](33-investigation-roadmap-and-acceptance.md).

Deliverable: Cross-stage user/operations guide, provenance/trust/inclusion matrix and compatibility evidence.

1. Reconcile supported investigation stages, provenance/trust/inclusion and compatible artifact adapters in one handoff matrix.
2. Run applicable HUN/core/C regressions and update editor/operator instructions with exact enabled versus unsupported features.

Completion evidence: Applicable HUN scenarios plus relevant core/C/MON regressions; enabled flags and exact unsupported features visible.

#### Work item EWP-69 — U1 user lifecycle and capability bundles

Primary milestone: **D3**. Prerequisites / owner: EWP-16/06/53/59; identity/product.
Source: [49 work registry](49-infrastructure-and-identity-delivery.md).

Deliverable: IAM-001–006 DTO/schema/UI/migration, role preview, invitations, session/offboarding and last-admin recovery.

1. Implement U1 multiple capability bundles and user invitation/session/disable/last-admin lifecycle.
2. Preview and qualify old effective-rights migration; workspace_admin alone cannot gain content/publication privileges.

Completion evidence: OPS-ACC-09/10/12 plus core identity/revision regressions; old editor/admin effective-rights mapping and no retroactive privacy claim.

#### Work item EWP-51 — Browser-profile H/C adapters

Primary milestone: **D3**. Prerequisites / owner: EWP-49/21/33/35/37/39; evidence/UX.
Source: [38 work registry](38-companion-roadmap-and-acceptance.md).

Deliverable: Separate qualified adapters for C1/H1/H2/H3/H4 with exact provenance/dependency/export mapping.

1. Deliver separate browser C1/H1/H2 adapter subgates in D2 after B1 and their own owning stage.
2. Complete H3/H4 subgates in D3 with exact profile/provenance/pins/export mapping; list unsupported combinations explicitly.

Completion evidence: B-ACC-05/10/11 plus relevant HUN/MON cases; each subgate needs only its corresponding completed stage.

### D4 work items

#### Work item EWP-24 — Watch state and quota contracts

Primary milestone: **D4**. Prerequisites / owner: EWP-23; backend/product.
Source: [26 work registry](26-adoption-roadmap-and-acceptance.md).

Deliverable: Watch/epoch/occurrence schema, owner policy, due-window/quota state and paused defaults.

1. Create watch/epoch/occurrence schema and owner/baseline/window/quota transitions with paused default.
2. Validate due slot, time zone and configuration before scheduler work; encode no backfill and meaningful-baseline prerequisites.

Completion evidence: State/permission/quota transactions and invalid-config examples; no new active watch backfill.

#### Work item EWP-25 — Scheduler and baseline integration

Primary milestone: **D4**. Prerequisites / owner: EWP-24; backend/operations.
Source: [26 work registry](26-adoption-roadmap-and-acceptance.md).

Deliverable: Durable occurrence admission/fencing, UTC/window/DST/coalescing, capture+comparison+baseline/event transaction.

1. Implement competing-safe due-slot admission and capture/comparison/baseline/event fencing transaction boundaries.
2. Exercise DST/window/coalescing/quota/late-epoch/restart cases with real PG workers; first baseline and failed attempts emit no false change.

Completion evidence: MON-ACC-04/09/10/12 real competing schedulers/workers, late epoch and pause races.

#### Work item EWP-26 — C3 operational qualification

Primary milestone: **D4**. Prerequisites / owner: EWP-25/59; security/operations/UX.
Source: [26 work registry](26-adoption-roadmap-and-acceptance.md).

Deliverable: Watch UI/history, capacity/failure diagnostics, restore/resume runbook and resource evidence.

1. Build watch list/detail/history with quota/failure/effective-state diagnostics and explicit pause/resume after restore.
2. Measure resource/storage growth and bad-watch isolation; qualify scheduler and restore-hold behavior before enabling automatic captures.

Completion evidence: MON-ACC-04/10/11/12; bad watch isolated, no catch-up storm or unbounded evidence growth.

#### Work item EWP-50 — B2 assisted session and qualification

Primary milestone: **D4**. Prerequisites / owner: EWP-49/59; browser/UX/security.
Source: [38 work registry](38-companion-roadmap-and-acceptance.md).

Deliverable: Side panel/badge, one-tab/origin session generation, minimal active-lease descriptor registration, debounce/quota, pause/stop and explicit batch-upload review.

1. Implement visible one-tab/origin side-panel session, gesture/grant/lease, minimal descriptor registration and bounded debounce/quota.
2. Prove pause/stop/restart/cross-origin/focus/expiry and explicit batch-upload review, including stopped unregistered manual-B1 handling.

Completion evidence: B-ACC-04/07/08/09/12 real browser, no cross-origin/background collection or automatic restart.

#### Work item EWP-52 — Companion release/handoff dossier

Primary milestone: **D4**. Prerequisites / owner: EWP-45/49/50/59; browser/operator/product.
Source: [38 work registry](38-companion-roadmap-and-acceptance.md).

Deliverable: Current supported build matrix, editor/operator guide, SBOM/source/artifact identities, privacy/distribution checklist and limitations.

1. Assemble supported B0/B1/B2 and adapter evidence, source/artifact/SBOM identities and privacy/distribution checklist.
2. Complete editor/operator onboarding and incident/upgrade guidance; store signing/submission/install/release need separate execution.

Completion evidence: Full enabled-stage B-ACC evidence; explicit supported adapter list; release/store/push/deploy separately authorized.

### D5 work items

#### Work item EWP-27 — Destination policy and outbox

Primary milestone: **D5**. Prerequisites / owner: EWP-26; security/backend.
Source: [26 work registry](26-adoption-roadmap-and-acceptance.md).

Deliverable: Explicit approved destination/owner binding, minimal payload contract and transactional dedupe/expiry.

1. Model approved destinations, owner-specific opt-in, minimal payload and deduplicated finite-lived outbox intent.
2. Check disclosure/current authority at commit without sending network traffic; prepare revoke/expiry and denied payload fixtures.

Completion evidence: MON-ACC-05/11; unauthorized payload/destination denied, no network side effects at commit.

#### Work item EWP-28 — Restricted webhook transport

Primary milestone: **D5**. Prerequisites / owner: EWP-27; backend/security.
Source: [26 work registry](26-adoption-roadmap-and-acceptance.md).

Deliverable: One versioned HTTPS adapter, protected secret reference, rate/timeout/retry/uncertain outcomes.

1. Implement one pinned restricted HTTPS transport with safe secret references, destination policy and bounded retry/rate/timeout.
2. Use a controlled receiver to test SSRF/redirect, remote-accept crash and ambiguous outcomes without claiming exactly-once delivery.

Completion evidence: MON-ACC-05/12 controlled receiver, provider-accept crash/redirect/SSRF/idempotency evidence.

#### Work item EWP-29 — Delivery UI and C4 qualification

Primary milestone: **D5**. Prerequisites / owner: EWP-28/59; UX/operations/security.
Source: [26 work registry](26-adoption-roadmap-and-acceptance.md).

Deliverable: Safe intent/attempt views, revoke and explicit replay, no fake channels/receipt claims.

1. Build intent/attempt/payload previews and explicit revoke/replay with expired/no-secret/uncertain states.
2. Test authority changes before initial send/retry and avoid fake provider receipts or unsupported channel controls.

Completion evidence: MON-ACC-05/11/12; revoke before send/retry, ambiguous acceptance and expired/no-secret UX.

#### Work item EWP-30 — Integrated extension handoff

Primary milestone: **D5**. Prerequisites / owner: EWP-21/23/26/29/59; engineering/operator.
Source: [26 work registry](26-adoption-roadmap-and-acceptance.md).

Deliverable: Additive migration, backup/restore/purge rehearsal, stage flags, known limits and supported contract matrix.

1. Rehearse additive C-stage migration/disable/backup/restore/removal with current enabled-contract descriptors.
2. Update stage-specific operating guide and MON evidence index; restored auto-work stays held until explicit review.

Completion evidence: Full applicable MON suite plus relevant core regressions; restored auto-work held before enablement.

#### Work item EWP-70 — U2 access spaces and scope closure

Primary milestone: **D5**. Prerequisites / owner: EWP-69/54/56/59; domain/security.
Source: [49 work registry](49-infrastructure-and-identity-delivery.md).

Deliverable: IAM-007–010 migrations, one-space membership/flat groups, scoped repositories/downloads/jobs/derived adapters and move/separation preview.

1. Implement one-space custody, flat groups/scoped grants and shared-default migration across every installed adapter.
2. Build controlled move/separation/revoke preview and test denied counts/snippets/files/jobs/outputs and concurrent stale authority.

Completion evidence: OPS-ACC-10/11/12; denied cross-space counts/snippets/files/jobs/outputs, stale grants/move/publication races and installed-adapter coverage.

### D6 work items

#### Work item EWP-71 — U3 federation and workload grants

Primary milestone: **D6**. Prerequisites / owner: EWP-69/70/59; identity/security.
Source: [49 work registry](49-infrastructure-and-identity-delivery.md).

Deliverable: IAM-011/012 provider/link/claim validation and explicit scoped service-principal protocol/rotation/expiry under reviewed contracts.

1. Implement configured OIDC explicit issuer/subject linking and separate scoped workload principals with rotation/expiry.
2. Qualify provider outage/key/state/replay/link/disable failures; reject email auto-link and workload admin/publication/owner-disable bypass.

Completion evidence: OPS-ACC-09/12; provider outage/key/issuer/replay/link failures, no email auto-link, no service publication/admin/owner-disable bypass.

## 16. Cross-cutting validation and evidence record

Every milestone dossier records source commit, component/package/profile versions,
image digests/SBOM, host/browser/DB/tool identities, fixture seed and expected hashes,
commands, actual result, timing/resource measurements and unavailable checks.
Reference large synthetic run outputs from an approved evidence location; do not
commit real case artifacts, credentials, uploads, DB dumps or backup data.

| Concern | Earliest blocking gate | Subsequent rerun trigger |
| --- | --- | --- |
| Build and dependency reproducibility | F0 / EWP-61 | Image, lockfile, browser/renderer/toolchain or host change |
| Network/browser isolation | F0/E0 / EWP-62/01/09 | Capture/launcher/recorder/network policy or supported host change |
| PG privilege/concurrency/durability | F0/E0 / EWP-63/03/07 | Schema/claim/lease/reservation/role or PG change |
| Integrity and publication withdrawal | E0/P0 / EWP-08/77/12 | New byte route/proxy/store/profile/authority/root fence |
| UI/editorial boundaries | P0 / EWP-10/11/31 | Form/revision/disclosure/accessibility or supported browser change |
| Backup/restore/removal | P0 / EWP-66/57/68 | Persisted feature, dependency edge, storage/config/identity/upgrade change |
| WARC/PDF/interoperability | R1 / EWP-75/76/78 | Recorder/renderer/reader/profile/normalization/font change |
| MV3 target/consent/lifecycle | D1/D2/D4 / EWP-41/45/49/50 | Browser/package/permission/journal/upload/session protocol change |
| Space and identity closure | D3/D5/D6 / EWP-69/70/71 | New installed adapter, role/grant/provider or custody move path |
| External uncertainty/disclosure | D5 / EWP-27–29 | Destination/transport/payload/secret/owner policy change |

Do not rerun every unrelated test after a prose change. Run targeted checks plus
mandatory stage regressions when the actual behavior/invariant changes. Governance
validation proves ownership, links and version policy only. The UI design smoke
checks prove synthetic DOM transitions/layout only. Neither substitutes for the
runtime table above or the [verification policy](../operations/testing.md).

## 17. Dependency and assignment control

The full task graph remains acyclic. Current platform prerequisite PC-SETUP-03
means Mac readiness. Put native Linux setup/qualification in separate backlog items
without an edge from them to current Mac implementation. Preserve the accepted
LOC-1/2 history and LOC-4 code/reviews. The platform transition does not admit every
backlog EWP or authorize a release. Important feature joins to preserve:

- EWP-01 waits for images/launcher (61/62); contracts 02 precede DB bootstrap 63 and
  schema 03. Writing application routes before shared auth/service contracts is
  an avoidable rework risk, not a new shortcut around these joins.
- Publication/export 12/13 wait for protected reads 77. EWP-77 waits for shared
  dependencies/reservations 54/55; this is a core V0 gate, independent of WARC.
- Backup 66 requires actual publication/export 12/13; operations 14 precedes removal
  57; evidence harness 58 and telemetry 67 join clean restore 68 before V0 qualification.
- EWP-31 joins context/importance into V0; H1 annotations 32/33 are later. “Hunchly
  inspiration” never moves those later dependencies into EWP-15.
- EWP-59 follows V0 handoff and provides a framework for each stage, not a gate
  that waits for every future stage before any can qualify.
- Production 73–78/17/18 follows V0 handoff without C/H/B/U dependencies. C/H/B/U
  work may run in parallel branches only after its own prerequisites and fixture setup.
- U2 covers every installed adapter, including capabilities shipped before it.
  Adding a new adapter after U2 requires its scoped denial proof before enablement.

The role labels in task sources describe needed expertise, not a claim that those
people exist. One person can hold several roles, but security/operational evidence
must still be reviewed explicitly. Estimate implementation after F0 feasibility and
team assignment using measured spikes, not the number of documents or HTML screens.
No calendar, staffing level or performance SLA is implied by this plan.

Recommended implementation start is a concrete small batch:

1. Create implementation issues for EWP-61 and EWP-02 with named owners, baseline
   source revision and the exact F0 evidence environment.
2. Produce clean image/build and machine-contract PRs; keep product flags off.
3. Start EWP-62 only from the pinned image outputs; execute real isolation proof.
4. Complete EWP-01 provider/runner disposition and EWP-63/03/64 DB foundations.
5. Review the F0 evidence dossier, resolve failed feasibility, then admit E0 work.

Creating issues/PRs on a remote service, pushing, deploying or running privileged
host infrastructure are future implementation operations; this documentation task
has not performed them. Routine authorized local implementation can follow this
plan without repeatedly seeking approval for reversible preparation.

## 18. Risks, decisions and release review

| Risk / uncertainty | Resolution owner and blocking work | Required disposition |
| --- | --- | --- |
| Candidate host cannot enforce sandbox/egress/resource policy | Deployment/security; 62/01/73 | Record actual failure; reopen launcher/provider ADR before dependent enablement |
| Same-attempt mandatory response coverage unavailable | Evidence/capture; 73–75 | Production blocked; preserve honest V0/partial identity, no wrapper/fallback |
| Candidate host cannot meet bounded simultaneous work | DB/deployment; 64/55/67/68/78 | Measure contention/reserve, adjust with reviewed contract/fixture changes |
| Legacy source data is incomplete or active public URLs exist | Operator/evidence; 04/14 | Dry-run inventory, anomaly quarantine and deliberate public mapping/review |
| PDF/independent reader unsupported on exact build | Evidence/security; 76/78 | Pin qualified implementation or block required production output |
| MV3 target consistency/permission unavailable | Browser/security; 41/46/50 | Support only measured profiles/browser versions; no broad-permission workaround |
| Role/space migration broadens authority | Identity/security; 69/70/71 | Preview effective-rights diff, deny unknown paths, clean recovery rehearsal |
| Report/import/automation retains hidden dependencies | Evidence/operator; 54/57 and owning stages | Exact pins/closure/invalidation; block output or use explicit allowed disposition |
| Desired release bundle exceeds real team capacity | Product/engineering after F0 | Split optional bundle with updated version/feature/evidence map, not waived gates |
| UI language and operational rollout details need newsroom review | Product/UX before P0 | Keep new canonical design English, preserve source language evidence; specify product localization before claiming support |

Before any actual release, review: enabled-feature/contract matrix, all applicable
requirement and scenario results, open critical defects, supported environment,
profile provenance/fidelity, migrations/rollback limits, clean recovery, operator
handoff, dependency/SBOM status and artifact identities. Select a product version
only for the verified bundle. A local commit, a generated screenshot or a complete
specification is not a release approval.

## 19. Current completion boundary

This change delivers only the linked interactive UI design, screen/state/interaction
specification, primary-milestone mapping and expanded steps for all 78 work items.
No EWP runtime ticket is marked done. All runtime feasibility, schema migration,
Docker/PG, provider/browser-extension, WARC/PDF, supported capacity and recovery gates
remain pending until actual implementation evidence exists. Keep this section and
the implementation-evidence index truthful as work proceeds.
