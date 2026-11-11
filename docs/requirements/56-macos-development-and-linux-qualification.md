# macOS development and separate Linux qualification

Date: 2026-11-10. Design revision: 0.11. Status: **adopted current delivery policy;
implementation and qualification are evidenced per task**.
Authority: [ADR-012](../decisions/0012-macos-development-and-linux-qualification.md).
Owners: implementation/database/browser/security/operator roles.

## 1. Scope and precedence

Develop and test on the operator's Mac now; provision and qualify native Linux
later. This changes platform sequencing and ticket acceptance scope, not product
features or evidence semantics. This platform interpretation supersedes older
Linux-first F0 statements in documents 09/13/17/44/49/55 and imported task text.
The 170 requirements, 78 EWP identities and 76 acceptance definitions stay stable.
Historical reports remain evidence of their original environment only.

| Lane | Environment | Acceptance establishes | Separate obligation |
| --- | --- | --- | --- |
| MAC-DEV, current | macOS arm64; native tools; Linux arm64 Docker Desktop guest | Reviewed/integrated implementation and applicable real local tests | No native x86_64 support or production/pilot release claim |
| LINUX-QUAL, later | Native Linux x86_64/Ubuntu 24.04, pinned engine/runtime | Native deployment/build/isolation/DB/recovery dossier | Actual release and optional feature enablement still need their own approval/evidence |

An ARM guest or emulated amd64 image does not satisfy LINUX-QUAL. Absence of a
Linux server shall not block current code, UI, contracts, local PG or image work.

## 2. Mac environment prerequisite

On 2026-11-10 read-only operator checks observed Darwin arm64, Docker Desktop
installed, context desktop-linux, Engine linux/arm64 29.9.3 and docker compose
v5.7.0. These are observations, not supported-version pins, an agent-access test or
application qualification. Earlier sandbox reports of missing Compose/denied
Docker socket must not be interpreted as absence of an operator-accessible engine.

PC-SETUP-03 now establishes the following on this Mac:

1. Record host OS/architecture, Python 3.12 environment, Docker context, guest
   architecture/kernel, Compose/build features, resource allocation and disk/inodes.
   Pin versions/digests after tests; do not reject a working Compose plugin solely
   because its major differs from the older document's v2 label.
2. Allocate a project-owned worktree, disposable PG16 DB/storage namespace and
   collision-free loopback endpoints. Exclude Paperclip port 3100, DB port 54329,
   embedded cluster, credentials and runtime data from application tests/config.
3. Verify ordinary Git staging/commit, matching scoped MCP and run-attributed
   Paperclip API writes through the actual agent profile. Retain bounded permissions.
4. Distinguish operator runtime access from agent sandbox access. Record the actual
   controlled runtime path and permitted build/test/cleanup scope. An approved
   operator-side runner may return authenticated redacted smoke evidence. Browser
   and decoder processes never receive a daemon socket or general management API.
5. Perform a minimal owned filesystem/runtime smoke and real disposable PG16
   connection for upcoming work; collect exact commands/results and owned cleanup.
   This is environment readiness, not application or isolation qualification.

A failure names the exact local executable, package destination, control/socket
path, permission or missing feature and its owner. Persist an actionable handoff.
Requesting Linux provisioning is not a valid MAC-DEV bootstrap remedy.

## 3. Local architecture and implementation requirements

Native Python/SSR development may use a project virtual environment plus dedicated
PG16; the integrated path uses role-specific linux/arm64 containers on Desktop.
Both exercise the same domain/service contracts. SQLite, in-memory queues and mocks
cannot replace real PG concurrency, migration or privilege checks.

Bind development listeners explicitly to 127.0.0.1 and inspect ports before
allocation. Container DB traffic stays on the owned internal network; any necessary
host DB port is loopback-only. Separate DB, artifacts, scratch and backup locations;
keep secrets, captures and graph state outside Git. Do not globally change the
user's Docker context, touch Paperclip resources or use daemon-global prune.

Dockerfiles/locks shall resolve for linux/arm64 now, with architecture-specific
wheel/browser/image identities. Do not require amd64 emulation for every build.
Later native amd64 builds reuse source/fixtures and record new platform digests.
Use container volumes for DB state; test bind-mount case sensitivity, permissions,
atomic rename/fsync and same-filesystem artifact promotion rather than assuming
Linux host semantics. Host capacity is measured, not copied from a server estimate.

The trusted local operator/launcher owns runtime control; web, browser and decoder
roles keep document 44's credentials/mount/network separation. A logged-in personal
host browser is not the isolated capture runner. Use controlled synthetic fixture
servers and no real investigations during qualification.

## 4. Validation and unavailable behavior

| Concern | Required MAC-DEV evidence | LINUX-QUAL rerun |
| --- | --- | --- |
| Contracts/build | Schemas/fixtures, independent validators where required, clean wheel and arm64 role-image build | Native amd64 dependencies/browser/image compatibility and identities |
| PostgreSQL | Real PG16 roles/migrations/concurrent transactions/timeouts/restart | Target storage/resource/engine behavior |
| Launcher/capture | Actual local sandbox/mount/resource/egress/generation tests | Native cgroups/seccomp/firewall/DNS/IPv4/IPv6/UDP/orphan behavior |
| Evidence/restore | Real bytes/hashes, promotion/crash cases, clean owned local restore | Clean target-host restore/durability and measured recovery |
| Web/companion | Real local API/browser/session/permission/consent checks | Deployment-origin and enabled-browser/adapter matrix |
| Operations | Local startup/readiness/upgrade/cleanup/redacted logs | Server install/TLS/host loss/backup destination/support evidence |

