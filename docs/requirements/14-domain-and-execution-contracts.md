# Domain, execution and engine contracts

Date: 2026-11-09. Status: **selected design contract; not implemented**.
Owner: backend/capture lead. Refines REQ-DAT-001–008, REQ-JOB-001–007,
REQ-ARC-001–008, REQ-SEC-001–004 and REQ-API-002/004/005.
Use [selected parameters](13-selected-v0-baseline.md); logical names below do not
claim existing DB tables. SQL/machine-readable contract work remains EWP-02/03.

## Data dictionary and constraints

New IDs are UUIDs; retain valid legacy UUID values. All timestamps use PostgreSQL
timestamptz/UTC. Integer revisions start at 1. JSON metadata is bounded by the
owning contract and is never a path for arbitrary unknown fields or executable code.

| Entity | Required fields and constraints | Mutation authority |
| --- | --- | --- |
| Source | id; canonical_url; exact requested URL kept on Capture; unique canonical URL within instance | Capture service; normalization never rewrites original requested value |
| Capture | id, source_id, requester_id, requested_at, options_revision, outcome, selected_attempt_id nullable, profile_id, manifest_sha256 nullable, legacy provenance flag | Capture/finalizer; accepted evidence fields immutable after terminalization |
| Attempt | id, capture_id, job_id, attempt_no, generation, started/finished, deadline, engine/browser/options actuals, error_code, staging_key | Worker under current lease; unique(job_id,attempt_no), immutable finished history |
| Artifact | id, attempt_id/capture_id, kind, storage_key, MIME, size bigint>=0, sha256 64 lowercase hex | Evidence finalizer; unique storage_key and unique(attempt_id,kind,path) |
| EditorialRevision | capture_id, revision, title, note, tag/membership snapshot, actor, timestamp, review state/reason | Editorial service; unique(capture_id,revision); append revisions, current pointer via compare-and-swap |
| Publication | id, capture_id, slug unique, approved_revision, screenshot_artifact_id, public_metadata_json, active/revoked, publisher/time, revoke actor/time | Publication service; partial unique active publication per capture |
| Job | id, type, entity_id, requester_id, status, state_revision, available_at, attempt_count, max_attempts, lease token/generation/expiry, cancel_requested_at, last_error | Job service; claimability index(status,available_at,id); state_revision changes on state mutation, not heartbeat |
| JobEvent | job_id, sequence bigint, kind, timestamp, bounded safe payload | State transaction; unique(job_id,sequence), stable ordering |
| BatchPreview / Row | actor_id, digest, revision, expires_at, parsed rows/errors/duplicate groups | Preview service; immutable input; 1 MiB and row cap |
| Batch / BatchRow | preview/selection digest, actor, row_no, job_id nullable, admission/result state | Batch admission; unique(batch_id,row_no), no duplicate job on confirmation replay |
| Session / OAuthState | token/state digest, browser binding digest, user or flow ID, created/expiry/revoked, permission_revision | Identity service; no raw bearer/state tokens in DB/audit |
| Idempotency | actor_id, operation, key digest, request digest, result resource/status, expiry | Same transaction as business intent; unique actor+operation+key |
| AuditEvent | id, actor/resource/action, UTC time, request_id, safe versioned details, legacy marker | Append only; runtime DB roles cannot UPDATE/DELETE |

Collection membership and capture tags have composite unique keys and FKs. Tag/
collection comparison key is NFC-normalized, stripped and Unicode-casefolded; display
name preserves entered case. Renames conflict on the comparison key. Do not silently
merge historically colliding tags: migration creates an explicit collision report.
Existing referenced users cannot be deleted by routine role administration.
New capture requester is mandatory; imported unknown requester may be null only
with a legacy-import provenance flag and original creator string preserved privately.

Source normalization: lowercase scheme/IDNA host, remove explicit default port and
fragment, preserve path, trailing slash, percent-encoded distinctions and query byte
order/duplicates; empty path becomes `/`. V0 rejects URL credentials, overlength,
non-HTTP(S), non-default ports and invalid host/IP policy. Retain exact requested
string separately, including fragment, as private provenance; no lossy dedupe.

## State transitions and transaction results

