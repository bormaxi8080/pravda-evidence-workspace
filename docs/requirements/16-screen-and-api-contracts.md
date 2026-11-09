# Screen, command, API and error contracts

Date: 2026-11-09. Status: **selected design; routes not implemented/verified**.
Owner: UX/API lead. Refines REQ-UX-001–007, REQ-API-001–006 and REQ-SEC-001/002/005/006.
This Markdown contract is design authority until EWP-02 materializes reviewed
OpenAPI/DTO schemas. No existing authoritative OpenAPI/collection was found. Do
not maintain a competing generated contract or publish documentation externally.

## Common request/response contract

Internal prefix `/api/v1`; authenticated same-origin session and CSRF token for
all mutations. JSON UTF-8 with unknown fields rejected. Resource ID UUID; public
slug is a separate opaque generated token, not a host path. Bounds/defaults come
from document 13. SSR calls the same authorized services; valid form mutations use
303 to the resulting page, while validation failures rerender with field errors.

Errors: `{ "error": { "code": "revision_conflict", "message": "Reload the current
revision before editing.", "request_id": "synthetic-request", "fields": {} } }`.
Messages contain no SQL, provider response, raw URL secrets or stack trace.

| HTTP | Codes / caller action |
| --- | --- |
| 401 | `session_required`, `session_expired`; sign in again, no silent replay of publish |
| 403 | `permission_denied`, `csrf_failed`; do not retry with same authority |
| 404 | `not_found`; generic for private/missing/revoked public resources |
| 409 | `revision_conflict`, `invalid_state`, `idempotency_conflict`, `preview_expired`; refresh/review before a new command |
| 413 | `input_too_large`; reduce input, no truncation |
| 422 | `validation_failed`, `target_denied`, `unsupported_option`; fix field/policy, no automatic retry |
| 429 | `queue_capacity`, `rate_limited`; Retry-After and safe bounded retry |
| 503 | `dependency_unavailable`, `storage_reserve`; preserve intent if acknowledged; query by idempotency key before new submission |

Async job errors additionally include `navigation_timeout`, `condition_timeout`,
`browser_failed`, `resource_limit`, `output_incomplete`, `integrity_failed`,
`permission_revoked`, `cancelled`. A 202 acknowledges durable intent, not capture success.

Idempotency-Key required for capture submission/retry, batch confirmation, publication
and export: 1–128 ASCII printable characters, stored as digest with actor+operation
and canonical request digest for 24h. Same input replays original result/resource;
different input conflicts. Lost response means query/replay, not blind new intent.
Revisioned commands require `expected_revision`; missing/invalid revision is 422,
stale revision is 409. State/audit/idempotency writes share a transaction.

## Core operations and DTOs

