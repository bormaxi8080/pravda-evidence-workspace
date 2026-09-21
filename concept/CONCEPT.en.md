# Provereno Evidence Workspace — CONCEPT

**Document status:** product and technical concept for the baseline production-ready v1.0  
**Language:** English  
**Basis:** `README.md`, the interactive HTML UI prototype, and the `Provereno Evidence Workspace` pitch deck  
**Purpose:** define the product model, architectural principles, v1.0 scope, core domain entities, and the implementation path from the existing prototype to a production-ready baseline release.

---

## 1. Executive summary

**Provereno Evidence Workspace** is an open-source, self-hosted system for preserving, organizing, reviewing, and publishing verifiable web evidence for independent newsrooms, fact-checking teams, investigative projects, and NGOs.

The system is designed as an editorial layer on top of the `opensanctions/pravda` web-capture engine powered by Playwright. It should allow an editor without terminal access or specialized archival expertise to:

1. submit a web page, post, or a batch of URLs;
2. perform a controlled browser capture;
3. preserve multiple independent representations of the source;
4. record timestamps, HTTP metadata, and capture conditions;
5. calculate cryptographic checksums of artifacts;
6. keep the evidence package within the newsroom's own infrastructure;
7. attach collections, tags, and editorial notes;
8. review the evidence;
9. optionally publish a safe public evidence link;
10. export a portable forensic package;
11. monitor later availability of the original URL;
12. maintain a durable audit trail of user and system actions.

The central product principle is:

> **Do not merely archive a page; convert a captured state of a source into manageable, verifiable evidence suitable for newsroom workflows.**

The baseline architecture should remain easy to deploy and operate: **FastAPI + PostgreSQL + server-side UI + worker processes + Pravda/Playwright + local artifact storage + Nginx + Docker Compose**.

The priority for v1.0 is not feature expansion. It is hardening the existing prototype into a dependable production product: automated tests, durable jobs, security, backup/restore, WARC support, auditability, browser-capture isolation, predictable upgrades, and pilot deployments in real newsrooms.

---

# 2. Source material and interpretation boundaries

This concept is derived from three project artifacts.

## 2.1. README

The README explicitly defines or proposes:

- Python 3.11+;
- FastAPI;
- PostgreSQL 15;
- GitHub OAuth;
- `admin` and `editor` roles;
- capture through `opensanctions/pravda` / Playwright;
- PostgreSQL `LISTEN/NOTIFY` for background jobs;
- SSE progress updates;
- collections and tags;
- CSV batch import of up to 500 URLs;
- forensic receipts;
- PNG + MHTML + JSON metadata + SHA-256;
- public evidence viewer;
- URL monitoring;
- append-only audit log;
- Jinja2 SSR;
- Docker Compose + Nginx;
- AGPL-3.0 licensing.

## 2.2. HTML prototype

The prototype confirms the main product/navigation model:

- Dashboard;
- New Capture;
- Jobs Queue;
- Snapshots;
- Snapshot Detail;
- Collections & Tags;
- Public Viewer;
- Forensic Receipt;
- Settings.

It also establishes important UX principles:

- private by default;
- publishing only after an explicit editorial decision;
- safe screenshot preview instead of executing archived HTML/MHTML;
- live job progress;
- batch workflows;
- origin URL status;
- light/dark themes;
- responsive/mobile layouts.

## 2.3. Pitch deck

The pitch deck adds critical product and operational context:

- the target customer is typically a newsroom or NGO of roughly 5–50 people;
- self-hosting is part of the value proposition;
- the product addresses disappearing and silently changing web sources;
- private evidence is important for sensitive investigations;
- a working prototype already exists;
- the main development objective is prototype → production;
- automated tests, CI/CD, security review, backup/restore, and WARC are explicitly required production tasks;
- pilots in 3–5 newsrooms are planned;
- the sustainability model is free AGPL code plus paid installation, managed hosting, updates, and support.

## 2.4. Architectural recommendations in this document

Some decisions below are **engineering recommendations rather than direct requirements from the source documents**. They include:

- separating `Source`, `Capture`, `Artifact`, and `Publication`;
- using a durable jobs table with `FOR UPDATE SKIP LOCKED`;
- treating `LISTEN/NOTIFY` as a wake-up mechanism rather than the queue itself;
- running web / worker / scheduler as separate processes;
- introducing an Evidence Manifest;
- creating a storage abstraction;
- SSRF defense and capture-browser network isolation;
- separating immutable evidence from mutable editorial metadata.

These recommendations should be validated against the current prototype during the implementation audit.

---

# 3. Problem statement

A web source is not a stable object.

It can:

- disappear;
- be edited without notice;
- move to a different URL;
- begin redirecting;
- become inaccessible without a VPN;
- move behind authentication;
- disappear from a social platform;
- change while keeping the same URL;
- block external archiving robots.

For journalism and fact-checking, a live URL alone is therefore not sufficient evidence of what existed at the moment a claim was checked.

