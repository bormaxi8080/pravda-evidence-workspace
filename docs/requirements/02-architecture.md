# Architecture requirements

Date: 2026-11-09. Status: **selected architecture; qualification pending**. Owner: engineering lead.
Sources: concept sections 6–8, 12, 15, 22–29; current `main.py`, `capture.py`,
`jobs.py`, `database.py` and Compose under `provereno-ui/`.
Decisions: DEC-02, DEC-03, DEC-07, DEC-08, DEC-09.

## Selected shape

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
Selected V0: direct Playwright behind an adapter in the isolated runner, per
[ADR-002](../decisions/0002-v0-scope-and-topology.md). Pravda is a later evaluated
adapter candidate; do not implement two engines for V0. EWP-01 proves feasibility.

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
PostgreSQL and maintenance command/process. The selected runner is project-owned Playwright
under ADR-002; do not deploy a second Pravda service unnecessarily.
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

Acceptance scenarios: ACC-03/04/08/09/10/12. Detailed network/volume/adapter contracts are in
[document 14](14-domain-and-execution-contracts.md); implementation and isolation
qualification remain EWP-01/09 obligations, not implemented facts.

## Detailed selected design

See [the baseline register](13-selected-v0-baseline.md),
[contracts and operator procedures](README.md) and
[assignable work packages](18-assignable-work-packages.md).
Implementation/qualification remain pending; source presence is not test evidence.

## Investigation services and trust boundaries

[ADR-006](../decisions/0006-investigation-context-and-handoff.md) reuses the modular
monolith, PostgreSQL, durable jobs and artifact store for context/triage and later
annotation, corpus/cue, report and transfer services. This H-stage design introduces
no search cluster. The browser companion is selected separately by ADR-007 below. Exact bytes, editorial metadata, triage, derived
findings and report snapshots are separate authorities with versioned references.

Flow for later H stages: authorized original -> bounded offline derivation ->
verified annotation/hit -> explicit frozen report/transfer selection -> controlled
private rendering/package. Untrusted import -> private quarantine -> bounded offline
validation -> admin mapping preview -> fenced staged promotion/transactional accept.
Offline decoders/extractors/renderers have no external network or general secrets;
only the trusted controller commits records/promotes output. The web process never
unpacks case archives or executes archived content. See documents 28–33 for exact
limits/permissions and qualification before enablement.

## Companion trust boundary

[Document 34](34-browser-companion-architecture.md) adds an optional external MV3
client and fixed HTTPS companion API to the existing topology. B0 calls authorized
server capture admission; B1/B2 send untrusted client-generated artifacts into a
separate quarantine/validation path. They do not call CaptureEngine or give a local
browser DB, publication, general evidence-read or server-session credentials.

Application owns PairingIntent/CompanionGrant/BrowserUpload/BrowserAcquisition and
later ResearchSession/Observation services. New manifests/profiles live in the
future Evidence Contracts component when implemented. Browser Extension remains
planned 0.0.0; no existing runtime depends on its build. Per-slot offsets, generation,
reservations and accepted byte identity reuse DB/finalization authority; isolated
validators have no source-fetch authority. See documents 35–37 for the contracts.

## Shared policy, dependency and admission authority

ADR-008/documents 40–43 refine the modular monolith with one purpose-specific
eligibility service, transactional dependency/removal-fence authority, shared
reservation/claiming service and effective-feature preflight. SSR, web/companion
APIs, workers and downloads reuse these services. No external policy engine or
production graph service is introduced. The development CodeBase MCP index is
not part of application execution or evidence dependency resolution.

One aggregate heavy-task permit initially bounds the sum of per-operation slots;
only bounded control/chunk/dispatch paths use their separately specified budgets.
Root fences deny affected reads/promotions before paged cleanup completes. These
core contracts are materialized with V0; C/H/B-specific adapters arrive only with
their stages. Actual memory/egress/DB/filesystem qualification is still required.
