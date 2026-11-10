# Maintenance, observability and recovery service requirements

Date: 2026-11-09. Status: **selected operator design; procedures not implemented/run**.
Owner: operations/security/database. Authority: ADR-009. Refines REQ-OPS-003–008,
REQ-DAT-006/008, REQ-EXT-005/006 and documents 17/41/42/44–46.

## Operator and service responsibility

Name a primary and backup host operator before a sensitive pilot; names/availability
are not assigned by this document. The operator owns host/TLS/DNS, accepted storage,
backups/keys, DB administrative access, patching, emergency containment and recovery.
Workspace admin owns application accounts/publication policy, not host root or the
ability to bypass the restore/removal procedure. Users get editorial status/actions
without a terminal; maintenance remains a bounded operator interface.

This single-host design has no automatic failover or promised uptime/RPO/RTO.
Define measured support windows, tolerated outage/data-loss objectives and escalation
contacts from actual rehearsal/pilot evidence. A process being up, a recent backup
file or a green scanner is not a recovery/service guarantee.

## Selected maintenance schedule to qualify

| Cadence / trigger | Work and safe expected result |
| --- | --- |
| Every 15s recovery scan, existing policy | Inspect expired leases/owned runner state; fence/stop before releasing capacity; no blind duplicate capture |
| Every minute status collection | Safe DB/pool/queue/reservation/disk/runner/egress/expiry gauges; no page bodies or credentials |
| Every 15min | Reconcile expired temporary namespaces/intents and output TTLs in bounded pages, respecting root fences/pins/generations |
| Daily operator review | Backup outcome/age, storage/inodes growth, queue/claim failures, DB vacuum/transaction risk, certificate/key expiry and critical security notices |
| Daily scheduled backup candidate | In a configured maintenance window, quiesced coherent DB+accepted-artifact backup with independent inventory verification; if manual scheduling is used in V0, show schedule not configured |
| Weekly rehearsal candidate | Isolated restore of latest representative backup, source/DB/artifact/fence checks, synthetic private workflow and actual duration/report |
| Monthly / significant change | Access/admin/grant review, supported image/browser/DB/host patch review and bounded full integrity scan progress review |
| After migration/incident/storage change | Full applicable recovery/authorization/egress/integrity qualification before normal resume |

These are selected operational targets to implement/test, not an existing cron
configuration or a contractual SLA. Automatic evidence deletion is never a cleanup
task. A retention window for backups (initial proposal: seven daily plus four weekly
verified sets) requires target capacity/operator approval at deployment, protected
removal-ledger awareness and a preserved known-good set. Pruning never substitutes
for verifying a new backup and never deletes accepted live evidence.

Large installations may not finish a full hash scan in one day. Persist bounded
scan cursors/coverage and verification times; unknown/unscanned is not verified.
Known corruption immediately fences affected operations; safe unaffected archive
reads may remain available under their actual readiness/authority.

## Health and telemetry contract

Keep minimal anonymous liveness/readiness separate from authenticated diagnostics.
Dimensions: read_ready, capture_ready, intake_ready, outbound_ready, maintenance/
restore_hold and effective enabled feature versions. No secret filesystem paths,
SQL/provider bodies or source URLs in anonymous health.

Metrics: oldest runnable queue age by class, claim/lease expiry, operation duration/
resource failure, accepted/partial/failed counts, reserved/actual pool bytes, disk/
inode headroom, orphan temp age, DB connections/locks/transaction age, backup age/
verification, restore rehearsal age, and grant/certificate/credential expiry where
safe. Use bounded labels/classification; capture/user/source IDs are not metric
labels, and URL/query/annotation text is not log context.

Logs carry request/job/attempt/generation and safe reason references under access-
controlled retention. Initial ordinary log retention target is 14 days with rotation/
size caps, distinct from authoritative audit/terminal history and protected removal
ledger. A future support bundle is explicit operator output: redacted config/image/
schema/feature/metric summaries, bounded logs and checksums, no original evidence,
DB dump, tokens, full user directory or secret files by default. Review before
sharing; documentation does not authorize sending it anywhere.

## Alert and incident matrix

| Signal / initial threshold | Required disposition and operator action |
| --- | --- |
| Disk at existing reserve or inode exhaustion | Deny new writes/admission safely, preserve old bytes; inspect pool/orphan/backup consumption without deleting evidence |
| Oldest due interactive job >5min or no worker heartbeat >2 leases | Mark degraded, inspect active process/generation/capacity; no duplicate worker storm or unbounded queue growth |
| DB unavailable/schema mismatch | Deny dependent reads/writes; expose safe readiness; restore connectivity/compatible schema, never grant cached access |
| Required original digest mismatch | Immediate affected root/integrity fence; retain expected hash/finding, compare matching backup under incident procedure |
| Expected daily backup absent/unverified >26h | Mark recovery degraded and escalate; never silently claim a valid daily schedule when none configured |
| Restore rehearsal absent >8 days when weekly policy enabled | Mark unqualified recovery coverage, schedule isolated rehearsal; do not invent passed restore from backup success |
| TLS expiry <14 days / failed renewal | Operator renewal/reload check with explicit error; do not bypass HTTPS/cookie policy |
| Suspected account/credential compromise | Disable/revoke relevant principals/grants, rotate affected purpose-specific credentials, inspect safe audit and disclosure scope |
| Unintended publication/outbound | Revoke server path/binding immediately, retain actual remote acceptance/uncertainty; state external-copy limit |

Thresholds are qualification defaults, not promises of continuous staffed response.
Initial notification is protected in-app/operator diagnostics plus an explicitly
configured independent host-monitor path. No automatic C4 destination/email/third-party
account is created; the service must diagnose its own broken outbound subsystem.

## Backup/restore and disaster drill dossier

For each backup record source bundle/schema/profile/config-reference identity,
maintenance/quiescence evidence, DB/archive tool identity, accepted byte inventory,
safe role/grant reconstruction, creation/verification time, protected target and
separate key/ledger recovery references. A same-host copy is insufficient against
host loss; qualify at least one independent protected target. Encryption/key escrow
is an operator deployment policy, never a key stored beside ciphertext in the same
unprotected export. Restore from untrusted foreign SQL is prohibited.

Drill into isolated new host/volumes with external serving/capture/sends held. Prove
restore with source unavailable, artifact counts/hashes, DB relationships/revisions/
scope, current removal ledger, new security epoch/session invalidation and explicit
resume. Record actual elapsed time and recoverable point, missing post-backup writes,
temporary uploads not restored and external-copy limits. Do not declare RTO/RPO
achieved without that exact evidence and stated failure scenario.

Runbooks cover full disk, DB crash/corruption, lost host/key, orphaned runner,
incompatible migration, credential compromise, accidental public disclosure and
operator absence. Each has stop/contain/diagnose/recover/verify/resume steps and
required authority. No daemon-global prune, volume deletion, audit erasure or
restoring stale grants is an acceptable generic fix. EWP-67/68 and OPS-ACC-07/08
materialize and qualify these procedures before claiming supported operations.

## Platform execution policy — 2026-11-10

Implement and test locally on macOS arm64/Docker Desktop under
[document 56](56-macos-development-and-linux-qualification.md). Real local PG,
configuration, recovery and safety checks remain required. Native server/kernel,
Linux installation and target host-loss qualification belong to its later Linux
iteration; they do not block Mac implementation. Keep per-lane evidence and never
claim Linux/production acceptance from local results alone.
