# Integrated design review and selected refinements

Date: 2026-11-09. Revision: 0.7. Status: **source-document self-review; runtime untested**.
Owner: engineering/evidence/security/operations. Authority: ADR-008 and the current
continuation request. Inputs: concept lifecycle and selected requirements 01–38.
This pass closes specification gaps without adding another product feature family.

## Review findings and dispositions

| Finding in existing design | Selected refinement / authority | Implementation evidence still required |
| --- | --- | --- |
| Complete, verified, reviewed and usable are separate, but checks are scattered across capture/export/watch/report/browser paths | Purpose-specific eligibility matrix and decision contract in document 40 | Same denial/allow result through SSR/API/worker/download; no provenance laundering |
| Source URL/time can be client/foreign claims, while mixed archive dates must remain stable | Explicit channel/time basis and cursor rules in document 40 | Future client clock/import collision fixtures; no rewritten historical provenance |
| Notes pin derivatives; caches expire; reports/search may retain copies after source loss | Dependency/pin inventory and root fence before cleanup in document 41 | Crash-safe closure, no stale snippets/crops/report downloads or rebuild resurrection |
| Each task type has a slot/budget, yet multiple one-slot services could collectively overwhelm one host | Shared heavy permit, pending/byte reservations and fairness in document 42 | Real contention/restart/full-disk evidence with capture, export and enabled extensions |
| Flags, contracts and migrations are described per feature, but disabling/restore compatibility needs one decision | Effective feature state and ordered rollout/rollback protocol in document 42 | Mixed-version and restore hold tests; disabled features never activate on startup |
| B2 stop permits keeping approved uploads, while document 35 also rejects expired session linkage | Freeze observation identity/consent separately from current recording epoch; document 40 | Stop/lease expiry followed by approved upload versus new observation; revoke still fences acceptance |
| Lists of schemas/fixtures are spread across tasks without a single materialization order | Executable contract catalogue and synthetic fixture/evidence record in document 43 | Real schema examples, generated client consistency, independent byte verification |
| Search runs and imports have bounded work, but failures need support diagnostics without leaking investigation data | Stable reason codes, bounded safe status and incident records in documents 40–43 | Denied access, redaction, unavailable/partial/stalled states; no raw content in telemetry |

These are selected engineering refinements of existing requirements, not findings
from an installed browser, running service, independent security audit or production
incident. Source documents remain canonical for exact profile inventories, payloads
and per-operation limits. ADR-008/documents 40–42 govern the named cross-cutting
conflicts; changing an immutable format still requires its own version/migration.

## Scope and sequence

This revision-0.7 refinement kept 158 requirements: 70 V0 and 88 later. No IDs are copied/renumbered.
Documents 40–43 map concrete rules to existing owners/IDs and add ten integration
scenarios plus eight implementation tasks. New total: 60 tasks and 56 scenarios.

First implement the already required V0 foundation: EWP-01 feasibility; EWP-02/03
schemas/migrations; identity/audit/queue/finalization; shared policy/dependency/admission
refinements; private capture/editorial/CSV/publication/export; recovery and real V0
qualification. C1–C4, H1–H4 and B0–B2 remain separately qualified branches.

Do not implement every future adapter to finish a core service. In V0, policy knows
its implemented server/legacy profiles, dependency authority covers actual capture/
export/publication state, and admission accounts only actual job types. Future
profile IDs may be explicitly unsupported; no planned package/runtime dependency.

## Architectural responsibility

| Responsibility | Future implementation owner | Explicit boundary |
| --- | --- | --- |
| Profile/DTO/receipt/event definitions and negative fixtures | Evidence Contracts when activated | Versioned data, not route or permission implementation |
| Eligibility, dependency fences, reservation, state transitions and disclosure authorization | Application services | One authority reused by SSR/API/workers; no alternate UI-only checks |
| Memory/CPU/temp/disk enforcement and supported host/build matrix | Deployment | Measurements and process isolation, not a product-readiness label |
| Browser observation/consent/local journal | Browser Extension when activated | Untrusted collector input; no server approval/publication or arbitrary API scopes |
| Cross-document rules, task/scenario mappings and gate records | Specification | Design/refinement only until exact implementation evidence exists |

Keep these services in the selected modular monolith. Do not introduce an external
policy engine, graph database, search cluster, native helper, AI service or new
deployment merely to satisfy the review. Logical dependency records use PostgreSQL
and do not make the development CodeBase MCP index a production dependency.

## Exit from this documentation pass

Review local references, ownership/version ledger, unchanged requirement IDs,
matrix coverage and the complete task DAG. Runtime gate records remain pending.
The next assignable work is EWP-01 plus the contract materialization sequence;
the design is not a reason to start every extension at once. Unclosed empirical
questions belong to the task that can measure them, with a fail-closed disposition.

A further integration finding is the first-qualification bootstrap: effective
production enablement requires proof, while obtaining proof needs running candidate
services. Document 42 resolves this with an explicitly isolated synthetic
qualification-only deployment, without weakening runtime controls or presenting it
as production readiness. EWP-59 is a reusable framework; owning stage tickets run
their candidate cases before each corresponding qualification gate.

ADR-009/documents 44–49 subsequently add twelve explicitly later IAM definitions
and technical subtask detail; the current package index reports 170 requirements,
72 tasks and 68 scenarios. Findings/dispositions above remain the historical
integration pass, not a claim that the current registry stopped at 158.
