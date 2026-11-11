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
| Evidence Contracts (`evidence-contracts`) | `0.1.0` | development |
| Governance (`governance`) | `0.1.5` | tooling |
| Specification (`specification`) | `0.1.10` | documentation |
| UI Prototype (`ui-prototype`) | `0.2.0` | prototype |
<!-- component-versions:end -->

### Integrated — accepted LOC-4 contracts on the Mac baseline, 2026-11-11

- Integrate the human-accepted EWP-02 source commit `06dab44` into local `main`,
  retaining its contract bytes and the newer macOS-first policy without rewriting
  either branch history.
- Resolve parallel Governance versions at 0.1.5, retain Specification 0.1.10 and
  design revision 0.11, and regenerate the combined component ledger/inventory.
- Evidence Contracts is now 0.1.0 development. Earlier pending-review notes below
  describe the original delivery stage; acceptance and integration are now recorded.
  Runtime consumers, independent schema/OpenAPI qualification, production and
  native Linux qualification remain outside this integration.

Product release/date remain null; no push, tag, deployment or release is included.

### Added — EWP-02 core contract implementation, 2026-11-10

- Preserve the accepted inventory schema/fixtures and add capture-engine/1
  request/result schemas from one deterministic Python authority with fingerprinted
  synthetic success, partial, cancellation, failure and negative examples.
- Validate request/result identity, generation, deadlines, output completeness,
  readiness, header allowlist and resource bounds without granting digest-hint authority.
- Keep this in the same Evidence Contracts 0.1.0 activation package.
  Add metadata/export/legacy and job/attempt/event schemas, full package checksum
  verification and generated cookie API DTO/OpenAPI with reproducible examples.
  Whole-package acceptance and integration remain pending.

### Added — EWP-02 first inventory review slice, 2026-11-09

- Activate Evidence Contracts at 0.1.0 with actual shared-contracts ownership,
  an exact workspace-capture-v0/1 manifest schema, synthetic positive/negative
  fixtures and executable canonical-byte/inventory/digest checks.
- Keep manifest self-hash external, reject unknown versions and missing outputs,
  and document review bounds and unavailable independent validator/runtime evidence.
- Advance Governance to 0.1.3: planned-state regression tests now construct their
  own planned fixture rather than assuming Evidence Contracts stays unimplemented.
- Remaining core profile/engine/API/OpenAPI contracts and whole-package acceptance
  remain pending; no application dependency, migration or product release is added.

### Documented — approved local Mac runtime transport, 2026-11-10

- Record the operator-approved isolated Docker Desktop project context/socket and
  loopback HTTP through owned containers, without copying registry authentication
  or disabling the private-network guard.
- Record real sandbox Docker/Compose and loopback HTTP smoke/cleanup evidence,
  preserving the distinction between a trusted fixture and capture isolation.

Governance advances to 0.1.4. No application feature, production or Linux
qualification, release, global Docker context change or broad network grant.

### Changed — macOS development and separate Linux qualification, 2026-11-10

- Adopt ADR-012 and platform requirements/runbook: macOS arm64 with native tools,
  PG16 and Docker Desktop is the current implementation and local evidence lane.
- Retarget PC-SETUP-03 to actual Mac readiness and move native Linux setup, V0 and
  production qualification into separate deferred orchestration tickets. Preserve
  existing EWP dependencies, human reviews, delivered code and release boundaries.
- Clarify local versus native-server acceptance across the versioned plan, Docker,
  DB, operations, verification policy, agent entry point, skills and prompts.
- Keep 170 requirement IDs, 78 product work items and 76 scenarios unchanged;
  real local failures never become passing evidence by calling Linux deferred.

Specification advances to 0.1.10, Governance to 0.1.3 and design revision to 0.11.
No runtime release, application qualification, Linux host or dependency installation
is created by this documentation change. Product release/date remain null.

### Added — interactive UI blueprints and versioned execution plan, 2026-11-09

