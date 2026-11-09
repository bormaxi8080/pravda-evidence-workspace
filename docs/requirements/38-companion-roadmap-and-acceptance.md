# Browser companion delivery roadmap and acceptance

Date: 2026-11-09. Status: **assignable design; no runtime tasks completed**.
Owner: browser/backend/evidence/security/operations. Authority: ADR-007.
Documents 34–37 add 24 later-stage requirements to the prior 134. Current total:
158 requirements, 70 V0 / 88 later; this pass has 52 implementation tasks.
ADR-008/document 43 subsequently refine delivery to 60 tasks and 56 scenarios,
without adding product requirements or changing stage scope. ADR-009/document 49
subsequently add 12 future IAM IDs; current totals are 170 requirements/72 tasks/68
scenarios. Browser stage scope/owning requirement IDs stay unchanged.

## Stages and independence

| Stage | Deliverable / qualification | Explicit boundary |
| --- | --- | --- |
| B0 | MV3 pairing, exact Workspace origin, context selection, explicit public-URL handoff/status | After qualified V0; no local capture or cookies; server SSRF still applies |
| B1 | Manual viewport/page profiles, local review/spool, resumable verified intake, private detail and own export | After B0; private authenticated page content possible, never credential replay or automatic publication |
| B2 | Visible one-tab/origin assisted local recording, pause/stop and reviewed upload | After B1; same-origin activeTab/foreground constraints; no background/all-sites history |
| Adapter subgates | H1 annotations, C1 comparison, H2 content search, H3 reports, H4 transfer | Only after the relevant H/C stage and exact browser-profile compatibility qualification |
| Deferred | Full-page stitching/OCR, arbitrary cross-origin/background recorder, cookie jars/debugger/network WARC, native helper/downloads, Firefox/Safari/mobile, public browser-profile publication | New acquisition/permission/fidelity/trust decision and tests, not hidden B1/B2 scope |

Browser API floor Chrome 120 is selected, not a supported-old-browser guarantee.
EWP-41 records current stable/previous supported stable behavior and exact OS/API
matrix. If pageCapture/permissions/worker limits fail feasibility, keep B0/viewport
profile independently qualified and reopen ADR-007; never claim the page profile works.
No arbitrary automatic server commands, browser session restore, AI runtime or SaaS.

## Assignable implementation tasks

| Ticket | Dependencies / owner | Bounded deliverable | Completion evidence |
| --- | --- | --- | --- |
| EWP-41 Browser feasibility and permission proof | EWP-16; browser/security | Minimal synthetic MV3 spike for activeTab, target/document/focus races, pageCapture, quota and worker termination; record package/browser/OS matrix | B-ACC-04/05/08/09/12 with real browser; exact supported profile decisions, no broad permission workaround |
| EWP-42 Companion machine contracts | EWP-41/02; evidence/API | Authoritative companion/1 request/error schemas, browser profile/receipt/export schema, state/offset examples and generated TypeScript types | Positive/negative example validation, inventory/self-hash/version/ownership review; activate planned components only with real files/checks |
| EWP-43 Pairing, scopes and revoke service | EWP-42/05/06; security/backend | Pairing approval UI, opaque token digests, narrow authorization, grant lifecycle, epoch and abuse limits | B-ACC-01/02/07 real DB/HTTP/browser; replay/race/lost token/denied actor/Origin cases |
| EWP-44 MV3 B0 shell and URL handoff | EWP-43/31; browser/UX | Build/package, options/action UI, exact host permission, pairing/status/context, explicit server capture intent, escaped messages | B-ACC-02/03/12, real gesture/permissions, no cookie/private-read/publication scope; unknown capabilities fail |
| EWP-45 B0 qualification and onboarding | EWP-44/14/59; browser/operator | Supported B0 package, server feature flag/config/runbook, upgrade/uninstall/revoke guidance | B-ACC-01/02/03/11/12 and relevant core identity/SSRF/queue regressions; standalone B0 usable |
| EWP-46 B1 capture and local spool | EWP-45/42; browser/evidence | Same-target coordinator, viewport/optional MHTML inventory, journal/limits/preview/consent and local migrations | B-ACC-04/05/08/12, real worker death/quota/tab race fixtures and no hidden recapture |
| EWP-47 B1 intake and durable finalization | EWP-45/42/08; backend/evidence/security | Owned reservations/chunks/offset reconciliation, isolated verifier/quarantine, fenced one-capture acceptance, revoke cleanup | B-ACC-05/06/07/11, real DB/filesystem crash points, hostile bytes/resource limits and authority races |
| EWP-48 B1 detail/history and independent export | EWP-46/47/13; evidence/UX | Channel/time/fidelity labels, private original access, context/editorial integration and browser-export verifier | B-ACC-03/05/10, external independent digest verification and denied unknown-profile publication/baseline |
| EWP-49 B1 qualification and operations | EWP-48/14/59; security/operator/browser | Supported profile matrix, bounded cleanup/restore/re-pair, disconnect/incident UX and B1 evidence dossier | All applicable B-ACC cases except B2-only recording; no mock-only DB/browser/restore proof |
| EWP-50 B2 assisted session and qualification | EWP-49/59; browser/UX/security | Side panel/badge, one-tab/origin session generation, minimal active-lease descriptor registration, debounce/quota, pause/stop and explicit batch-upload review | B-ACC-04/07/08/09/12 real browser, no cross-origin/background collection or automatic restart |
| EWP-51 Browser-profile H/C adapters | EWP-49/21/33/35/37/39; evidence/UX | Separate qualified adapters for C1/H1/H2/H3/H4 with exact provenance/dependency/export mapping | B-ACC-05/10/11 plus relevant HUN/MON cases; each subgate needs only its corresponding completed stage |
| EWP-52 Companion release/handoff dossier | EWP-45/49/50/59; browser/operator/product | Current supported build matrix, editor/operator guide, SBOM/source/artifact identities, privacy/distribution checklist and limitations | Full enabled-stage B-ACC evidence; explicit supported adapter list; release/store/push/deploy separately authorized |

