# Selected V0 baseline and parameter register

Date: 2026-11-09. Revision: 0.6. Status: **engineering choices selected; runtime
qualification pending**. Owner: engineering lead; reviewer roles remain unassigned
to individuals. This continuation resolves design alternatives without claiming
human sign-off, tested behavior, a production release or implementation of contracts.

## Decision authority and links

The user requested continuation of all four documentation waves. Use the following
decisions to make the plan concrete and reviewable. The accepted engineering
governance remains unchanged. Architecture choices are recorded as selected design
ADRs: [ADR-002](../decisions/0002-v0-scope-and-topology.md),
[ADR-003](../decisions/0003-evidence-and-publication.md),
[ADR-004](../decisions/0004-execution-storage-and-identity.md).
Empirical feasibility can reopen a choice; it cannot waive evidence/privacy invariants.

| Decision | Selected disposition | Remaining qualification |
| --- | --- | --- |
| DEC-01 | V0 scope label; compatible patch fixes first; future incompatible runtime package 2.0.0; no product release now | Migration/route compatibility tests and release operation later |
| DEC-02 | Modular Python 3.12 SSR monolith, PostgreSQL 16, one-host Compose, Linux x86_64 qualification target | Pin image/dependency/browser digests after real build tests |
| DEC-03 | Direct Playwright in isolated runner, one engine/capability contract; Pravda adapter deferred | Egress/sandbox/output feasibility in EWP-01 |
| DEC-04 | Separate capture/export V0 profiles; WARC and required PDF remain production delta | Format/verifier tests; WARC fidelity design before EWP-17 |
| DEC-05 | Admin-published screenshot/allowlisted metadata, no-store, new slug on republish | Anonymous/proxy asset and disclosure tests |
| DEC-06 | Shared newsroom archive, editor review, admin publication, no two-person rule | Service-level role/revision tests |
| DEC-07 | PostgreSQL lease/fencing/polling, explicit cancel winner and durable sequence | Competing/late worker and reconnect tests |
| DEC-08 | Staged immutable namespaces, fenced finalization/reconciliation, quiesced backup | Crash-point and isolated restore tests |
| DEC-09 | Exact starting limits below; fail closed on unsupported resource enforcement | Measured resource and overload qualification |
| DEC-10 | Preserve/map IDs; suspend unreviewed legacy public links with explicit mapping/report | Synthetic legacy migration and operator review rehearsal |
| DEC-11 | Durable sessions, browser-bound OAuth state, operator bootstrap, enabled-role checks | Live OAuth and recovery/disablement tests |
| DEC-12 | Concept production criteria retained; ADR-005 selects C0 in V0 and C1–C4 later | WARC/PDF/security/pilot/support remain independent; stage qualification per document 26 |
| DEC-13 | ADR-005: C0 history in V0, C1–C4 comparison/monitoring later | Stage gates and extension resource/permission contracts in documents 21–26 |
| DEC-14 | ADR-006: explicit private submission context and independent importance in V0; H1–H4 investigation/handoff later | EWP-31 before V0 qualification; HUN-ACC and stage gates in document 33 |
| DEC-15 | ADR-007: optional post-V0 MV3 companion, explicit server/local modes and narrow paired intake | EWP-41–52, B-ACC-01–12; native API/permission/fidelity/restore gates before enablement |

ADR-005 supersedes the earlier optional-candidate treatment: C0 Source history is
explicit V0 scope; C1–C4 are selected later-stage work. Documents 21–26 define the
40 adopted requirements, parameter/permission boundaries and assigned-stage gates.
V0 limits below remain independent; extension limits do not silently enable features.

## Starting configuration contract

These are selected defaults to implement and test, not already available environment
variables. Validate startup values and cross-field constraints. Expose safe effective
values through status; secret values never appear there. Changing limits cannot
retroactively relabel incomplete output as complete.

