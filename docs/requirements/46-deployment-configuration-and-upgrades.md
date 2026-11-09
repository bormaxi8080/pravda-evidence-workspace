# Deployment configuration, installation and upgrade contract

Date: 2026-11-09. Status: **target procedures, not executable deployment instructions**.
Owner: deployment/backend/operator. Authority: ADR-009. Refines REQ-OPS-001–005,
REQ-API-006, REQ-EXT-004/005 and effective feature state in document 42.

## Environment profiles and configuration precedence

| Environment | Data/credentials and network | Allowed claim |
| --- | --- | --- |
| Local development | Synthetic isolated data; loopback-only debug ports; separate fake/provider test credentials | Developer behavior, never pilot security/readiness |
| Qualification | Exact candidate images/contracts, synthetic fixtures, controlled targets and test identity; enforced isolation | Measured evidence for named tests/environment, no real investigations/public deployment |
| Controlled pilot | Qualified supported bundle, real TLS/admission/backup/operator; only explicitly enabled capabilities | Bounded pilot with known limitations, not production merely by label |
| Production baseline | All mandatory concept/format/security/recovery/pilot gates and separately authorized release | Supported recorded scope/build/environment only |

Never share DB/artifact/temp/secret paths, Compose project names, OAuth callback
registrations or companion development IDs across these profiles. Qualification
mode cannot be enabled by an HTTP header/user role or point at production storage.

One validated settings schema defines types/defaults/source precedence: base safe
defaults -> explicit environment profile -> operator nonsecret config -> service-scoped
secret files. Unknown keys/conflicting duplicate sources fail before admission.
Environment overrides are allowlisted; secret material cannot fall back to an old
development literal. Effective status shows redacted value/source/policy revisions,
never resolved secret bodies. No remote fetched executable configuration.

## Configuration groups to materialize

| Group | Required values/validation |
| --- | --- |
| Identity/origin | Canonical HTTPS host, trusted proxy addresses, exact OAuth callback/admission policy, secure cookie settings; reject empty allowlists/default secrets |
| Data | Explicit DB DSN secret reference; separate accepted artifact/temp/cache/quarantine/ledger locations, ownership and same-filesystem promotion |
| Runtime | Fixed image digests/job templates, launcher identity, network policy, finite per-service and shared reservations/limits |
| DB/schema | Supported PostgreSQL/schema compatibility, roles/pool budget/timeouts, one-shot migration state |
| Features | Implemented descriptor/version, qualification applicability, requested enablement and default-disabled C/H/B/U stages |
| Publication/exports | Existing private/public/profile policy, no-store, bounded ZIP/PDF availability; no proxy artifact alias |
| Companion | Exact extension IDs/origins and protocol range, intake/profile caps and security epoch, all optional endpoints initially off |
| Maintenance | Backup target/key references/schedule, expected operator, logs/metrics retention and safe incident/restore holds |

Settings names above describe contracts, not already implemented environment variables.
The future checked Compose bundle has role-specific targets, health gates, resources,
mounts and networks; operator secrets/config are generated outside the repository.
Do not commit a plausible production .env containing invented working credentials.

## Clean installation sequence

1. Operator selects supported host/image/config bundle and records its digest,
   schema/profile/contract matrix, TLS/DNS and backup/operator prerequisites.
2. Preflight validates filesystem/reserve, clock, port exposure, network sandbox,
   secret files, role separation, deployment identity and environment isolation.
   Failure preserves a diagnostic hold; it does not launch a reduced-security mode.
3. Initialize fresh private DB/accepted volumes and protected ledger/control state;
   apply schema and role migrations once under operator authority. Reused volume
   discovery is explicit; never silently treat old data as a new install.
4. Bootstrap verified initial admin through the operator procedure, not first-login
   promotion. Start web/controller/scheduler with admissions held and inspect safe
   effective readiness/status.
5. Run synthetic login/private capture/review/export verification and deployed SSRF/
   asset-denial/restart checks. Record outcomes, prove a clean restore, then explicitly
   enable the qualified scope for pilot use. Initial optional features remain disabled.

Document who owns DNS/TLS, admin access, disk capacity and backup keys before handoff.
No sample command in another document substitutes for implementing this sequence.
The selected first pilot uses a maintenance window and one host; no blue/green or
rolling zero-downtime claim is implied by restarting containers.

## Upgrade and rollback sequence

Freeze source/target bundle and contract/schema/support differences. Perform an
isolated rehearsal from representative synthetic backup first; include pending
jobs, publications/revocations, pins/fences, users/grants and installed optional stages.
Confirm free space for old/new images, migration temp and coherent backup.

Enter maintenance, stop new admission, drain/fence runner generations, stop automatic
sends and verify write quiescence. Create and independently verify DB+artifact+
configuration-reference backup; protect separate removal ledger and secret escrow.
Pull/build the exact tested artifacts without automatically replacing running services.
Migrate under the single migrator, start compatible readers/writers, reconcile and
run synthetic smoke/recovery checks before deliberate operator resume.

On failure keep maintenance/serving hold, preserve logs/versions safely and choose
tested forward repair or compatible binary rollback. If a coherent restore is
needed, explicitly account for post-backup writes, rotate sessions/epochs and replay
newer removal/revocation ledger before any serving. An image tag change is not a
database downgrade. Never recover by dropping volumes, disabling constraints or
changing public/private flags en masse.

## Secret, certificate and dependency rotation

Each secret has purpose, owner, storage, consumers, rotation mechanism and recovery
reference. Rotate DB service credentials with tested overlap/reconnect and explicit
DB changes, then remove old authority; changing container environment alone is not
the rotation procedure. Rotate OAuth/session/signing/companion epoch material under
their distinct policies. Public certificate renewal verifies key permissions and
edge reload before expiry; it does not grant extra trusted proxy hosts.

Dependency/base-image/browser patches require build/compatibility/security and
relevant behavior checks with recorded digests. A patched browser can change capture
bytes/fidelity; retain old engine provenance rather than relabel old captures.
Do not auto-update production containers to a moving tag or treat vulnerability
scanner absence as proof of isolation. Preserve tested last-known bundle/backup.

## Scaling boundary

First scale within the measured one-host envelope: tune DB queries/pools/disk,
then qualify additional worker/shared heavy permits. More replicas require durable
leases/events/idempotency and shared limits already in the design, not process-local
authority. Multi-host storage/HA/database failover, external secret managers and
rolling upgrades need separate qualified adapters/procedures; they are not enabled
by this document. EWP-65/66 and OPS-ACC-03/06/08 cover the selected deployment.
