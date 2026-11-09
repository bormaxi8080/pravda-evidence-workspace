# Domain and data requirements

Date: 2026-11-09. Status: **selected domain design; implementation pending**. Owner: domain/backend lead.
Sources: concept sections 9–12, 15–21, 24–25; current `models.py` and `database.py`.
Decisions: DEC-04/05/07/08/10/11. Logical entities below are target contracts,
not a claim that corresponding tables or migrations exist.

## Entity dictionary

| Entity | Required meaning and principal fields |
| --- | --- |
| User | Stable ID, provider numeric ID, current login, role, enabled flag, created/last-login times |
| Session | Opaque-token digest, user, created/expiry/revocation times; no token body in audit |
| Source | Stable ID, original/canonical URL policy, host, first-seen time; one-to-many capture requests |
| Capture | Stable ID, source, requester, requested options/time, terminal outcome, selected successful attempt, profile, final manifest digest |
| CaptureAttempt | Attempt ID/number, job/lease owner, engine/browser versions, start/navigation/end times, actual URL/status, warnings/error and output staging reference |
| Artifact | Stable ID, capture/attempt, kind, MIME, relative storage key, size, SHA-256 and creation time |
| CaptureIntentContext | Immutable private submitted collection IDs/rationale and requester/time; context assertion, not captured provenance |
| CaptureTriage | Shared normal/important state, independent revision and actor/time; no approval/publication side effect |
| CaptureEditorial | Capture ID, revision, title/note, review state, reviewer and timestamps; separate from capture provenance |
| Collection / Tag | Unique normalized identifiers/names, title/description, creator, membership relations |
| Publication | Stable ID/public slug, capture, status, revision of approved public metadata/artifact allowlist, publisher/time and revocation record |
| Job / JobAttempt | Durable execution state, type, entity, limits, available time, attempt count, worker, lease token/expiry and structured errors |
| Batch / BatchRow | Preview/confirmation identity, row results, dedupe choices, accepted jobs and aggregate progress |
| JobEvent | Job-scoped monotonic sequence, event type, safe payload, timestamp and retention policy |
| AuditEvent | Actor, action, resource, timestamp, request ID and bounded safe details; append-only through application roles |
| OriginObservation | Source/capture reference, observed time, probe method, availability classification and bounded diagnostics |

CaptureAttempt and JobAttempt can share a physical representation if their lifecycles
remain unambiguous. Never create duplicate competing attempt counters. This is a
schema-design decision to settle before migration code.

## Requirements

### REQ-DAT-001 Stable identity and time semantics

Use stable opaque IDs for captures/artifacts/jobs/publications; slugs are unique
and separate from storage paths. Persist timestamps as timezone-aware UTC. Distinguish
request, browser start/finish, artifact finalization, review, publication and probe
time. Imported unknown provenance stays unknown; do not substitute migration time
as historical capture time. A host clock reading is not trusted timestamping.

### REQ-DAT-002 Preserve source identity without unsafe normalization

Keep the exact requested URL in provenance. Store a separately normalized source
identity under a documented algorithm. Do not reorder/remove query parameters or
merge distinct pages merely because they look similar. A repeat capture creates
a new capture; it does not replace prior evidence. Reject embedded URL credentials.
Potential sensitive URL query values shall not be copied into general logs/public views.

### REQ-DAT-003 Separate execution, evidence and editorial states

Job state, capture outcome, review state, publication state and origin observation
shall be independent fields/entities. V0 review states: `unreviewed`, `in_review`,
`approved`, `rejected`. Only complete evidence can be approved for publication.
Complete/partial/failed captures must remain distinguishable. Worker progress cannot
publish or approve a capture. Editorial revisions shall not change evidence digests.

### REQ-DAT-004 Immutable finalized evidence and attempt history

Finalized attempt artifacts/provenance shall not be overwritten by retry or edits.
Each automatic attempt gets separate staging/output identity. A retry of an already
terminal capture requested by an editor creates a new capture linked to the source
and prior request; it cannot mutate an exported record. Append corrections/history
with actor/reason where appropriate rather than rewriting original facts.

### REQ-DAT-005 Constraints and transactional mutations

Define foreign keys and uniqueness for artifact paths, job attempt numbers, session
digests, normalized tags, collection membership and public slugs. Use optimistic
editorial revisions or equivalent conflict detection. Publish/revoke/editorial
changes and their audit records shall commit together. A failed audit write prevents
the corresponding business mutation; no browser execution occurs inside DB transactions.

### REQ-DAT-006 Lifecycle and deletion boundaries

