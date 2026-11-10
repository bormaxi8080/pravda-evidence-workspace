# Migration and operations design playbook

Date: 2026-11-09. Status: **target procedures specified; commands not implemented or run**.
Owner: operations/backend. Refines REQ-OPS-001–008, REQ-DAT-006/007/008 and
REQ-API-006. All target `workspace-admin` commands below are proposed interfaces
to implement in EWP-13/14, not instructions that work in the current checkout.

## Environment and permissions

Current development target: macOS arm64, Python 3.12, PG16 and Docker Desktop,
with private owned local DB/worker/runner services and storage. Follow
[document 56](56-macos-development-and-linux-qualification.md) and the
[Mac runbook](../operations/macos-development.md). Native Linux x86_64/Ubuntu 24.04,
server TLS and clean-target recovery qualification belong to the later Linux iteration.
The build task pins exact dependency/Chromium/image digests and proves installability.
The current Dockerfile/pyproject are not an accepted production build. Dev-only
local HTTP is explicitly labeled and cannot enable a pilot config with insecure cookies.

Web reads finalized artifacts through authorization; only trusted finalizer writes
final namespaces; browser sees job-local temp output only. Host operator controls
backup/secrets/purge, independently of UI admin. Runtime DB roles have least
privilege and no audit UPDATE/DELETE. Migration role is distinct and not shipped
to browser/request execution. Secret files are readable only by the relevant service.

## Legacy mapping and anomaly disposition

| Existing object | Target mapping | Required handling |
| --- | --- | --- |
| User.github_id/login/role | User provider_id/current_login/enabled/permission revision | Keep IDs where valid; verify role enum/collisions, disabled default for invalid identities |
| Process-local sessions/state | No reliable exportable authority | Invalidate all legacy sessions/state; require fresh login |
| Snapshot ID/URL/timestamps/creator | Capture + Source + imported attempt/provenance | Keep valid UUID; map invalid/colliding IDs; retain exact original URL/time/creator string with unknown markers |
| mhtml_path / screenshot_path | Validated Artifact keys under import namespace | Restrict paths to approved source data root, reject links/traversal, copy bytes then compare digests |
| mhtml_sha256 | Original claimed digest plus newly computed actual digest | Mismatch is quarantined anomaly; never overwrite original claim as if it matched |
| Snapshot note/tags/collections | Editorial revision and memberships | Preserve context; report normalized key collisions before choosing merges |
| is_public | Legacy publication candidate + old-URL mapping | Require admin disclosure/review confirmation; no automatic active Publication |
| Job queued/capturing/done/error | Imported Job/Attempt/history | Pending work cancelled with migration reason by default; no implicit fresh Internet capture during cutover |
| AuditLog | Imported immutable AuditEvent with provenance | Preserve original payload privately with safe projection; do not invent absent user/job events |
| UrlCheck/status | Imported dated OriginObservation | Missing time stays unknown; old status is not current availability |

Historical captures lacking real engine details, complete artifacts or profile data
use `workspace-legacy-import/1`, never `workspace-capture-v0/1`. It is read-only,
explicitly incomplete/unknown where appropriate, preserves original file digests
and gets an import manifest separate from original provenance. Future complete
recapture creates a new Capture. No new success profile is fabricated by migration.
Unqualified legacy-import records are not eligible for new public publication in
V0. An old-link mapping may point to an explicitly reviewed new eligible capture;
it must not relabel old bytes to bypass the profile gate. The migration report
identifies suspended links and required operator/editorial actions before cutover.

## Procedure A: preflight and migration rehearsal

1. Freeze the source commit/config identifiers and restrict input to synthetic
   fixtures initially. Inventory DB tables/rows, artifact count/bytes/digests and old links.
2. `workspace-admin migration inspect --source ... --report ...` performs bounded
   read-only inventory; expected report lists versions, missing/corrupt files, ID/
   normalized-name/path collisions and publication candidates. Any silent omission fails.
3. Copy DB + bytes into an isolated rehearsal environment, with runner egress,
   publication and provider login disabled. Import/migrate with the reviewed mapping.
4. Compare counts, ID mappings, file byte hashes, memberships/audit and visibility.
   Quarantine anomalies and record disposition; do not erase the original evidence.
