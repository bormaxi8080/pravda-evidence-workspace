# Acceptance, verification and requirement traceability

Date: 2026-11-09. Status: **proposed test design; scenarios not executed**.
Owner: engineering/QA lead with security and operations reviewers.
Sources: concept sections 30–34; [testing policy](../operations/testing.md);
requirement documents 01–09, V0 history in document 21 and context/triage in 28.
This matrix is not test-result evidence; later-stage coverage is in documents 26/33/38.

## Scenario catalogue

### ACC-01 Core private evidence lifecycle

Fixture: synthetic HTTP(S) page with controlled screenshot/text/headers and two
admitted roles. Editor logs in, creates capture, sees progress, inspects required
artifacts/provenance and verifies the capture manifest. Add note/tag/collection,
review and export. Assert bytes/digests stay unchanged and no public access appears.
Use real PostgreSQL, filesystem and isolated browser for end-to-end qualification.
Include Source history with repeated byte-identical captures and non-complete
requests; verify paging, authorization and no inferred content-change claim.
Include explicit per-tab collection/rationale intent and a queued-edit race as
HUN-ACC-01; importance changes/filtering use HUN-ACC-02 and never approve evidence.

### ACC-02 CSV and admission boundaries

Test empty/invalid UTF-8/quoted/malformed/oversized CSV, row limit and one-over-limit,
invalid/blocked URLs, duplicate groups, repeated confirmation, expired preview and
capacity exhausted between preview and confirm. Assert preview creates no jobs,
confirmation creates one atomic selected set and oversize input is not truncated.
Pin explicit collection/rationale defaults per row in preview revision/digest; a
context switch before confirm cannot silently submit a different selection.

### ACC-03 Lease, restart and notification loss

With disposable PostgreSQL run two competing claimers even though V0 defaults to
one. Drop notifications; kill workers before/after claim, during capture and around
finalization. Expire leases and allow late old-worker output. Assert bounded recovery,
fenced stale writes, one accepted complete result, no lost queued work and honest
attempt/event/batch state. A mocked queue cannot establish these guarantees.

### ACC-04 Partial capture, retry, cancellation and limits

Inject navigation/condition timeouts, HTTP 404, renderer crash, missing MHTML/PNG,
byte/dimension/disk limits and persistence failure. Distinguish useful complete
404 evidence from incomplete output. Exercise every cancel/finalize race order,
transient retry exhaustion and permanent security denial. Assert no false success,
no publication of partial evidence, no overwrite on manual retry and bounded cleanup.

### ACC-05 Publication disclosure and revocation

Before publication, anonymous page/assets/raw download/metadata access fails even
with known IDs. Editor publish is denied; admin publishes exact approved projection.
Inspect response bodies/headers for notes, usernames, secrets, paths and raw archives.
Revoke and try all previously valid asset URLs through the actual proxy; new server
requests fail, no-store policy is present. Confirm old slug remains revoked after
republication. State that external retained copies cannot be recalled.

### ACC-06 Editorial conflict and review

Two users edit the same revision: one succeeds, stale write conflicts. Review a
complete capture; reject approval of partial/corrupt evidence. Change editorial
revision and confirm review invalidation for future publication while existing
public projection stays pinned. Remove collection/tag membership without deleting
evidence. Independent triage revisions leave approval/public projection unchanged;
stale triage writes conflict without a GET mutation (HUN-ACC-02). Archive only as
admin after revoking public access; no silent hard purge.

### ACC-07 Export and integrity outside the installation

Export synthetic complete profiles with/without optional PDF. Verify extracted
bytes/inventory/digests using an independent environment. Tamper one byte; remove,
duplicate or rename a member; use unsupported profile, empty checksum inventory,
traversal names, hostile receipt text and resource URLs. Assert correct failure,
safe rendering, no network fetch and no silent missing required artifact. Repeated
exports may differ in export time/editorial snapshot but original capture bytes do not.

### ACC-08 SSRF and browser isolation

Use controlled test infrastructure for loopback/private/metadata addresses, IPv6,
alternate encodings, DNS changes, redirects, subresource/WebSocket and browser egress.
Attempt access to DB/host/socket/secrets and unbounded resource consumption. Verify
actual deployed container/network rules; a URL validator unit test is insufficient.
Repeat relevant cases for monitoring and receipt/PDF rendering when enabled.

### ACC-09 Consistency, backup and clean restore

