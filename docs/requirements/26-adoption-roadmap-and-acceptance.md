# Adopted ideas: delivery roadmap and complete acceptance coverage

Date: 2026-11-09. Status: **selected stage requirements; scenarios/tasks not executed**.
Owner: engineering/product/security. Authority: ADR-005. Original 67 requirements
remain stable; this pass adds 40 requirements: one C0/V0 history requirement and
39 requirements for adopted post-V0 stages. Total selected requirements: 107.
V0 has 68 applicable requirements; later-stage definitions are not V0 exit gates.

## Stage boundary and component ownership

| Stage | Selected result | Scope and gate |
| --- | --- | --- |
| C0 / V0 | Source history + existing engine-capability clarity | Existing source/capture records only; EWP-10/15 qualify history; no diff/watch/send |
| C1 | Offline stored-capture comparison | EWP-19–21 after qualified V0; deterministic safe parsing, inputs/results/provenance and cache lifecycle |
| C2 | Revisioned profiles + personal attention | EWP-22/23; filters cannot mutate evidence or masquerade as source edits; explicit per-user POST ack |
| C3 | Opt-in durable watches and internal events | EWP-24–26; capacity, epoch/lease races, DST, restart and baseline qualification |
| C4 | Restricted external delivery | EWP-27–30; explicit policy/outbox/receiver semantics, revocation, disclosure and restore qualification |
| Later evaluation | Visual/native-format/selector/inheritance/transports | Document 27; no implementation or stable release promise |

Specification owns these documents. Application will own logical analysis/watch/
attention/outbox services when implemented; Evidence Contracts owns real schemas;
Deployment owns offline-worker/egress/resource policy. This creates no microservice
per feature or new versioned runtime component by documentation alone. Product
release/date and existing Application 1.1.0 remain unchanged in this pass.

Comparison work may proceed as a separately staffed increment after V0, but does
not replace required production WARC/PDF/security/recovery work in EWP-17/18.
Do not call a release production-ready because comparison/notifications work.

## Assignable adopted-stage tickets

Existing EWP-01–18 are defined in document 18. IDs below extend the same registry;
roles need actual assignees/estimates when execution starts. No code is implemented here.

| Ticket | Dependencies / owner | Bounded deliverable | Completion evidence |
| --- | --- | --- | --- |
| EWP-19 Comparison contract/fixtures | EWP-16; evidence/backend | C1 schemas, exact extractor main-document/line rules and synthetic MHTML corpus, identity/failure catalogue | Known valid/ambiguous/malformed/unsupported/limit fixtures; deterministic analysis-key examples |
| EWP-20 Offline analysis and derived storage | EWP-19; backend/security | Bounded no-network parser/diff jobs, input/output digests, cache/dependency/cancel/rebuild authority | MON-ACC-01/02/08/11/12; no original-byte mutation, real worker/resource/permission evidence |
| EWP-21 Comparison UI and C1 qualification | EWP-20; UX/evidence | Ordered pair UI, escaped line/word output, provenance/limits/errors, source-history integration | MON-ACC-01/02/03/08 real browser, XSS/denied input checks, independent original integrity |
| EWP-22 Profiles and previews | EWP-21; evidence/UX | Immutable revisions/fingerprint, restricted rules, raw/filtered preview and reanalysis labeling | MON-ACC-01/02/09; changed rules reprocess same bytes without spurious source-change event |
| EWP-23 Personal attention and C2 qualification | EWP-22; backend/UX | Internal event/ack model, personal inbox, explicit idempotent acknowledge/reopen | MON-ACC-03/09/11; two users, read-only GET, no review/publication side effects |
| EWP-24 Watch state and quota contracts | EWP-23; backend/product | Watch/epoch/occurrence schema, owner policy, due-window/quota state and paused defaults | State/permission/quota transactions and invalid-config examples; no new active watch backfill |
| EWP-25 Scheduler and baseline integration | EWP-24; backend/operations | Durable occurrence admission/fencing, UTC/window/DST/coalescing, capture+comparison+baseline/event transaction | MON-ACC-04/09/10/12 real competing schedulers/workers, late epoch and pause races |
| EWP-26 C3 operational qualification | EWP-25; security/operations/UX | Watch UI/history, capacity/failure diagnostics, restore/resume runbook and resource evidence | MON-ACC-04/10/11/12; bad watch isolated, no catch-up storm or unbounded evidence growth |
| EWP-27 Destination policy and outbox | EWP-26; security/backend | Explicit approved destination/owner binding, minimal payload contract and transactional dedupe/expiry | MON-ACC-05/11; unauthorized payload/destination denied, no network side effects at commit |
| EWP-28 Restricted webhook transport | EWP-27; backend/security | One versioned HTTPS adapter, protected secret reference, rate/timeout/retry/uncertain outcomes | MON-ACC-05/12 controlled receiver, provider-accept crash/redirect/SSRF/idempotency evidence |
| EWP-29 Delivery UI and C4 qualification | EWP-28; UX/operations/security | Safe intent/attempt views, revoke and explicit replay, no fake channels/receipt claims | MON-ACC-05/11/12; revoke before send/retry, ambiguous acceptance and expired/no-secret UX |
| EWP-30 Integrated extension handoff | EWP-21/23/26/29; engineering/operator | Additive migration, backup/restore/purge rehearsal, stage flags, known limits and supported contract matrix | Full applicable MON suite plus relevant core regressions; restored auto-work held before enablement |