| Operation | Required input / optional fields | Success and important conflict |
| --- | --- | --- |
| POST `/captures` | `url`; condition_type default load; condition optional except css/text; title/note/tags, collection_ids and rationale<=2048 optional; explicit context confirmed | 202 `{capture_id,job_id,state:"queued",profile}`; policy/queue errors create no job |
| GET `/captures` | q/host/creator/tag_ids/collection_id/states/date_start/date_end/importance; cursor; limit 25 | 200 `{items,next_cursor}`; stable captured_at/id descending; unknown filter 422; importance is shared triage, not approval |
| GET `/captures/{id}` | Authorized ID | 200 capture outcome/profile/provenance/artifact summaries/editorial revision/review/publication summary, private submitted context and triage state/revision; never host paths |
| GET `/sources/{id}/captures` | Authorized source, cursor/limit, optional importance filter | 200 safe capture history including identical/non-complete requests; requested_at/ID descending, no implicit change/ack |
| GET `/captures/{id}/artifacts/{artifact_id}` | Artifact belongs to capture | Safe private byte response; MIME/attachment/no-store; missing/corrupt denied |
| PATCH `/captures/{id}/editorial` | expected_revision; selected title/note/tag_ids/collection_ids | 200 new revision/current fields and review=in_review; empty no-op may return current revision |
| PATCH `/captures/{id}/triage` | expected_triage_revision; importance=normal/important | 200 independent triage revision; stale 409, no review/public mutation |
| POST `/captures/{id}/review` | expected_revision, state=in_review/approved/rejected, reason<=2048 chars | 200 new revision/state; reject approval if partial/integrity-blocked |
| POST `/captures/{id}/retry` | Terminal capture; idempotency key; optional revised allowed options | 202 new linked capture/job; old result unchanged |
| GET `/jobs/{id}` | Authorized ID | 200 state/state_revision/attempt/phase/next_retry/error/terminal capture ID, no fabricated progress |
| POST `/jobs/{id}/cancel` | expected_revision matching job.state_revision | 202 cancel request or 200 already-cancelled replay; completed/stale revision conflicts |
| POST `/batch-previews` | Multipart CSV upload or explicit text, never both; explicit collection_ids/rationale defaults | 201 preview id/revision/expiry/digest, row results; no jobs |
| POST `/batches` | preview_id, expected_revision, selected_rows, duplicate override; idempotency key | 202 batch ID + row/job mapping; actor/expiry/capacity conflicts are atomic |
| GET `/batches/{id}` | cursor/limit | Aggregate authoritative counts + bounded row page, mixed outcomes explicit |
| GET/POST `/collections` | Create name, optional description<=2048 | 200 list / 201 ID; normalized name collision 409 |
| PATCH/DELETE `/collections/{id}` | expected_revision; fields on PATCH | 200 updated / 204 group removed; capture bytes remain |
| PUT/DELETE `/collections/{id}/captures/{capture_id}` | Authorized relation, expected editorial revision for mutation | Idempotent membership result plus new capture editorial revision; never bypass revision/audit |
| GET/POST `/tags`; PATCH/DELETE `/tags/{id}` | Normalized bounded display name, expected revision on mutations | List/create/rename/remove grouping only; affected capture revisions audited/invalidated |
| POST `/captures/{id}/publications` | expected_revision, manifest_sha256, approved public fields; key | Admin 201 slug/projection; stale/not-approved/already-active 409 |
| POST `/publications/{id}/revoke` | Reason, expected revision | Admin 200 revoked; replay stable, no toggle |
| POST `/captures/{id}/exports` | profile, include_pdf/editorial/actor booleans, expected source/editorial refs; key | 202 export/job IDs; no silent profile fallback |
| GET `/exports/{id}`; `/download` | Reauthorize user, ready result within expiry | 200 state or private ZIP; pending/failed/expired not a successful file response |
| POST `/captures/{id}/archive` | expected_revision, reason | Admin 200 hidden; active publication 409; no purge |
| GET `/audit`, `/audit/export` | Admin, bounded filters/date/page | Safe list/CSV; neutralize formula-capable cells; audit failures explicit |
| GET `/settings/status` | Authenticated; fields role-filtered | Effective non-secret settings/versions and availability; no fake controls |
| GET `/users`; PATCH `/users/{id}` | Admin; enabled/role, expected permission_revision | 200 new role/enabled state, revoke sessions and pending access; last-admin safeguard 409 |

Membership changes through separate endpoints also use the editorial service and
increment the same capture revision; no side channel leaves approval valid. Tag
rename/delete can affect multiple captures: bound work or queue a versioned bulk
mutation, report affected revisions and invalidate future publication approval.
V0 need not expose bulk rename if its transaction/evidence gate is not implemented.

Example capture request (synthetic):

```json
{"url":"https://example.org/article","condition_type":"load","tags":["research"]}
```

Example accepted response (IDs illustrative):

```json
{"capture_id":"d27fb124-e73b-4b5f-849c-b5e2063cce88","job_id":"08cc5791-0237-41d1-b844-d14e1a347c67","state":"queued","profile":"workspace-capture-v0/1"}
```

If two tabs publish different revisions, the stale request returns 409; it does
not mutate the current editorial revision or create a second active publication.
If a 202 reply is lost, replay with the same key returns the original IDs. If queue
admission fails, no subset of a confirmed batch is created.

Submission context is pinned per request/tab and in the actor-bound CSV preview
revision/digest; confirmation cannot silently use a subsequently switched collection.
Initial editorial membership is created at admission; workers never overwrite later
edits. Context and triage stay private and outside default evidence/export metadata.
Importance has its own revision; the common expected_revision rule applies to the
resource's named revision field, including expected_triage_revision here. See
[document 28](28-investigation-context.md) for complete H0 bounds/migration behavior.

## Screen specification by observable behavior

