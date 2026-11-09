# Docker runtime, host and isolation requirements

Date: 2026-11-09. Status: **selected technical refinement; no image/Compose built**.
Owner: deployment/security/backend. Authority: ADR-009. Refines REQ-ARC-001/002/003/
005/007, REQ-SEC-003/004, REQ-OPS-001/006/007 and the common budgets in document 42.
The source two-service Compose is not this topology; platform evidence is in the
[source register](../reference/deployment-and-database-platform-review.md).

## Host and environment contract

Initial qualification: Linux x86_64/Ubuntu 24.04, supported pinned Docker Engine and
Compose v2, Python 3.12/PostgreSQL 16, 4 CPU/8 GiB RAM and 40 GiB free local storage.
Recheck vendor support/security at each real release; do not promise an old patch
as perpetually supported. Docker Desktop/ARM/Windows are development candidates,
not production-qualified by using similar YAML. Kubernetes/multi-host HA remain deferred.

Host preflight checks CPU architecture, cgroup/resource enforcement, UID mappings,
filesystem atomic rename/fsync behavior, time sync, disk/inodes/reserve, private
service reachability, TLS/DNS/canonical origin and external backup destination.
Artifact promotion stays on one tested filesystem; NFS/object storage is a separate
qualified adapter. Containers cannot create missing final volumes silently on the
wrong host path. A 500-row CSV or 1,000-position queue is a cap, not a promise that
this test host can reserve every worst-case artifact simultaneously.

## Process/image and exposure matrix

| Process | Image/function | Network/exposure | Credentials / write authority |
| --- | --- | --- | --- |
| Edge | Pinned minimal TLS/reverse-proxy target | Only public 443; optional 80 redirect, no evidence path alias | TLS key; proxy requests, no DB or finalized evidence mount |
| Web | Application runtime without Chromium/build tools | Private edge/backend; bounded identity-provider egress | Web DB role/session/OAuth keys; authorized reads and bounded intake only |
| Trusted controller/worker | Same application artifact, different command | Private DB/control and bounded launcher endpoint | Worker DB role, staged/final artifact authority, no daemon socket |
| Scheduler/reconciler | Application command, no browser | Private DB; no arbitrary Internet | Dedicated least-privilege role and safe audit; bounded reservation/lease repair |
| DB | Pinned PostgreSQL 16 image | Internal only, no host-published 5432/5434 | Separate DB data volume, service credentials, operator-only administrative access |
| Migration/operator jobs | Explicit one-shot application target | Private maintenance/DB only when invoked | Migration/backup/ledger credentials; never present in ordinary web/browser |
| Host-trusted launcher | Minimal fixed job-lifecycle controller | Private authenticated control endpoint, no public listener | Container-daemon authority at operator boundary; fixed templates only |
| Ephemeral browser runner | Dedicated matched Playwright/browser target | Per-job isolated network, only policy egress | Job-scoped input/output; no DB/session/OAuth/final-volume/daemon access |
| Ephemeral offline parser/renderer | Purpose-specific target | No external network or application/DB access | Only selected immutable inputs and bounded output namespace |
| Egress gateway | Audited resolver/proxy policy | Sole browser outbound route to permitted public targets | No DB/evidence/session secrets; source destinations not ordinary telemetry |

Use fixed non-root UIDs/GIDs for application/browser/decoder processes, read-only
rootfs where applicable, bounded tmpfs, init/reaping, PID/CPU/memory/ulimit/shm
budgets and a reviewed seccomp/capability set. No privileged mode, host network/PID/
IPC, broad host mounts or disabled seccomp as an unexplained browser workaround.
Chromium sandbox must work or an explicitly reviewed equivalent must be demonstrated;
the current --no-sandbox baseline cannot qualify. Failure disables public capture.

## Initial container ceilings to measure

| Service/job | Candidate memory / process budget | Candidate CPU / writable-space boundary |
| --- | --- | --- |
| Web | 512 MiB/process, at most two processes, 128 PIDs/container | One CPU ceiling per process, bounded request/intake temp; no browser |
| Controller | 512 MiB, 128 PIDs | One CPU, trusted bounded staging; heavy child budget is separate |
| Scheduler / reconciler | 128 MiB each, 64 PIDs each | 0.5 CPU each; bounded control/temp, no source parser |
| PostgreSQL | 2 GiB memory ceiling, 256 PIDs initially | Two CPU ceiling, dedicated persistent DB volume; server settings in 45 |
| Browser job | 1 GiB, 512 PIDs, private shm 256 MiB | Two CPU, 120s attempt plus teardown; existing artifact/temp/volume caps |
| Offline parser/validator/renderer | Existing 512 MiB and purpose-specific deadline, 128 PIDs | One CPU, read-only selected input and existing bounded output/temp |
| Edge / gateway / launcher | 128 MiB each, bounded PID count from measured process needs | 0.5 CPU each, bounded logs/temp; no original artifact storage |

