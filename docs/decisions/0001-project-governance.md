# ADR-001: Adopt project governance and component versions

Status: **accepted for engineering governance**. Date: 2026-11-09.

## Context

The user requested separate MCP registration/index verification for three projects,
then active rules, vision, versioning, changelog, skills and prompts for Evidence
Workspace, using The OA as a reference, and local commits before detailed planning.
The repository contains both prototype code and a future production concept.

## Decision

Adopt AGENTS/CONTRIBUTING, component manifests, a derived version ledger and
Unreleased inventory, standard-library validation with regression tests and CI,
local project skills and prompt starters. Preserve inherited application package
1.1.0 as a prototype baseline; assign 0.1.0 to existing specification, UI prototype,
deployment and governance. Reserve evidence contracts at planned 0.0.0.
Workspace release/date remain null. Use English for new engineering artifacts;
retain the existing bilingual concepts and user-language communication.

Use independent MCP project identities and ignored local persistent graph archives.
Record parser gaps and verify actual symbol/source retrieval. The OA is a read-only
workflow reference, with no dependency or imported product architecture.

## Consequences

Future coherent changes increment affected existing components and update
Unreleased. Planned metadata does not imply implementation. Governance checks
prove consistency, not runtime security or production readiness. Product/architecture
recommendations require their own decisions; this ADR does not accept them all.
This requested local commit does not create a release, push or deployment.