| Current job | Trigger/precondition | Next job / capture result |
| --- | --- | --- |
| queued / retry_wait | Due, capacity and enabled requester; claim row + slot | leased; new token/generation/attempt, capture pending |
| leased | Runner accepted exact attempt before deadline | running; durable phase event |
| leased / running | Transient failure, attempts remain, old runner stopped | retry_wait; completed attempt failure retained |
| leased / running | Permanent failure or exhausted attempts | failed; capture partial if useful validated output exists, else failed |
| running | Candidate artifacts meet profile and current lease | finalizing; durable finalization intent |
| finalizing | Promoted inventory verified, current lease, no cancel | completed; capture complete + manifest ref + terminal event/audit atomically |
| queued / retry_wait | Authorized cancel | cancelled; capture cancelled; no future claim |
| leased / running / finalizing | Cancel commits before completion | cancel requested; fence final success, stop runner, then cancelled |
| completed / failed / cancelled | Conflicting state command | No mutation; 409 unless an idempotent replay of the original command |
| Expired leased/running/finalizing | Recovery owns row, inspects runner and finalization intent | Reconcile candidate first; fence old generation, then retry/terminalize; never blind recapture |

PostgreSQL is the transition arbiter. Increment sequence and write audit with the
business transition. Attempt errors do not erase previously validated partial
bytes; partial terminal evidence remains private/read-only with warnings. Manual
retry of terminal captures creates a new linked Capture/Job. Cancelling after
completion cannot retroactively erase the accepted result.

Review transitions: unreviewed -> in_review; in_review -> approved/rejected;
approved/rejected -> in_review by explicit command or editorial edit. Approve requires
complete/integrity-valid evidence and expected editorial revision. Every editorial
change increments revision and invalidates approval for future publication. Existing
public projection is pinned; changing a tag must not silently alter its contents.

## CaptureEngine request/result

Internal authenticated worker-to-runner control contract `capture-engine/1`:

- Request: attempt/job/capture IDs, generation, opaque job-scoped authorization,
  absolute deadline, exact URL, validated capture options, resource caps, temporary
  output namespace and network policy ID. No DB/session/GitHub tokens or final paths.
- Supported conditions: `load`, `networkidle`, `css`, `text`; optional selector/text
  bounded to 1,024 characters. Default viewport 1280x900, locale `en-US`, timezone
  `UTC`; effective values pinned in request and actual provenance. No arbitrary JS,
  authentication cookies, interaction steps, locale inference or engine substitution.
- Result: contract/engine/browser versions, attempt/generation, start/end times,
  requested/final URL and redirects, actual main-document status/filtered headers,
  condition result, bounded warnings/error code, output kind/path/size and runner
  digest hints. Trusted finalizer recomputes hashes; hints never establish integrity.
- Result errors: `target_denied`, `invalid_options`, `navigation_timeout`,
  `condition_timeout`, `browser_failed`, `resource_limit`, `output_incomplete`,
  `cancelled`. Main-document 4xx/5xx with complete artifacts is preserved with status;
  readiness condition failure remains partial, never complete.

Runner output is untrusted: allow only regular files under the job's namespace,
reject symlinks/hardlinks/device files/traversal, validate PNG/MHTML bounds and sizes,
and copy/verify into trusted staging before promotion. Browser cannot mount final
storage or another job's output. Reject late or wrong-generation responses.

## Network design to implement and prove

Browser network namespace may initiate only the policy egress proxy connection.
The proxy permits HTTP/CONNECT on 80/443 for approved public destinations, resolves
and pins a validated public IP per connection while preserving TLS hostname checks,
and rejects internal/reserved/metadata/mixed private DNS targets. New destinations
and redirects are revalidated. Deny direct DNS/TCP/UDP/WebRTC bypass and access to
control-plane services; only established worker control replies are permitted.
Compose attachment alone does not enforce this: EWP-01 must prove actual isolation
mechanics before enabling public-target capture. Failed feasibility reopens ADR-002.

## Batch and events

CSV dialect: UTF-8, optional BOM, comma-separated, double-quote escaping, strict
parser, exact header names `url`, `note`, `tags`; reject duplicate/unknown headers.
Tags cell is a semicolon-separated list, no implicit comma dialect. Parsed rows with
empty URL count and fail validation; blank physical lines ignored by the parser
do not become jobs. Preview reports all row failures without truncation. Confirmation
includes preview ID/revision and selected row numbers; digest pins full ordered input.
Default selection dedupes identical canonical URLs in that preview, with explicit
override to retain intentional repeats. Confirmation reserves all queue capacity
and persists batch/jobs/idempotency/audit in one transaction.

SSE fields: id=`job_uuid:sequence`, event=`state|phase|terminal|reset`, data contains
job ID, sequence, state, safe code/message and timestamp. No secret URL/notes. Missing
or expired replay history yields reset + authoritative snapshot; never fabricate
progress percentage. A 15-second transport heartbeat does not extend a job lease.
Protected streams reauthorize within 30 seconds and bound slow-consumer buffering;
close slow streams with a recoverable status path instead of unlimited memory growth.