These are initial qualification ceilings, not measured requirements or permission
to run every process/job at peak together. Reserve at least 2 GiB host headroom in
the 8 GiB test envelope and measure total cgroup/kernel/cache pressure. Shared
heavy permit remains one; CPU ceilings are limits, not guaranteed reservations.
Changing process count/PIDs/shm/memory must preserve the same aggregate accounting
and prove safe partial/failure behavior. Root/host IPC or unbounded memory is not
a supported fix for legitimate pages exceeding these caps.

## Per-job lifecycle without exposing the Docker socket

The launcher is host-privileged operational code, not an application-admin feature.
Whether it uses a host service or a tightly deployed controller, its daemon access
is equivalent to trusting that host operator; a wrapper is not a sandbox against
launcher compromise. Only the worker receives the authenticated bounded control
interface. It exposes create/inspect/stop/read-output for fixed job templates.

Request fields are attempt ID/generation/deadline, policy ID, bounded typed engine
input and declared resource reservation. Server-selected image digest/mount/network/
command templates cannot be overridden by page content, user URL, worker-supplied
arbitrary JSON fields or an API admin. No build/exec/general container-management
operation exists on this interface. Register owned containers/volumes with generation
and deadline; inspect/reap only those owned resources, never unrelated host containers.

Create separate read-only input and writable output volumes for one job, never the
whole final artifact tree or shared cross-job staging. Browser control input has
only job-scoped authority. Return output through bounded regular-file inventory;
the trusted finalizer recomputes hashes and promotes valid output. A runner's
reported hash is a hint. Stop/prove absence before a new generation reuses the
shared heavy permit. Startup reconciliation finds orphaned owned runners even if
the application died; no daemon-global prune is an incident recovery procedure.

This is the transport implementation of capture-engine/1. Offline jobs use similarly
fixed templates without network. It is unrelated to the browser extension's deferred
native-messaging helper. Real launcher credential/auth/replay/orphan/isolation tests
are required; no code or local daemon action is authorized by these example contracts.

## Network policy and volumes

Separate edge/backend, private DB/control and per-job egress zones. Internal network
names or a hidden port are not sufficient egress enforcement. Browser may contact
only the gateway; host forwarding/firewall policy blocks direct IPv4/IPv6/DNS/UDP/
QUIC/WebRTC/internal/control/metadata paths even if browser flags are ignored.
Gateway resolves/pins approved public destinations per connection, rechecks redirects/
new connections and preserves TLS verification. No private-IP override for real
capture. Identity-provider egress from trusted web uses its own bounded policy.

Persist DB, finalized artifacts and protected removal/epoch control records separately
from disposable per-job/cache/export/quarantine storage. Give each service explicit
read/write mounts. Edge serves no raw artifact directory; web artifacts always pass
current application authorization/integrity/publication checks. Offline jobs mount
only selected inputs read-only. Backups target protected storage outside the working
tree and failure domain; a second directory on the same disk is not disaster recovery.

Secrets are service-scoped files with correct host/container permissions; no literal
production password, committed .env, build ARG secret, browser token or shared admin
DB credential. Rotation/reload semantics are explicit. File-mounted secrets do not
encrypt host files by themselves. Redact resolved config, image history and diagnostics.

## Build, startup and shutdown contract

Build application wheels from a valid backend with package source present; lock
dependencies/OS packages and record source/wheel/image/Chromium digests. Test wheel
installation in a clean runtime before selecting a supported image. Separate app,
browser and offline-render dependencies; no browser launch/install during ordinary
web startup. Multi-stage build output includes required fonts/libraries, no compiler
or test credentials. Produce SBOM/vulnerability disposition with the release dossier.

Start DB health -> explicit serialized migration/preflight success -> web/controller/
scheduler readiness -> operator-approved admission. Container health is not schema/
integrity/readiness. Web retries bounded transient DB startup errors and fails closed
on incompatible schema. Startup never runs create_all as an upgrade or a destructive
automatic migration. Restart policy cannot revive automatic actions held after restore.

On SIGTERM: stop admissions/claims, drain or fence current generation, stop child
jobs and flush state before exit. Selected container stop grace is 150s, covering
the 120s operation budget plus teardown/reconciliation; test kill-after-grace. Force
termination leaves durable recovery state, not a fabricated success. Pinned images
and a checked Compose/config bundle are deployment artifacts, not a release by tag alone.

EWP-61/62 materialize these refinements; OPS-ACC-01/02/03/08 in document 49 require
real container/host network, resource, orphan and restart evidence before pilot use.
