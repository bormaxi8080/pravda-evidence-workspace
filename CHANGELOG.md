# Changelog

Human-readable entries describe coherent changes. Component manifests own versions;
the inventory below is generated. No Workspace product release is declared here.
The inherited Python package 1.1.0 is a prototype baseline, not a newly issued release.

## [Unreleased]

<!-- component-versions:start -->
| Component | Version | Status |
| --- | --- | --- |
| Product release | `None` | development |
| Application (`application`) | `1.1.0` | prototype |
| Deployment (`deployment`) | `0.1.0` | prototype |
| Evidence Contracts (`evidence-contracts`) | `0.0.0` | planned |
| Governance (`governance`) | `0.1.1` | tooling |
| Specification (`specification`) | `0.1.1` | documentation |
| UI Prototype (`ui-prototype`) | `0.1.0` | prototype |
<!-- component-versions:end -->

### Added — proposed requirements package, 2026-11-09

- Detailed documentation work packages, dependencies, review outputs and implementation-ready gates.
- Separate product/prototype scope, architecture, domain, capture/jobs, evidence/export,
  editorial UX, security/publication, API/events and operations/migration requirements.
- Complete requirement-to-scenario traceability, a derived software delivery roadmap
  and an open decision/risk register, all in English.
- Explicit V0 versus production boundaries, including proposed WARC/PDF deferrals
  and mandatory privacy, isolation, durable-state and recovery controls for the prototype.

Specification advances to 0.1.1 and design revision to 0.2. Architecture and numeric
defaults are proposals; runtime components, package version and release/date are unchanged.

### Fixed

- Governance delivery tests now derive the next fixture version from its manifest
  instead of assuming 0.1.1, preserving validation across future version increments.
  Governance advances to 0.1.1.

### Added — engineering baseline, 2026-11-09

- Source-backed product vision, prototype/target gap review and brief for the next design phase.
- AGENTS/CONTRIBUTING, component ownership/version registry, validation, regression tests and CI.
- Local orientation/specification/delivery skills and reusable prompt starters.
- Independent Codebase Memory registration, full indexing, symbol/source/coverage checks and runbooks.
- Testing and release discipline adapted from The OA without runtime dependencies.

### Changed

- README now distinguishes existing prototype code from production concept and verified behavior.
- Ignore local secrets, captures, backups, exports, caches and persistent MCP graph artifacts.
- Remove tracked Finder metadata from Git; preserve local files.

Runtime behavior and inherited application version remain unchanged. Product release
and release date are null; no tag, push, publication or deployment is part of this baseline.