Typical failure mode:

```text
A newsroom publishes a story
        │
        ├── links to a source
        │
        └── days later the source is changed or deleted
                         │
                         ▼
        reader / lawyer / editor can no longer verify
        the original context
```

Public archive services solve only part of the problem:

- sensitive evidence cannot always be sent to a third party;
- capture may fail for technical reasons;
- modern social platforms and JavaScript-heavy applications are difficult to archive;
- there is no integrated editorial workflow;
- there is no local access control;
- there are no newsroom-native collections, notes, roles, or audit trail;
- the newsroom does not control the external service or its availability.

---

# 4. Product hypothesis

The target user is a small or medium-sized newsroom / NGO that:

- regularly references content likely to disappear or change;
- wants to control where evidence is stored;
- does not have a dedicated archival engineer;
- does not want to build and operate complex archival infrastructure;
- needs collaborative team workflows;
- sometimes needs to publish evidence for readers, partners, or legal review;
- prefers open source and independent self-hosting.

The core competitive advantage of Provereno Evidence Workspace should therefore be **not the crawler itself, but a simple editorial workflow around reliable capture and preservation**.

---

# 5. Product scope

## 5.1. Baseline v1.0 scope

### Capture

- single-URL manual capture;
- CSV batch capture;
- durable queue;
- retries;
- progress events;
- concurrency limits;
- capture through Pravda/Playwright.

### Evidence preservation

- PNG screenshot;
- MHTML;
- structured metadata JSON;
- WARC/WARC.GZ;
- SHA-256;
- evidence manifest;
- capture provenance.

### Editorial workspace

- users;
- roles;
- collections;
- tags;
- notes;
- search/filter;
- review state;
- private by default.

### Publication

- explicit Publish action;
- public evidence page;
- screenshot preview;
- timestamp;
- source URL;
- checksums;
- origin availability state;
- safe downloads;
- unpublish/revoke.

### Forensic export

- ZIP package;
- receipt HTML;
- receipt PDF;
- screenshot;
- MHTML;
- WARC;
- metadata;
- manifest;
- SHA256SUMS.

### Operations

- Docker Compose;
- Nginx;
- HTTPS-ready deployment;
- database migrations;
- backup;
- restore;
- upgrade procedure;
- health checks;
- structured logging.

### Security

- GitHub OAuth;
- RBAC;
- Secure/HttpOnly cookies;
- SSRF protection;
- safe artifact serving;
- browser isolation;
- input validation;
- rate/concurrency controls;
- security review.

### Quality

- unit tests;
- integration tests;
- E2E tests;
- security tests;
- CI/CD.

---

## 5.2. Explicitly not P0 for v1.0

To avoid turning prototype hardening into an open-ended platform project, the following should not be mandatory for the baseline release:

- Kubernetes;
- microservices;
- multi-tenant SaaS;
- Elasticsearch/OpenSearch;
- RabbitMQ/Kafka;
- AI content analysis;
- advanced semantic diffing;
- browser extension;
- full end-user CLI;
- per-artifact application-level encryption;
- mandatory cryptographic manifest signatures;
- distributed capture clusters;
- a separate SPA frontend.

The architecture should not prevent these features later, but v1.0 must not depend on them.

---

# 6. Architectural principles

## 6.1. Modular monolith

The baseline product should remain a **modular monolith**, not a microservice system.

One Python codebase and one primary PostgreSQL database, with multiple runtime processes:

```text
web
worker
scheduler
```

This isolates background work without introducing distributed-system complexity.

## 6.2. Private by default

A completed capture never becomes public automatically.

```text
Capture completed
      │
      ▼
   PRIVATE
      │
      ▼
Editorial review
      │
      ├── remain private
      │
      └── publish
```

## 6.3. Immutable evidence, mutable editorial context

The system must distinguish between:

### Immutable

- capture URL;
- timestamps;
- HTTP metadata;
- browser/capture provenance;
- artifacts;
- checksums;
- manifest.

### Mutable

- title;
- note;
- tags;
- collections;
- review state;
- publication status.

Editorial edits must not rewrite the forensic capture core.

## 6.4. Safe rendering

Archived MHTML/HTML must never be executed inside the public viewer.

The viewer may display:

- screenshot;
- textual metadata;
- hashes;
- download links.

MHTML and WARC are downloaded as attachments.

## 6.5. Durable state

Critical job state is stored in PostgreSQL. `LISTEN/NOTIFY` must not be the only queue mechanism.

## 6.6. Self-hosting first

For v1.0, the preferred deployment model is:

```text
one newsroom = one deployment
```

---

# 7. High-level architecture