EWP-51 lists the prerequisites for the complete adapter set; its C1/H1/H2/H3/H4
subtasks can qualify independently after EWP-49 plus their respective EWP-21/33/35/
37/39. No adapter or EWP-52 is a prerequisite for B0/B1. B2's gate is EWP-50;
EWP-52 is integrated handoff rather than permission to delay earlier stage delivery.
Actual people/estimates require assignment; no schedule or completed review invented.

## Scenario catalogue

### B-ACC-01 Pairing, phishing and token exchange

Exercise correct/wrong/expired codes, matching phrase, denied admission, CSRF,
unsolicited origin/code, parallel approval/token exchanges, slow polling and lost
token response. One approval yields one expiring grant; a consumed response cannot
mint a second token. Secrets do not enter page DOM/URLs/logs/content scripts.

### B-ACC-02 Credential isolation and narrow authority

Use missing/expired/revoked/foreign tokens, disabled user, changed epoch, spoofed
Origin/extension ID and absent/disallowed Origin. Deny cross-user upload/status,
arbitrary private artifact read, review/admin/publication/watch access and unapproved
scope upgrade. Reject page-controlled fetch/message/redirect. Cookies never act as
fallback authentication on the companion API; web approval still requires CSRF.

### B-ACC-03 Mode/context and disclosure journey

Two tabs/collections and one logged-in controlled page: compare B0's independent
public-server capture with B1's local view. No session/cookie transfer or silently
changed mode. Instance/account switches preserve old destination; CSV/V0 unaffected.
Verify explicit inventory/thumbnail/upload consent, real status and private UI link.

### B-ACC-04 Wrong-tab and non-atomic acquisition

Activate another tab/window between every pre/probe/PNG/MHTML/post boundary;
navigate/reload same URL, cross origin, close/discard tab or mutate SPA content.
Abort unverifiable target/generation; wrong-tab bytes never enter an accepted
inventory. Stable identity still carries non-atomic caveat and separate times;
virtualized/offscreen/iframe content is not promised complete. Test activeTab expiry.

### B-ACC-05 Profiles, integrity and resource limits

Verify viewport-only/page profiles and independent originals/receipts; missing MHTML
cannot silently downgrade. Inject fake hashes/MIME/PNG, huge image dimensions,
malformed/compressed MHTML, metadata/path tricks, native Blob oversize and late API
completion. Limits/failure are visible; no live resource fetch or invented headers/
trusted time. Measure actual browser-native allocation limitations explicitly.

### B-ACC-06 Chunk durability, replay and finalize crashes

Drop each request/response, repeat identical/different chunks, interleave writers,
use wrong offsets/slot/actor, expire reservations and kill DB/controller around
write/offset/promotion/commit. Durable status plus reconciliation yields exact bytes
and at most one accepted capture for the client ID, never accepted partial content.
Lost finalize queries status; queue/storage failure is not a successful receipt.

### B-ACC-07 Revoke, cancel and authorization races

Expire token, revoke grant, disable user or stop/discard while chunk/validation/
finalization runs. Fence stale generations; commit order has one defined winner.
Unaccepted revoked bytes cannot be adopted; accepted evidence remains private and
unchanged. No later callback resurrects discarded data or silently restarts work.

### B-ACC-08 Offline, worker restart and local migration

Kill MV3 worker after every transition, close popup, restart browser/update/disable,
fill quota, corrupt IndexedDB or lose token response. Retained inventory survives
only where actually committed; interrupted capture is not re-created from a live
tab. Explicit reconnect/status/adoption handles pending bytes; expired/mismatched
instance/account/profile fails visibly. Check cleanup when Chrome returns after TTL.