Create evidence plus editorial/publication history; inject orphan/missing/corrupt
files and full disk. Reconcile without deleting valid evidence. Quiesce, back up,
restore into an isolated fresh environment, invalidate sessions, verify IDs/digests/
relationships/audit and run core workflow before enabling external access. Record
data consistency and recovery results; simulated commands do not pass this scenario.

### ACC-10 Migration and interface compatibility

Migrate synthetic fixtures matching legacy Snapshot/Job/public flags and file paths,
including incomplete files, unknown timestamps and in-progress jobs. Preserve or
map identifiers, original bytes/hashes and public-link policy. Exercise old aliases,
unsupported schemas and rollback/restore failure paths. Verify old records are not
silently labeled production-complete or made newly public.

### ACC-11 Identity, API/event and UX boundaries

Exercise admitted/denied identities, empty allowlist, OAuth error/state replay,
expired/revoked session, role/user disablement, CSRF, unsafe return URL and last-admin
recovery. Check all protected endpoints/downloads/SSE, idempotency conflicts,
pagination and event replay/reset after restart. Use actual browser navigation to
check error text, keyboard flow, focus, responsive themes and truthful settings.
Mocks may support early development but do not prove live OAuth-provider integration.

### ACC-12 Production qualification delta

After V0 gates: validate actual WARC fidelity/interoperability and complete PDF
profile, bounded availability probes, upgraded build/schema support, dependency/
container review, security review, operator runbooks and pilot workflows. Measure
resource/capacity/recovery behavior. All mandatory production conditions must pass
before declaring a production release; 3–5 pilot newsrooms remain a concept target,
not an already completed test.

## Complete requirement-to-scenario coverage

Source sections are recorded in the owning requirement documents. All identifiers
below are normative definitions in documents 01–09, REQ-HIS-001 in document 21
and REQ-ORG-001/002 in document 28,
not duplicate definitions here.
Scenario references indicate planned verification, never passed status.