```text
                              INTERNET
                                  │
                                  ▼
                           ┌─────────────┐
                           │    Nginx    │
                           │ TLS / proxy │
                           └──────┬──────┘
                                  │
                                  ▼
                    ┌────────────────────────┐
                    │       FastAPI          │
                    │                        │
                    │ SSR pages + REST API   │
                    │ Auth / RBAC            │
                    │ SSE endpoints          │
                    └───────────┬────────────┘
                                │
                   ┌────────────▼────────────┐
                   │      PostgreSQL         │
                   │                         │
                   │ Users / Sources         │
                   │ Captures / Artifacts    │
                   │ Jobs / Batches          │
                   │ Collections / Tags      │
                   │ Publications            │
                   │ Audit                   │
                   └────────────┬────────────┘
                                │
              ┌─────────────────┼────────────────┐
              │                 │                │
              ▼                 ▼                ▼
       ┌─────────────┐   ┌─────────────┐  ┌─────────────┐
       │ Capture     │   │ Scheduler   │  │ Export      │
       │ worker      │   │ / monitor   │  │ worker      │
       └──────┬──────┘   └─────────────┘  └─────────────┘
              │
              ▼
       ┌─────────────┐
       │   Pravda    │
       │ Playwright  │
       └──────┬──────┘
              │
              ▼
         External Web

                 Artifacts
                    │
                    ▼
             ┌──────────────┐
             │ Filesystem   │
             │ Evidence     │
             │ Storage      │
             └──────────────┘
```

---

# 8. Components

## 8.1. Nginx

Responsibilities:

- TLS termination;
- HTTP → HTTPS redirects;
- reverse proxy to FastAPI;
- upload size limits;
- security headers;
- cache policy;
- safe serving of explicitly approved static assets.

It must not expose evidence directories directly.

## 8.2. FastAPI application

Responsibilities:

- server-rendered pages;
- REST API;
- authentication;
- sessions;
- permission enforcement;
- editorial CRUD;
- job creation;
- public evidence pages;
- SSE streams;
- audit event recording.

The request-serving process must not perform heavy browser captures itself.

## 8.3. PostgreSQL

Stores:

- users;
- editorial state;
- capture metadata;
- artifact metadata;
- durable jobs;
- batches;
- audit events;
- publication state;
- monitoring state.

It should not be the primary binary store for MHTML/WARC/PNG.

## 8.4. Capture worker

Claims capture jobs, invokes the capture engine, builds evidence artifacts, and persists final state.

## 8.5. Scheduler / monitor

Responsible for:

- URL probes;
- retry recovery;
- stale-job detection;
- scheduled maintenance;
- optional periodic integrity checks.

## 8.6. Pravda adapter

Pravda should be hidden behind an internal capture-engine interface.

```python
class CaptureEngine:
    async def capture(self, request: CaptureRequest) -> CaptureResult:
        ...
```

This keeps the domain layer independent from a specific capture implementation.

## 8.7. Artifact Store

The v1.0 implementation should use a local filesystem volume.

Internal interface:

```python
class ArtifactStore:
    async def put(...): ...
    async def open(...): ...
    async def exists(...): ...
```

An S3-compatible backend can be introduced later.

---

# 9. Domain model

## 9.1. Source

Represents the logical web source.

```text
Source
------
id
canonical_url
domain
source_type
created_at
```

A source may have multiple captures.

```text
Source
 ├── Capture 1
 ├── Capture 2
 └── Capture 3
```

## 9.2. Capture

Represents a preserved state of a source at a specific point in time.

```text
Capture
-------
id
source_id
requested_by
requested_at
started_at
captured_at
finished_at
status
engine
engine_version
browser
browser_version
http_status
final_url
capture_condition
condition_met
error_code
error_message
manifest_sha256
```

Once successfully completed, a Capture is treated as an immutable forensic record.

## 9.3. Artifact

```text
Artifact
--------
id
capture_id
type
storage_backend
storage_key
mime_type
size_bytes
sha256
created_at
```

v1.0 artifact types:

- screenshot;
- mhtml;
- warc;
- metadata;
- manifest;
- receipt_html;
- receipt_pdf.

## 9.4. Editorial Metadata

A separate record or related table set.

```text
CaptureEditorial
----------------
capture_id
title
note
review_state
updated_by
updated_at
```

## 9.5. Collection

A newsroom investigation/project grouping.

Capture ↔ collection should be many-to-many.

## 9.6. Tag

Normalized tags with canonical name/slug and uniqueness constraints.

## 9.7. Publication

Public visibility is not a boolean field on Capture. It is a separate entity.

```text
Publication
-----------
id
capture_id
public_slug
status
published_at
published_by
revoked_at
revoked_by
```

States:

```text
draft
published
revoked
```

## 9.8. Job

```text
Job
---
id
type
entity_id
status
priority
attempt_count
max_attempts
available_at
worker_id
heartbeat_at
created_at
started_at
finished_at
last_error
```

## 9.9. Batch

Groups jobs created by a CSV import.

## 9.10. Audit Event

```text
AuditEvent
----------
id
timestamp
actor_type
actor_id
action
entity_type
entity_id
request_id
ip_address
user_agent
data_json
```

Audit records are not deletable through the UI.

