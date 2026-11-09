# Decision register and risk ownership

Date: 2026-11-09. Status: **design dispositions selected; qualification risks remain**.
Owner: engineering lead; reviewer roles below require named assignees before delivery.
Sources: concept sections 2.4, 34–35; [source review](../04-current-state.md).
Governance ADR-001 is unchanged; selected engineering ADR-002–004 now record
V0 choices. The concept's example ADR numbers are not the adopted registry.
[Document 13](13-selected-v0-baseline.md) is the current disposition/parameter register;
the table below retains alternative/context and qualification obligations.

## Decision context and remaining qualification

| ID | Recommendation and alternatives | Owner/reviewer | Blocking gate and evidence needed |
| --- | --- | --- | --- |
| DEC-01 Scope/package/release naming | Use V0 as a controlled-prototype scope label; retain inherited package 1.1.0 until a deliberate compatible/breaking naming/version migration. Alternative: new package identity with explicit compatibility bridge | Product + engineering | V0 planning: approve scope matrix and inherited 1.x contract/release treatment |
| DEC-02 Topology and supported baseline | One-host modular monolith/Compose; separate web, trusted worker and isolated browser; qualify one PostgreSQL major (current Compose uses 16). Alternatives: separate engine service shape, supported host/image versions | Engineering + operations/security | V0 architecture: process/network/volume diagram, tested build/install direction and exact supported versions |
| DEC-03 Capture implementation | Prefer one adapter; reuse direct Playwright only inside isolated runner for lowest migration cost, evaluate Pravda against required options/artifacts. Do not build both by default | Capture + security/evidence | V0 capture: controlled engine investigation, request/result contract, isolation and provenance/fidelity evidence |
| DEC-04 Evidence profiles and WARC | V0 PNG/MHTML/JSON/manifest; explicit WARC/PDF deferral. Production WARC fidelity + mandatory PDF; profile/schema evolution retains historical meaning | Evidence + product | V0 profile and production preservation: canonical manifest/size/hash rules; WARC recording/replay strategy before production implementation |
| DEC-05 Public projection and withdrawal | Admin-reviewed screenshot/approved metadata; raw packages private in V0; no-store, active publication checks for all assets. Alternatives need explicit disclosure/cache/revocation contract | Product + security | V0 publication: exact field allowlist, sensitive URL policy, preview and proxy/cache tests |
| DEC-06 Review and role policy | Shared archive, editor review allowed, admin publication only, no two-person rule in V0. Alternatives: editor publishing, reviewer role or per-collection ACLs later | Product + security | V0 identity/UX/API: role/action matrix and revision/approval semantics |
| DEC-07 Queue and asynchronous contracts | PostgreSQL claims/leases/fencing + polling, optional NOTIFY, bounded retries and durable event sequence. Define cancel winner, idempotency TTL, heartbeat/lease/backoff and event retention | Backend + operations | V0 execution: state tables, crash/race outcomes and real DB test design |
| DEC-08 Storage/finalization/backup | Local staged immutable namespaces, DB metadata, reconciliation, quiesced consistent V0 backup. Alternatives: object store/outbox variants, live snapshots later | Evidence + operations | V0 preservation/recovery: crash-point matrix, backup boundary and isolated restore procedure |
| DEC-09 Limits and capacity | Starting values in document 01; one browser by default. Decide screenshot pixel cap, export cap, disk reserve, preview/session/event/lease limits and resource budget | Operations + product/capture | V0 pilot: reviewed bounded config and measured environment; production supported limits require pilot/load evidence |
| DEC-10 Legacy schema and public routes | Preserve bytes/IDs or explicit mappings; migrate old public flags via reviewed publication policy. Alternatives: compatible old links vs documented withdrawal with operator/user notice | Backend + product/security | V0 migration: table/path/route map, anomaly handling, old-link privacy and rollback/restore limits |
| DEC-11 Admission/session/admin lifecycle | Fail-closed GitHub policy, durable opaque sessions, operator admin bootstrap, enabled/role checks, disable queued/stream access, protected audit | Security + operations | V0 identity: exact organization-membership failure policy, expiry/rotation, last-admin and incident recovery |
| DEC-12 Production readiness and support | Maintain concept's WARC/PDF/security/recovery/pilot requirements, set performance/recovery objectives from measurements | Product + operations/security | Production release: complete acceptance/evidence matrix and known-limitations/support policy |
| DEC-13 Adopted comparison/monitoring | C0 Source history in V0 and staged C1–C4 comparison/profile/watch/delivery, per ADR-005 | Product + evidence/security/operations | Documents 21–26: 40 requirements with stage gates; deferred investigations in 27 remain separate |
| DEC-14 Investigation/handoff | ADR-006: H0 explicit request context/importance in V0; H1–H4 annotations, search/cues, reports and native transfer later | Product + evidence/security/operations | Documents 28–33: provenance/revision/disclosure/quarantine limits and EWP-31 before V0 qualification |
| DEC-15 Browser companion | ADR-007: independent MV3 B0/B1/B2, narrow expiring pairing/API, client-claimed acquisition profiles and verified quarantine; no baseline dependency | Browser + evidence/security/operations | Documents 34–38; real native API/permission/target/memory feasibility, B acceptance and EWP-41–52 |
| DEC-16 Integrated policy/delivery | ADR-008: shared purpose eligibility, dependency/removal authority, aggregate resource reservations, feature/schema gates and registered-observation upload consent | Evidence/backend/security/operator | Documents 39–43; EWP-53–60 with actual core/owning-stage SYS evidence, not added product requirements |