- Add offline English Workspace and browser companion designs with synthetic local
  assets, light/dark and responsive layouts, connected core consent/revision flows,
  stage/role/state previews and separate popup/side-panel/options surfaces.
- Specify 23 Workspace screens and nine companion surface groups, including private
  versus public projections, browser provenance, pairing, explicit upload consent,
  pause/stop and unregistered-session recovery; select ADR-011.
- Expand all 78 EWP tasks into 11 dependency-ordered milestones with proposed product
  targets, technical steps, owners, outputs, migration/recovery and evidence gates.
  Preserve the 170 requirements/76 runtime scenarios and independent production gate.
- Add a dependency-free isolated-Chrome design smoke checker and seven inspected
  synthetic screenshots; runtime application/extension/security proof remains pending.

UI Prototype advances to 0.2.0, Specification to 0.1.9 and design revision to 0.10.
No runtime feature, MV3 installation, schema migration, deployment or product release
is created; future product/component numbers in the plan are proposed coordinates.

### Refined — production preservation and protected byte delivery, 2026-11-09

- Select ADR-010 and English same-attempt WARC/recording scope, production capture/
  export inventory, engine/2 negotiation and isolated independent replay contracts.
- Specify controlled safe PDF receipts, required-output semantics, nested decode/
  inventory limits, independent verifier evidence and no historical profile relabeling.
- Refine the core protected read path with pre-header verified snapshots, shared
  temp/compute/transfer accounting, bounded reauthorization and revoke/IO races.
- Add EWP-73–78 and PRD-ACC-01–08 without new requirement IDs: 170 requirements,
  78 acyclic planned tasks and 76 scenarios. Keep WARC/required PDF production-only
  and later C/H/B/U features independent of the baseline.

Specification advances to 0.1.8; design revision to 0.9. Recorder/reader/renderer
selection needs actual qualification; no runtime/provider/schema dependency, PDF,
WARC, deployment or product release is created by this documentation change.

### Added — technical deployment and future identity design, 2026-11-09

- Select ADR-009 and English Docker/host/isolation, PostgreSQL/schema/role/pool,
  deployment/config/upgrade and maintenance/telemetry/recovery specifications,
  grounded in current source and primary platform references.
- Define a fixed host-trusted launcher with per-job isolation and no Docker socket
  in application/browser/decoder containers; retain real sandbox/egress proof gates.
- Add 12 post-V0 IAM requirements: fixed role bundles/user lifecycle, one-space
  evidence custody and group/move policy, qualified federation/workload principals.
- Add EWP-61–72 and OPS-ACC-01–12, refine core task prerequisites and preserve the
  shared admin/editor V0 boundary. Totals: 170 requirements (70 V0/100 later),
  72 tasks and 68 scenario definitions.

Specification advances to 0.1.7; design revision to 0.8. Runtime Docker/DB/config,
application/deployment component versions, credentials and product release remain
unchanged. No build, daemon operation, SQL migration, real account, backup,
deployment, identity-provider or recovery qualification was performed.

### Refined — integrated evidence policy and delivery gates, 2026-11-09

- Review the existing server, C/H and browser design together; resolve profile/
  provenance eligibility, mixed archive time basis and B2 stop/upload-consent ambiguity.
- Select ADR-008 and English specifications for exact dependencies/pins, immediate
  removal fences, bounded cleanup, shared permits/reservations/fairness and effective
  feature/schema/qualification/restore state.
- Add executable contract/fixture catalogues, SYS-ACC-01–10 and EWP-53–60; update
  existing task prerequisites without adding product requirements or future-feature
  prerequisites to V0. Totals remain 158 requirements, now 60 tasks/56 scenarios.
- Select one aggregate heavy permit, 100 interactive positions within the existing
  1,000 pending cap and a shared 1 GiB temporary-output pool; retain per-operation
  ceilings and require actual host/resource qualification.

Specification advances to 0.1.6; design revision to 0.7. Runtime, machine schemas,
planned components and product release remain unchanged; no tests of proposed
runtime behavior, cleanup, migration or external delivery are claimed.

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