---

# 10. Core data relationships

```text
User
 │
 ├──────── requests ────────┐
 │                           ▼
 │                        Capture
 │                           │
 │                           ├──────── Artifact
 │                           │
 │                           ├──────── Editorial Metadata
 │                           │
 │                           ├──────── Collection (*)
 │                           │
 │                           ├──────── Tag (*)
 │                           │
 │                           └──────── Publication (0..n)
 │
 └──────── AuditEvent

Source
  │
  └──────── Capture (*)

Batch
  │
  └──────── Job (*)
```

---

# 11. Capture workflow

## 11.1. Single URL

```text
Editor submits URL
        │
        ▼
Normalize URL
        │
        ▼
Security validation
        │
        ▼
Create/reuse Source
        │
        ▼
Create Capture
        │
        ▼
Create durable Job
        │
        ▼
Notify worker
        │
        ▼
Worker claims Job
        │
        ▼
Pravda / Playwright capture
        │
        ▼
Persist raw artifacts
        │
        ▼
Generate WARC / metadata
        │
        ▼
Compute SHA-256
        │
        ▼
Generate manifest
        │
        ▼
Persist artifact records
        │
        ▼
Capture = DONE
        │
        ▼
Editorial review
```

## 11.2. Job state machine

```text
created
   │
   ▼
queued
   │
   ▼
claimed
   │
   ▼
capturing
   │
   ▼
processing
   │
   ▼
hashing
   │
   ▼
persisting
   │
   ├────────────► failed
   │                 │
   │                 ▼
   │             retry_wait
   │                 │
   └─────────────────┘
   │
   ▼
done
```

Final states:

- `done`;
- `failed`;
- `cancelled`.

## 11.3. Heartbeats and orphan recovery

Workers update `heartbeat_at`.

The scheduler detects stale jobs:

```text
status in (claimed, capturing, processing)
AND heartbeat_at older than threshold
```

After validation, the job is retried or marked failed.

---

# 12. Durable PostgreSQL queue

The README proposes PostgreSQL `LISTEN/NOTIFY`. For production, use:

```text
Jobs table = source of truth
LISTEN/NOTIFY = low-latency wake-up signal
```

Claim query:

```sql
SELECT *
FROM jobs
WHERE status = 'queued'
  AND available_at <= now()
ORDER BY priority DESC, created_at
FOR UPDATE SKIP LOCKED
LIMIT 1;
```

Benefits:

- lost notifications do not lose jobs;
- worker restart does not corrupt the queue;
- multiple workers safely compete;
- retries are straightforward;
- Redis/RabbitMQ are unnecessary for the initial scale.

---

# 13. Batch import

CSV import of up to 500 URLs should use a two-phase workflow.

```text
Upload CSV
   │
   ▼
Parse
   │
   ▼
Preview
   │
   ▼
Validate
   │
   ▼
Confirm
   │
   ▼
Create Batch + Jobs
```

Preview should identify:

- valid URLs;
- malformed URLs;
- duplicates;
- unsupported schemes;
- blocked/private targets;
- parsed collection/tags.

Importing 500 URLs must **not** launch 500 Chromium sessions simultaneously.

Concurrency is configuration-controlled.

---

# 14. Evidence artifacts

## 14.1. PNG screenshot

Purpose:

- visual human verification;
- safe public preview;
- fast newsroom review.

## 14.2. MHTML

Purpose:

- browser-oriented representation;
- portable preservation of DOM/resources.

Must not be rendered inline on the public site.

## 14.3. WARC/WARC.GZ

Purpose:

- durable archival representation;
- interoperability with the web-archiving ecosystem;
- long-term preservation.

WARC is an explicit production requirement from the pitch deck.

## 14.4. Metadata JSON

Should include:

- source URL;
- final URL;
- timestamps;
- HTTP status;
- headers;
- redirect chain;
- capture condition;
- engine version;
- browser version;
- viewport;
- locale/timezone when applicable;
- errors/warnings.

## 14.5. Evidence Manifest

The manifest is the central index of an evidence package.

Example:

```json
{
  "schema": "provereno-evidence/1",
  "capture_id": "01K...",
  "source_url": "https://example.org/article",
  "captured_at": "2027-03-17T18:43:11Z",
  "engine": {
    "name": "pravda",
    "version": "x.y.z"
  },
  "artifacts": [
    {
      "path": "screenshot.png",
      "sha256": "..."
    },
    {
      "path": "page.mhtml",
      "sha256": "..."
    },
    {
      "path": "archive.warc.gz",
      "sha256": "..."
    }
  ]
}
```

Canonical manifest + SHA-256 is sufficient for v1.0. Digital signatures can be added later.

---

# 15. Artifact storage

Recommended layout:

```text
data/
└── captures/
    └── <capture-id>/
        ├── evidence/
        │   ├── screenshot.png
        │   ├── page.mhtml
        │   └── archive.warc.gz
        ├── metadata/
        │   ├── capture.json
        │   └── http.json
        └── integrity/
            ├── manifest.json
            └── SHA256SUMS
```