V0 written design choices now have selected dispositions in ADR-002–004 and
documents 13–17. Production WARC fidelity and measured operational objectives remain
production work. No human reviewer sign-off or empirical qualification is fabricated.
Failed feasibility reopens the affected choice and dependent tickets, as described
in [the four-wave review](19-documentation-review.md).

## Risks and planned mitigations

| Risk | Impact | Mitigation and responsible role |
| --- | --- | --- |
| Captured page reaches host/internal network | Credential/evidence compromise | Isolated browser and network egress tests; security lead |
| DB/filesystem split during finalization | False success or lost/orphan evidence | Fenced commit, staging/reconciliation, crash tests; evidence/backend lead |
| Stale worker or duplicate retry writes | Conflicting result/provenance | Attempt identity and lease fencing; backend lead |
| Cached public asset survives revoke on server path | Unintended disclosure | Publication-scoped access/no-store and proxy tests; security/publication lead |
| Human publishes sensitive screenshot/URL | Irreversible third-party disclosure | Exact preview, conservative public projection and explicit copy-retention limits; product/editorial lead |
| Manifest/checksum self-reference or incomplete inventory | Unverifiable export | Separate capture/export inventories, independent verifier; evidence lead |
| Misleading success on empty/partial capture | Editorial reliance on missing evidence | Profile completion gates and visible partial outcome; capture/product lead |
| Migration invents history or loses public-link meaning | Broken trust/compatibility | Preserve unknowns, explicit mapping/anomalies, rehearsal/backup; backend/operator |
| Disk/browser/export resource exhaustion | Service failure/evidence loss | Streaming caps, admission control and reserve; operations lead |
| Wrong tab or unintended authenticated content collected | Private browser content disclosure | Foreground/document generation checks, explicit scope/preview/consent, B2 pause and private-only profile gate; browser/security lead |
| Compromised paired collector or leaked bearer | Forged provenance or unauthorized submission | Narrow expiring scopes, digest-only grants, revoke/epoch fencing, client-claim labels and quarantine; security/evidence lead |
| Native browser API allocates before enforcing caps | Client exhaustion or misleading safety promise | Measure large-page native behavior, bound retained bytes, disable unqualified profiles; browser lead |
| Per-feature slots multiply host pressure | Queue starvation, OOM/full spool or lost work | One aggregate heavy permit, shared byte/position reservations and fair classes; backend/deployment lead |
| Delayed cleanup leaves stale derived content readable | Renewed disclosure after source removal | Root fence before paged closure and current-read/finalizer checks; security/evidence lead |
| Disabled flag masks incompatible writers/readers | Invalid data or accidental restored actions | Effective feature/schema/qualification/restore gate and compatibility rehearsal; operator/backend lead |
| Scope expands into crawler/AI/OSINT platform | Prototype never qualifies | Enforce V0/production/out-of-scope matrix; product lead |
| Hashes marketed as truth/trusted time | False assurance | Precise receipt/UI language and known limitations; product/evidence lead |
| Operator backup cannot restore | Irrecoverable newsroom evidence | Clean isolated restore with byte/record verification; operations lead |

## Cross-document review checklist

Check vocabulary/state/role tables agree; no deferred capability is accidentally a
V0 success prerequisite; no required security/recovery control is deferred with it.
Check each requirement is covered in document 10 and each runtime stage has an
accepted input/verification gate. Record updates in Specification/Unreleased.
No architecture decision, review sign-off or test run is fabricated in this baseline.