V0 shall offer admin-only archival/hiding from routine internal lists; this does not
erase bytes or revoke a publication automatically. Active publications must be revoked
before an archival action. General user-facing hard deletion/automatic retention is
excluded until an explicit retention/purge policy defines holds, backups and audit.
An urgent data-removal operator procedure is required before sensitive use; it shall
state replica/backup/download limits and preserve a minimal accountable tombstone.

### REQ-DAT-007 Legacy migration must preserve evidence meaning

Map Snapshot to Capture + Editorial + Artifact records while preserving identifiers
or an explicit lookup mapping, original timestamps, creators and file digests. Map
jobs/batches/collections/tags/audit without inventing lost history. Legacy `is_public`
records shall enter a reviewable publication migration path; do not silently broaden
visibility or silently break public URLs. DEC-10 resolves old link compatibility.

### REQ-DAT-008 Derived state must be reconstructible

Batch counters, dashboards and search indexes shall derive from authoritative rows.
DB inventory shall reconcile with filesystem contents and manifest hashes. Orphans,
missing bytes and mismatched digests become diagnosable findings, never fabricated
artifacts. Rebuilding a projection must not reset review/publication or audit history.

## Key lifecycle interactions

| Event | Allowed result | Forbidden side effect |
| --- | --- | --- |
| Complete capture | Final manifest committed; review remains unreviewed | Automatic public link activation |
| Change note/tag | New editorial revision | Rehashing/replacing original evidence |
| Change importance | New triage revision/audit | Editorial approval invalidation or public projection changes |
| Approve evidence | Approved review revision with actor/time | Publishing without separate admin command |
| Edit after approval | Return to in_review for future publication | Silently changing an already published projection |
| Revoke publication | Original publication slug remains revoked | Deleting underlying private evidence |
| Re-publish | New publication revision/slug after explicit decision | Reactivating old withdrawn links implicitly |
| Retry completed/partial request | New linked capture | Replacing bytes in the old package |

V0 permits one active public publication per capture. Production may allow multiple
projections only after defining independent audience/revision/disclosure rules.
Acceptance scenarios: ACC-01/03/04/05/06/07/09/10.

## Detailed selected design

See [the baseline register](13-selected-v0-baseline.md),
[contracts and operator procedures](README.md) and
[assignable work packages](18-assignable-work-packages.md).
Implementation/qualification remain pending; source presence is not test evidence.

## Investigation domain continuation

[ADR-006](../decisions/0006-investigation-context-and-handoff.md) and documents
28–32 separate request context, current editorial grouping and triage. Later
AnnotationRevision, ResearchTask, SavedView, ResearchCue/Hit, ReportRevision and
CaseTransfer/Import are logical contracts owned by those stages. None is an ACL,
an automatic evidence approval, or an implemented table. Byte/provenance history,
editorial approval, triage, personal attention and report disclosure remain separate.

## Browser acquisition extension

ADR-007/documents 35–37 introduce PairingIntent, CompanionGrant, BrowserUpload and
ArtifactSlot, BrowserAcquisition and later ResearchSession/Observation. The upload
is not a successful Capture until validated fenced acceptance. BrowserAcquisition
holds client-claimed URL/time/environment separately from server submitter/receipt/
verifier observations; origin_client_submitted is distinct from origin_imported and
server acquisition. Existing review/publication/context/triage state stays separate.
A Source groups claimed URL identity, not independently attested source ownership.
Unknown browser profiles are ineligible for automatic baselines/publication.

## Integrated authority records

Documents 40–42 refine existing state separation with exact typed DependencyEdge,
PinReference, RemovalFence/epoch, ResourceReservation/generation and FeatureDescriptor/
qualification applicability. These are future logical contracts, not tables already
present in source. Dependency writes commit with consumer identity; pins/counters
are reconciled from authoritative references; no cached policy answer grants access.
Core V0 uses only actual capture/export/publication dependencies. Channel-specific
foreign/browser claims remain separate from receipt/integrity/permission facts.

## Later identity/access domain

Document 48 adds future IdentityAssociation/UserLifecycle, versioned RoleBundle/
RoleAssignment, Invitation, AccessSpace/SpaceMembership/flat GroupGrant and scoped
ServicePrincipal. User-facing roles are independent of PostgreSQL roles in 45.
U2 gives each capture exactly one custody space; collections and derived selections
must stay within it. Global URL identity is not a grant or a way to reveal hidden
capture history. Scope moves mutate audited access metadata and fences, never
original bytes/provenance. V0 still implements none of these future privacy claims.