The database stores `storage_key`, not an absolute host path.

---

# 16. Forensic export

Portable package:

```text
evidence-<id>.zip
├── README.txt
├── receipt.html
├── receipt.pdf
├── evidence/
│   ├── screenshot.png
│   ├── page.mhtml
│   └── archive.warc.gz
├── metadata/
│   ├── capture.json
│   └── http.json
├── manifest.json
└── SHA256SUMS
```

Verification:

```bash
sha256sum -c SHA256SUMS
```

The receipt should explain:

- which URL was preserved;
- when;
- by whom/which system;
- which artifacts are included;
- how checksums can be verified;
- the current source availability state at receipt-generation time.

---

# 17. Public Evidence Viewer

The public viewer is a separate read-only presentation layer.

## Displays

- source URL;
- capture timestamp;
- publisher/organisation;
- screenshot;
- hash/manifest information;
- current origin state;
- explicitly allowed downloads;
- evidence identifier.

## Does not

- execute MHTML;
- embed archived HTML in an iframe;
- expose private notes;
- reveal internal usernames unless explicitly intended;
- expose administrative APIs.

## HTTP hardening

For MHTML/WARC downloads:

```http
Content-Disposition: attachment
X-Content-Type-Options: nosniff
```

The public viewer should use a strict CSP.

---

# 18. URL monitoring

Monitoring is a support function, not a replacement capture engine.

Baseline states:

```text
online
redirected
deleted
blocked
unreachable
unknown
```

Probe sequence:

```text
HEAD
 │
 ├── usable response → persist state
 │
 └── unsupported/ambiguous
          │
          ▼
     bounded GET probe
```

Availability/status monitoring is sufficient for v1.0. Reliable semantic change detection may be added later.

---

# 19. Search and filtering

Filters:

- URL/domain;
- collection;
- tag;
- author;
- capture date;
- capture status;
- review state;
- publication state;
- origin state.

For expected scale, PostgreSQL is sufficient using:

- B-tree indexes;
- GIN;
- `pg_trgm`;
- `tsvector` when needed.

Elasticsearch is not required for v1.0.

---

# 20. Authentication and RBAC

## 20.1. GitHub OAuth

The README defines access policies based on:

- allowed organizations;
- allowed logins.

Environment configuration should control admission policy, while users are persisted in the database.

```text
User
----
id
github_id
github_login
display_name
avatar_url
role
enabled
last_login_at
```

## 20.2. v1.0 roles

To keep the baseline workflow simple:

### admin

- users/settings;
- all captures;
- publish/unpublish;
- deletion policies;
- audit;
- system operations.

### editor

- create captures;
- collections/tags;
- notes;
- review;
- publish if product policy permits editors to do so.

A dedicated `reviewer` role may be introduced later if pilots require separation of duties.

---

# 21. Audit log

The audit log should be append-only at the application level.

Minimum event set:

```text
user.login
user.logout
capture.requested
capture.completed
capture.failed
capture.exported
collection.created
tag.added
tag.removed
publication.created
publication.revoked
settings.changed
backup.created
restore.performed
```

Audit UI is admin-only.

A future version may add hash chaining of audit events.

---

# 22. Security model

This is a critical part of the product because the system intentionally opens untrusted URLs.

## 22.1. SSRF

Block access to at least:

```text
127.0.0.0/8
10.0.0.0/8
172.16.0.0/12
192.168.0.0/16
169.254.0.0/16
::1
fc00::/7
fe80::/10
```

Validation must happen:

- before capture;
- after DNS resolution;
- after every redirect.

## 22.2. URL schemes

Allow by default:

```text
http
https
```

Block:

```text
file:
ftp:
data:
javascript:
chrome:
```

## 22.3. Browser isolation

Pravda/Playwright container should run with:

- non-root user;
- no Docker socket;
- no host networking;
- no unnecessary database-network access;
- CPU/memory/PID limits;
- read-only filesystem where practical;
- dedicated temporary/writable storage.

## 22.4. Application security

- CSRF protection for state-changing SSR forms;
- secure sessions;
- HTTPS;
- backend permission checks;
- path traversal protection;
- filename normalization;
- CSP;
- safe Content-Disposition;
- dependency scanning.

## 22.5. Sensitive evidence

A private capture must not become accessible merely by knowing its UUID.

Public URLs may resolve only through explicit `Publication` records.

---

# 23. Deployment

Production instance:

```text
server/
├── docker-compose.yml
├── .env
├── data/
├── backups/
└── nginx/
```

Services:

```text
nginx
app
worker
scheduler
postgres
pravda
```

`worker` and `scheduler` may use the same Docker image as the application with different startup commands.

---

# 24. Backup and restore

Backup is a P0 production-readiness requirement.

It must include:

- PostgreSQL dump;
- artifacts;
- system metadata;
- checksums;
- version information.

