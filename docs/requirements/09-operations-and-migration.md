# Operations, migration and recovery requirements

Date: 2026-11-09. Status: **proposed**. Owner: operations/backend lead.
Sources: concept sections 23–26, 29–33; existing Compose/Dockerfile/Nginx,
`main.py`, `config.py` and [source review](../04-current-state.md).
Decisions: DEC-01/02/08/09/10/11. Nothing here asserts a working deployment runbook.

## Deployment baseline to specify

One Linux host, Compose, a qualified PostgreSQL version, filesystem volume and TLS
edge. Existing Compose uses PostgreSQL 16 while README/concept mention 15; select
and pin a tested major in DEC-02 rather than promising both. Pin the tested engine/
browser and Python/dependency builds; no unqualified latest-image compatibility claim.
Document host architecture, storage permissions, temporary space and resource limits.

## Requirements

### REQ-OPS-001 Reproducible installation and secure configuration

Document prerequisites, exact commands, expected health output, volume creation,
OAuth callback setup, allowlists, initial admin and a synthetic first capture.
Configuration validation shall reject default secrets, inconsistent limits and
unsafe bind/network settings for pilot deployment. Keep secrets outside Git/indexes,
avoid leaking them in logs/diagnostics and provide rotation procedures. Resolve the
current package build-backend defect before claiming installability.

### REQ-OPS-002 Automated schema migration and preflight

Replace startup `create_all` as upgrade authority with ordered migrations and
schema compatibility checks. Back up before mutation, rehearse migration against
synthetic prototype fixtures, verify counts/IDs/relationships/bytes/hashes and
produce an anomaly report. Missing legacy artifacts, unknown provenance and old
public links require explicit disposition; migration cannot invent completeness.

### REQ-OPS-003 Consistent backup with a defined capture boundary

V0 may use a documented maintenance window: stop new mutations, drain/cancel/fence
workers, prevent artifact writes, then snapshot DB + finalized bytes + version/
configuration references with a backup inventory/digests. In-flight staging output
is not complete evidence. Encrypt/protect backup copies under operator policy;
do not include plaintext secrets unnecessarily. A DB dump alone is not sufficient.

### REQ-OPS-004 Restore into an isolated clean environment

Verify backup inventory before restore. Restore DB/artifacts together, run schema
compatibility and integrity reconciliation, create fresh secret/session material
as appropriate and invalidate old sessions. Keep publication/egress disabled during
validation so a rehearsal cannot expose old public links or contact real targets.
Verify original capture IDs/digests/relationships, then deliberately enable service.
Record actual restore duration/results; a backup script alone does not pass.

### REQ-OPS-005 Upgrades with honest rollback limits

Define compatible application/schema/profile ranges, preflight, drain, backup,
migrate, deploy, verify and resume steps. On failure do not automatically run unsafe
downgrades; choose rollback from a coherent snapshot or forward recovery according
to the migration contract. Document downtime and changes lost after restore.
Package/product naming/version transition must be settled before a release/tag.

### REQ-OPS-006 Health and minimal operational visibility

Separate liveness from readiness. Readiness shall expose safe dependency status for
DB, writable artifact store, compatible schema, worker heartbeat and engine availability.
Detailed diagnostics are protected. An unavailable worker prevents capture readiness
without implying that archived evidence must become publicly exposed or deleted.
Document whether read-only access remains available during degraded operation.

Logs/metrics shall correlate IDs while redacting sensitive URLs, headers, notes,
tokens and captured content. Track queue age/failures/retries, browser timeouts,
disk/temp usage, integrity findings and backup/restore results; audit is separate.

### REQ-OPS-007 Resource pressure and incident procedures

Define disk-reserve, memory/time/byte/dimension caps and admission response before
pilot use. On pressure, stop new work safely and preserve finalized evidence.
Provide procedures for stuck leases, full disk, corrupt/missing artifacts, compromised
session, unintended publication, failed upgrade and urgent removal. Include who may
act, what state changes, what is audited and how service resumes. No silent deletion
of old captures to recover disk space.

### REQ-OPS-008 Qualification and production operations

V0 shall demonstrate clean install, prototype migration and backup/restore on the
documented test environment. Production shall add scheduled/monitored backup routines,
tested upgrade support, operator/onboarding/disaster runbooks, dependency/container
review and pilot-derived supported limits. Define acceptable data-loss/recovery
objectives and retention only with product/operator agreement and measurements;
this package promises no uptime, throughput or restore-time SLA.

## Legacy mapping work required

Record old table/field/path -> target mapping; preserve or map snapshot/public IDs;
handle invalid roles, incomplete files, queued/in-progress jobs, path relocation and
untrusted legacy absolute paths. Preserve bytes before relocation; refuse path
traversal and do not ingest arbitrary host files. Imported audit history keeps its
origin/unknowns. Never make a data migration public by default.

Acceptance: ACC-01/03/04/05/07/08/09/10/12. Detailed executable commands and validated
container/platform choices are implementation-stage outputs after decisions close.
