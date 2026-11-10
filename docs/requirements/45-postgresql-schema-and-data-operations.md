# PostgreSQL schema, integrity and database operations

Date: 2026-11-09. Status: **selected technical refinement; no SQL/migration run**.
Owner: backend/database/operator. Authority: ADR-009. Refines REQ-DAT-001–008,
REQ-ARC-004/006, REQ-JOB-001/002/007, REQ-OPS-002–005 and documents 14/41/42.
Use [primary platform sources](../reference/deployment-and-database-platform-review.md).

## Database boundary and role model

Use one PostgreSQL 16 database per newsroom installation. Exact patched image and
client versions are release-tested/pinned; changing major requires an explicit
upgrade plan. No SQLite fallback, application-created production schema, public
DB port or shared superuser account. Use UTC timestamptz and UTF-8; explicit project
normalization keys remain separate from display strings and filesystem paths.

| DB principal | Selected privileges | Excluded authority |
| --- | --- | --- |
| Schema owner | NOLOGIN owner for application schema/functions | Not an HTTP/process credential |
| Migrator | Temporary operator-managed login, controlled ownership/DDL path | No automatic use by web/worker startup; not shipped to runner |
| Web | Required read/identity/editorial/admission/publication operations | No schema ownership, superuser/BYPASSRLS, audit rewrite, arbitrary final-byte mutation |
| Controller/finalizer | Scoped job/attempt/artifact/finalization writes and required reads | No unrestricted DDL/user administration/audit deletion |
| Scheduler/reconciler | Required due/lease/reservation and safe reconciliation mutations | No credential administration or unrestricted source-content export |
| Backup/maintenance | Explicit operator privileges for the chosen tool/procedure | No browser/normal API credential; secrets separate from ordinary reports |

Runtime login roles cannot create roles/extensions, change schema grants, disable
audit protections or directly rewrite finalized evidence fields. Enforce critical
invariants through FK/unique/check constraints and reviewed triggers/functions where
needed, with fixed search paths and narrow grants. Business authorization still
checks the actual enabled application user; a DB role is not a publisher/admin UI role.
DB/host operators remain trusted, not hidden behind a false tamper-proof claim.

## Schema/data dictionary implementation checklist

Materialize documents 14/41/42 with ordered migrations and constraints:

- Unique canonical Source identity; retain exact submitted URL/provenance unchanged.
- Capture/Attempt/Artifact references, generation/attempt uniqueness and one accepted
  finalization result; no cascading original deletion from tags/collections/users.
- Editorial/triage/annotation revisions with compare-and-swap pointers and durable
  actor/audit; publication slug uniqueness and one active projection/capture.
- Durable queued/leased/retry/finalization state, idempotency result and job-event
  sequence; business mutation/audit/event commit together.
- Exact typed dependency/reverse indexes, pins, removal fences and reservation
  ownership/generation; safe tombstones survive dependent-content cleanup.
- Foreign IDs and unknown legacy facts remain namespaced/unknown. File blobs stay
  in the artifact store, not unbounded JSON/BYTEA diagnostic columns.

Initial useful indexes: Source canonical key; Capture(source_id,requested_at,id);
archive sort/state/time keys matching actual queries; Job(status,available_at,id);
JobEvent(job_id,sequence); unique actor/operation/idempotency digest; active Publication
lookup; reverse DependencyEdge(target identity); active reservation owner/pool.
Validate execution plans with realistic synthetic cardinalities; do not add an
index for every field or treat a tiny seeded DB as performance evidence. Deletion
and retention still follow exact domain policy rather than ORM cascade defaults.

Future U2 adds AccessSpace IDs/composite scope relationships and filtered indexes
only through its migration/gate. RLS may add defense in depth after real bypass/
pool-context tests, but does not replace application/filesystem authorization. V0
does not pretend its shared archive is already row-isolated.

## Connections, transaction and query budgets

Selected initial max_connections=100, three superuser emergency positions plus
seven operator-reserved positions; runtime roles cannot consume those reserves.
Cap all application pools/dedicated listeners combined at 30, with no unlimited
overflow. Example allocation ceiling: two web processes x5, controller5,
scheduler2, reconciler2, two dedicated listeners and diagnostics2 =23, leaving
seven runtime positions for explicitly budgeted services. Replicas cannot silently
multiply pools. Backup/migration/maintenance capacity is separately planned.

