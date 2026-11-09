# Editorial functionality and UX requirements

Date: 2026-11-09. Status: **selected UX requirements; implementation pending**. Owner: product/UX lead.
Sources: concept sections 2.2, 13, 17–20, 27; root `index.html` and existing
Jinja templates. Decisions: DEC-01/05/06. The mockup is design input, not evidence
that filters/settings/review/queue behavior are implemented.

## Screen and function inventory

| View | V0 responsibilities | Required non-happy states |
| --- | --- | --- |
| Login | Explain newsroom admission, start GitHub login, safe return destination | Denied membership, provider failure, expired state/session |
| Dashboard | Recent captures/jobs and truthful aggregate counts | Empty installation, dependency warning, unavailable metrics |
| New capture | URL, condition, tags/note, limits and private default | Invalid/blocked URL, queue full, duplicate submission, unsupported options |
| Batch import | Upload/text CSV, preview/row choices, confirm, mixed progress | Parse/size errors, duplicate rows, expired preview, capacity conflict |
| Jobs queue/detail | Current phase, attempts, safe errors, retry/cancel controls | Disconnected progress, stale worker, exhausted retry, cancelled work |
| Capture archive | URL/domain, dates, creator, state, tags/collection filters and pagination | No matches, invalid filter, large page request |
| Capture detail | Screenshot, provenance, artifacts, integrity, editorial/review/publication state | Partial/corrupt/missing files, unknown provenance, edit conflict |
| Collections/tags | Many-to-many membership and metadata management | Duplicate names, membership conflict, empty group |
| Publication preview | Exact public screenshot/metadata, review revision, disclose/revoke controls | Not approved, sensitive fields, stale approval, role denial |
| Public viewer | Active publication projection only | Unknown/revoked slug, removed artifact, no live origin check |
| Export/receipt | Profile, omissions, explicit editorial-data choices and result | Missing required output, PDF unavailable, export limit/error |
| Settings/status | Effective limits, deployment/profile version and service state | Read-only setting, restart required, secret redaction |
| Audit | Admin-only search/list and bounded CSV export | Denied access, empty results, export failure |

## Requirements

### REQ-UX-001 One coherent source lifecycle

Use consistent terms across navigation, detail, queue and receipt: source, capture,
attempt, artifact, review and publication. Existing "snapshot" routes may remain
as compatibility aliases, but shall not imply that a source has only one capture.
Expose private/public, evidence complete/partial and review state separately.

### REQ-UX-002 Organization and shared archive

Editors shall add/remove captures from multiple collections, normalize tags and
edit title/notes without changing evidence. Collection/tag deletion removes the
grouping, not its captures. All admitted users share V0 internal evidence; do not
present collections as private folders. Filter/sort/pagination parameters shall
survive navigation where useful and have stable documented ordering. Selected V0:
case-insensitive URL/title query, exact normalized host/creator, collection,
all-selected-tags matching, review/publication/capture states and UTC date interval
with inclusive start/exclusive end. Sort by capture time descending, then ID;
reject reversed intervals rather than silently changing the query.

### REQ-UX-003 Explicit review with revision awareness

An editor/admin shall move complete evidence through unreviewed/in_review/approved/
rejected with actor/time and bounded reason. Approval refers to an exact evidence
and editorial revision. Further editorial edits invalidate approval for a
new publication and return review to in_review. Existing public projections remain
pinned until explicitly updated/revoked. V0 allows a user to review their own work;
two-person approval is a later optional policy, not an implied safeguard.

### REQ-UX-004 Publication is a separate deliberate workflow

Only admins publish/revoke in selected V0. The UI shall preview exactly what an
anonymous visitor can see and require an explicit action on approved complete
evidence. Creating a capture, tagging, reviewing or exporting shall never publish it.
Show an active public link and its withdrawal limits. Raw archive/private export
buttons shall not appear as public viewer capabilities in V0.

### REQ-UX-005 Actionable errors and honest progress

Show queued/running/retrying/partial/failed/cancelled states with next action and
safe reason. Do not show fabricated percent-complete values without a defined basis.
SSE disconnect shows reconnecting and reloads durable status; it does not imply job
failure. A retried terminal capture points to the new capture. Monitoring absent
means unknown/not checked, never a reassuring "online" inferred from old HTTP status.

### REQ-UX-006 Accessible and responsive core workflow

Provide keyboard-operable forms/actions, visible focus, associated labels, readable
status/error text and non-color-only state indicators. Keep dark/light themes and
responsive layouts from the prototype. Use the WCAG 2.2 AA evaluation target selected in document 16 and test contrast/focus
before making a compliance claim; no
current conformance certification is asserted by this document.

### REQ-UX-007 Settings reflect actual configuration

Show only implemented controls with their permission/effect/restart requirements.
V0 configuration may remain environment-managed; read-only settings must look
read-only. Never render secrets or provider token values in HTML/diagnostics. Do
not add mock controls for AI, tenancy or unsupported storage/engines as working features.

## Journeys to specify and demonstrate

1. Editor preserves a public article, inspects complete evidence, adds notes/tags,
   organizes it and approves review while the capture remains private.
2. Admin previews the public projection, publishes, opens an anonymous session,
   then revokes and verifies every server-served public asset is denied.
3. Editor previews a mixed-validity CSV, confirms selected rows once, watches mixed
   outcomes and retries a failed source without duplicating successful siblings.
4. Operator recovers a worker or restores the installation; editor can locate and
   independently verify the same evidence afterward.

Keep destructive/irreversible consequences explicit in the product flow without
exposing irrelevant implementation details to newsroom users. Acceptance:
ACC-01/02/03/04/05/06/07/09/11/12.

## Detailed selected design

See [the baseline register](13-selected-v0-baseline.md),
[contracts and operator procedures](README.md) and
[assignable work packages](18-assignable-work-packages.md).
Implementation/qualification remain pending; source presence is not test evidence.
