# Hunchly-inspired requirements: stages, tasks and acceptance

Date: 2026-11-09. Status: **selected documentation design; runtime not implemented**.
Owner: product/evidence/engineering/security. Authority: ADR-006. Add 27 requirements
to the stable prior 107: two H0/V0, 25 later-stage. Total 134; V0 has 70 applicable
requirements, and later stages have 64 in this adoption pass. ADR-007/document 38
subsequently bring requirement totals to 158, 70 V0 / 88 later and 52 tasks in that
pass. ADR-008/document 43 refines delivery to 60 tasks/56 scenarios with IDs unchanged.
ADR-009/document 49 subsequently added 12 future IAM requirements: that pass
totaled 170 requirements, 72 tasks and 68 scenarios. ADR-010/document 53 refines
delivery to 78 tasks/76 scenarios with all 170 requirement IDs unchanged.
Original IDs/scenarios stay stable.

## Stage boundaries and original implementation

| Stage | Selected result | Dependencies / explicit scope |
| --- | --- | --- |
| H0 / V0 | Collection/rationale request context; independent shared importance | Existing capture/editorial services, EWP-10/11 plus EWP-31; no browser extension |
| H1 | Anchored quote/crop/comment revisions, research tasks and saved views | Qualified V0 and C1 derivation; no live viewport capture or private collection ACLs |
| H2 | Private content search, literal research cues and source-linked candidate observations | H1/C1; separate first literal-search gate and later maintained built-in extractor gate |
| H3 | Frozen selective reference/original-evidence reports | H1 + verified export; H2 search is helpful but not required |
| H4 | Reviewed Workspace-native case transfer/import | H1 + verified export/migration/recovery; no Hunchly interchange claim |
| Selected separate browser stages | B0 handoff, B1 manual local view/MHTML, B2 restricted assisted sessions | ADR-007/documents 34–38; post-V0, not implicit H1–H4 prerequisites |
| Deferred | Credential replay/cookie jars, native photos/attachments/EXIF, regex/custom extractors, signatures/trusted time and graph integrations | Separate acquisition/format/trust work, not V0 or implicit H1–H4 capability |

C0–C4 remain selected in documents 20–26. H stages reuse those foundations without
turning research cues into CSS profiles, annotation edits into watch changes, or
reports into public pages. Production WARC/PDF/security/recovery gates remain
independent. Component ownership remains Application for future services, Evidence
Contracts for actual schemas, Deployment for resource/isolation and Specification
for this prose. No runtime component/dependency is created here.

## Assignable tasks and gates

| Ticket | Dependencies / owner | Bounded deliverable | Completion evidence |
| --- | --- | --- | --- |
| EWP-31 V0 context/importance refinement | EWP-10/11; UX/backend | Pinned collection/rationale submission and CSV context, separate triage revision/filter, migration defaults | HUN-ACC-01/02, no worker overwrite of pending editorial edits or review/public side effects; prerequisite for EWP-15 |
| EWP-32 Annotation contract/derivation | EWP-16/21; evidence/backend | Real quote/crop/comment schemas, exact anchors, bounded derivative jobs and revision/retraction mapping | HUN-ACC-03/04/09; multibyte/repeated quote, stale/missing input and pixel/scale/bounds fixtures |
| EWP-33 H1 working context/UI | EWP-32/59; product/UX/backend | Annotation detail/history, tasks and personal/shared saved views with explicit context | HUN-ACC-03/04/05/09; actual browser conflict/access/GET-no-mutation tests and no changed evidence/review |
| EWP-34 H2 corpus/index/cue contracts | EWP-33/20; search/backend | Versioned unfiltered text index/coverage, literal cue revisions and exact source hit records | HUN-ACC-06/07/09; no-index versus no-hit, original-byte spans and query/private-context boundaries |
| EWP-35 H2 search and observation qualification | EWP-34/59; UX/evidence/security | First gate: search/literal cues UI; later gate: only qualified maintained email/IP extractors | HUN-ACC-06/07/09/10; coverage/limits/reindex/purge, no identity/truth/graph or automatic notification claims |
| EWP-36 Report profiles/snapshot contracts | EWP-33/13; evidence/API | Reference-only and original-evidence report inventories, frozen selection/preview and citation contracts | HUN-ACC-08; unknown/purged/retracted dependency and changing live collection fixtures |
| EWP-37 H3 report generation/UI | EWP-36/59; product/evidence/security | Ordered report editor/preview, bounded HTML/package job and independent verification | HUN-ACC-08/09/10; safe renderer, exact disclosure, no silent missing output/latest-revision substitution |
| EWP-38 Transfer profile/quarantine contracts | EWP-33/13; evidence/security | Own native profile, bounded archive validation, foreign namespace/identity mapping and preview | HUN-ACC-09/10; no authority import, unsafe archive/unknown profile/collision/false-trust cases |
| EWP-39 H4 acceptance/export/restore | EWP-38/14/59; backend/operator | Idempotent atomic import/selection export, anomaly/quarantine disposition and recovery/purge paths | HUN-ACC-09/10; real DB/filesystem crash/restore, preserved original hashes and no auto publish/send/watch |
| EWP-40 Integrated investigation handoff | EWP-35/37/39/59; engineering/operator | Cross-stage user/operations guide, provenance/trust/inclusion matrix and compatibility evidence | Applicable HUN scenarios plus relevant core/C/MON regressions; enabled flags and exact unsupported features visible |

EWP-31 depends on existing editorial/CSV work, not EWP-15; adding it to V0 qualification
does not form a cycle. H1 gates at EWP-33, H2 at the explicit EWP-35 substage, H3 at
EWP-37 and H4 at EWP-39. EWP-40 is integrated handoff, not a circular prerequisite
for earlier stages. Tasks require real assignees/estimates when executed; no named
review, supported vendor compatibility or completed runtime test is invented.

