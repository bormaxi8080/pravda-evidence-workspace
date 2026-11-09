# Adopted extension contracts, capacity and operations

Date: 2026-11-09. Status: **selected staged interface design; not implemented**.
Owner: backend/evidence/operations. Applies only when C1/C2/C3/C4 starts. Existing
V0 profile/API contracts remain stable. No schema/OpenAPI file or runtime component
is created by this prose contract. Authority: ADR-005 and requirements 21–24.

## Requirements

### REQ-EXT-001 Separate versioned internal contracts

Define typed bounded DTOs/profile/result schemas before each stage's implementation;
same-origin sessions, CSRF, idempotency, revision checks and safe errors reuse V0
services. Unknown contract versions fail explicitly. Every derived read checks
current access and input integrity. No public comparison/watch/attention/delivery
API or implicit publication endpoint is introduced.

### REQ-EXT-002 Dependency graph and derived storage authority

Persist references from representations/runs/events/delivery intents to exact input
artifacts, profile revisions and epochs. Original captures remain immutable and
independently exportable. Derived storage is private under separate namespaces;
cache hash never substitutes for original evidence hash. Corruption, emergency
purge and missing input invalidate dependent outputs and queued sends before reuse.
Retain safe tombstones where needed to explain history, not misleading working links.

### REQ-EXT-003 Bounded resource admission and fair scheduling

Each job type shall declare CPU/memory/time/input/output/temp limits and a durable
installation-wide slot policy. Share no unlimited pools or per-process-only quota.
The existing installation-wide pending-job admission cap applies across new job
types; an extension cannot obtain a separate unlimited queue. C4 also caps unsent
outbox intents at 1,000, with explicit delivery-capacity disposition on overflow.
Protect manual capture and existing archive reads from analysis/watch/delivery load;
show delayed/skipped/rate-limited reason. Resource-limit output is explicit failure,
never silent successful truncation. Test disk reserve and payload/parser bounds.

### REQ-EXT-004 Additive migration and disabled rollout

Introduce extension tables/contract versions with ordered migrations and rehearsal.
Old captures and review/publication retain identity and interpretation; do not
invent historical comparisons, notifications or automatic watches. Start each new
feature disabled until its gate passes and an admin enables it. Backward compatibility
and rollback bounds are documented per schema/producer-consumer change; deployment
version alone is not a data migration.

### REQ-EXT-005 Recovery and retention with explicit input loss

Back up original artifacts plus extension authoritative state, pinned profiles and
dependency records. Cached derived bytes may be rebuilt only from preserved inputs
and supported versions; record rebuild as the same verified computation or a new
analysis when versions differ. Restore pauses watches/sends, revokes sessions and
applies deletion/revocation ledger before enablement. Cache expiry does not erase
capture history, event acknowledgement or delivery disposition.

### REQ-EXT-006 Complete observability and stage qualification

Expose safe metrics for analysis failure/cache hit/limits, watch lag/quota/pause,
baseline epoch, personal attention state and delivery accepted/failed/uncertain/
expired outcomes. No raw source text/rules/credentials in general logs or public
metrics. Each stage has happy/denied/limit/race/crash/restore evidence before enablement.
Core V0/production security/format/recovery gates remain independent and cannot be
declared passed by extension schema/tests alone.

## Stage-specific API inventory

| Stage / operation | Selected input and output | Consequential failure |
| --- | --- | --- |
| C0 GET `/api/v1/sources/{id}/captures` | Existing bound cursor/limit; safe capture history | 401/403/404; no mutation/implicit ack |
| C1 POST `/api/v1/comparisons` | left_capture_id, right_capture_id, profile_revision_id/options, Idempotency-Key -> 202 run/job IDs | 409 no_baseline/incompatible inputs; 422 unsupported profile/options |
| C1 GET `/comparisons/{id}`, `/result` | Current state, exact input refs/profile and bounded escaped result | 409 pending/incomparable; 410 derived_output_expired; no raw archived HTML |
| C1 POST `/comparisons/{id}/rebuild` | Exact key/version still available, key -> existing verified result or bounded rebuild job | Unsupported extractor/input purged/integrity denied; no automatic live fetch |
| C2 POST `/comparison-profiles`, `/comparison-profiles/{id}/revisions` | Bounded effective rules, expected_revision -> immutable revision/fingerprint | Rule syntax/complexity rejection, 409 revision conflict |
| C2 POST `/comparison-profile-previews` | Exact revision and stored capture IDs -> job/preview with raw/filtered text and warnings | selector_missing/empty_result/resource_limit explicitly incomparable |
| C2 GET `/attention`; POST `/attention/{event_id}/acknowledge` or `/reopen` | Current user's list/state, idempotent explicit command | No permissions/state leak; GET never marks seen |
| C3 POST/PATCH `/source-watches/{id}`; POST `/enable`, `/pause`, `/resume`, `/archive` | Source/owner/profile/cadence/window/quota + expected_revision -> state/epoch/next_due | 409 stale revision, 422 invalid timezone/limits, 429 capacity |
| C3 POST `/source-watches/{id}/check-now` | Explicit normal occurrence under quota, key -> occurrence/job | Not unrestricted manual bypass, coalesces existing occurrence |
| C3 GET `/source-watches/{id}/occurrences` | Bounded durable result/skip/pause history | No fabricated stability from missing/failed run |
| C4 POST/PATCH `/notification-destinations/{id}`; POST `/enable` or `/revoke` | Admin-safe destination/payload policy + secret reference, expected_revision | No secret echo or unapproved URL/redirect/private target |
| C4 POST `/source-watches/{id}/notification-bindings` | Admin-approved destination/policy + owner opt-in, expected watch revision | Authorization/disclosure denied; no automatic send |
| C4 GET `/notification-deliveries`; POST `/{id}/replay` | Admin-safe attempts/disposition, explicit reviewed replay -> linked intent | uncertain/policy revoked/expired; no silent duplicate-risk replay |

