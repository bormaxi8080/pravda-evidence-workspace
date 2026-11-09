# Source watches and durable scheduling requirements

Date: 2026-11-09. Status: **selected C3 design; implementation pending**.
Owner: backend/operations/product. Depends on qualified C1/C2 and V0 recovery/
authorization/egress. Origin: ADR-005; unchanged production availability requirements
remain REQ-JOB-008. Content monitoring is an additional adopted stage.

## Objects and authority

SourceWatch stores ID/source/owner, revision+epoch, state, cadence/window/timezone,
profile revision, next due/last occurrence, selected baseline capture, quotas and
failure state. WatchOccurrence stores unique(watch_id,epoch,due_slot_utc), job/capture/
comparison IDs, lease generation, accepted times, result and skip/pause reasons.
Watch history never replaces Capture history. One accepted complete capture remains
independent evidence, including when derived content is unchanged.

## Requirements

### REQ-MON-001 Explicit opt-in watch creation

Watches shall be disabled/draft by default. Enabling requires an admitted editor/
admin, an eligible source/profile, visible cadence/quota/storage consequences and
expected revision. No URL import/capture/collection action creates an active watch.
The owner must retain capture permission; disabled/revoked owner pauses future
work and fences unaccepted in-flight results under normal capture policy.

### REQ-MON-002 Distinct watch lifecycle

States shall be draft, active, paused_user, paused_policy, paused_quota,
paused_error or archived. Display reason/actor/time and permitted resume action.
User pause never auto-resumes. Quota pause may resume at the configured next UTC
quota period only if still enabled/permitted; error/policy pauses need explicit
correction/resume. Archiving stops new work and preserves old captures/events.

### REQ-MON-003 Durable UTC occurrence identity

Persist due instants in UTC, named IANA timezone for local windows and immutable
schedule revision. Claim/enqueue occurrence and capacity/idempotency atomically,
with at most one pending/running occurrence per watch. Use stable occurrence identity
for retries/restarts. Invalid timezone/config pauses only that watch, never the
entire scheduler. DB time is the shared scheduling clock; log significant clock changes.

### REQ-MON-004 Defined windows, DST and missed-run behavior

Cadence is elapsed UTC time; allowed weekly local windows gate admission. A missing
local hour yields no invented run; a repeated hour does not duplicate a UTC occurrence.
Cross-midnight windows use an explicit start day/duration. After downtime coalesce
missed slots into at most one current eligible occurrence, never a replay storm.
Outside a current window record a skip/next allowed time. Bounded nonnegative jitter
must remain within the window; crossing its end moves to the next allowed slot.

### REQ-MON-005 Shared capacity, fairness and quotas

All automatic captures shall use existing durable jobs, capture slots, SSRF/egress,
deadlines and artifact limits; no separate uncontrolled browser pool. Enforce daily
per-watch/instance quotas before job creation and storage reserve while processing.
Prefer manual admission while preventing indefinite automatic starvation: bounded
fair selection and visible delayed/skipped reasons, no guaranteed instant frequency.
Do not delete old captures or silently lower fidelity to satisfy quota/disk pressure.

### REQ-MON-006 Baseline and comparison transaction

First eligible complete capture in an epoch establishes baseline and internal
baseline-established event without a content-change alert. Each later complete
eligible capture compares with the pinned baseline under the same profile epoch.
Only accepted changed/unchanged comparison can advance baseline to that new capture,
transactionally with occurrence/event state. Incomparable/failed/partial/cancelled
work retains the prior baseline. Stale epoch/lease output can never advance it.

For the first C3 content baseline, eligible additionally means HTTP 2xx, met capture
condition and meaningful supported derived text. A complete 404/blocked/error-page
capture still remains valid preserved evidence, but cannot replace the prior article
baseline. It produces technical/status attention, not a confident article-deletion
or content-change claim; failed comparable occurrences count toward the pause limit.

### REQ-MON-007 Honest error and availability classification

Track target availability, capture completeness and content comparison as separate
outcomes. DNS/timeout/auth block does not prove deletion; 404 may be a complete
capture of an error page and creates a technical/status event before any editorial
claim. Selector failure is not no-change. Repeated failures use bounded backoff;
three consecutive failed occurrences pause_error with safe diagnostic attention.
Successful comparable occurrence resets consecutive failure count, not history.

### REQ-MON-008 Recovery and no unintended publication

Pause/profile edit/archive/cancel and late finalization shall serialize using watch
revision/epoch plus job fencing. Preserve already finalized capture bytes even if
subsequent watch policy changed; reject its use for a newer epoch/baseline/delivery.
Resume is explicit and starts from persisted due/baseline state or declared new epoch,
not from hidden in-memory state. Automatic capture/comparison/alert never approves
review or publishes evidence. Restore keeps watches paused until operator validation.

## Selected first C3 defaults

Default cadence 24h, minimum interval 1h, maximum 20 active watches per installation;
at most 24 admitted occurrences/watch/UTC day and 50 automatic captures/instance/UTC
day. All attempts retain the normal three-attempt maximum and total storage caps;
each new capture admission consumes quota, retries stay within that occurrence's
bounded attempt budget. Jitter up to min(10% interval,300s), scheduler poll 15s.
These are starting configuration requiring actual load/storage tests, not guarantees.

Quota counts are transactional and global, not per scheduler process. A manual
"capture now" stays a manual capture and does not bypass watch quotas by impersonation;
an explicit "check watch now" is a normal occurrence under watch rules. Source history
can become large even on unchanged pages; operators see projected storage and stop
new work safely at reserve. No monitoring-specific automatic evidence retention purge.

## Race examples to qualify

- Worker completes while owner pauses: retained capture stays private; baseline/event
  follows whichever watch revision transition won, with no delivery under stale policy.
- Profile changes while an old comparison runs: old epoch history remains; new epoch
  needs its own complete baseline and suppresses stale source-change notifications.
- Scheduler restarts after a week: no seven-day catch-up burst; one eligible occurrence
  or documented skip is admitted under capacity/window rules.
- One malformed timezone: only that watch pauses; unrelated watches and manual
  captures remain runnable. The scheduler process being alive alone is not readiness.