C1/C2 have their own completed operational gates at EWP-21/23; EWP-30 is integrated
handoff for all adopted stages and is not a circular prerequisite for earlier work.
No dependency on later speculative C5 features exists.

## Scenario catalogue

### MON-ACC-01 Deterministic original-versus-derived comparison

Use two controlled article captures with changed content and rotating menu/clock.
Verify exact ordered input/profile/algorithm digests, immutable originals, correct
added/removed/context output and raw-byte versus derived equality. Change profile
with identical input bytes and require a new reproducible analysis, not cache reuse.

### MON-ACC-02 Extraction, selector and resource failures

Exercise malformed/ambiguous MHTML, MIME/decode bomb bounds, missing selector,
empty meaningful text, unsupported rules, parser timeout/memory/temp/output caps and
non-complete/incompatible inputs. Assert explicit failed/incomparable, no unchanged
claim, no successful truncation, no network/resource fetch or original mutation.

### MON-ACC-03 Authorization, personal attention and inert rendering

Two admitted users view/ack/reopen the same event independently; GET has no mutation.
Disabled user and anonymous diff/result/input access fail. Test HTML/patch/selector
payloads as inert escaped text. Verify acknowledgement never changes editorial
review, public visibility or another user's attention state.

### MON-ACC-04 UTC, DST and scheduler fault isolation

Use named zones, missing/repeated local hours, cross-midnight windows, invalid zone,
clock movement, downtime, duplicate due claims and bounded jitter at window edges.
One invalid watch pauses itself; unrelated/manual work proceeds. At most one eligible
coalesced occurrence is admitted after downtime, not all missed slots.

### MON-ACC-05 Delivery disclosure, retries and uncertainty

Controlled fake receiver: reject unapproved destination/payload; revoke permission
between intent/claim/send/retry; simulate timeout before/after acceptance, 429/5xx,
redirect, TLS failure and process crash. Assert minimal payload, safe diagnostics,
unique intent, finite retries/expiry, honest uncertain outcome and no publication.

### MON-ACC-06 Deferred format evaluation

Reserved for later visual/PDF/JSON profile evaluations in document 27. It is not
a release gate of C0–C4; no adopted requirement depends solely on this scenario.
It must eventually prove original-format fidelity, bounded extraction and explicit
visual/context limits before those features become selected implementation scope.

### MON-ACC-07 V0 source history

Create two byte-identical manual captures, one complete different capture, partial/
failed/cancelled requests and legacy unknown-time data. Verify stable paged Source
history, exact links/statuses, shared internal authorization and no inferred change,
automatic watch, public history or implicit acknowledgement. Refines core ACC-01/04/10/11.

### MON-ACC-08 Cancellation, cache expiry and rebuild

