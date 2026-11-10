# Infrastructure and future identity delivery/acceptance

Date: 2026-11-09. Status: **selected implementation plan; no runtime task completed**.
Owner: deployment/database/backend/identity/security/operator. Authority: ADR-009.
Documents 44–47 refine existing technical requirements; document 48 adds 12 future
IAM requirements. Totals: 170 requirements, 70 V0 / 100 later, 72 tasks and 68
scenario definitions. Prior IDs/scenarios remain stable, not renumbered.

## Stage boundaries

| Stage | Result / dependencies | Explicit boundary |
| --- | --- | --- |
| Core technical refinement | Role-specific images/launcher isolation, DB roles/migrations/pools, installation/update/backup/monitoring/recovery | Implements existing V0 technical controls; does not enable U/C/H/B features |
| U1 | Stable users, provisioning/offboarding, fixed multiple role bundles and compatible migration | After qualified V0/core identity, no restricted spaces or new SSO implied |
| U2 | AccessSpace custody, flat group grants, scope closure/moves and optional separation policy | After U1 and all actually enabled adapters' scoped-path qualification; unsupported optional modules stay disabled |
| U3 | Qualified federation and exact-scope workload principals | After U1/U2; no browser-token reuse, auto account linking, SaaS tenant or implicit admin claims |

IAM work does not become a V0/baseline-production prerequisite. A core operator
can use the existing two-role shared newsroom after technical qualification while
these later stages remain unimplemented. U2 is not implemented by changing a
collection flag or enabling PostgreSQL RLS alone.

## Assignable tasks

| Ticket | Dependencies / owner | Bounded deliverable | Completion evidence |
| --- | --- | --- | --- |
| EWP-61 Reproducible role-specific images | None; backend/deployment | Clean wheel/build correction, locked app/browser/offline targets, source/image/SBOM fingerprints and runtime UID/dependency manifest | OPS-ACC-01; clean install/start, no hidden compiler/secrets/Chromium in web; exact supported versions recorded |
| EWP-62 Isolated job launcher and network proof | EWP-61; deployment/security | Fixed host-trusted lifecycle API/templates, per-job volumes/generations, real sandbox/resource/egress enforcement and owned-orphan reap | OPS-ACC-02/03; real host/container DNS/IPv4/IPv6/UDP/metadata/DB/daemon denial and late/orphan generation tests |
| EWP-63 PostgreSQL schema/role bootstrap | EWP-02/61; database/backend | Reviewed owner/runtime/migrator grants, ordered migration framework and core constraints/index foundations from 45 | OPS-ACC-04/05; fresh real PG16 roles/DDL/audit denial, failed/duplicate migration and integrity fixtures |
| EWP-64 Database budgets and routine maintenance | EWP-03/63; database/operator | Bounded pools/listeners/SQL waits, realistic query/index measurements, vacuum/WAL/transaction/disk diagnostics and maintenance runbook | OPS-ACC-04/05/07; actual competing sessions/pool exhaustion/lock timeout and representative cardinalities |
| EWP-65 Deployment config and clean install | EWP-01/03/05/56; deployment/operator | Validated redacted settings schema, environment separation, pinned Compose/network/mount/secret bundle, readiness and operator bootstrap | OPS-ACC-03/06; default-secret/empty-policy/wrong-path/schema/exposure failures, clean synthetic installation |
| EWP-66 Coherent backup and upgrade procedure | EWP-65/08/12/13; operator/backend | Actual quiescence, verified DB+artifact/config/role backup, purpose-specific key rotation and tested upgrade/rollback interfaces | OPS-ACC-06/08; interrupted upgrade, compatible/incompatible reader and matched backup/byte proof |
| EWP-67 Maintenance telemetry and incident guide | EWP-65/55/64; operator/security | Bounded metrics/logs/support bundle, schedule/threshold state, owned temp cleanup, incident escalation/runbooks | OPS-ACC-07; no-content/no-secret telemetry, absent-backup/unhealthy-worker/full-disk and quota diagnostics |
| EWP-68 Clean-host recovery and technical qualification | EWP-14/57/58/66/67; operator/security | Isolated clean-volume/host restore, removal/epoch/grant/quarantine reconciliation, network/resource rerun and measured support evidence | OPS-ACC-01–08 as applicable plus ACC/SYS core gates; actual failure scenario/time/recoverable point, no fake RPO/RTO |
| EWP-69 U1 user lifecycle and capability bundles | EWP-16/06/53/59; identity/product | IAM-001–006 DTO/schema/UI/migration, role preview, invitations, session/offboarding and last-admin recovery | OPS-ACC-09/10/12 plus core identity/revision regressions; old editor/admin effective-rights mapping and no retroactive privacy claim |
| EWP-70 U2 access spaces and scope closure | EWP-69/54/56/59; domain/security | IAM-007–010 migrations, one-space membership/flat groups, scoped repositories/downloads/jobs/derived adapters and move/separation preview | OPS-ACC-10/11/12; denied cross-space counts/snippets/files/jobs/outputs, stale grants/move/publication races and installed-adapter coverage |
| EWP-71 U3 federation and workload grants | EWP-69/70/59; identity/security | IAM-011/012 provider/link/claim validation and explicit scoped service-principal protocol/rotation/expiry under reviewed contracts | OPS-ACC-09/12; provider outage/key/issuer/replay/link failures, no email auto-link, no service publication/admin/owner-disable bypass |
| EWP-72 Technical/user operations handoff | EWP-16/68/59; product/operator | Supported host/image/DB/config/backup matrix, operator and enabled-U-stage guides, access-review/support and evidence index | Applicable OPS scenarios and actual enabled versions; U cases remain pending until their owning tasks qualify, release/deploy separately authorized |