### B-ACC-09 Assisted-session scope and pause

Explicit start on one tab/origin, repeated navigation events, same-origin grant,
cross-origin redirect, tab/window focus switch, 20-item/30min cap, token expiry and
missing side panel controls. Recording pauses/fences as specified, never resumes
on return/update. No background/history/DOM-mutation capture; each upload batch
requires disclosure review. Stop distinguishes retained local and approved uploads.

### B-ACC-10 Editorial, source and H/C compatibility

Preserve repeated client/server captures in Source history with exact channel/
time labels. Pending editorial edit cannot be overwritten at acceptance. Review/
triage/context/export do not change bytes. Unknown browser profiles cannot publish,
become watch baselines or masquerade as local server captures. Each enabled H/C
adapter verifies exact quote/crop/representation/report/transfer origin references.

### B-ACC-11 Backup, clean restore and incident removal

Back up accepted originals/context/receipts, leave incomplete quarantine out, restore
into a clean isolated installation, rotate epoch and reconcile/deletion ledger before
serving. Old tokens/pairings/intake cannot resume. Test orphan cleanup and reservation
release after interrupted upload. State actual remaining local/offline/downloaded
copies; server revoke cannot promise remote erasure. Re-pair needs deliberate action.

### B-ACC-12 Build, privacy and distribution boundaries

Inspect bundled executable code, manifest permissions/CSP, extension messages,
storage access levels, telemetry/redaction and dependency/artifact identity. Test
real gesture prompts, keyboard/focus/status, malicious titles/notes, incognito,
denied schemes/local-host patterns, no wildcard grant and exact Workspace host.
Current supported browser/OS and quota behavior need measured evidence; store,
signing, Firefox/Safari/Edge compatibility remain unclaimed until separately verified.

## Complete added-requirement coverage

| Requirement IDs | Stage / owning document | Planned scenarios |
| --- | --- | --- |
| REQ-BRW-001, REQ-BRW-002 | B0–B2 / 34 | B-ACC-03, B-ACC-05, B-ACC-12 |
| REQ-BRW-003, REQ-BRW-004 | B0–B2 / 34 | B-ACC-02, B-ACC-03, B-ACC-04, B-ACC-09, B-ACC-12 |
| REQ-BRW-005, REQ-BRW-006 | B0–B2 / 34 | B-ACC-03, B-ACC-08, B-ACC-09, B-ACC-12 |
| REQ-BCP-001, REQ-BCP-002 | B0+ / 35 | B-ACC-01, B-ACC-02, B-ACC-07, B-ACC-11 |
| REQ-BCP-003, REQ-BCP-004 | B0/B1+ / 35 | B-ACC-02, B-ACC-06, B-ACC-08, B-ACC-12 |
| REQ-BCP-005, REQ-BCP-006 | B0/B1+ / 35 | B-ACC-02, B-ACC-03, B-ACC-06, B-ACC-07, B-ACC-10, B-ACC-11 |
| REQ-BAE-001, REQ-BAE-002 | B1+ / 36 | B-ACC-03, B-ACC-04, B-ACC-05, B-ACC-10 |
| REQ-BAE-003, REQ-BAE-004 | B1+ / 36 | B-ACC-02, B-ACC-05, B-ACC-06, B-ACC-11 |
| REQ-BAE-005, REQ-BAE-006 | B1+ / 36 | B-ACC-05, B-ACC-07, B-ACC-10, B-ACC-11 |
| REQ-BLC-001, REQ-BLC-002 | B1/B2 / 37 | B-ACC-04, B-ACC-07, B-ACC-08, B-ACC-09, B-ACC-12 |
| REQ-BLC-003, REQ-BLC-004 | B0–B2 / 37 | B-ACC-02, B-ACC-06, B-ACC-08, B-ACC-12 |
| REQ-BLC-005, REQ-BLC-006 | B0–B2 / 37 | B-ACC-02, B-ACC-07, B-ACC-08, B-ACC-11, B-ACC-12 |

All 24 definitions appear once in documents 34–37. Scenario mappings are planned
tests, not results. The original V0/core, MON and HUN registries remain stable;
applicable core denied-access/integrity/queue/restore checks remain mandatory.
No new browser acceptance scenario becomes a hidden V0 or baseline-production gate.
If EWP-41 commits executable spike files under the reserved browser-extension path,
it activates that component with real ownership/checks in the same commit; a planned
manifest cannot coexist with unowned implementation. Temporary feasibility artifacts
otherwise remain outside that reserved path and outside the committed evidence set.

Open empirical items: native allocation/fidelity/permission timing, exact browser/OS
matrix and sustainable quotas; EWP-41/45/49/50 must close them before enabling modes.