Kill/duplicate/cancel analysis workers around writes/commit; expire/evict derived
bytes; revoke source access or purge an input. Verify fenced state, correct unavailable
or bounded rebuild, deterministic same-version bytes, explicit unsupported-version
failure and no hidden live recapture or loss of capture/export history.

### MON-ACC-09 Profile epoch and reanalysis races

Change profile while an old run/watch occurrence is in progress. Old result is
history only, not a new-epoch baseline or source-edit notification. First eligible
capture in the new epoch establishes baseline with no content-change alert. Manual
reanalysis remains labeled, and filter edits never retroactively erase past events.

### MON-ACC-10 Baseline, capture and availability distinction

First capture, unchanged normalized content, changed article, HTTP 404/blocked
page, timeout, partial output and selector disappearance yield distinct results.
Only eligible accepted comparable outcomes advance the pinned baseline. Quota,
manual pause, owner disablement and repeated failure must not discard old evidence.

### MON-ACC-11 Migration, restore and emergency removal

Migrate fixtures with/without extensions, restore into a fresh isolated environment,
reapply deletion/revocation ledger and inspect dependencies. Watches/destinations
stay paused, pending delivery cannot replay, source bytes/ack/history remain correct,
and erased inputs cannot regenerate cached diffs or content-bearing notifications.

### MON-ACC-12 Shared capacity and deployed isolation

Competing schedulers/analysis/dispatch workers under manual capture load hit shared
slots/quotas/rates/storage reserve without starving reads or starting uncontrolled
browser pools. Verify offline-parser network denial and actual webhook egress/TLS/
redirect boundaries; mocked counters alone do not prove installation-wide limits.

## All adopted requirement coverage

| Requirement IDs | Stage / document | Scenarios |
| --- | --- | --- |
| REQ-HIS-001 | C0 / 21 | MON-ACC-07; core ACC-01/04/10/11 |
| REQ-CMP-001, REQ-CMP-002 | C1 / 21 | MON-ACC-01/02/03 |
| REQ-CMP-003, REQ-CMP-004, REQ-CMP-005 | C1 / 21 | MON-ACC-01/02/03/09 |
| REQ-CMP-006, REQ-CMP-007, REQ-CMP-008 | C1 / 21 | MON-ACC-03/08/11/12 |
| REQ-PRF-001, REQ-PRF-002, REQ-PRF-003 | C2 / 22 | MON-ACC-01/02/09 |
| REQ-PRF-004, REQ-PRF-005, REQ-PRF-006 | C2 / 22 | MON-ACC-02/03/09/11 |
| REQ-ATT-001, REQ-ATT-002, REQ-ATT-003, REQ-ATT-004 | C2 / 22 | MON-ACC-03/09/11 |
| REQ-MON-001, REQ-MON-002 | C3 / 23 | MON-ACC-03/04/09/10 |
| REQ-MON-003, REQ-MON-004, REQ-MON-005 | C3 / 23 | MON-ACC-04/10/12 |
| REQ-MON-006, REQ-MON-007, REQ-MON-008 | C3 / 23 | MON-ACC-04/09/10/11 |
| REQ-NTF-001, REQ-NTF-002, REQ-NTF-003 | C4 / 24 | MON-ACC-05/11 |
| REQ-NTF-004, REQ-NTF-005, REQ-NTF-006, REQ-NTF-007 | C4 / 24 | MON-ACC-05/11/12 |
| REQ-EXT-001, REQ-EXT-002 | C1–C4 / 25 | MON-ACC-01/03/08/09/11 |
| REQ-EXT-003, REQ-EXT-004, REQ-EXT-005, REQ-EXT-006 | C1–C4 / 25 | MON-ACC-02/04/05/08/11/12 |

MON shorthand `/NN` continues the `MON-ACC-` prefix; core `ACC-*` keeps its own
registry. This matrix describes planned acceptance, not executed evidence.
Stage gates apply only the listed implemented scope, including relevant core
privacy/integrity/DB/browser/recovery regressions. Empty/skipped required evidence
does not pass. No selected C0–C4 requirement is covered only by deferred MON-ACC-06.