Use bounded pool acquisition (5s), the existing 5s lock-wait ceiling, 5s interactive
statement target and 30s short background SQL ceiling; idle-in-transaction timeout
30s. Bulk migration/backup uses explicit maintenance timeouts and measured plans,
not disabled protection on ordinary request roles. No browser/render/parser work
or network call runs while holding a DB transaction/row lock.

SSE does not reserve a pooled SQL connection for every viewer. Dedicated LISTEN
connections use the global budget; NOTIFY remains a wake-up hint and persisted
JobEvent sequence/polling remains authority. Reconnect/retry cannot lose queued work
or repeat business mutation without idempotency/generation checks.

Use consistent lock order for job -> business intent -> reservation/fence resources;
bounded retries only for classified transient serialization/deadlock failures with
original idempotency identity. Permission/validation conflicts are not transient.
Keep fsync/durable commit behavior enabled; do not trade away accepted-evidence
durability to improve a benchmark. Actual durability still depends on tested host storage.

## Migration protocol

1. Inventory source schema/version/data anomalies; dry-run against synthetic legacy
   and current fixtures with accepted artifact hashes and visibility recorded.
2. A single maintenance migrator owns a database-wide migration lock; normal worker
   leases do not serialize DDL. Version/preflight mismatch blocks new writes.
3. Apply reviewed incremental steps, backfill in bounded restart-safe pages, record
   checkpoints/counts/digests and validate constraints before enabling new writers.
   Future identity mapping cannot silently grant restricted data access.
4. Rehearse interruption, lock timeout, duplicate execution, old-reader incompatibility
   and post-backup write loss. Schema migration IDs and package/profile versions
   have different meanings; forward repair or coherent restore is the rollback plan.

No generic down-migration drops original/audit/role history to make an older binary
start. Online DDL/index operations need their own lock/transaction/failure plan; the
normal one-host maintenance window is acceptable until online behavior is qualified.
Migrations create required role/grant configuration declaratively and audit changes,
without embedding passwords in checked SQL or shell arguments.

## Backup, restore and ongoing DB maintenance

V0 uses the quiesced DB-plus-final-artifact backup boundary from document 17, with
selected pg_dump custom archive plus explicit schema/role/grant configuration and
artifact/manifest inventory. The operator records exact tools and exit/warning
results. pg_dump consistency does not capture separate files or global roles.
Restore only a trusted backup under the controlled operator process; an H4 case
file can never become SQL/pg_restore input.

Restore into fresh volumes/database, apply compatible roles/schema, verify counts/
digests/relationships/fences and reset sessions/companion epochs before deliberate
resume. Exclude unfinished quarantine from accepted backup claims. WAL/PITR and
replicas are later operator capabilities requiring artifact/version/ledger alignment;
they do not automatically recover external immutable bytes or deliver an RPO/RTO.

Monitor connection use, long/idle transactions, blocked queries, dead tuples,
autovacuum progress, transaction-age risk, WAL/temp/DB growth, errors and disk/inodes.
Keep autovacuum/statistics maintenance active; reviewed workload tuning is preferable
to blanket disabling. VACUUM FULL/reindex/large maintenance requires explicit impact/
lock/space planning, not an automatic online weekly command. Safe query telemetry
redacts values/URLs/notes; use query fingerprints/aggregate timing where possible.

EWP-63/64 implement these refinements; OPS-ACC-04/05/08 in document 49 require real
PostgreSQL concurrency, grant, backup/restore, maintenance and schema evidence.

Candidate settings within the 2 GiB DB test ceiling: shared_buffers 512 MiB,
work_mem 4 MiB per operation and maintenance_work_mem 128 MiB, with autovacuum
concurrency measured explicitly. These are tuning inputs, not total-memory
guarantees: concurrent queries/plan nodes/connections/background processes consume
additional memory. Retain runtime connection and heavy-task limits; qualify OOM/
connection-loss recovery instead of disabling durability or exhausting host RAM.

## Platform execution policy — 2026-11-10

Implement and test locally on macOS arm64/Docker Desktop under
[document 56](56-macos-development-and-linux-qualification.md). Real local PG,
configuration, recovery and safety checks remain required. Native server/kernel,
Linux installation and target host-loss qualification belong to its later Linux
iteration; they do not block Mac implementation. Keep per-lane evidence and never
claim Linux/production acceptance from local results alone.