EWP-61/62 are implementation subtasks of the existing EWP-01 feasibility/build
milestone; EWP-63 refines EWP-03; EWP-65/66 refine EWP-14 operations. They are not
duplicate independent rewrites. Updated core prerequisites keep these parent gates
after their real outputs. EWP-68 precedes EWP-15, never depends on it. EWP-69–71
are later stages; EWP-72 can hand off the supported core without waiting for them.
Future U chapters are appended when actually qualified. No dates/assignees invented.

## Technical acceptance scenarios

### OPS-ACC-01 Build and image identity

Build from clean source using recorded locks/base/tool identities; install the wheel
with source available, run app/worker/browser/offline targets as intended UIDs and
verify needed fonts/native dependencies. Inspect image/config for default secrets,
wrong Python/browser pairing and accidental build/Chromium/daemon access in web.
Record unsupported platform/version gaps rather than claiming all Docker hosts work.

### OPS-ACC-02 Launcher, browser and decoder containment

Submit malformed job IDs/generations/template/image/mount/command overrides to the
bounded launcher. Browser/offline jobs cannot reach DB/control/host socket/final
store/other jobs; actual DNS/direct TCP/IPv6/UDP/metadata and proxy bypass tests
fail closed. Rootless/sandbox/seccomp/resource settings must work on the real host;
trusted-test Playwright success is not containment proof. Kill/reap an owned orphan
without deleting unrelated containers or permitting two active generations.

### OPS-ACC-03 Exposure, mounts and lifecycle

From outside the host verify only intended edge ports; DB/web/control are not
published. Deny edge raw artifact aliases, wrong forwarded host, reused test/prod
volumes and absent/wrong ownership paths. Exercise startup DB healthy but schema
incompatible, graceful drain, SIGKILL and restart hold. No automatic migration,
missing volume recreation, public admission or action replay follows a failed boot.

### OPS-ACC-04 PostgreSQL roles, pools and durable transitions

Use real distinct DB roles to attempt prohibited DDL/role creation/audit rewrite/
final evidence mutation. Exhaust pools/listeners, lock rows and terminate competing
claimers; runtime budget/reserve, timeouts, durable sequence and same-generation
acceptance hold. Long SSE/browser/render work does not hold a transaction. A mock
DB cannot qualify grants, locks, durability or connection behavior.

### OPS-ACC-05 Schema, indexes and database maintenance

Apply fresh/legacy/current migrations twice and interrupt bounded backfills. Verify
constraints, history/visibility/hash preservation, migration lock and old-reader
compatibility. Load representative synthetic volumes and record query plans/latency,
vacuum/statistics/transaction-age and WAL/temp behavior. Large maintenance requires
explicit lock/space plan; unsupported downgrade stays blocked, never drops evidence.

### OPS-ACC-06 Settings, upgrade and rotation

Test unknown/conflicting settings, empty admission, default/missing secret files,
incompatible feature/schema and wrong callback/origin/proxy. Rehearse tested bundle
upgrade/failure/rollback, purpose-specific DB/OAuth/session/epoch/TLS rotation and
client reconnect without exposing old credentials. Public/restore holds and removed
content remain enforced; image rollback is not an implicit SQL rollback.

### OPS-ACC-07 Maintenance, support and safe alerting

Inject no heartbeat, stalled queue, full disk/inodes/pinned pool, blocked DB, missing
backup, stale rehearsal and near-expiry certificate. Observe correct degraded state/
safe threshold/escalation, cleanup generation/pin preservation and bounded logs/
metrics. Review support bundle for forbidden bodies/URLs/tokens/DB dump. A missing
configured schedule is shown, not reported as a passed automatic service.

### OPS-ACC-08 Coherent backup and clean-host recovery

Create synthetic captures/editorial/publication/revocation/fence/role/grant state,
quiesce and independently verify backup. Lose the source host, restore onto fresh
volumes under held network/serving, recover keys/current ledger, invalidate old
sessions/epochs and compare DB/counts/digests/relationships. Missing temporary bytes
do not become accepted evidence. Record actual duration/recoverable point/loss;
old outbox/watch/upload authority never restarts automatically.

## Later identity/access acceptance scenarios

### OPS-ACC-09 User identity, admission and lifecycle

Rename provider login/email, replay/expire/redeem invitation, attempt duplicate/link
by email, suspend/deactivate an owner and disable the last admin. Preserve stable
identity/history, deny ambiguous admission and revoke subsequent operations without
cascade deletion. Operator recovery is explicit; no test makes a real account,
sends an invitation or proves provider integration solely through mocked claims.

