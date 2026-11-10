# ADR-002: Select V0 scope and process boundaries

Date: 2026-11-09. Status: **selected engineering baseline for implementation planning**.
Authority: the user instructed continuation of the four documentation waves.
This records engineering choices under that scope; no external reviewer sign-off,
runtime verification, release or deployment is claimed. Covers DEC-01/02/03/06.

## Decision

V0 serves one newsroom with shared internal evidence, admin/editor roles, editor
review and admin-only publication. Keep WARC, mandatory PDF, scheduled recapture,
content comparison, external notifications and authenticated-target browser steps
outside V0. Require privacy, bounded capture, durable state and clean restore in V0.

Keep one Python monolith at `provereno-ui/`, SSR/Jinja, PostgreSQL 16 and filesystem
storage. Select Python 3.12 and PostgreSQL 16. [ADR-012](0012-macos-development-and-linux-qualification.md)
supersedes the original Linux-first sequencing: macOS arm64/Docker Desktop is the
current development target; native Linux x86_64/Ubuntu 24.04 is a separate later
qualification iteration. Pin platform-specific dependency/browser/image digests
after install tests. The candidate 4 CPU/8 GiB/40 GiB Linux envelope is unmeasured;
Mac allocations must be recorded independently. Neither lane implies production readiness.

Separate edge, web, trusted worker/maintenance and browser runner. Reuse direct
Playwright behind CaptureEngine in an isolated runner for V0; do not build a Pravda
service simultaneously. Preserve a typed capability descriptor so unsupported
conditions fail explicitly. Pravda remains a future adapter candidate; selection
of Playwright is based on existing source and migration cost, not a comparative
benchmark or assertion about Pravda limitations.

The browser gets no application/DB/OAuth/session credentials or finalized artifact
volume. Network policy permits only the controlled egress proxy and established
control responses. Web/worker services can reach their required internal stores;
the browser cannot reach them by virtue of sharing a Compose network.

Retain package 1.1.0 in this documentation change. Compatible packaging fixes use
normal patch increments. The first incompatible schema/API runtime increment selects
package/component 2.0.0 with migration notes; Workspace product release remains a
separate null ledger value until an authorized release. V0 is not a version reset.

## Alternatives and consequences

Pravda-first would add integration discovery before the known prototype can be
bounded; dual engines multiply tests. An in-web browser preserves current shortcuts
but conflicts with credential/isolation goals. Microservices/SPA/SaaS do not solve
the initial newsroom workflow and are excluded. Shared internal access is explicit;
collections are not private folders and a reviewer role/two-person rule is not implied.

## Verification obligations

EWP-01 must prove packaging/capabilities and deployed egress/sandbox feasibility.
If isolation cannot meet the contract, stop browser exposure and reopen runner
topology, not the privacy requirement. Real build/browser/DB/security/migration
evidence and individual task assignment remain pending. See requirements documents
13–19 for selected parameters, contracts and work packages.