5. Rehearse restore/abort before live cutover. Exit: zero unexplained loss, compatible
   schema, safe legacy links and a signed-off operator anomaly report still to obtain.

## Procedure B: clean installation target

Install exact tested build, create private DB/volume/secrets, set allowlists/TLS/base
URL, validate config and run migrations. `workspace-admin preflight` exits nonzero
on default secrets, unsafe binds, schema mismatch, unsupported caps or inadequate
disk reserve. `workspace-admin user bootstrap --github-id ...` requires a verified
identity; never promote the first arbitrary login. Only then enable web login.

Expected live checks: liveness process ok; protected diagnostics show DB/storage/
schema/worker/runner/network policy; capture readiness is false until all required
capture dependencies are qualified. Complete one synthetic private capture/export
and verify it before allowing pilot work. No arbitrary real target is a smoke fixture.

## Procedure C: coherent backup

`workspace-admin maintenance enter` stops admission and user mutations, issues
drain/cancel, waits for bounded runner stop and fences unresolved leases. Verify
no finalization writer remains, then collect DB snapshot plus finalized artifacts,
schema/component/profile/build IDs and redacted config references. Make backup
manifest/digests and protect output outside the application/index tree. Separate
secret escrow uses operator policy; plaintext keys are not appended to routine reports.

`workspace-admin backup create --output ...` fails if the maintenance/write boundary
cannot be established. Verify backup inventory before exiting maintenance; never
report success based only on pg_dump exit status. Expected counts/digests must
match the quiesced source inventory; record creation time and actual operator outcome.

## Procedure D: isolated restore

Verify backup checksums before applying it. Restore DB and bytes together onto a
fresh instance with publication and egress disabled. Install matching compatible
build/schema, rotate required secrets, revoke all sessions/flows and clear stale
lease ownership without automatic queued work execution. Reconcile, verify artifacts,
private/public mapping/audit and run the synthetic core workflow. Report duration,
counts/hash mismatches and unresolved anomalies. Only deliberate operator resume
enables capture/publication; a restore rehearsal never republishes live data.

## Procedure E: upgrade and rollback

Preflight target build/schema/profile compatibility; enter maintenance; create and
verify coherent backup; apply migration; deploy exact image; validate health/schema/
integrity/auth/public mapping and core synthetic flow. Resume only after checks.
If migration fails, keep maintenance active and select documented forward recovery
or restore the complete pre-upgrade snapshot. Do not assume a DB downgrade restores
filesystem bytes or post-upgrade writes. State expected downtime/data-loss interval
from measured rehearsal, never an invented zero-downtime guarantee.

## Failure and incident paths

| Trigger | Required safe behavior | Operator evidence/action |
| --- | --- | --- |
| DB unavailable | Deny mutations/protected reads; no grant-cache fallback | Correlated safe error, restore DB, reconcile ambiguous commits |
| Runner unavailable/stale | Durable jobs retained; capture readiness false | Stop/fence stale run, inspect attempt/slot, recover under lease rules |
| Storage reserve/full disk | Stop admission/finalization safely; keep old evidence | Inventory temp/orphans; cleanup only authorized namespaces, no automatic evidence pruning |
| Integrity failure | Block complete export/new publication; suspend affected public asset serving | Preserve original finding, compare backup, quarantine and restore only with provenance |
| Unintended publication | Revoke slug/assets immediately on server | Record actor/reason and acknowledge external-copy limit; inspect disclosure scope |
| Compromised user/session | Disable/revoke sessions/queued access, rotate relevant secrets | Audited incident, check exports/publications and pending jobs |
| Emergency evidence purge | Operator-only maintenance with ID/dependency report | Revoke publications, remove selected bytes/metadata under explicit scope, preserve minimal non-sensitive tombstone |

Emergency purge reports dependent exports/caches/backups and authorized removal
scope. Record a protected deletion ledger outside ordinary restored data and replay
it after backup restore before enabling serving, so removed material is not resurrected.
Do not promise erasure of third-party downloads or inaccessible backup copies.
Normal archive/hide remains non-destructive and cannot call this procedure.

## Health, logs and retained operational state