| Requirement IDs | Owning document | Planned acceptance scenarios |
| --- | --- | --- |
| REQ-SCP-001, REQ-SCP-002 | [Product](01-product-and-prototype.md) | ACC-01, ACC-02, ACC-05, ACC-11 |
| REQ-SCP-003 | [Product](01-product-and-prototype.md) | ACC-04, ACC-07, ACC-12 |
| REQ-SCP-004, REQ-SCP-005 | [Product](01-product-and-prototype.md) | ACC-02, ACC-04, ACC-08 |
| REQ-SCP-006 | [Product](01-product-and-prototype.md) | ACC-09, ACC-12 |
| REQ-HIS-001 | [Source history](21-source-history-and-comparison.md) | ACC-01, ACC-04, ACC-10, ACC-11; detailed MON-ACC-07 in document 26 |
| REQ-ORG-001, REQ-ORG-002 | [Context/triage](28-investigation-context.md) | ACC-01, ACC-02, ACC-06, ACC-11; HUN-ACC-01/02 in document 33 |
| REQ-ARC-001, REQ-ARC-002, REQ-ARC-003 | [Architecture](02-architecture.md) | ACC-01, ACC-03, ACC-08 |
| REQ-ARC-004, REQ-ARC-006 | [Architecture](02-architecture.md) | ACC-03, ACC-04, ACC-09 |
| REQ-ARC-005 | [Architecture](02-architecture.md) | ACC-05, ACC-07, ACC-08 |
| REQ-ARC-007, REQ-ARC-008 | [Architecture](02-architecture.md) | ACC-09, ACC-10, ACC-12 |
| REQ-DAT-001, REQ-DAT-002 | [Domain/data](03-domain-and-data.md) | ACC-01, ACC-10 |
| REQ-DAT-003, REQ-DAT-004 | [Domain/data](03-domain-and-data.md) | ACC-03, ACC-04, ACC-06, ACC-07 |
| REQ-DAT-005 | [Domain/data](03-domain-and-data.md) | ACC-05, ACC-06, ACC-11 |
| REQ-DAT-006 | [Domain/data](03-domain-and-data.md) | ACC-06, ACC-09, ACC-10 |
| REQ-DAT-007, REQ-DAT-008 | [Domain/data](03-domain-and-data.md) | ACC-09, ACC-10 |
| REQ-JOB-001, REQ-JOB-002 | [Execution](04-capture-and-jobs.md) | ACC-02, ACC-03, ACC-04 |
| REQ-JOB-003, REQ-JOB-004, REQ-JOB-005 | [Execution](04-capture-and-jobs.md) | ACC-01, ACC-04 |
| REQ-JOB-006 | [Execution](04-capture-and-jobs.md) | ACC-02 |
| REQ-JOB-007 | [Execution](04-capture-and-jobs.md) | ACC-02, ACC-03, ACC-11 |
| REQ-JOB-008 | [Execution](04-capture-and-jobs.md) | ACC-08, ACC-12 |
| REQ-EVD-001, REQ-EVD-002, REQ-EVD-003 | [Evidence](05-evidence-and-export.md) | ACC-01, ACC-04, ACC-07, ACC-10 |
| REQ-EVD-004 | [Evidence](05-evidence-and-export.md) | ACC-03, ACC-04, ACC-09 |
| REQ-EVD-005, REQ-EVD-006, REQ-EVD-008 | [Evidence](05-evidence-and-export.md) | ACC-05, ACC-07 |
| REQ-EVD-007 | [Evidence](05-evidence-and-export.md) | ACC-10, ACC-12 |
| REQ-UX-001, REQ-UX-002, REQ-UX-003 | [Editorial/UX](06-editorial-and-ux.md) | ACC-01, ACC-06, ACC-11 |
| REQ-UX-004 | [Editorial/UX](06-editorial-and-ux.md) | ACC-05, ACC-06 |
| REQ-UX-005 | [Editorial/UX](06-editorial-and-ux.md) | ACC-02, ACC-03, ACC-04, ACC-11 |
| REQ-UX-006, REQ-UX-007 | [Editorial/UX](06-editorial-and-ux.md) | ACC-11, ACC-12 |
| REQ-SEC-001, REQ-SEC-002 | [Security](07-security-and-publication.md) | ACC-05, ACC-11 |
| REQ-SEC-003, REQ-SEC-004 | [Security](07-security-and-publication.md) | ACC-04, ACC-08 |
| REQ-SEC-005, REQ-SEC-006 | [Security](07-security-and-publication.md) | ACC-05, ACC-06 |
| REQ-SEC-007 | [Security](07-security-and-publication.md) | ACC-05, ACC-07, ACC-08 |
| REQ-SEC-008 | [Security](07-security-and-publication.md) | ACC-01, ACC-05, ACC-06, ACC-09, ACC-11 |
| REQ-API-001, REQ-API-003 | [API/events](08-api-and-events.md) | ACC-01, ACC-02, ACC-05, ACC-11 |
| REQ-API-002, REQ-API-004, REQ-API-005 | [API/events](08-api-and-events.md) | ACC-02, ACC-03, ACC-05, ACC-06, ACC-11 |
| REQ-API-006 | [API/events](08-api-and-events.md) | ACC-10 |
| REQ-OPS-001, REQ-OPS-002, REQ-OPS-005 | [Operations](09-operations-and-migration.md) | ACC-09, ACC-10, ACC-11 |
| REQ-OPS-003, REQ-OPS-004 | [Operations](09-operations-and-migration.md) | ACC-09 |
| REQ-OPS-006, REQ-OPS-007 | [Operations](09-operations-and-migration.md) | ACC-03, ACC-04, ACC-08, ACC-09 |
| REQ-OPS-008 | [Operations](09-operations-and-migration.md) | ACC-09, ACC-10, ACC-12 |

## Exit gates and evidence records

V0 requires applicable ACC-01 through ACC-11, HUN-ACC-01/02 and the documentation-ready gate,
with disabled optional monitoring/PDF clearly recorded. No critical privacy,
evidence-loss, isolation or authorization defect may be deferred behind "prototype".
ACC-12 and all concept section 33 conditions are additional production gates.

For every run record source commit, environment/image/browser/schema/profile
versions, synthetic fixture identity, exact command/scenario steps, outcome,
failure artifact and limitations. Separate unit, real DB, browser, live provider,
isolation and recovery evidence. Empty/skipped required suites fail their gate;
unavailable checks stay unavailable. No percentage coverage alone proves readiness.

Specification review also checks every mandatory requirement is implemented or
explicitly excluded from that stage, with rationale and remaining production gate.
The existing 36 governance tests validate engineering tooling only; they do not
execute the proposed runtime scenarios above.

The V0 registry now has 70 requirements (67 original, history and two context/triage).
The 88 later-stage requirements have coverage in the
[comparison/monitoring matrix](26-adoption-roadmap-and-acceptance.md) and
[investigation matrix](33-investigation-roadmap-and-acceptance.md) and
[browser companion matrix](38-companion-roadmap-and-acceptance.md).
Their gates apply to their stated later stages, not as hidden V0 prerequisites.