Every case records host OS/architecture, guest OS/kernel/architecture when present,
source/runtime/images, fixture, command, actual result and cleanup. Use passed,
failed, blocked-local or deferred-linux. Deferred Linux evidence is a tracked
obligation, never a passed/skipped required local test. Reuse scenario IDs with a
lane/environment field; do not duplicate the 76 scenario definitions.

If local browser isolation/egress fails, preserve that failure and keep affected
public/arbitrary capture disabled. Independently testable code and trusted-fixture
work may continue with explicit limits. Mocks or --no-sandbox cannot qualify the
local capture gate. Linux-only server checks move to the Linux dossier; ordinary
local runtime failures cannot all be reclassified as Linux-only. Privacy, access
checks, immutable bytes and safe viewers remain mandatory in both lanes.

## 5. Iterations and proposed versions

Document 55's future product numbers remain planning coordinates. Lane labels do
not change artifact profile versions or create releases. Product release/date stay
null; component manifests, CHANGELOG, meaningful checks and commits still apply.

| Iteration | Work and exit | Scheduling |
| --- | --- | --- |
| M0 | PC-SETUP-03: actual Mac tool/runtime/access smoke and operating procedure | Current, after accepted PC-SETUP-01/02 |
| M1 / F0-DEV | EWP-61/02/62/01/63/03/64 on Mac topology | Current feature dependencies; no Linux environment prerequisite |
| M2 / E0-DEV | Private synthetic evidence/domain/read/UI vertical slice | Applicable local runtime/security gates |
| M3 / P0-DEV | Local V0 workflow, backup/restore and handoff | Reviewed, integrated implementation with local evidence |
| M4+ | R1/G1 and optional D1–D6 implementation on Mac | Local readiness; no production/Linux acceptance implied |
| L0 / LINUX-SETUP-01 | Native x86_64 target/resources/scoped access/disposable smoke | Backlog until explicit Linux admission |
| L1 / LINUX-QUAL-01 | V0/core target builds, isolation, PG, install/upgrade/clean-host recovery | L0 + accepted MAC-DEV EWP-16 handoff |
| L2 / LINUX-QUAL-02 | Production preservation/replay/protected read and release dossier on Linux | L1 + accepted MAC-DEV EWP-18 local readiness; release remains separate |

Linux core must not wait for all optional C/H/B/U capabilities. Their target checks
follow actual enablement. Native findings reopen affected code and require reruns.

## 6. Paperclip migration and task completion

Keep LOC/EWP IDs, comments, attachments, commits and human decisions. Preserve
LOC-4 commit 06dab44012b9330d90925a83629ea38dad297dfc and pending whole-package
review; first-slice acceptance does not accept that entire package.

| Task | Current scope and prerequisite |
| --- | --- |
| LOC-1/2 | Historical accepted workspace/protocol prep stays done |
| LOC-3 / PC-SETUP-03 | Mac bootstrap; old Linux question superseded, historical reports retained; depends on LOC-1/2 |
| LOC-4 / EWP-02 | Delivered platform-neutral contracts/review preserved; MAC-DEV completion policy |
| LOC-5 / EWP-61 | After LOC-2/3, local linux/arm64 role-image builds; LOC-3 now means Mac readiness |
| LOC-6 / EWP-62 | After LOC-5, local launcher implementation and real local checks |
| LOC-7 / EWP-01 | After LOC-5/6, controlled local Playwright feasibility |
| LOC-8 / EWP-63 | After accepted/integrated LOC-4/5, real local PG16 bootstrap |
| Other current EWP tickets | Existing feature dependencies/admission; MAC-DEV evidence scope; native-target cases linked to Linux dossier |

L0/L1/L2 are separate backlog orchestration tickets, not new product EWPs or
requirements. No MAC-DEV ticket depends on them. Retargeted LOC-3 is admitted for
Mac preparation by this instruction; LOC-4–8 stay admitted. Other EWP backlog
packages are not all admitted by this migration. Concurrency remains one.

A MAC-DEV ticket becomes done after its entire current-lane scope, required real
local checks, human acceptance and integration into the agreed local development
base. Link deferred native-target obligations to the Linux dossier. A slice,
missing local runtime evidence or a green governance suite alone is insufficient.

An unintegrated accepted upstream commit is a versioned artifact, not code already
on the shared base. Consumers may integrate an accepted prerequisite commit into
their own branch, resolving version/ownership/changelog conflicts and retaining
source identity. After whole-package acceptance and required checks, agents may
integrate into local main under the operator's standing authorization and the
[serialized integration procedure](../operations/paperclip-integration.md).
Preserve reviewed
branches; clean unstarted worktrees may fast-forward to the new policy commit and
new worktrees use the updated project base. Completion of a Mac release-readiness
EWP does not authorize G1 production release or Linux support; L1/L2 remain gates.

An in_review handoff names human review, a specific local action, or deferred Linux
work. Use one actionable interaction; unchanged blocker wakes are not new consent.

## 7. Migration checks and primary platform references

Check local links/versions/ledger/governance; preserve source/review artifacts.
Audit task lane, admission, source policy, superseded question and acyclic edges.
Confirm Linux orchestration is backlog and no current Mac task depends on it.
This policy update does not itself build or qualify the application.

Docker describes its [Desktop VM/network boundary](https://docs.docker.com/desktop/features/networking/)
and [architecture-specific builds and emulation](https://docs.docker.com/build/building/multi-platform/).
These distinguish local guest checks from native server evidence. Exact supported
versions, resource limits and image compatibility remain measured outcomes.
