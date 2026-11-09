# ADR-004: Select durable execution, storage and session contracts

Date: 2026-11-09. Status: **selected engineering baseline; qualification pending**.
Covers DEC-07/08/09/10/11. Definitions are in requirements documents 13–17.

## Decision

Use PostgreSQL row claims with lease tokens/generations, bounded heartbeat/retry,
polling and durable state/event history. NOTIFY is an optimization only. Fence
stale finalization, serialize cancel versus completion, and reconcile ambiguous
commit outcomes before starting a fresh browser attempt. Execution is at-least-once;
only one accepted result may complete a capture.

Use per-attempt staging and immutable generation-specific final directories on
the same filesystem. Persist a finalization intent, validate/copy output, atomically
promote, then commit under current lease. Reconcile any DB/filesystem split. Do not
let a stale worker overwrite the path selected by a completed capture.

Select durable opaque sessions stored as digests, explicit expiry/revocation and
fail-closed GitHub admission. OAuth state binds to the initiating browser and is
single-use/expiring; a server dictionary of unbound state strings is insufficient.
Queued work and protected streams observe disabled users and revoked permissions.

Retain legacy capture IDs where valid; migrate publication flags into explicit
review-required legacy records. Old public URLs resolve only to approved mappings.
During maintenance show safe temporary unavailability; after cutover unreviewed
legacy public links remain unavailable with an operator report. Do not automatically
publish legacy data, silently break links without a migration report, or claim that
old cached third-party responses can be purged by the migration.

V0 backup uses a quiesced DB+artifact boundary and isolated restore rehearsal.
Operator emergency purge has an explicit report/tombstone and backup re-deletion
procedure. Normal UI archival never purges bytes.

## Alternatives and consequences

In-memory queue/session authority fails restart and multi-process requirements.
Exactly-once browser execution is not promised by SQL locking. Uncoordinated live
DB dumps miss filesystem consistency. Automatically preserving every legacy public
flag conflicts with new disclosure review. Conservative link suspension is a
documented compatibility change accompanying the future package major increment.

## Verification obligations

EWP-01/03/04/05/06/07/08/13/14 must test real DB races, external runner cancellation,
bounded resources, safe legacy path handling, session/role changes and clean restore.
Selected limits are starting configuration, not proven safe throughput or an SLA.