### OPS-ACC-10 Capability bundles, migration and separation

Preview old editor/admin mapping and test every capability independently. Workspace
admin without content/publisher grant cannot read/publish restricted material.
Researcher cannot approve without reviewer; publisher cannot bypass stale approval/
profile eligibility. Enable optional two-person rules with viable/nonviable teams,
then disable a reviewer; no silent waiver or fabricated historical approval.

### OPS-ACC-11 Space closure, groups, move and publication races

Two spaces contain captures with identical URLs and private terms. Exercise all
enabled list/count/autocomplete/history/file/search/report/import/export/job/SSE/
companion/publication adapters; no unauthorized existence/snippet/body leaks. Add
multiple in-space collections, stale/nested/over-limit group grants and denied
cross-space membership. Move with active publication/pending jobs/pins; either an
audited coherent transition succeeds or it fails before exposure. No inferred grant
from tags/source equality/admin status or an imported package.

### OPS-ACC-12 Federation, grants and offboarding races

For U3 validate wrong issuer/audience/subject/state/nonce, code replay, provider
outage/key rollover/unsupported fresh-auth assertions and controlled identity link.
Reject unreviewed IdP admin mapping. Service principal/browser/web/DB credentials
are not interchangeable; scope/expiry/owner disable/revoke blocks every relevant
admission/finalization/stream. In U1/U2 apply only actual lifecycle/grant/membership
cases, never claim OIDC or workload success before that stage exists.

## Complete added IAM requirement coverage

| Requirement IDs | Stage / owning document | Planned scenarios |
| --- | --- | --- |
| REQ-IAM-001, REQ-IAM-002 | U1 / 48 | OPS-ACC-09, OPS-ACC-12 |
| REQ-IAM-003, REQ-IAM-004 | U1 / 48 | OPS-ACC-10, OPS-ACC-11, OPS-ACC-12 |
| REQ-IAM-005, REQ-IAM-006 | U1/U2 / 48 | OPS-ACC-09, OPS-ACC-10, OPS-ACC-12 |
| REQ-IAM-007, REQ-IAM-008, REQ-IAM-009 | U2 / 48 | OPS-ACC-10, OPS-ACC-11, OPS-ACC-12 |
| REQ-IAM-010 | U2 / 48 | OPS-ACC-11, OPS-ACC-12 |
| REQ-IAM-011, REQ-IAM-012 | U3 / 48 | OPS-ACC-09, OPS-ACC-12 |

## Existing technical requirement refinement coverage

| Existing requirement IDs | Detailed contract | Planned scenarios |
| --- | --- | --- |
| REQ-ARC-002, REQ-ARC-003, REQ-ARC-005, REQ-SEC-003, REQ-SEC-004, REQ-OPS-001 | 44 images/launcher/isolation | OPS-ACC-01, OPS-ACC-02, OPS-ACC-03 |
| REQ-DAT-005, REQ-DAT-007, REQ-DAT-008, REQ-JOB-001, REQ-JOB-002, REQ-OPS-002 | 45 DB roles/migration/maintenance | OPS-ACC-04, OPS-ACC-05, OPS-ACC-08 |
| REQ-API-006, REQ-OPS-003, REQ-OPS-004, REQ-OPS-005, REQ-EXT-004, REQ-EXT-005 | 46 deployment/upgrade/recovery | OPS-ACC-03, OPS-ACC-06, OPS-ACC-08 |
| REQ-OPS-006, REQ-OPS-007, REQ-OPS-008, REQ-EXT-006 | 47 maintenance/observability | OPS-ACC-07, OPS-ACC-08 |

This refinement matrix does not duplicate requirement definitions. Complete original
coverage remains 10/26/33/38; new IAM coverage is above. Actual evidence records
follow document 43: source/artifact/schema/config/fixture/environment identity,
exact commands/results, safe failure references and limitations. Empty/skipped/
metadata-only checks cannot pass real host/DB/browser/recovery/identity gates.
All described runtime scenarios remain unexecuted by this documentation pass.

ADR-010/document 53 later refines existing preservation/read obligations with
EWP-73–78/PRD-ACC-01–08. Current overall totals are 170 requirements, 78 tasks
and 76 scenarios; this document's twelve IAM IDs/owning matrix and technical task
scope stay unchanged. Neither production WARC nor U-stage implementation becomes
a new V0 dependency.

## Current platform and completion scope — 2026-11-10

[ADR-012](../decisions/0012-macos-development-and-linux-qualification.md) and
[document 56](56-macos-development-and-linux-qualification.md) select Mac development
first. EWP-61–68 now implement and exercise their applicable local behavior on the
Mac/Desktop topology; native Linux reruns are separate orchestration work. The
scenario bodies above retain their invariants and IDs. Record the lane/host/guest
and exact deferred target cases; do not call skipped local PG/security/recovery
checks passed. MAC-DEV task completion unlocks local dependants, not Linux support
or production enablement. PC-SETUP-03 is Mac readiness, not Linux provisioning.
