# Capture, batch and durable execution requirements

Date: 2026-11-09. Status: **selected execution design; implementation pending**. Owner: capture/backend lead.
Sources: concept sections 8.4–8.6, 11–13, 18, 22, 30;
current `capture.py`, `jobs.py`, `routers/job_routes.py`, `url_monitor.py`.
Decisions: DEC-03, DEC-07, DEC-09. Limits: [prototype scope](01-product-and-prototype.md).

## Workflow

Validate the user's request and admission limits; persist capture intent, job and
audit atomically; claim a short lease; execute outside the transaction; stage and
validate outputs; finalize artifacts and DB state with lease fencing; emit a durable
terminal event. SSE is an observer of this state, never its owner.

Capture outcome vocabulary: `pending`, `complete`, `partial`, `failed`, `cancelled`.
Job states: `queued`, `leased`, `running`, `finalizing`, `retry_wait`, `completed`,
`failed`, `cancelled`. Detailed browser phases are events, not mandatory DB states.
A job is `completed` only when the capture meets its complete profile; exhausted
attempts with useful but incomplete bytes yield capture `partial` and job `failed`.

## Requirements

### REQ-JOB-001 Durable submission and bounded claiming

Persist job/capture request and actor before acknowledging submission. Claims shall
use a transaction with row locking/`SKIP LOCKED` or a demonstrated equivalent.
Store worker identity, lease token/generation and expiry before execution. Poll
the jobs table even when notifications are absent. Enforce queue/concurrency caps
across processes; in-memory counters alone are insufficient.

### REQ-JOB-002 Lease fencing and crash recovery

Heartbeat extends a current lease. Expired work can be recovered after the runner
is stopped or its result is fenced off. Every heartbeat/finalization checks current
lease ownership so a stale worker cannot overwrite a newer attempt. Claiming
transactions shall not hold locks during browser execution. Execution may occur
more than once after failures; only one accepted result may finalize a capture.
Store attempts and recovery reasons instead of promising exactly-once execution.

### REQ-JOB-003 Explicit retries and terminal failures

Classify errors: validation/security denial, unsupported options, timeout/network,
browser crash, resource limit, storage/DB failure and incomplete artifacts. Retry
only eligible transient outcomes, with bounded backoff/jitter and total attempts.
Do not retry SSRF denial or malformed input automatically. Retain safe diagnostics,
attempt history and next retry time. Failed/partial work remains private and cannot
be approved or published as a complete capture.

### REQ-JOB-004 Cancellation with race semantics

Cancellation of queued/retry_wait work shall be durable and prevent later claims.
Running work receives a cancellation request; stop the runner, fence writes and
clean temporary output under the documented policy. Serialize final commit and
cancel: if completion already committed, return a terminal-state conflict; if
cancellation won, no success event or finalized publication may appear afterward.
Disconnecting SSE or closing a browser tab shall not cancel work.

### REQ-JOB-005 Capture conditions and outcome truth

V0 shall support documented lifecycle conditions (`load`, `networkidle`) and bounded
CSS/text conditions retained from the current prototype. Persist the exact requested
condition and its actual result. Preserve final URL, HTTP status, redirects, engine/
browser versions, viewport, locale/timezone, timestamps and warnings. An HTTP 404
page may be captured as evidence if the profile is complete, with status visible;
an empty artifact set must never become successful merely because no exception escaped.
Separate readiness-condition timeout from transport/engine error.

### REQ-JOB-006 Preview-confirm CSV import

Define UTF-8 CSV with required `url`, optional `note`/`tags`, header/case rules,
quoted-field behavior and byte/row limits. Do not silently fall back to unrelated
formats. Preview shall show row number, parse/URL/policy results, duplicate group
and proposed metadata. No jobs exist until explicit confirmation. Confirmation
pins the preview revision/input digest, selections and dedupe policy, then atomically
creates Batch/rows/jobs under queue capacity. Duplicate confirmation is idempotent.
Revalidate DNS/network policy at execution even if preview passed earlier.

Recommended V0 dedupe: flag identical normalized URLs within the batch and select
one by default; let the user deliberately request repeats. Existing captures are
informational matches and do not suppress a deliberate new capture automatically.

### REQ-JOB-007 Durable progress and batch accounting

Persist meaningful state/terminal events with monotonic job-scoped sequence IDs.
Expose current state after reload/reconnect even if all progress events were missed.
Batch counts reconcile with member rows; mixed success/failure/cancellation is
visible and never represented as universal success. Retrying one source must not
reset successful sibling results. Bound event payload size, retention and subscribers.

### REQ-JOB-008 Availability monitoring does not recapture

When monitoring is implemented for production, use bounded HTTP probes under the
same SSRF/egress policy as capture. Record `online`, `redirected`, `deleted`, `blocked`,
`unreachable`, `unknown`, observation time and method. Unsupported HEAD can trigger
a bounded GET. A timeout does not prove deletion; status/header differences do not
prove semantic change. Probe state never modifies prior capture bytes/hashes.
V0 may omit probes and display `unknown / not checked`; it shall not invent status.

## Engine request/result contract to finalize

Input: attempt/correlation IDs, validated target, options, time/byte/dimension limits,
allowed network policy and output staging namespace. Output: actual engine/browser
identity, exact provenance, artifact inventory with sizes, per-condition outcomes,
warnings and structured failure. Credentials and arbitrary host paths are not inputs.

Selected heartbeat/lease/backoff, preview/event retention and engine/CSV/SSE
contracts are in [document 13](13-selected-v0-baseline.md) and
[document 14](14-domain-and-execution-contracts.md). Real recovery/race evidence
remains an implementation obligation. Acceptance: ACC-01/02/03/04/08/11/12.

## Detailed selected design

See [the baseline register](13-selected-v0-baseline.md),
[contracts and operator procedures](README.md) and
[assignable work packages](18-assignable-work-packages.md).
Implementation/qualification remain pending; source presence is not test evidence.