Example:

```text
backup-2027-03-17/
├── database.dump
├── artifacts.tar.zst
├── backup-manifest.json
└── SHA256SUMS
```

A key quality criterion:

> **A backup script is not enough. Restore must be tested.**

Integration scenario:

```text
create capture
    ↓
backup
    ↓
restore into clean environment
    ↓
verify DB records
    ↓
verify artifact SHA-256
```

---

# 25. Upgrade model

Required:

- semantic versioning;
- Alembic migrations;
- pre-upgrade backup;
- migration validation;
- release notes;
- documented rollback limitations.

Support tooling should expose:

```text
Application version
Database schema version
Pravda version
Storage backend
```

---

# 26. Health and observability

Endpoints:

```text
/health/live
/health/ready
```

`ready` should verify at least:

- database;
- artifact store;
- Pravda;
- worker heartbeat.

Structured logs should include correlation fields:

```text
request_id
user_id
job_id
capture_id
batch_id
```

Example:

```json
{
  "level": "INFO",
  "event": "capture.completed",
  "capture_id": "01K...",
  "duration_ms": 8241
}
```

---

# 27. UI architecture

For the baseline release, server-side rendering remains preferable.

Recommended stack:

```text
FastAPI
Jinja2
HTML/CSS design system derived from the prototype
small JavaScript layer
SSE
optional HTMX/Alpine.js
```

React/Next/Vue are not required for the current feature set.

Template structure:

```text
templates/
├── base.html
├── dashboard.html
├── capture.html
├── jobs.html
├── snapshots.html
├── snapshot_detail.html
├── collections.html
├── settings.html
├── public/
│   └── evidence.html
└── components/
    ├── badge.html
    ├── job_row.html
    ├── snapshot_row.html
    └── pagination.html
```

The existing HTML mockup should be reused as the design/UI baseline rather than discarded.

---

# 28. API outline

Internal/public API should use a version prefix:

```text
/api/v1/
```

Example endpoints:

```text
POST   /api/v1/captures
GET    /api/v1/captures/{id}
GET    /api/v1/captures

GET    /api/v1/jobs
GET    /api/v1/jobs/{id}
GET    /api/v1/jobs/{id}/events

POST   /api/v1/batches
GET    /api/v1/batches/{id}

POST   /api/v1/collections
PATCH  /api/v1/collections/{id}

POST   /api/v1/captures/{id}/tags
DELETE /api/v1/captures/{id}/tags/{tag}

POST   /api/v1/captures/{id}/publish
POST   /api/v1/captures/{id}/unpublish

GET    /api/v1/captures/{id}/export
```

Server-rendered pages may call application services directly; they do not need loopback HTTP calls to the REST API.

---

# 29. Proposed repository structure

```text
provereno/
├── pyproject.toml
├── alembic.ini
├── docker-compose.yml
├── .env.example
│
├── src/provereno/
│   ├── main.py
│   ├── config.py
│   │
│   ├── domain/
│   │   ├── sources.py
│   │   ├── captures.py
│   │   ├── artifacts.py
│   │   ├── collections.py
│   │   ├── publications.py
│   │   └── audit.py
│   │
│   ├── db/
│   │   ├── models.py
│   │   ├── session.py
│   │   └── repositories/
│   │
│   ├── capture/
│   │   ├── base.py
│   │   ├── pravda.py
│   │   ├── pipeline.py
│   │   └── warc.py
│   │
│   ├── storage/
│   │   ├── base.py
│   │   └── filesystem.py
│   │
│   ├── jobs/
│   │   ├── queue.py
│   │   ├── worker.py
│   │   └── events.py
│   │
│   ├── forensic/
│   │   ├── manifest.py
│   │   ├── receipt.py
│   │   └── export.py
│   │
│   ├── monitoring/
│   │   └── urls.py
│   │
│   ├── security/
│   │   ├── auth.py
│   │   ├── permissions.py
│   │   ├── sessions.py
│   │   └── urls.py
│   │
│   ├── api/
│   ├── pages/
│   ├── templates/
│   └── static/
│
├── migrations/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── e2e/
│   └── security/
│
├── deploy/
│   ├── nginx/
│   └── docker/
│
└── scripts/
    ├── install.sh
    ├── upgrade.sh
    ├── backup.sh
    ├── restore.sh
    └── healthcheck.sh
```

---

# 30. Testing strategy

## Unit

- URL normalization;
- SSRF checks;
- permissions;
- checksum generation;
- manifest generation;
- state transitions;
- retry policy.

## Integration

- PostgreSQL repositories;
- queue locking;
- Pravda adapter;
- artifact storage;
- WARC generation;
- export package;
- audit persistence.

## E2E

```text
login
→ create capture
→ wait for job
→ inspect evidence
→ add tags
→ publish
→ open public page
→ download package
→ verify hashes
```

## Security tests