`/health/live` returns minimal process status. `/health/ready` returns minimal
service readiness and safe code; authenticated operator diagnostics separate
`read_ready` and `capture_ready`. Archive reads can remain available during runner
failure if DB/storage/auth are healthy; DB or relevant storage failure denies reads.
Maintenance denies mutations and can keep safe read paths only if the backup
consistency boundary permits it. No health endpoint discloses paths/credentials.

Record queue age, attempts/expired leases, capture duration, resource denials,
storage reserve, integrity findings, backup success and restore rehearsal results.
Keep detailed job events 7 days/export spool 24h; retain job summaries/audit per
explicit operator retention policy without UI deletion. Captures have no automatic
retention purge in V0. Define production RPO/RTO/backup schedules after measurements.

## H0 context/triage migration and later investigation rollout

V0 migrations add private request context and independent triage with normal default.
Do not infer legacy rationale/entry mode or historical importance from tags, notes,
review or public flags. Preserve current editorial revisions and publication pins.
CSV intent records include context in preview/admission digests; workers never
restore stale editorial fields. Backups include these application records; default
capture/export/public metadata does not. EWP-31/HUN-ACC-01/02 qualifies this delta.

Later H1–H4 rollout follows documents 28–33: annotation revisions/dependency pins;
versioned private corpus/cues; frozen report selections; native transfer/quarantine.
Foreign identities remain claims, not accounts. Reconcile promoted package bytes
against acceptance state on restart. Restore initially disables automatic analysis/
generation/import acceptance, applies deletion/revocation ledgers, invalidates removed
input dependencies and checks access before any resumed work. Include search snippets,
crops, report spools and quarantine in the emergency-purge dependency report.

## Companion rollout/restore continuation

ADR-007/document 37 defines B0/B1/B2 flags default off, exact extension ID/origin
allowlists, digest-only grants, quota-reserved quarantine and epoch rotation on
restore. Add ordered schemas and source-channel labels without relabeling old
server/imported captures. Back up accepted evidence/receipts/context; incomplete
quarantine is temporary, and restored upload metadata cannot assert missing bytes
survived. No token/session/recording restart after restore; deliberate re-pairing,
reconciliation and removal-ledger replay precede serving. Intake uses separate
one-slot bounded validation and existing installation admission/disk reserves.

## Integrated admission, removal and rollout refinement

ADR-008/documents 41/42 specify shared reservations/permit recovery, root removal
fences with ledger-before-reopen containment, and effective feature/schema/
qualification/restore state. Preflight validates actual enabled job budgets and
compatibility. Individual one-slot services cannot all run concurrently under the
initial one-heavy-task ceiling. Drain/reconcile actual processes before releasing
stale reservations; do not subtract a successor generation's capacity.

Removal ledger and DB are not one atomic store: any ambiguous step keeps a durable
serving hold until reconciled. Restore replays the protected ledger, rotates epochs,
verifies accepted bytes and marks missing temporary uploads interrupted before any
resume. EWP-57/58 qualify the core procedure; EWP-59 exercises each later enabled
branch. Commands/procedures remain target interfaces, not executed operations.

## Concrete infrastructure/user continuation

Documents 44–47 refine the target Compose/build/runtime, DB role/migration/pool,
settings/installation/update and scheduled maintenance/clean-host drill contracts.
Only edge ports are public; temporary job containers get no application/daemon
credentials. DB backup alone does not capture accepted artifacts or current removal
ledger. EWP-61–68 provide real subtask evidence for core parent gates; no procedure
here was executed against a live installation.

Future U1/U2/U3 migration in 48/49 previews effective permissions, preserves the
shared default scope/history, prevents last-admin lockout and applies scoped access
only after complete installed-adapter qualification. Preserve unknown historic
privacy; do not label old collections restricted. Host/DB operator recovery remains
separate from application role administration. Restore invalidates old grants and
keeps stage-specific automation disabled until authority/scope/ledger checks pass.

## Preservation/read-plane qualification continuation

Documents 50–53 add strict production recording/profile and safe receipt/verifier
contracts without mutating old evidence. Restore accepted WARC/receipt/dependency
inventories under ledger/epoch holds; temporary read snapshots confer no restored
transfer authority. Replay qualification has no app cookies or live fallback, and
is not a newly published archive viewer. Shared read temp/stream/compute limits
are included in preflight/incident diagnostics. Actual provider/replay/renderer/
file-substitution/slow-client proof remains EWP-73–78 work.
