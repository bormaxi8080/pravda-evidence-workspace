# API, service and event requirements

Date: 2026-11-09. Status: **selected API design; implementation pending**. Owner: API/backend lead.
Sources: concept sections 11–13, 20, 26–28; current routers under `provereno-ui/`.
Decisions: DEC-06/07/09/10/11. This document does not publish OpenAPI or change
existing routes. A machine-readable contract is a subsequent implementation artifact.

## Selected interface inventory

All internal JSON paths below have `/api/v1` prefix. SSR may invoke the same
authorized services directly. Public/auth/health routes have separate purposes.

| Method/path | Purpose | Permission and principal result |
| --- | --- | --- |
| POST `/captures` | Submit one capture intent with explicit collection_ids and optional rationale | Editor/admin; 202 with capture/job IDs and initial state |
| GET `/captures`, `/captures/{id}` | Bounded list/detail | Editor/admin; authorized DTO without host paths |
| GET `/sources/{id}/captures` | Paged Source history, including non-complete/identical captures | Editor/admin; requested_at/ID descending, no GET mutation or public history |
| GET `/captures/{id}/artifacts/{artifact_id}` | Private download | Editor/admin; artifact belongs to capture, safe file response |
| PATCH `/captures/{id}/editorial` | Notes/title/tags/review command | Editor/admin; expected revision and resulting revision |
| PATCH `/captures/{id}/triage` | Set normal/important with expected_triage_revision | Editor/admin; independent revision/audit, no review/public effect |
| POST `/captures/{id}/retry` | New linked terminal-capture request | Editor/admin; 202, new capture/job IDs |
| GET `/jobs/{id}`, `/jobs/{id}/events` | Current status and SSE | Editor/admin; no cross-object access leak |
| POST `/jobs/{id}/cancel` | Cancel queued/request running stop | Editor/admin; actual accepted/current state |
| POST `/batch-previews` | Parse/validate CSV, no jobs | Editor/admin; bounded preview ID, rows, expiry and revision |
| POST `/batches` | Confirm exact preview/selected rows | Editor/admin; 202, atomic batch/job set |
| GET `/batches/{id}` | Aggregate and paged row results | Editor/admin; durable mixed outcomes |
| GET/POST `/collections`; PATCH `/collections/{id}` | Grouping CRUD | Editor/admin; no evidence deletion cascade |
| PUT/DELETE `/collections/{id}/captures/{capture_id}` | Membership | Editor/admin; explicit idempotent relation mutation |
| GET/POST `/tags` | Tag list/create | Editor/admin; normalization conflict response |
| POST `/captures/{id}/publications` | Publish reviewed projection | Admin; 201 publication ID/slug/revision |
| POST `/publications/{id}/revoke` | Revoke public access | Admin; idempotent resulting revoked state |
| POST `/captures/{id}/exports` | Request chosen private package | Editor/admin; 202 export job or bounded ready result |
| GET `/exports/{id}`, `/exports/{id}/download` | Status/download | Editor/admin; complete selected profile only |
| POST `/captures/{id}/archive` | Hide from normal internal lists | Admin; no byte purge, active publication conflict |
| GET `/audit`, `/audit/export` | Bounded audit access/CSV | Admin; redacted safe fields |
| GET `/settings/status`; admin user-management commands | Effective non-secret config and role management | Status fields permission-filtered; mutations admin-only |

Public: GET `/evidence/{slug}` and publication-scoped screenshot/metadata paths.
Auth: GitHub start/callback/logout with safe method/protocol handling. Health:
`/health/live`, `/health/ready` with public-safe minimal results and private diagnostics.
Selected compatibility behavior for `/public/evidence/{id}` is in documents 16/17.

## Requirements

### REQ-API-001 Contract before route implementation

Define typed input/output DTOs, field bounds/enums, auth/CSRF rules, status codes
and synthetic examples for every implemented command. Version public/consumer
contracts separately from package versions. Do not reuse ORM objects as unrestricted
responses or expose storage paths, provider tokens, stack traces or raw secret headers.

### REQ-API-002 Idempotency and conflict detection

Capture submission, batch confirmation, export and publication commands shall
define idempotency scope/key lifetime. Repeating the same actor/key/payload returns
the same logical result; key reuse with different input conflicts. Persist the
idempotency record with the business transaction. Editorial/review/publication
commands include expected revision and reject stale writes. Client retries shall
not create extra jobs/publications or toggle state unpredictably.

### REQ-API-003 Bounded lists and structured errors

Specify stable sort and pagination tokens/page bounds; validate filters and page
sizes. Return a common error body with code, safe message, field details where
appropriate and request ID. Distinguish unauthenticated/forbidden/not-found,
validation failure, state/revision conflict, capacity/rate limit and service outage.
Public missing/private/revoked resources shall not leak internal existence details.
Async failure is visible in the job resource, not an HTTP success fiction.

### REQ-API-004 Durable reconnectable progress

SSE shall send typed state/progress/terminal events with job-scoped sequence IDs.
Accept Last-Event-ID under a defined bounded retention window; replay retained
events or issue a reset/snapshot response when history expired. On reconnect/reload
the client retrieves authoritative current state. Heartbeats are not progress or
lease renewal. Terminal state remains retrievable after disconnect and process restart.

### REQ-API-005 Permission changes affect long-running access

Authenticate and authorize before creating streams/exports and revalidate active
streams on bounded intervals or revocation signal. Session expiry/disablement must
terminate protected SSE and prevent downloads of previously generated exports.
The async worker stores requester identity and rechecks enabled status/capture
permission before starting and finalizing new work. If revoked, cancel/fence that
pending attempt with an auditable reason; preserve previously finalized evidence.
No silent privilege inheritance from a queued request is permitted.

### REQ-API-006 Explicit compatibility and schema evolution

Inventory existing SSR/form/public paths before changes. Define supported aliases,
redirects, response changes and deprecation/migration. Never redirect a former public
link to private content without policy checks. Schema/profile unknown versions fail
explicitly. Published client contracts cannot be broken merely because V0 is a scope
label; inherited package 1.x compatibility is addressed by DEC-01/10.

## Detailed contract and implementation output

[Document 16](16-screen-and-api-contracts.md) defines DTO/examples, errors, revision/
idempotency behavior, user/role routes and legacy mapping; documents 13/14 define
retention/SSE/queue limits. EWP-02 materializes and validates OpenAPI/DTO schemas.
EWP-06–13 implement and verify the actual service behavior.
The V0 API is for the same-origin editorial client; no token API/public integration
SDK is implied. Acceptance: ACC-01/02/03/04/05/06/07/10/11/12.

## Detailed selected design

See [the baseline register](13-selected-v0-baseline.md),
[contracts and operator procedures](README.md) and
[assignable work packages](18-assignable-work-packages.md).
Implementation/qualification remain pending; source presence is not test evidence.

## Post-V0 companion protocol

[Document 35](35-companion-pairing-and-upload-protocol.md) selects a separate
`/api/companion/v1` bearer protocol for expiring pairing, narrow URL intents,
owned upload slots/chunks/status/finalization and revoke. The existing `/api/v1`
web contract is unchanged; UI grant approval/revoke uses cookie/CSRF services.
No access token is accepted on arbitrary web/public endpoints. Capabilities negotiate
protocol/profile versions; unknown browser metadata on the existing server capture
DTO fails rather than selecting another acquisition channel. Generate OpenAPI,
negative examples and TypeScript types at EWP-42, not a competing handwritten SDK.
