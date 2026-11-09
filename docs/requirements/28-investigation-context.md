# Investigation context, importance and working views

Date: 2026-11-09. Status: **selected staged requirements; not implemented**.
Owner: product/backend/UX. Authority: ADR-006; source comparison in the Hunchly
review. H0 applies to V0; H1 follows qualified V0/C1. Collection remains a shared
grouping, not a tenant, secret folder or new authorization boundary.

## Requirements

### REQ-ORG-001 Explicit acquisition context in V0

URL/CSV submission shall allow selected collection IDs and an optional bounded
reason for preservation. Show that context before confirmation and pin it with the
durable capture/batch intent. Validate IDs/permission; do not infer a case from the
last viewed screen or silently reuse another tab's context. Preserve original
requested context as a private application record, separate from observed technical
provenance and later editable notes/membership. Initial editorial/membership state
is created at submission; worker completion must not overwrite edits made meanwhile.
Unknown/imported context stays unknown. No automatically inferred browsing history.

### REQ-ORG-002 Independent importance triage in V0

Editors/admins shall set/clear a shared newsroom importance flag with actor/time,
revision conflict detection and audit, and filter archive/Source history by it.
CaptureTriage is separate from approved EditorialRevision: changing importance
does not approve/reject, acknowledge an event, invalidate approval, rewrite evidence
or change a pinned Publication. GET is read-only; UI labels this as triage. New
captures default normal; migration does not invent prior importance/history.

### REQ-ORG-003 Collection-scoped research tasks in H1

H1 shall support bounded research tasks with collection, text, optional capture/
annotation link, optional enabled assignee/due date and open/in_progress/done/
cancelled state. Mutations record actor/time/revision; task completion never counts
as evidence review, watch acknowledgement, publication or proof that a source was
captured. Tasks are shared newsroom context with no automatic reminders/outbound
send or full project-management system. Archive collection stops new tasks without
purging evidence. Reassignment after user disablement is explicit.

### REQ-ORG-004 Reproducible saved working views in H1

H1 shall save validated archive/history/search filter definitions with owner,
revision, scope and query-language version. Personal definitions are owner-readable/
editable by default; explicit sharing exposes the definition to the newsroom, not
new evidence access. A saved view is a live query, not a frozen report or collection
membership snapshot. Unsupported/changed filters require review, never silent
broadening to all evidence. Exporting the query definition is a separate choice.

## H0 data, UX and API contract

CaptureIntentContext: capture_id, submitter, entry_mode=`manual_url|csv`, requested
collection IDs, rationale<=2,048 chars, requested_at and immutable revision/digest.
Legacy records use unknown entry mode/context rather than synthetic manual input.
Requested collection IDs are an immutable snapshot, not cascading membership FKs;
removing/renaming a collection cannot rewrite the historical request.
Only existing explicit user input is recorded; it is not a source observation.
Current editorial notes/membership have their own revisions. Sensitive context stays
out of capture.json, public metadata, notification payloads and default exports.
An explicit report/transfer option may include a selected snapshot later.

CaptureTriage: capture_id unique, revision, importance=`normal|important`, actor_id,
updated_at. It is shared in the newsroom; per-user attention remains UserAttention.
No external alert or capture retry follows a flag change. Capture deletion/purge
disposition also removes/inactivates dependent triage/context under operator policy.

POST `/api/v1/captures` adds optional `collection_ids` and `rationale`; CSV preview
has explicit batch-level collection/rationale defaults shown per selected row.
The existing strict CSV `url,note,tags` grammar stays unchanged; no new implicit
dialect. Notes remain editable notes, not immutable rationale. Confirmation pins
resolved selected-row context and must reject stale/deleted collection references.

PATCH `/api/v1/captures/{id}/triage` requires expected_triage_revision and importance;
returns updated triage revision or 409 without touching editorial revision. Existing
list/history filters accept importance; invalid values are 422. Visible active
collection context in forms is explicit, never a silent browser-global default.

## H1 task/view contract and limits

ResearchTask has UUID, collection/capture/annotation references, state/revision,
text<=2,048 chars, optional due_date (ISO date, not an automatic schedule), assignee,
created/updated/done actors/times. Target cap: 200 open tasks/collection, paged 25/100.
POST `/api/v1/research-tasks` creates a task; PATCH `/{id}` requires the current
expected_revision. Both use shared collection authorization and safe links.
H1 adds collection active/archived lifecycle and explicit revisioned POST
`/api/v1/collections/{id}/archive`; archiving is not evidence purge or publication
revocation. Removing a grouping preserves safe historical task/context references. UI uses editorial task language, never EWP IDs.

SavedView has UUID, owner, shared flag, name<=128 chars, validated query JSON<=8 KiB,
schema version and revision; target cap 100 active/user. GET/list and POST/PATCH/
archive under `/api/v1/saved-views` recheck definition visibility and result access.
No saved view stores a bearer URL/token or reveals personal search terms in general
logs. Import preserves query text only as disabled foreign context until reviewed.

The selected limits are starting values requiring resource/UX tests. Initial
submission, collection mutation, task and triage races use existing transaction/
audit/idempotency rules; source bytes and public projections remain independent.

## Later browser context adapter

ADR-007 B0 retains the server acquisition channel while recording explicit
submitted_via=companion intent privately. B1 adds a versioned browser_companion
entry mode only to the new intake contract, preserving V0 manual_url/csv meanings.
The server records the authenticated actor and submitted collection/rationale as
context, not technical source observation. H1 anchors are created only after exact
accepted artifact/derivation validation; live selected text is not an anchor.
