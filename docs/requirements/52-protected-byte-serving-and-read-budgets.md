# Protected byte serving, snapshots and read resource budgets

Date: 2026-11-09. Status: **selected existing-contract refinement; unimplemented**.
Owner: application/evidence/security/deployment. Authority: ADR-010. Refines
REQ-ARC-005/006, REQ-EVD-004/008, REQ-SEC-002/006/007, REQ-API-005,
REQ-EXT-003 and the pre-success verification rule in document 15. Core V0 implements
its actual supported-artifact subset; production/U/H/B adapters remain stage-specific.

## Byte authority and read phases

All screenshot/raw artifact/export/report routes use one protected read service.
Input is a resource ID and named action, never an unchecked storage key/hash/path
from the caller. Resolve current principal/resource/publication/scope policy first;
private missing/foreign/revoked remains generic denial. Public assets require an
active exact publication projection, not a capture ID or former publisher's session.

1. Authorize and resolve immutable expected artifact/profile/size/hash plus current
   root/dependency/permission/publication revisions. Reject known corruption/removal.
2. Reserve bounded read validation/snapshot and transfer capacity before touching
   large bytes. Open only the trusted regular file with no-follow/path containment.
3. Copy/stream into a private bounded immutable read snapshot and compute size/hash
   before sending success headers. A mismatch or interrupted copy is an explicit
   integrity/error state, not a partly successful 200 response.
4. Reauthorize/recheck exact resource/fences after validation and just before headers.
   If revocation/removal won meanwhile, discard snapshot and deny; a prior allowed
   check or copied file is not continuing authority.
5. Serve the verified snapshot under a transfer lease, retaining its file handle
   and byte reservation. Release compute/DB locks before slow network transfer.
6. On completion/disconnect/expiry/revoke, close/release only this lease generation;
   bounded cleanup cannot erase a snapshot still used by another live authorized lease.

The snapshot is a private derivative with exact input dependency, expected/actual
digest, creation/expiry and lease reference. It cannot outlive a root removal fence
for serving. Do not substitute a mutable source path after verifying a different
file. Accepted storage remains protected, but file existence, old hash metadata
or an HTTP cache validator alone is not verification of newly served bytes.

## Shared accounting and deadlock prevention

Selected initial limits: two active transfer leases/instance, one new large validation
at a time, 512 MiB aggregate read snapshots, max 512 MiB one result, 60s validation
deadline, 5min transfer deadline and 30s client-idle timeout. Actual package/artifact
caps may be smaller. Account read snapshots in the existing shared 1 GiB temporary
pool; this is not a fresh unlimited cache. Unknown/freed reservation does not imply
physical disk is available; existing disk/inode reserve still applies.

Large copy/hash uses the shared heavy permit and declared job resource ceiling;
release it after verification/before streaming. Small screenshots can use the same
bounded path, never unlimited synchronous decoders. If resources are unavailable,
return a safe capacity/unavailable result or explicit async preparation status;
no anonymous request creates unlimited durable work or evicts protected evidence.

Generators must not wait for another heavy permit while retaining their own: stop/
prove absence of the previous process before phase transfer, or execute successive
bounded phases under the same parent reservation/generation. A renderer waiting on
an export download validator cannot deadlock the sole heavy slot. Reserve actual
spool bytes once with exact ownership; duplicate logical refs do not double-release.

Read-ready reuse requires exact immutable input digest plus current authority/fences
and a still-live owned snapshot. It is an optimization to qualify, not a metadata-only
shortcut over unknown/mutated bytes. External/shared cache URLs and public object-store
redirects are not selected. Corrupt/removed bytes never become a ready snapshot by
retrying from the live source or matching another source URL.

## Revocation, headers and slow streams

Recheck enabled principal, expiry, current permission/scope and root/publication
fences at most every 5s and before each bounded 64 KiB application chunk. Stop
on denial. New requests after committed public revocation/removal deny before
headers; an already started transfer may have emitted bytes which cannot be recalled.
Record that limit honestly, including transport/proxy buffers; never promise erasing
recipient copies or instantaneous remote revocation.

Do not hold a DB connection/transaction for the transfer. Authorization checks are
short bounded service calls and slow-client/backpressure occupies only its declared
transfer/file resources. Configure actual edge buffering/timeouts with the contract;
no alternate Nginx raw artifact alias/sendfile path bypasses checks.

Send exact Content-Length, fixed validated Content-Type, safe generated filename,
attachment for raw archives/PDF/packages, nosniff and no-store. Screenshot inline
access is only the authorized UI/public projection. Do not execute receipt/archive
HTML in the app origin. No user-supplied MIME/filename/response header interpolation.

First contract supports whole-file GET and metadata HEAD. It does not advertise
resumable ranges; Range may be ignored with a complete authorized 200 and
Accept-Ranges:none, never a partial-hash verification shortcut. Conditional requests
are processed only after authorization; no 304/HEAD/error path leaks private existence
or bypasses known integrity/removal checks. Precise HTTP implementation and old-client
compatibility are EWP-77 negative fixtures, not a claim that all headers work today.

## Crash and removal outcomes

| Boundary/failure | Required result |
| --- | --- |
| Before validation completes | No byte-success headers; safe error/capacity state and bounded orphan cleanup |
| File/path changed during validation | Expected/actual mismatch or descriptor failure; quarantine finding, no fallback file |
| Root/publication/permission changes after copy | Pre-header recheck denies; dependent snapshot cannot grant access |
| Revoke during transfer | Stop at next bounded check; preserve actual bytes-served/denial diagnostic without pretending recall |
| Client stalls/disconnects | Bounded timeout and lease release; no heavy permit/transaction held until client resumes |
| Worker/web restart | Reconcile live lease/snapshot generations; expired unserved snapshots are temp, not accepted evidence |
| Clean restore | Do not restore old transfer authority; ledger/epoch/permission checks precede new reads |

Audit safe action/resource/generation/outcome/byte counts where applicable; never
body, bearer, source query or raw storage path. Public throttling uses bounded safe
counters and no user-tracking body metadata. PRD-ACC-07/SYS removal cases qualify
actual pre-header, stream, resource and proxy behavior; no HTTP/IO test ran here.

Operational read reservation/audit/cache bookkeeping is not editorial mutation:
GET never captures, acknowledges attention, approves, publishes or changes user
context. HEAD returns only authorized bounded metadata/current known integrity
state; it does not claim newly verified content without a byte check. Logs define
byte counts as emitted to the server transport, not proof of remote receipt/read.
Internal export/renderer input verification reuses the authorized parent reservation/
phase service, never a loopback HTTP download or a nested heavy-permit request.
