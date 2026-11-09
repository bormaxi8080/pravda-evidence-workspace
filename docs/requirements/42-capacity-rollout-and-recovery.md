# Shared capacity, feature rollout and recovery contracts

Date: 2026-11-09. Status: **selected design limits; unmeasured/unimplemented**.
Owner: backend/deployment/operator. Authority: ADR-008. Refines REQ-SCP-004,
REQ-JOB-001/002/006, REQ-OPS-001–007, REQ-EXT-003/004/005/006,
REQ-BCP-004/005/006, REQ-BLC-005/006. Per-operation limits remain in 13/25/28–37.

## Capacity has one accounting authority

Per-service slots are upper bounds, not permission for all services to consume
their maximum simultaneously. Start with one shared installation-wide heavy-task
permit across capture, parsing/crops, report/export rendering and import validation.
Keep each named service's one-slot ceiling. Increasing aggregate concurrency requires
new host-specific isolation/memory/temp/latency/restore evidence; adding workers does
not multiply configured capacity. This refines the previously independent slot
descriptions without changing immutable evidence profiles or their byte caps.

Small authenticated DB reads/pairing/status and bounded chunk I/O do not take the
heavy permit. They have explicit request/concurrency limits; they are not unlimited
parallel parsers or renderers. C4 network dispatch retains its own one-slot/rate/
deadline and secret/egress policy; it cannot borrow a browser or offline-parser slot.

| Account | Selected rule / authoritative counter |
| --- | --- |
| Pending work | Existing 1,000 total queued/retry_wait/admission reservations; 100 reserved for small explicit URL/export commands, bulk/automatic/derived work combined <=900 |
| Batch CSV | Still <=500 rows with all-or-nothing preview confirmation; bulk cap may reject before the global cap, with explicit capacity reason |
| Upload intent | Reserves one pending-work position and declared byte budget at creation; finalize converts reservation to validation job without double charging |
| Heavy execution | One shared permit plus operation-specific slot/generation; process memory/CPU/temp ceilings must be finite and qualified for the enabled job type |
| Browser quarantine | Existing 1 GiB instance-wide declared/actual/reserved byte bound, upload TTL/per-actor limits; do not multiply by grants/processes |
| Derived cache | Existing shared 1 GiB pinned+unpinned derived-byte budget; count physical blobs once, separately track logical references/pins |
| Export/report/import temporary data | Existing operation limits plus a selected shared 1 GiB temporary-output reservation ceiling; input quarantine and this pool both respect actual disk reserve |
| Companion binary requests | At most two in-flight chunk writes/instance, one/upload; 1 MiB chunk bound and existing 20s deadline |
| Disk safety | Existing reserve max(1 GiB,10% volume) applies to total filesystem pressure; logical pool separation cannot promise the same free bytes to two producers |

Control metadata gets bounded DTO/page/row limits and actual DB/disk monitoring;
it must not become an alternate unlimited content store. Accepted originals still
have no automatic retention deletion. When authoritative retained data fills storage,
stop new work and expose an operator action; never prune evidence to make a quota fit.

Reservation records: owner intent/job, pool, amount, generation, state, acquisition/
expiry and actual consumption. Admission/counter update is transactional, including
concurrent CSV/companion/watch requests. A failed admission releases all acquired
positions/bytes. Expired execution cannot release a permit while its process may
still run: fence, stop/prove absence and reconcile before reuse. Cleanup releases
only the old generation's reservation; late cleanup cannot subtract a successor's.

## Claim fairness and overload semantics

Use a persisted bounded round-robin cursor across runnable classes: interactive,
bulk CSV, derived analysis, transfer/render and automatic watch. Within each class
use due time/ID FIFO; skip empty/ineligible classes without spinning. Core export
requested by a user can be interactive while retaining its full execution budget;
one large batch never creates 500 separate priority overrides. Manual browser
intake validation remains transfer class, not arbitrary client-claimed priority.

Once a heavy job starts it is not preempted by UI traffic; enforce its existing
deadline and cleanup. Fairness bounds claiming opportunities, not wall-clock SLA.
A manual command can wait behind the active bounded operation. Priorities/classes
are assigned server-side from the operation, never a client header. Watch check-now
still obeys watch quotas and cannot impersonate manual capture.

Response/status distinguishes queue_capacity, bulk_capacity, pool_capacity,
storage_reserve, delayed_by_fairness and worker_unavailable. No acknowledged intent
is silently dropped. Outbox capacity denial keeps the valid change event/evidence
and records a no-delivery disposition as already specified; it does not recursively
create unlimited retry jobs. Retry-After and diagnostics must be safe and truthful.

## Effective feature state

Each implemented feature has a descriptor: stable key, contract/profile versions,
required schema migration range, dependency keys, operation/resource policy,
qualification-record applicability and configured enablement. No dynamic executable
code or browser permission can arrive through this descriptor.

