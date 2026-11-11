# Role images — LOC-5 / EWP-61

Status: MAC-DEV implementation prepared for human review; not a release or deployment.
Source baseline: `cf30f2154ff31816f21884f0f13ecd6fb6a05e4a`.
Branch: `chore/LOC-5-workspace`. Application 1.1.1; Deployment 0.1.1.

The inherited build selected a nonexistent setuptools backend, installed before
copying package sources, omitted wheel templates/static files, and combined web,
Chromium and native build dependencies. The new wheel is built with sources present
and copied into isolated virtual environments; package resources resolve relative
to the installed package, independently of the working directory.

## Build and inspect

```sh
python3.12 provereno-ui/build-tools/build_images.py --output /tmp/loc5-evidence
python3.12 provereno-ui/build-tools/verify_images.py --identities /tmp/loc5-evidence/identities.json
```

Use the approved isolated `pravda-macos-local` Docker context. Builds explicitly
select linux/arm64; Python base is digest-pinned, Debian packages resolve against
the dated immutable archive, and all Python dependencies use exact versions and
artifact hashes. `--no-cache` requests a clean rebuild. This fixes dependency inputs;
OCI metadata/attestations can differ, so byte-identical image output is not claimed.
Locks record uv regeneration commands; regeneration is a deliberate dependency
update, not a build step. The capture extra pins Playwright 1.56.0 with Chromium
141.0.7390.37 / build 1194. The offline extra pins WeasyPrint 66.0.

Build output records context-file SHA-256 identities, baseline commit, actual image
IDs/architecture/UID and SHA-256 of installed CycloneDX Python/Debian inventories.
Inventories are generated inside the installed runtime without source overlays or
package installers. Keep generated inventories outside the repository. Source
fingerprints describe dirty build inputs as well as the recorded baseline commit;
the baseline alone does not identify uncommitted changes.
Verification rejects changed source, retagged images and changed SBOMs before
starting fixtures, so a successful old build cannot validate newer source.

## Runtime inventory and compatibility

| Target | Command / dependency boundary | Mounts and authority |
| --- | --- | --- |
| web (also default) | Uvicorn :8080; no Playwright, Chromium, WeasyPrint or compiler | No declared volumes; externally supplied DB configuration; trusted web DB access only |
| capture | Read-only matched-browser inventory; no capture admission | No DB/session secrets, daemon socket or final evidence store; eventual isolated launcher owns input/output |
| offline | Synthetic in-memory PDF smoke and inventory | No credentials/network/final evidence mounts; eventual launcher owns selected input and bounded output |

All targets use UID:GID 10001:10001. Runtime profiles should use read-only root,
private bounded /tmp, dropped capabilities, no-new-privileges and explicit resource
limits. These flags are exercised by verify_images.py; Dockerfiles cannot enforce
caller-supplied runtime isolation. No host socket is mounted. No app secrets are
baked into images: the positive build context excludes local .env/data/caches.
Supply DATABASE_URL and a SESSION_SECRET_KEY of at least 32 characters externally; there is no development credential fallback. Empty signing keys fail validation.

Web startup performs SELECT 1 only; it does not create/upgrade schema or start the
legacy browser, monitor or in-process worker. Capture enqueue returns 503 pending
launcher qualification. This intentionally withholds unqualified acquisition.
Existing schema/data is not migrated or rewritten. Legacy Compose is not a
qualified multi-role deployment; EWP-62 and later packages own launch/dispatch,
DB bootstrap and migration. Capture/offline commands are image checks, not working
production job consumers. Their inventory success is not hostile-input isolation.
Do not expose the prototype as a production service.

## Verification record

Agent host: Darwin arm64, Python 3.12.10. Approved Docker context:
`pravda-macos-local`; Engine 29.9.3 linux/arm64; Compose v5.7.0.

- Governance validator and 36 governance unit tests passed on 2026-11-11.
- Installed web wheel imports outside source with no browser packages.
- Three-role builds and real dedicated PostgreSQL 16.10 startup passed. The installed
  wheel served the login page and CSS with HTTP 200; startup left zero public tables.
- All roles ran as UID:GID 10001:10001 with read-only root, dropped capabilities,
  no-new-privileges and bounded resources. Root-write rejection, missing web browser/
  compiler/installer packages and capture enqueue denial (503) passed.
- Offline WeasyPrint rendered a 3,800-byte synthetic PDF without network access.
  Chromium reported 141.0.7390.37 and ldd found no missing native libraries.
  This checks installed dependencies, not browser sandbox/egress qualification.
- On resume, an old web image failed the new empty-session-key rejection check.
  The final build had been interrupted; refreshed builds and source/image/SBOM
  identity checks prevent that stale-image result from qualifying current source.
  The resumed three-role build and verification subsequently passed against the
  final source fingerprints, including empty-session-key rejection (2026-11-11).
- Initial template API and host login readiness attempts failed; subsequent runs
  passed after the template-call correction already present in this worktree.
  The transient host readiness failure was not assigned a proven root cause.
- The original backend import was reproduced with setuptools 80.9.0:
  ModuleNotFoundError for setuptools.backends. Corrected wheel builds passed.
- Guest kernel: 7.0.14-linuxkit aarch64. Agent Docker access was exercised directly;
  no operator-only test result is counted. Dedicated fixtures were removed by ID.
  No schema/data migration or production recovery behavior is introduced.
- Web images contain the base libstdc++ Python debugger helpers under /usr/share/gcc;
  these are runtime support files, not an installed GCC compiler.

Native Linux x86_64 qualification remains LOC-82/83/84. Browser sandbox/egress,
worker dispatch/recovery, full authorization and production readiness remain
separate gates. Public capture remains disabled. Human acceptance and integration
are required before LOC-5 is complete.
