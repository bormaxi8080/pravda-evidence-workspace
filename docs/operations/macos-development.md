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
