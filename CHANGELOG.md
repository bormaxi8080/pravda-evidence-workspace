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
| Browser Extension (`browser-extension`) | `0.0.0` | planned |
| Deployment (`deployment`) | `0.1.0` | prototype |
| Evidence Contracts (`evidence-contracts`) | `0.0.0` | planned |
| Governance (`governance`) | `0.1.2` | tooling |
| Specification (`specification`) | `0.1.5` | documentation |
| UI Prototype (`ui-prototype`) | `0.1.0` | prototype |
<!-- component-versions:end -->

### Added — optional browser companion implementation design, 2026-11-09

- Select ADR-007 and B0 URL handoff, B1 explicit viewport/MHTML acquisition and B2
  bounded foreground-tab assisted recording; preserve independent baseline V0 gates.
- Add 24 English requirements for MV3 permissions/UI, expiring human-approved pairing,
  narrow bearer API, resumable uploads, client/server provenance, offline spool,
  quarantine/fenced acceptance, own export profile, revoke/restore and distribution.
- Record current primary Chrome/RFC references, native API fidelity/resource limits,
  B-ACC-01–12 and EWP-41–52. Totals: 158 requirements, 70 V0 / 88 later, 52 tasks.
- Reserve the independent Browser Extension component at planned 0.0.0 with no
  implementation dependency; update its catalog and component ownership/version ledger.

Specification advances to 0.1.5, Governance to 0.1.2 for the component catalog, and
design revision to 0.6. No extension/runtime/schema package, store listing, browser
qualification, deployment or product release is produced by this documentation change.

### Added — evidence-linked investigation and handoff design, 2026-11-09

- Compare Hunchly's documented workflows with the current source and selected
  target; record source dates, edition limits and acquisition/trust differences.
- Select ADR-006 and 27 English requirements for request context, independent
  importance, anchored annotations, research tasks/views, evidence content search,
  literal research cues, frozen reports and Workspace-native case transfer.
- Add two requirements to V0 and 25 to later stages: 134 total, 70 V0 and 64 later.
  Extend traceability with HUN-ACC-01–10 and EWP-31–40, including V0 dependencies.
- Specify resource, disclosure, revision, quarantine, recovery and provenance
  boundaries; defer browser-session capture, native attachments, regex and signatures.

Specification advances to 0.1.4; design revision is 0.5. This is documentation
design, not Hunchly interoperability, runtime implementation or qualification.
No upstream code/assets, runtime dependencies or product release are introduced.

### Added — adopted comparison and monitoring design, 2026-11-09

- Adopt changedetection.io ideas through ADR-005 and detailed Source history,
  offline comparison, profile/attention, watch/scheduling, notification/outbox and
  shared API/storage/operations requirements in English.
- Add 40 requirements with complete stage/scenario coverage: one explicit V0 history
  requirement plus 39 later-stage requirements; retain the original 67 IDs unchanged.
- Define EWP-19–30, resource limits, epoch/baseline and permission races, deterministic
  cache rebuild, restore/purge behavior and honest uncertain-delivery semantics.
- Separate later visual/native-format/selector/inheritance/transport investigations
  from the selected C0–C4 delivery stages and mandatory production gates.

Specification advances to 0.1.3; design revision is 0.4. Adoption is documentation
and roadmap work only: runtime, schemas, dependency list and product release remain unchanged.

### Added — selected design and source-monitoring research, 2026-11-09

- Complete the written four-wave design pass with three selected engineering ADRs,
  exact V0 parameters, domain/execution/engine, evidence/publication, screen/API and
  migration/operations contracts, and a consistency/refinement review.
- Derive 18 assignable implementation work packages with dependencies, responsible
  roles, concrete outputs and verification gates; feasibility/runtime qualification remain pending.
- Review changedetection.io at pinned commit c01f1546417a2fb34eb5add32b35ca56002e248c;
  record source/test/license evidence, adoption priorities and implementation-level lessons.
- Propose optional post-V0 comparison/filter/watch/notification increments while
  preserving the 67 core requirements and existing prototype scope.

Specification advances to 0.1.2; design revision is 0.3. Engineering choices are
selected for planning, not represented as human sign-off or tested implementation.
No upstream code/assets/dependencies, runtime behavior or release metadata changed.

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