Effective states: unsupported, migration_required, unqualified, disabled, dependency_
blocked, capacity_unconfigured, restore_hold, enabled. Enable only when every predicate
passes; operator configuration alone is insufficient. Core diagnostic/read readiness
and task admission readiness remain separate. Authenticated status exposes bounded
safe reason codes, never deployment secrets/raw investigation data.

| Family | Minimum activation boundary |
| --- | --- |
| Core V0 | Implemented compatible schema/identity/private evidence/profile/jobs/storage/isolation and applicable V0 proof |
| C1/C2/C3/C4 | Owning qualified stage; automatic watches/destinations start paused/disabled and require explicit policy enablement |
| H1/H2/H3/H4 | Exact annotation/derivation/search/report/transfer contracts and their owning gates |
| B0 | Qualified pairing/scopes plus core server capture; no local-upload capability implied |
| B1 | Qualified browser profile/intake/private inspection/export/quarantine and B0; public browser publication stays unsupported |
| B2 | Qualified scope/foreground/session lease/consent gate plus B1; no history/background/all-sites capability |
| H/C browser adapter | Its individual owning H/C gate plus B1 and named profile adapter; no need to wait for all other adapters |

Disabling a feature stops its new admissions and automatic actions. Revoke/cancel
unaccepted work explicitly where its safety policy requires; an already accepted
capture is not rewritten/deleted. Existing supported private downloads still need
read authorization/integrity. If a reader is unsafe/unsupported, return unavailable;
do not turn off its integrity check to keep downloads working. Public withdrawal
is an explicit revoke/incident fence, never a side effect of hiding a UI control.

## Ordered rollout, downgrade and restore

1. Freeze source/artifact/schema/profile/descriptor identities; run preflight and
   record which features are implemented, qualified and requested. No planned
   component is activated merely by a design/version number.
2. Rehearse ordered additive schema migration on synthetic old/new state, defaults
   disabled, including enum/profile/channel/source-time/dependency/reservation backfill.
   Backfill unknown historical facts as unknown, never successful work or approval.
3. Introduce compatible readers before writers when mixed versions are supported.
   Otherwise use maintenance/drain; do not allow a half-upgraded writer to emit a
   profile an active reader falsely treats as the old one.
4. Execute exact fixture/gate evidence in an isolated environment. Enable only the
   selected feature/dependencies, observe safe diagnostics and record operator action.
   Schema compatibility or a green metadata test is not feature qualification.
5. On failure disable admissions, fence/drain writers and keep evidence intact.
   Roll back binaries only if the old reader/writer contract supports all committed
   data. Otherwise use the documented forward fix or coherent backup restore,
   explicitly recording any lost post-backup writes. No generic destructive down-migration.

Qualification records name fixture/command/outcome, source/artifact/contract/security
policy/environment identities and limitations. Applicability follows the affected
binary/dependency/contract/environment closure, not an unrelated documentation-only
commit. An old passing record is not proof of a changed parser/browser/egress policy.

Restore defaults to no protected serving/outbound/automatic admission until the
removal ledger, integrity, authority, schema and reservation reconciliation passes.
Rotate companion security epoch and invalidate web sessions/pairings. Reconstruct
reserved bytes from existing verified namespaces/DB intent; missing temporary bytes
make pending work interrupted, not completed. Never replay restored outbox/watch/
browser uploads automatically. Separate deliberate resume decisions by family.

V0 uses only core counters, descriptor subset and actual capture/export/removal
paths. Unknown future features stay unsupported. SYS-ACC-05–09 in document 43
cover shared admission, migration/restore and compatibility; measured host capacity
remains pending, not a new invented uptime/RPO/RTO claim.

## First qualification without a readiness cycle

A candidate can be exercised in an explicit isolated qualification deployment before
its production evidence record exists. The operator/test harness selects the exact
candidate build, synthetic fixture namespace/accounts, fixed controlled targets and
network/resource policy. This is a startup/deployment mode, never a request header,
web-admin shortcut or bearer scope that can unlock an ordinary installation.

The deployment advertises qualification_only/unqualified, cannot use real investigation
storage/production secrets or public publication/outbound destinations, and cannot
claim pilot/production readiness. Existing security/integrity/resource controls still
apply; tests target the actual services/process boundaries and cannot waive them.
Failure to establish isolation/fixture-only scope aborts qualification startup.

After recording the real results and applicability review, normal deployment still
needs its explicit configuration/compatibility/restore checks before effective
feature enablement. Importing a passing-looking JSON report alone cannot grant a
feature; the operator validates provenance/applicability. An ordinary service never
self-promotes because a test process wrote a success flag. EWP-59 provides the
rehearsal framework; each owning stage supplies its candidate and required cases.
