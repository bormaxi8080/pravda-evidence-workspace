# Current-state review

Date: 2026-11-09. Baseline source commit: `f3ad669`. Method: local source,
configuration and concept review plus MCP symbol/source/coverage checks. This is
an orientation review, not a complete security audit or a running-deployment test.
No original investigations, credentials or runtime datasets were used.

## Source versus target

| Area | Present in source | Target / gap |
| --- | --- | --- |
| Capture | `capture.py` directly launches Chromium/Playwright, including `--no-sandbox` | The concept favors an isolated engine/adapter boundary; no Pravda HTTP adapter in current code |
| Jobs | `jobs.py` persists Job rows, then puts IDs in an in-process `asyncio.Queue`; SSE subscribers are in memory | No durable claim/restart recovery, leases, cross-process events or PostgreSQL LISTEN/NOTIFY implementation found |
| Processes | `main.py` starts capture, job worker and monitor in FastAPI lifespan | Separate web/worker/scheduler is a proposal |
| Data | `models.py` has User, Snapshot, Job, collections/tags, UrlCheck and AuditLog | Source/Capture/Artifact/Publication separation, review state and migration history are not implemented |
| Schema | `Base.metadata.create_all` on startup | Alembic upgrade/data-migration path is absent |
| Sessions | `auth.py` maps random session tokens to logins in a process-local dictionary | Persistent/expiring sessions and multi-process behavior require design and tests |
| Publication | `Snapshot.is_public` defaults false; public routes check it | Publication records/revocation semantics are proposals; screenshot responses currently advertise a one-year immutable public cache |
| Artifacts | PNG and MHTML written to paths from `DATA_DIR`; path strings stored in DB | Storage keys, atomicity/reconciliation and immutable artifact records require design |
| Export | `forensic.py` writes MHTML/PNG/JSON/HTML/checksums, optional PDF | No WARC/manifest; PDF failures are swallowed, so completeness needs an explicit contract |
| Audit | Writer and audit UI exist | Coverage, non-bypassability, permissions and append-only guarantees need integration review |
| Deployment | Compose defines `db` (PostgreSQL 16) and `web`, exposing 5434/8080 | README says PostgreSQL 15 and Nginx/Pravda topology; those services are absent from current Compose |
| Health/admin | README describes `/health` and `provereno.cli promote-admin` | No health route or CLI module found in the current source |
| Packaging | `pyproject.toml` declares 1.1.0 and `setuptools.backends.legacy:build` | Build backend/installability should be verified and corrected during prototype audit |
| Tests | No pre-existing automated test suite or CI workflow found | This change adds governance validation only; runtime verification remains outstanding |

## Priority questions for the design phase

1. How should existing snapshot/job/session data migrate without evidence loss?
2. Which capture failures count as partial versus successful? `CaptureResult.error`
   can be returned while `_run_job` continues to create a snapshot and mark done.
3. How should database commits and filesystem writes reconcile after crashes?
4. How should publication withdrawal interact with already cached screenshots and exports?
5. What can an editor publish/delete/export, and how are those decisions audited?
6. Where are URL/DNS/redirect/egress controls enforced for capture and monitoring?
7. What archival fidelity, receipt escaping, PDF rendering isolation and hash
   coverage must export guarantee?

Do not infer secure operation from the absence of a parser warning or from
README claims. These findings guide a fuller prototype/threat-model audit before
implementation planning. This baseline deliberately leaves runtime behavior unchanged.