All paths after the first row share `/api/v1`. Resource create/list operations use
collection path (POST `/source-watches`, POST `/notification-destinations`); PATCH
requires an existing ID. No personal attention record is created by viewing a GET.
Protected input/result/download serving uses the same authorization/no-store rules.

C2 POST `/comparisons/{id}/attention-events` explicitly saves a selected run to
internal attention with an idempotency key; it does not publish or send externally.
The event is unique for the logical save of that run, and reanalysis creates a
different run only when the full analysis key changes.

All admitted users can read shared authorized source/run/profile/event history;
profile/watch mutation is owner-or-admin, acknowledgement is current-user-only,
destination management is admin-only and watch binding needs owner/admin plus
approved destination policy. Admin ownership transfer pauses automatic work and
increments epoch until the new owner explicitly resumes under current permissions.
Secret/delivery diagnostics are admin-only. Shared collection membership grants no
extra transport/disclosure permission.

Idempotency hashes the canonical client request and stores the first resolved
default/profile snapshot with intent. Replays return that stored result without
re-resolving a changed instance default; a different client payload under the same
key conflicts. Deterministic derived bytes exclude compute timestamps (stored on
run metadata), so same-key rebuild must match its prior expected digest or report
non-determinism; it cannot overwrite an old digest as if nothing changed.

## Selected initial extension limits

| Scope | Selected default to qualify |
| --- | --- |
| C1 offline MHTML input | 16 MiB/input, 20 MiB total decoded MIME content/input, 1,000 parts, nesting depth 64 |
| Derived text | 2 MiB UTF-8/input, no silent truncation |
| Diff result | 8 MiB, 10,000 changed segments, 3 context lines default, 10 max |
| Analysis worker | One slot, 30s/job, 512 MiB memory, 128 MiB temp; no network |
| C2 profiles | At most 100 active profiles, 8 include/exclude selector entries total, 100 literal-ignore lines of at most 256 chars |
| CSS subset | Element names, class/ID, descendant/child combinators; no dynamic pseudo-classes, functions or network/executable queries |
| Derived output cache | 30 days default, 1 GiB instance cap with bounded least-recently-used eviction of unpinned cache bytes only |
| Source history / inbox / occurrences | Existing 25 default / 100 maximum paging, bounded stable cursor |
| C3 watch cadence/quota | Document 23: 24h default/1h minimum; 20 active watches, 24/watch/day, 50 automatic captures/instance/day |
| C4 payload/retry/rates | Document 24 is authoritative; one dispatch slot, finite TTL and attempt budget |

Large valid V0 captures may exceed the smaller C1 parsing budget. Show a supported-
input limit error without invalidating the original capture/export. Cache eviction
never deletes original captures, immutable profiles, run metadata, accepted events
or delivery audit. Protected comparisons held by an investigation may pin output;
if pinned bytes fill capacity, deny new analysis rather than erase a hold.

## Migration and rollout sequence

C1 adds derived representations/runs/dependencies and a built-in immutable base
profile. C2 adds profile revisions and per-user attention; C3 adds watch/epoch/
occurrence/baseline state with all watches initially draft; C4 adds destination/
binding/outbox/delivery records with all destinations disabled. Backfill is limited
to schema references/known source history, not speculative historic content changes.

Restore keeps all automatic work paused. Reconcile completed compare results by
input/output digests, leave unsupported-version output unavailable, and never use
"rebuild" to acquire a now-changed live URL. Re-enable watches/destinations separately
after role, input, network, secret and disclosure review. Do not replay historical
events simply because an application component was upgraded.

## Exports and support

Original capture/export profiles do not grow optional hidden diff/watch payloads.
A future comparison report has its own profile and includes exact input references,
analysis versions/options, caveats and explicit content permission. Initial C1
offers protected screen inspection only; shareable/public diff and derived-report
export need separate acceptance before exposure. No content-bearing notification
is an indirect substitute for that permission.

H3 report profiles in [document 31](31-investigation-reports.md) are investigation
reports with their own evidence/annotation disclosure gate. They do not silently
export C1 diff outputs or C2/C3/C4 definitions/payloads. A shareable comparison-report
profile remains separate work. H1 anchors/H2 runs reuse exact versioned C1 input
references and the bounded derived-data dependency policy; pinned context cannot be
evicted as ordinary cache. Original export inventories remain unchanged.

ADR-008/documents 40–42 refine these existing contracts across all implemented
stages. Per-type budgets are ceilings under one initial shared heavy permit and
a shared reservation authority; pending/byte capacity cannot multiply per worker.
Document 41 owns exact dependency/pin/root-fence semantics. Document 42 owns safe
feature/schema/qualification/restore gates. Existing C1/C2/C3/C4 profile/payload/
algorithm limits and stage requirements remain unchanged.
