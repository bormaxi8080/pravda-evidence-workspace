# Brief for the next design phase

Status: **proposed documentation scope**, not an implementation plan. The user
intends to design implementation documentation and a detailed plan next.

Start from [vision](01-vision.md), [source review](04-current-state.md) and both
concept documents. Resolve contradictions before assigning implementation tasks.
Use stable requirement IDs (`REQ-*`), ADR numbers and traceable acceptance scenarios.

Expected specification areas:

- Product scope, roles, user journeys, UI states and exclusions.
- Domain/state transitions, evidence immutability, publication, retention/deletion.
- Evidence formats, WARC fidelity, provenance, manifest/hash and export contracts.
- Capture adapter, URL validation, browser isolation, durable jobs and retry/recovery.
- PostgreSQL schema, migration from prototype data, storage consistency and reconciliation.
- Auth/session/RBAC, private/public file access, audit and threat model.
- API/SSE/SSR contracts, producer/consumer compatibility and versioning.
- Deployment, configuration, secrets, upgrade, backup/restore and observability.
- Verification matrix: unit, real PostgreSQL, browser/E2E, security and recovery.

For each specification record status/owner, source requirements, current behavior,
target behavior, alternatives, data/contracts, authorization, failure modes,
migration/rollback limits, acceptance criteria and unresolved questions. Separate
decided, proposed and blocked decisions; do not silently approve concept proposals.

After reconciling these documents, derive a dependency-ordered plan with bounded
milestones. Each milestone needs deliverables, prerequisites, affected components,
test evidence, data compatibility, completion gates and risks. Bring security and
recovery checks into the stage that introduces their behavior. The concept's
12-stage outline is input, not an already detailed or verified delivery schedule.

Use [evidence-spec](../.agents/skills/evidence-spec/SKILL.md) and the
[specification template](reference/specification-template.md) when that work is requested.