## Scenario catalogue

### HUN-ACC-01 Explicit request context and pending-edit race

Two tabs with different collections, a CSV with preview defaults and a queued
capture. Confirm exact selected collection/rationale, immutable initial context and
current editable notes/membership. Change context/collection before confirmation
or edit notes while worker runs; reject stale intent and preserve actual latest
editorial state at completion. Unknown legacy context remains unknown, not inferred.

### HUN-ACC-02 Importance is triage

Set/clear flag with stale/current revisions, filter archive/history and migrate old
captures. Verify shared flag semantics, read-only GET, normal default and safe audit.
Editorial approval, personal attention, original bytes and pinned publication stay
unchanged. Anonymous/disabled mutation is denied.

### HUN-ACC-03 Quote/crop anchor integrity

Use repeated/multibyte text, invalid UTF-8 offsets, modified derivation, missing
original, scaled screenshot, out-of-bounds rectangle and resource-limit failures.
Only exact validated anchors become source quotes/regions; unsupported inputs fail
or remain explicitly user comments. Original PNG/MHTML/profile digests remain intact.
No live page/scripts/resources are fetched to repair an anchor.

### HUN-ACC-04 Revision, assertion and provenance separation

Edit/retract annotations in two tabs, inspect user-asserted relation versus recorded
capture redirect and imported/unknown origin. Old report pins do not float to latest.
An annotation timestamp is not capture time; server recapture is not browser-session
proof. Note/task/importance actions never approve evidence or publish/send it.

### HUN-ACC-05 Tasks and saved views

Complete/reassign/cancel a research task, disable its assignee, mutate collection
membership and use personal/shared saved queries. Validate view-definition visibility
separately from shared evidence access. Unsupported/stale filters cannot silently
broaden results or freeze a report. No automatic reminders, external sends or new ACLs.

### HUN-ACC-06 Corpus coverage and literal research cues

Use eligible/unindexed/failed/unsupported captures, multiple versions of one URL,
casefold expansion and repeated matches. Assert exact pinned spans/hashes, correct
source-versus-commentary scope, visible partial coverage and no CSS-profile/watch-
epoch changes. Query terms and cue values remain private; cap overflow is explicit.

### HUN-ACC-07 Observations are not entity truth

The same email/IP-like string appears on unrelated controlled pages or in a note.
Record tentative source-linked observations only; no automatic identity merge,
ownership assertion, graph relationship, watch, review or external notification.
Reindex/revise cue/extractor and preserve previous run/version/time provenance.
Only qualified built-ins are enabled; unsupported regex/custom extractor is rejected.

### HUN-ACC-08 Frozen report, disclosure and verification

Change collection membership/note after preview, retract a pinned note, exceed
selection/output caps and request unavailable PDF. Reject stale/missing dependencies,
never silently change selection/profile. Verify exact quote/crop/original refs,
reference-only versus original-byte inclusion and independent package hashes.
Escaping/resource-fetch tests prove an inert report; no unselected private context.

### HUN-ACC-09 Import, dependencies, emergency purge and restore

Round-trip synthetic own-native selection with conflicting foreign IDs/users,
unknown profile, corrupt/missing bytes and DB/filesystem crash points. Quarantine
failure has no accepted half-case. Foreign roles/public links/watches/destinations
do not activate. Reapply removal/revocation ledgers after clean restore, invalidate
dependent notes/index/hits/report/payloads and do not resurrect removed input.

### HUN-ACC-10 Limits, trust and deferred features

Test archive/decode/member/path/link/JSON/crop/report/index CPU/memory/temp bounds,
denied direct input reads and unsafe renderer/import egress. Present imported bytes
as byte-verified foreign claims, not locally witnessed captures. Unsupported vendor
case files, browser cookies, downloads/native formats, regex and signatures cannot
appear as working features or false legal/time/identity assurances.

## Complete added-requirement coverage

| Requirement IDs | Stage / document | Planned scenarios |
| --- | --- | --- |
| REQ-ORG-001, REQ-ORG-002 | H0/V0 / 28 | HUN-ACC-01/02; core ACC-01/02/06/11 |
| REQ-ORG-003, REQ-ORG-004 | H1 / 28 | HUN-ACC-04/05/09 |
| REQ-ANN-001, REQ-ANN-002, REQ-ANN-003 | H1 / 29 | HUN-ACC-03/04/09/10 |
| REQ-ANN-004, REQ-ANN-005, REQ-ANN-006 | H1 / 29 | HUN-ACC-04/08/09/10 |
| REQ-FND-001, REQ-FND-002, REQ-FND-003 | H2 / 30 | HUN-ACC-05/06/09/10 |
| REQ-FND-004, REQ-FND-005, REQ-FND-006 | H2 / 30 | HUN-ACC-06/07/09/10 |
| REQ-RPT-001, REQ-RPT-002, REQ-RPT-003 | H3 / 31 | HUN-ACC-04/08/09 |
| REQ-RPT-004, REQ-RPT-005, REQ-RPT-006 | H3 / 31 | HUN-ACC-08/09/10 |
| REQ-XCH-001, REQ-XCH-002, REQ-XCH-003 | H4 / 32 | HUN-ACC-08/09/10 |
| REQ-XCH-004, REQ-XCH-005 | H4 / 32 | HUN-ACC-09/10 |

Shorthand `/NN` continues the `HUN-ACC-` prefix; core ACC and MON registries remain
independent. All scenarios are planned, not executed. H0 joins V0 gates; H1–H4
do not silently become V0 prerequisites. Empty/skipped required evidence cannot
qualify a feature; documentation/schema/tooling checks are not those runtime tests.
