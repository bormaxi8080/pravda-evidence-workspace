# macOS development and local verification runbook

Date: 2026-11-10. Status: **adopted procedure specification; application commands
and qualification remain implementation work**. See [ADR-012](../decisions/0012-macos-development-and-linux-qualification.md)
and [platform plan](../requirements/56-macos-development-and-linux-qualification.md).

## Worktree and tooling

Use the assigned worktree and committed planning policy; read AGENTS/CONTRIBUTING
and affected manifests. Match MCP to this checkout. Preserve implementation branches.

```sh
pwd
git branch --show-current
git rev-parse HEAD
git status --short
uname -sm
python3.12 --version
docker context show
docker version --format '{{.Server.Os}}/{{.Server.Arch}} {{.Server.Version}}'
docker compose version
```

Record operator and actual agent results separately. An operator Docker context
does not prove access inside Codex's isolated HOME/sandbox. Use ordinary scoped
Git staging/commit through the repaired launcher. Request an exact local control,
package destination or permission when absent; retain profile/credential isolation.

## Configuration and execution

Use a project-owned Python 3.12 virtual environment and locked packages. The legacy
README/Dockerfile commands are not a verified installer for the new system. Missing
package access does not authorize a homemade replacement for independent validation.
Use a dedicated local PG16 instance for real DB behavior; native Python/SSR is a
supported development mode, not a substitute for a qualified isolated capture runner.

EWP-61/65 own the actual local Compose profile/files/commands. Until implemented,
do not invent a working compose.dev.yaml. Select arm64 image/browser variants and
record Desktop's guest kernel/resources/digests. Do not force amd64 emulation for
ordinary local development or assume a specific Compose plugin major is required.

Allocate owned runtime/data/secret namespaces and unused loopback ports. Paperclip
3100/54329 and its embedded data/credentials are excluded. DB/container traffic
uses the owned network; all necessary host ports bind to 127.0.0.1. Secrets/runtime
state stay outside Git and indexes. Do not globally switch Docker context or prune.

Start owned DB health, serialized migration/preflight, web/worker readiness, then
admit only tested capabilities. Startup create_all is not an upgrade authority.
Never expose browser/decoder to the daemon, DB/session secrets or writable final
store. Controlled fixture servers and disposable browser profiles replace personal
logged-in browsing in tests. Keep arbitrary public capture off until its actual
local isolation/egress gate passes; no --no-sandbox workaround qualifies it.

## Evidence, integration and cleanup

Run governance and owning behavior checks. Use actual PG transactions/privileges,
bytes/hashes, controlled browser and container checks for corresponding claims.
Document case sensitivity, VM volumes/bind mounts, storage promotion and Desktop
network differences. Mocks remain unit tools; skipped local runtime gates are not
passed. Label each record MAC-DEV, with host/guest/tool/image/source/fixture identities,
commands/results and exact unavailable cases. Link deferred-linux cases to the
separate Linux dossier. Obtain human review and integrate accepted upstream code
into the agreed local base before claiming dependency completion.

Stop admissions, fence/drain jobs and remove only exact owned fixture resources
whose IDs/labels match this run. Retain redacted evidence and reviewed worktrees;
never reset implementation work or use daemon-global cleanup. Rehearse real local
backup/restore where required; a second folder on one disk is not disaster recovery.

The later Linux iteration reuses code/locks/synthetic fixtures, then independently
qualifies native builds, storage, isolation and clean-host recovery. Do not copy the
Mac's Paperclip DB, personal browser profile or agent credentials to that target.


## Approved project runtime connection — 2026-11-10

The operator explicitly authorized the original Codex project profile to use the
local Docker Desktop API and loopback development servers. The private launcher
selects the independent `pravda-macos-local` Docker context through its own
DOCKER_CONFIG, with Desktop CLI/plugin discovery and a writable owned buildx cache.
It does not copy the user's registry credentials or change the global context.
The precise approved Desktop Unix socket is configured by the operator; agents
must not infer authority to use unrelated sockets or alter profiles themselves.

The broad allow_local_binding flag was rejected by automatic approval review and
is not enabled: it disables the private-network guard more widely than needed.
Use project containers with explicit 127.0.0.1 published ports for agent-started
HTTP services/fixtures while native host bind remains restricted. Record the actual
allocated port; do not bind 0.0.0.0 or reuse Paperclip ports. For native development
without a sandboxed listener, in-process tests remain useful but do not replace the
actual container/browser workflow. Broader access needs a separate concrete decision.

A sandbox probe verified the isolated context, arm64 Engine/Compose, public command
HTTP denial and an owned non-root read-only HTTP fixture returning its expected
marker through a loopback-only published port. The fixture had no host mounts or
application/DB secrets, dropped capabilities and no-new-privileges; its exact
container/network were removed afterward. Its owned bridge network was a trusted
fixture transport, not browser egress/isolation qualification. The tested internal
network did not expose a usable published port in this environment, so record that
observation instead of weakening the product capture network policy.

Docker API authority is an explicitly trusted engineering/operator capability.
Never mount its socket into web/browser/decoder test processes or treat access to
the engine as proof that the application's hostile-content boundary is qualified.
