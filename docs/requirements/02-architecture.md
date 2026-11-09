# Architecture requirements

Date: 2026-11-09. Status: **proposed**. Owner: engineering lead.
Sources: concept sections 6–8, 12, 15, 22–29; current `main.py`, `capture.py`,
`jobs.py`, `database.py` and Compose under `provereno-ui/`.
Decisions: DEC-02, DEC-03, DEC-07, DEC-08, DEC-09.

## Recommended shape

One Python modular monolith serves editorial workflows, backed by PostgreSQL and
a filesystem artifact store. Request serving and hostile browser execution are
separate process/security boundaries. Logical modules are not new microservices.
Use the existing FastAPI/Jinja/CSS implementation as the migration starting point.

```text
Editor / reader
      |
  Nginx / TLS
      |
  FastAPI web ---- application services ---- PostgreSQL
      |                                       |
  authorized read                       durable jobs/events
      |                                       |
Artifact store <---- finalizer / worker -------+
                           |
                 capture-engine adapter
                           |
                 isolated browser runner ---- public Internet

Scheduler/maintenance -> leases, retries, optional availability probes
Operator -> migrations, quiesced backup/restore, health and diagnostics
```

## Requirements

### REQ-ARC-001 Modular monolith with explicit ownership

Domain/application services shall own capture, editorial, publication, jobs and
audit rules. SSR and HTTP interfaces shall use the same services and permission
checks. Avoid loopback HTTP calls inside the server. UI/routes shall not implement
alternate authorization, publish flags or independent artifact-write rules.

### REQ-ARC-002 Separate request and browser execution

The web process shall enqueue and serve bounded requests; it shall not start a
browser capture in its lifespan or hold HTTP requests open until capture completes.
Web/worker/maintenance may share a built image with different commands. A separate
browser runner shall not receive GitHub/session secrets or general DB credentials.
The trusted worker may hold bounded DB/storage access; the browser process shall
have only job-scoped temporary output and restricted network access.

### REQ-ARC-003 Replaceable capture-engine boundary

The application shall call a versioned internal CaptureEngine contract, supplying
validated URL, capture options, limits and correlation IDs. The result shall contain
artifact references/bytes, actual provenance, navigation outcome, warnings and
structured errors. No provider-specific object becomes a domain model.
Recommended V0: preserve direct Playwright behind an adapter in the isolated runner;
Pravda remains the preferred candidate subject to contract/fidelity evaluation.
Only one implementation is required for V0. DEC-03 must settle this before coding.

### REQ-ARC-004 PostgreSQL owns durable workflow

PostgreSQL shall own jobs, leases, attempts, event sequence, publication, editorial
state and artifact metadata. LISTEN/NOTIFY may wake workers, but missed signals
shall not lose work. In-memory queues/cache may optimize but never define truth.
No Redis, broker, search cluster or distributed database is required for V0.

### REQ-ARC-005 Artifact authority and access path

The artifact store shall own bytes; DB records shall own identity, location and
digests. Authorization shall be checked before each file read/download through a
service. Nginx shall not expose evidence directories as static roots. Storage keys
shall be relative, validated identifiers; request-supplied absolute paths are forbidden.
Keep private/public projections and temporary output distinct.

### REQ-ARC-006 Reconciliation across DB and filesystem

Completion shall use a staged finalization protocol with durable intent and a
reconciliation path. Write bounded temporary artifacts, hash them, validate profile,
promote atomically on the same filesystem, then commit final records with lease
fencing. A crash between promotion and DB commit shall leave recoverable orphans,
not falsely completed captures. Never imply a cross-resource ACID transaction.

### REQ-ARC-007 Deployment and observability boundaries

Use one-host Compose for V0: edge proxy, web, trusted worker, isolated runner,
PostgreSQL and maintenance command/process. Whether runner is a Pravda service or
project-owned Playwright service is DEC-03; do not deploy both unnecessarily.
Only edge HTTP(S) is public in the target topology. Internal services/DB are not
public ports. Correlate requests, jobs, attempts, captures and publications in logs.

### REQ-ARC-008 No premature repository rewrite

Refactor incrementally from `provereno-ui/`; map legacy paths to proposed modules
before moving files. The concept's `src/provereno/` tree is illustrative. A move
requires package/import/container/migration checks and component ownership updates.
Domain separation alone does not require a new package or service per module.

## Logical module contracts

| Module | Owns | Must not assume |
| --- | --- | --- |
| Identity/security | Admission, sessions, permissions, URL policy | Editorial access from organization membership alone |
| Capture | Engine request/result normalization and provenance | All sites or all HTTP 200 pages are captured successfully |
| Jobs | Claim/lease, attempts, retries, cancellation, events | Exactly-once browser execution from a row lock alone |
| Evidence/storage | Artifact profile, hashes, finalization, verification | A filesystem rename commits DB metadata |
| Editorial | Notes/tags/collections/review revisions | Editorial edits can mutate original bytes |
| Publication | Public allowlist, review revision, revoke | Knowledge of capture ID is authorization |
| Export | Bounded package derivation and verification | Missing optional output may be silently omitted |
| Operations | Migration, backup, restore, maintenance | Backup existence proves restorability |

## Failure and verification

If browser runner is unavailable, queued work remains durable and UI shows the
dependency failure. DB outage denies mutations and protected reads rather than
serving stale grants. Disk exhaustion prevents finalization and new admission with
an operator-visible reason. Worker crash is governed by document 04, not by an
unobserved background-task exception.

Acceptance scenarios: ACC-03/04/08/09/10/12. Detailed deployment network/volume
permissions and adapter selection are blocking design outputs, not implemented facts.