- localhost/private-IP targets;
- DNS rebinding/redirect to private network;
- path traversal;
- unauthorized evidence access;
- dangerous MIME types;
- malformed CSV;
- session/RBAC bypass;
- artifact filename injection.

---

# 31. CI/CD

Pipeline:

```text
commit / PR
     │
     ▼
format/lint
     │
     ▼
type checks
     │
     ▼
unit tests
     │
     ▼
integration tests
     │
     ▼
Docker build
     │
     ▼
dependency/container scan
     │
     ▼
E2E
     │
     ▼
release candidate
```

A migration test from the existing prototype schema/data should exist before v1.0.

---

# 32. Implementation stages to baseline v1.0

## Stage 0. Existing prototype audit

**Goal:** determine what should be preserved and what must be refactored.

### Tasks

- inventory current modules;
- DB schema review;
- auth review;
- audit-log review;
- Pravda integration review;
- filesystem layout review;
- background task review;
- threat model;
- dependency audit;
- document current user flows.

### Output

- Architecture Decision Record set;
- migration plan;
- list of prototype shortcuts;
- baseline test fixtures.

---

## Stage 1. Domain/data model

### Tasks

- introduce Source;
- normalize Capture;
- introduce Artifact;
- separate Editorial Metadata;
- many-to-many Collections;
- Tags;
- Publication;
- Job/Batch;
- AuditEvent;
- Alembic migrations.

### Acceptance criteria

- current prototype data can be migrated;
- evidence metadata is independent of UI metadata;
- capture has a stable identifier;
- publication is independent from capture.

---

## Stage 2. Durable jobs and workers

### Tasks

- jobs table;
- `SKIP LOCKED` claiming;
- retry policy;
- worker heartbeat;
- orphan recovery;
- LISTEN/NOTIFY wakeup;
- SSE events;
- batch states;
- concurrency configuration.

### Acceptance criteria

- worker restart does not lose jobs;
- failed captures can be retried safely;
- two workers cannot execute the same job;
- UI receives progress.

---

## Stage 3. Evidence pipeline

### Tasks

- Pravda adapter;
- screenshot persistence;
- MHTML persistence;
- metadata normalization;
- WARC generation/export;
- SHA-256;
- manifest;
- filesystem storage abstraction;
- integrity verification service/command.

### Acceptance criteria

- every successful capture creates the complete minimum evidence set;
- SHA-256 values are reproducible;
- manifest unambiguously references artifacts;
- WARC is included in export.

---

## Stage 4. Editorial workspace

### Tasks

- Dashboard;
- capture form;
- jobs queue;
- snapshot list;
- snapshot detail;
- collections;
- tags;
- notes;
- review state;
- filters/search;
- batch import preview.

### Acceptance criteria

- the main newsroom workflow works without CLI;
- UI follows the prototype;
- all state-changing operations are permission checked.

---

## Stage 5. Publication and forensic export

### Tasks

- Publication model;
- publish/unpublish workflow;
- public viewer;
- OpenGraph metadata;
- safe downloads;
- receipt HTML;
- receipt PDF;
- ZIP generation;
- SHA256SUMS;
- public/private access tests.

### Acceptance criteria

- private captures cannot be opened publicly;
- public viewer does not execute archived active content;
- exported package passes checksum verification.

---

## Stage 6. Authentication, RBAC, audit

### Tasks

- GitHub OAuth hardening;
- allowed org/logins;
- persisted user DB;
- admin/editor permissions;
- session security;
- complete audit coverage;
- audit CSV export.

### Acceptance criteria

- unauthorized users cannot sign in;
- editor/admin boundaries behave correctly;
- significant actions appear in audit;
- audit cannot be deleted through the UI.

---

## Stage 7. Security hardening

### Tasks

- SSRF defenses;
- redirect validation;
- DNS/IP checks;
- browser-container isolation;
- resource limits;
- CSP/security headers;
- upload validation;
- safe Content-Disposition;
- secret handling;
- dependency/container scanning.

### Acceptance criteria

- private/internal targets are blocked;
- archived HTML cannot execute JavaScript in the public viewer;
- capture container cannot reach sensitive host resources.

---

## Stage 8. Operations

### Tasks

- production Docker Compose;
- Nginx config;
- TLS documentation;
- health endpoints;
- structured logs;
- backup script;
- restore script;
- restore test;
- upgrade script;
- migration checks.

### Acceptance criteria

- clean installation is documented;
- backups restore into a fresh environment;
- upgrades do not require manual DB edits.

---

## Stage 9. Automated quality

### Tasks

- unit suite;
- integration suite;
- E2E suite;
- security regression suite;
- CI;
- release builds;
- coverage of critical paths.

### Acceptance criteria

- broken core workflows block a PR;
- capture/export/public-access paths are automatically tested.

---

## Stage 10. Release Candidate

### Tasks

- external/internal security review;
- documentation;
- admin runbook;
- disaster-recovery runbook;
- onboarding guide;
- known limitations;
- release checklist.

