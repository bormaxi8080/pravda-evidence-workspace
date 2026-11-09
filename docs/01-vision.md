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
the current prototype uses Playwright directly. [ADR-002](decisions/0002-v0-scope-and-topology.md)
selects an isolated direct-Playwright runner for V0 behind a replaceable contract;
Pravda remains a later evaluated adapter candidate. Runtime isolation is unqualified.

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

Selected V0 decisions, parameters and contracts now live in
[the baseline register](requirements/13-selected-v0-baseline.md) and ADR-002–004.
Empirical build/isolation, runtime/migration/restore evidence, production WARC
fidelity and measured support objectives remain work, not completed properties.

## Evidence for readiness

The core acceptance flow is login, capture, await completion, inspect evidence,
organize/review, publish, open public viewer, export and verify hashes. Also prove
denied private access, unpublish behavior, failure/retry, worker restart, malicious
URL rejection and restore into a clean deployment. Metrics should track capture
success and latency, queue recovery, storage growth, restore correctness and editor
completion of the workflow; set numeric targets with pilot constraints later.

The [requirements package](requirements/README.md) expands this vision into a
selected V0 boundary, architecture, functional/nonfunctional requirements,
documentation work packages, acceptance scenarios and a derived implementation
roadmap. The [original specification brief](05-next-design-phase.md) remains context.
The [four-wave review](requirements/19-documentation-review.md) and
[18 assignable work packages](requirements/18-assignable-work-packages.md) record
design handoff and pending qualification. The requirement package does not
implement or certify the target product. [ADR-005](decisions/0005-adopt-comparison-and-monitoring.md)
now adopts C0 Source history into V0 and C1–C4 comparison/profile/watch/delivery
into later stages, grounded in the [changedetection.io source review](reference/changedetection-io-review.md).
The [stage requirements and EWP-19–30](requirements/26-adoption-roadmap-and-acceptance.md)
define that continuation; visual/native-format and richer transport ideas remain deferred.

[ADR-006](decisions/0006-investigation-context-and-handoff.md) and the
[Hunchly comparison](reference/hunchly-comparison.md) extend the vision from storing
pages to preserving research context and handing off source-linked findings.
V0 gains explicit collection/rationale context at submission and independent shared
importance. Later H1–H4 add anchored annotations/tasks/views, private content search
and research cues, frozen selective reports and reviewed native case transfer.
An editor's assertion remains distinct from observed acquisition metadata; derived
crops/quotes remain distinct from immutable originals. Reports pin selected revisions
and inclusions rather than becoming a changing collection or an implicit public page.
[Investigation requirements and EWP-31–40](requirements/33-investigation-roadmap-and-acceptance.md)
define the staged continuation. Browser-session acquisition remains separate work.

[ADR-007](decisions/0007-browser-companion-acquisition.md) now selects that optional
browser channel: B0 explicitly hands a public URL to the server; B1 preserves a
user-selected local viewport/optional MHTML with client-claimed provenance; B2
assists recording a single foreground tab/origin with visible pause and reviewed
upload. These stages do not delay or become a dependency of baseline V0/production.
Private submitted bytes are verified on receipt, not represented as independently
witnessed server captures. [The browser delivery plan](requirements/38-companion-roadmap-and-acceptance.md)
defines permissions, expiring pairing, offline recovery, trust and release gates.

[ADR-008](decisions/0008-integrated-evidence-policy-and-delivery.md) consolidates
these branches into one consistent implementation boundary: purpose-specific
eligibility preserves acquisition/provenance distinctions; dependencies prevent
removed content from resurfacing; shared reservations protect the one-host model;
and qualified feature/schema gates control rollout/restore. The
[integrated contract and delivery catalogue](requirements/43-contract-catalog-and-delivery-gates.md)
refines the existing 158 requirements rather than expanding the product scope.

[ADR-009](decisions/0009-deployment-database-and-future-identity.md) and
[the technical/identity delivery plan](requirements/49-infrastructure-and-identity-delivery.md)
make Docker job isolation, PostgreSQL authority, deployment and maintenance concrete.
Future U1–U3 add explicit capability bundles, AccessSpace custody and qualified
federation/workload identities. V0 keeps the shared two-role newsroom; restricted
spaces do not pretend the trusted host/DB operator cannot access stored evidence.
