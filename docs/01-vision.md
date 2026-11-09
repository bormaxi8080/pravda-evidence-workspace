# Product vision

Date: 2026-11-09. Status: **synthesis for the next design phase**. Engineering
governance is adopted separately; this document does not accept every architectural
recommendation or claim production readiness.

## Purpose and users

Provereno Evidence Workspace is a self-hosted evidence lifecycle workspace for
newsrooms, fact-checkers, investigative teams and NGOs. The concept targets teams
of roughly 5–50 people and a pilot with 3–5 newsrooms. Those are design assumptions,
not verified capacity or deployment results.

The product's value is preserving a source in the newsroom's control and making
its capture understandable, reviewable and exportable after the live page changes
or disappears. An editor should complete this flow without a terminal:

```text
URL / CSV -> capture -> preserve -> verify -> organize -> review
                                                        |-> keep private
                                                        |-> publish / export
```

Publication is an explicit editorial decision. A checksum supports checking byte
integrity against a reference hash; it alone proves neither source truth, capture
authorship, trusted capture time nor legal admissibility.

## Foundation and sources

- [English concept](../concept/CONCEPT.en.md) and [Russian concept](../concept/CONCEPT.ru.md)
  describe the target lifecycle, data model, security, operations and release gates.
- [HTML prototype](../index.html) is a UI/design reference with simulated behavior.
- [Current source review](04-current-state.md) records the actual Python/Compose baseline.
- [README](../README.md) retains the inherited project description, with a current-status caveat.

The concept cites a pitch deck; no standalone deck was found in this checkout.
Its statements here are attributed to the concept, not an independently inspected deck.
The OA was inspected only for engineering structure; its SaaS/AI/research architecture
is not imported into this product.

## Target baseline

Prefer a modular Python monolith, FastAPI/Jinja server rendering, PostgreSQL,
separate worker/scheduler processes, a replaceable capture-engine boundary, local
artifact storage, Nginx and Docker Compose. The concept favors Pravda/Playwright;
the current prototype uses Playwright directly. Resolve the adapter choice in an ADR.

One newsroom per deployment is the initial operational model. Keep deployment
simple enough to install, upgrade, back up and restore without a permanent engineer.

Separate the intended domain responsibilities:

| Object | Purpose |
| --- | --- |
| Source | Identity and normalization of the original URL |
| Capture | A particular capture attempt and immutable provenance |
| Artifact | Stored bytes, media type, size, digest and storage key |
| Editorial metadata | Mutable title, notes, tags, collections and review |
| Publication | Explicit public projection and revocation, separate from capture |
| Job / Batch | Durable execution state, attempts, ownership and progress |
| Audit event | Accountable history of user/system actions |

These are target domain boundaries, not new microservices or implemented models.
Captured evidence and editorial edits must have independent histories. Failures,
incomplete captures, retries and unavailable artifacts must remain visible.

## Production outcomes

- PNG/MHTML/structured metadata/WARC with provenance, a manifest and verifiable hashes.
- Durable jobs, bounded concurrency, predictable retries and restart recovery.
- Private evidence, server-side role checks, secure sessions and safe downloads.
- Screenshot-based public viewer, explicit publication/revocation and portable export.
- Collections, tags, notes, review and useful search/filtering.
- Tested installation, migrations, backup/restore and upgrades with known rollback limits.
- Threat model, browser isolation, SSRF defenses and automated core-workflow checks.

Define WARC fidelity before implementation: a wrapper around MHTML is not necessarily
a faithful network capture. Define deletion/retention and publication cache revocation
before claiming irreversible preservation or effective withdrawal. URL monitoring
reports availability; reliable semantic change detection is a separate capability.

## Boundaries and open decisions

Multi-tenant SaaS, Kubernetes, distributed crawling, an SPA rewrite, AI fact-checking,
mandatory signatures, browser extensions and semantic diffs are outside the initial
critical path. Locus and the country OSINT catalog stay independent repositories;
no integration or cross-repository graph relationship is implied by MCP registration.

Next decisions: package/product naming and release migration; direct Playwright vs
Pravda adapter; evidence schemas/WARC strategy; queue/worker ownership; publication
and cache withdrawal; permissions/deletion; migration from prototype data; storage
consistency and recovery boundaries. Record alternatives and consequences as ADRs.

## Evidence for readiness

The core acceptance flow is login, capture, await completion, inspect evidence,
organize/review, publish, open public viewer, export and verify hashes. Also prove
denied private access, unpublish behavior, failure/retry, worker restart, malicious
URL rejection and restore into a clean deployment. Metrics should track capture
success and latency, queue recovery, storage growth, restore correctness and editor
completion of the workflow; set numeric targets with pilot constraints later.

The [requirements package](requirements/README.md) expands this vision into a
proposed V0 boundary, architecture, functional/nonfunctional requirements,
documentation work packages, acceptance scenarios and a derived implementation
roadmap. The [original specification brief](05-next-design-phase.md) remains context.
Architecture decisions and runtime qualification are still outstanding; the
requirement package does not implement or certify the target product.