| Setting | Selected value | Rule |
| --- | --- | --- |
| CSV input | 1 MiB; at most 500 parsed data rows | Count invalid/empty rows in input limit; no silent slicing |
| Confirmable batch jobs | At most 500 selected valid rows | Admission of all selected jobs is atomic |
| Pending jobs | 1,000 installation-wide | Includes queued/retry_wait and reservations; serialize admission |
| Capture slots | 1 by default | Do not start another runner until old process terminated or proven absent |
| Export slots | 1 by default | Independent bounded job/spool/renderer budget; no unbounded web-thread exports |
| Navigation / entire attempt | 60 / 120 seconds | Entire deadline includes conditions and output; cancellation teardown grace 10 seconds |
| Screenshot | At most 40,000,000 pixels | Inspect dimensions before allocation; never silently crop to meet completeness |
| Artifact / attempt total | 100 / 250 MiB | Enforce while writing and validating runner output |
| Export ZIP | 512 MiB including archive overhead | Bounded temporary spool; fail with profile/limit error |
| Free artifact/temp reserve | max(1 GiB, 10% of corresponding volume capacity) | Admission check plus write-time checks; stream limits still apply |
| Heartbeat / lease | 10 / 45 seconds | Heartbeat checks generation; expired execution is fenced before recovery |
| DB polling / recovery scan | 2 / 15 seconds | NOTIFY can reduce latency, never defines durability |
| Attempts / retry delays | 3 total; 10 then 30 seconds plus 0–20% jitter | Transient errors only; no automatic retry for policy/format/size denial |
| OAuth state | 10 minutes, single-use | Bound to browser nonce and safe local return path |
| Session lifetime | 8 hours idle, 7 days absolute | Rotation on login/role change; disabled user denied immediately on next check |
| Protected SSE recheck | At most every 30 seconds | Expiry/disable closes stream; current state remains independently queryable |
| Preview lifetime | 30 minutes | Actor-bound immutable input/selection revision; stale preview cannot confirm |
| Idempotency record | 24 hours | Actor+operation+key; same payload replays, changed payload conflicts |
| Detailed job events | 7 days | Current/terminal summary persists with job; expired replay sends reset |
| Ready export temp lifetime | 24 hours | Private, reauthorized each download; source capture not deleted |
| List / input strings | 25 default, 100 max; URL 8,192 bytes; title 256 chars | Reject excess; do not truncate silently |
| Notes / tags / names | Note 16,384 chars; 50 tags/capture; tag 64, collection 128 chars | Unicode display retained; comparison keys specified in document 14 |
| Submission rationale | Optional, at most 2,048 chars | Private context assertion, pinned with explicit collection IDs; no default manifest/export/public inclusion |
| Capture ports | HTTP 80, HTTPS 443 | Other ports excluded from V0; never implicit private-network exceptions |

DB transactions for admission, state change and lease operations have a selected
5-second lock-wait limit. Storage/finalization recovery must inspect durable intent
before deciding whether to retry acquisition. Receipt/export operations have a
120-second execution deadline and bounded spool; operation-specific slots prevent
export from consuming the capture slot indefinitely.

## Terminology and compatibility

Source is a URL identity; Capture is one request with an immutable accepted result;
Attempt is execution history. Artifact stores exact bytes; Profile defines the
required inventory. Editorial revision, Review, Publication and Availability are
independent. Snapshot is a legacy/UI synonym, not a new domain identity. Export is
a derived package with its own time/inventory. Comparison is a later derived
analysis, never a substitute for Capture or Review.

Definition detail lives in documents 14–17. The original 67 requirement IDs remain
stable. REQ-HIS-001 adds explicit Source history to V0; the 39 comparison/profile/
watch/delivery requirements apply only to selected later stages. No automatic
monitoring/send becomes a V0 requirement.

## Investigation/handoff adoption

[ADR-006](../decisions/0006-investigation-context-and-handoff.md) adds REQ-ORG-001/002
to V0: immutable private request context and separately revisioned shared triage.
The ADR-006 pass produced 134 requirements, including 70 V0 and 64 later-stage.
ADR-007 adds 24 browser-channel requirements: current total 158, 70 V0 / 88 later.
[Document 28](28-investigation-context.md) defines H0 fields, races and migration.
Documents 28–32 own later-stage bounds for tasks/views, annotations, search/cues,
reports and native transfer. Those limits do not enable a feature in V0 or replace
the original engine/export budgets. Exact source/derivative/report identities and
individual stage gates remain mandatory; selectors in Hunchly are research terms,
not our browser readiness or comparison extraction CSS selectors.

## Browser channel boundary

ADR-007/documents 34–38 select optional post-V0 B0/B1/B2. V0 server capture and
all parameters above remain unchanged. Browser limits are authoritative in 35–37:
15min credentials, 1 MiB chunks, 48 MiB submission, PNG 10 MiB/10Mpx, MHTML 32 MiB,
100 MiB/20-item local spool, 24h pending expiry and one-tab 30min assisted sessions.
These smaller channel-specific caps never silently truncate larger valid V0 evidence.
Native browser allocation/fidelity and exact supported versions remain EWP-41 gates.