### Output

`v1.0.0-rc1`.

---

## Stage 11. Pilots

Deploy to 3–5 newsrooms.

Measure:

- capture success rate;
- median/p95 capture duration;
- failed jobs;
- total captures;
- batch usage;
- public evidence links;
- exported packages;
- later deleted/changed origins;
- deployment time;
- backup/restore failures;
- support incidents;
- usability issues.

---

## Stage 12. Baseline v1.0

After pilots:

- fix P0/P1 defects;
- freeze schema v1;
- finalize upgrade process;
- finalize docs;
- ship stable Docker images;
- publish v1.0.

---

# 33. Baseline v1.0 definition of done

The product should not be considered production-ready until all of the following are true.

### Capture

- jobs are durable;
- retries are predictable;
- browser isolation works;
- batch imports cannot overload the instance.

### Evidence

- PNG/MHTML/WARC/metadata;
- SHA-256;
- manifest;
- reproducible verification.

### Privacy

- private by default;
- no public access without Publication;
- correct RBAC.

### Public viewer

- safe rendering;
- no active archive execution;
- hashes/timestamp visible.

### Operations

- installation documented;
- backup works;
- restore tested;
- upgrade documented;
- migrations automated.

### Security

- SSRF controls;
- secure sessions;
- security headers;
- browser resource limits;
- dependency review.

### Quality

- automated tests;
- CI;
- core E2E flow;
- security regression suite.

---

# 34. Architectural risks

## 34.1. Capture engine reliability

Modern sites may require authentication, anti-bot handling, or platform-specific logic.

**Approach:** do not promise universal capture; expose capture failures and engine limitations; keep an adapter boundary.

## 34.2. WARC generation complexity

Converting preserved browser output to WARC is not necessarily equivalent to a complete network-level capture.

**Approach:** explicitly define what the v1.0 WARC contains and what it guarantees.

## 34.3. Disk growth

PNG + MHTML + WARC can consume substantial storage.

**Approach:** metrics, configurable retention policies, disk warnings, and capacity-planning documentation.

## 34.4. Browser attack surface

The capture engine intentionally opens hostile content.

**Approach:** isolation, SSRF protection, resource limits, and timely Chromium updates.

## 34.5. False forensic claims

SHA-256 proves that a file has not changed since the digest was computed; by itself it does not legally prove who captured it or the trusted time of capture.

**Approach:** use precise terminology. Stronger guarantees can later use signatures and trusted timestamping.

## 34.6. Scope creep

There is a risk of turning the product into crawler + CMS + OSINT platform + AI fact-checker.

**Approach:** keep the product core narrow:

```text
capture
→ preserve
→ organize
→ review
→ publish/export
```

---

# 35. Architecture Decision Records to create

Before active implementation, create at least:

1. **ADR-001:** Modular monolith vs microservices.
2. **ADR-002:** PostgreSQL durable queue.
3. **ADR-003:** Capture-engine adapter boundary.
4. **ADR-004:** Evidence artifact set: PNG/MHTML/WARC/JSON.
5. **ADR-005:** Immutable Capture vs mutable Editorial Metadata.
6. **ADR-006:** Publication as a separate entity.
7. **ADR-007:** Filesystem artifact storage for v1.0.
8. **ADR-008:** Private-by-default policy.
9. **ADR-009:** WARC implementation strategy.
10. **ADR-010:** Backup/restore format.

---

# 36. Future extensions after v1.0

Once the core is stable, consider:

- S3-compatible artifact storage;
- browser extension;
- command-line capture client;
- cryptographic manifest signatures;
- trusted timestamping;
- semantic content diff;
- scheduled recapture;
- notifications;
- platform-specific capture adapters;
- API tokens;
- organization-specific SSO;
- stronger encryption policies;
- optional managed multi-instance control plane;
- external archival replication.

These must not delay the baseline production release.

---

# 37. Final product model

Provereno Evidence Workspace should not be implemented as merely a “GUI for Pravda”. It should be treated as an **editorial evidence lifecycle system**.

```text
        FIND
         │
         ▼
      CAPTURE
         │
         ▼
      PRESERVE
         │
         ▼
       VERIFY
         │
         ▼
      ORGANIZE
         │
         ▼
       REVIEW
         │
         ├──────────────► KEEP PRIVATE
         │
         ▼
      PUBLISH
         │
         ▼
       EXPORT
         │
         ▼
      PRESERVE
      LONG-TERM
```

`Pravda/Playwright` is the capture engine.  
`PostgreSQL` stores workflow state.  
`Artifact Store` stores evidence.  
`FastAPI UI` provides newsroom interaction.  
`Audit`, `hashes`, `manifest`, `backup`, and `WARC` provide integrity and durability.

The primary objective before v1.0 is **not to add as many features as possible, but to make the existing prototype safe to deploy in a real newsroom, trustworthy for important evidence, recoverable after failures, and operable without constant developer involvement.**