| Screen | Inputs / actions | Rendering and error contract |
| --- | --- | --- |
| Login | GitHub start; no registration bypass | Admission explanation, provider/denied/session-expired states; safe local return |
| Dashboard | Recent jobs/captures, create/import links | Actual counts, private/public/review separate; empty state and degraded dependencies |
| New capture | URL, four allowed condition types, notes/tags, explicit collections/rationale | Show engine-supported conditions and limits; retain safe entered data on field error, never secret query in generic error logs |
| Batch preview | File/text, context defaults, row/dedupe selections, explicit confirm | Every parsed row numbered; errors/duplicates explain selection; expired preview requires regeneration |
| Queue/job | State, attempt history, cancel/retry | Reconnecting banner with authoritative refresh; no spinner-only success and no percent invention |
| Archive | Bound filters, stable cursor paging | Date interval invalidity shown; collections not described as private ACLs |
| Capture detail | Screenshot, artifact/profile/integrity/provenance, editorial actions, independent importance | Partial/missing/corrupt warnings; download attachments; terminal retry creates linked capture |
| Source history | Paged capture outcomes, safe times/profile/review/publication links | Same-byte/manual attempts retained, legacy unknown time explicit; no Compare/Watch/Notify controls before their stage |
| Collections/tags | Group CRUD/membership | Explain group removal preserves captures; revision collisions reload rather than overwrite |
| Review/publication preview | Approve/reject, admin preview/publish/revoke | Preview is exact anonymous projection; original secrets/notes not auto-selected; publish and review distinct |
| Public viewer | Active slug only | Screenshot/allowlisted metadata, hash/time caveat; generic 404 on unknown/private/revoked |
| Export/receipt | Profile/options, job state/download | Exact inclusions/omissions, explicit PDF-required failure and temp expiry |
| Settings/users/audit | Role-allowed operational information/admin commands | Read-only config is read-only, secret values omitted, last-admin/disable consequences visible |

V0 adopts a WCAG 2.2 AA evaluation target for core screens (keyboard/focus, labels,
contrast, error association, non-color status, responsive zoom). This is a target
for EWP-10/15 tests, not certification. Preserve light/dark themes and use plain
editorial language rather than internal lease/storage details in routine flows.

## Identity and SSE specifics

OAuth start issues browser-bound expiring state. Callback consumes it once,
validates provider response and admission, rotates session and drops provider token
after required checks. Organization and login matches are case-insensitive against
verified provider identity; a permitted login OR verified permitted organization
admits. Empty lists deny; organization-only checks must execute. Provider/membership
lookup failure denies that route, never grants by default. Refresh admission at
login and at most hourly for active sessions; lookup failure suspends protected
access until revalidation, rather than extending access indefinitely.

POST `/auth/logout` revokes server session; GET callback remains protocol-only.
SSE GET `/api/v1/jobs/{id}/events` follows document 14 event schema and reauthorization.
Transport disconnect does not cancel capture. Preserve SSE identity only in the
same-origin cookie; never put bearer session tokens in query strings.

## Legacy route compatibility

Authenticated GET `/snapshots` and `/snapshots/{id}` map to new authorized views;
private artifact/export aliases reauthorize and retain attachment semantics. Old
POST `/jobs` and `/bulk` can adapt forms to new services only with CSRF/preview rules;
old toggle-public/delete endpoints return explicit 410 guidance, not silent toggle
or purge. Old public `/public/evidence/{id}` resolves through a reviewed publication
mapping or safe unavailable response. Route migration changes are listed in the
future package-major notes, tested in ACC-10 and reported before cutover.

## Companion UI/API continuation

The companion popup/options/later side panel and Workspace connection/received-
evidence views are specified in documents 34–37. Add web UI flows for logged-in
pairing approval with CSRF, own grant list/revoke, admin revoke-any and client-origin
capture labels. Do not add browser-byte or token fields to POST `/captures` above:
separate `/api/companion/v1` DTOs/scopes govern those operations. Uploaded/validating
is not ready; client detail displays claimed capture time and separate server receipt.
Unknown/ineligible browser profile cannot pass the existing publication command.

## Integrated eligibility/status behavior

Documents 40/42 refine internal operation decisions and safe feature/readiness states.
An authenticated detail view can explain why its particular action is unsupported,
incomplete, unavailable, awaiting qualification or capacity-blocked. Missing/foreign
resources still receive generic denial; diagnostic convenience cannot enumerate
private evidence. GET remains read-only. Every command/worker/download rechecks
current authority/revisions/fences rather than trusting an earlier rendered button.
The future mixed-stage DTO/cursor makes archive time basis explicit; V0's existing
captured_at ordering is unchanged until that adapter/version is qualified.

## Future U-stage API/UX migration

Document 48 specifies later user lifecycle, role preview/assignment, invitation,
space/group/identity-link and move-preview commands. They require explicit typed
DTO/version/permission/policy revisions, cookie CSRF, bounded previews and safe
transactional audit; they are not added to the current V0 routes by this prose.
The U1 migration replaces literal admin/editor checks with reviewed capabilities,
while U2 filters every list/count/history/download/derived path by current custody
scope. Old unscoped clients cannot silently fall back to shared when a restricted
scope is required. Provider linkage is never inferred from email/name.
