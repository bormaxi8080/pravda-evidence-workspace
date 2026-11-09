# Identity, security, publication and audit requirements

Date: 2026-11-09. Status: **proposed**. Owner: security/backend lead.
Sources: concept sections 6.2–6.4, 17, 20–22, 34; current `auth.py`,
`routers/auth.py`, `routers/public.py`, `routers/snapshots.py`, `audit.py`.
Decisions: DEC-05/06/09/11. No security review or runtime qualification is claimed.

## Proposed V0 permissions

| Operation | Anonymous | Editor | Admin |
| --- | --- | --- | --- |
| View active public projection/screenshot | Yes | Yes | Yes |
| Read internal captures/artifacts/jobs/collections | No | Yes, shared newsroom | Yes |
| Submit/cancel capture jobs, edit notes/tags/collections/review | No | Yes | Yes |
| Private export | No | Yes | Yes |
| Publish/revoke | No | No | Yes, approved complete evidence |
| Archive/hide evidence | No | No | Yes, after active publication revoked |
| Audit list/export; user/role administration | No | No | Yes |
| Host backup/restore/secrets/purge | No | No | Operator procedure, not granted by UI admin role |

There are no per-collection ACLs or separate reviewer role in V0. Editor publishing
and stronger separation of duties require an explicit future policy change.

## Requirements

### REQ-SEC-001 Fail-closed admission and durable sessions

Admit GitHub identities only under configured organization/login policy; empty
allowlists shall deny admission. Document provider failure/membership semantics;
do not infer membership from an unverified client claim. Persist users by provider
ID, keep current login as mutable metadata. Use OAuth state/appropriate protocol
protections and local safe return URLs. Persist opaque revocable sessions with
absolute/idle expiry; rotate on login/role change and set HttpOnly/Secure/SameSite
cookies. Logout revokes server state. No process-local dictionary is session authority.

### REQ-SEC-002 Uniform access checks and CSRF

Recheck enabled user/role for every protected service call, including artifact reads,
export/status/SSE and batch endpoints. Deny private-object access by guessed UUID.
Cookie-authenticated state changes shall use CSRF protections and safe HTTP methods;
GET does not publish, delete, cancel or change editorial state. Same-origin browser
API is sufficient for V0; API keys and cross-origin integrations are excluded.

### REQ-SEC-003 SSRF policy at every network boundary

Allow public HTTP(S) destinations only. Validate scheme, host, ports, credentials,
all resolved IPv4/IPv6 addresses, redirects and browser subrequests/WebSockets;
block loopback/private/link-local/reserved/cloud-metadata and internal service
networks, including alternate encodings and DNS rebinding. A DNS check followed
by unrestricted browser egress is insufficient. Enforce restricted routes/egress
outside hostile page JavaScript. Capture, probes, engine callbacks and receipt/PDF
rendering shall not create alternate unrestricted network paths.

### REQ-SEC-004 Isolated bounded hostile-content processing

Run browser execution with least privilege, working sandbox or demonstrated
equivalent isolation, dedicated temporary volume, bounded CPU/memory/PIDs/disk/time,
no host network/socket and no application/session/database secrets. The current
`--no-sandbox` baseline is not accepted as evidence of safe isolation. Validate
runner outputs before trusted finalization. Safe operation on synthetic pages is
not a proof of containment; document/test the deployed network/process boundary.

### REQ-SEC-005 Explicit versioned publication projection

Publishing shall atomically verify approved complete evidence and create an active
Publication referencing a pinned public allowlist/revision. V0 public projection
contains approved display/source URL, capture time, screenshot, profile, screenshot
digest and optional approved availability observation. Do not expose original raw
headers/URLs with secrets, notes, usernames, internal paths, jobs, audit or private
export. Admin preview must reveal screenshot/content disclosure risks; unsupported
redaction means keep private, not edit original evidence bytes.

### REQ-SEC-006 Revocation across pages and assets

Resolve every public page/screenshot/metadata request through active publication
state; capture ID alone is insufficient. Send no-store for V0 public and private
evidence responses, remove long-lived immutable caching, and prevent proxy/CDN
bypass. After revocation, new server requests shall deny the page and all its
assets consistently. Already downloaded/browser-retained/third-party copies cannot
be recalled; state that limit before publication. A revoked slug stays revoked.

### REQ-SEC-007 Safe rendering and files

Public and private previews shall render screenshots plus escaped metadata;
never execute archived HTML/MHTML in the application origin. Private raw downloads
use safe generated names, attachment disposition and nosniff; sanitize MIME handling
and enforce path containment. Strict CSP/security headers shall cover UI/public
views. ZIP/CSV receipt/audit output shall handle injection/traversal and formula
interpretation risks in their actual consuming format.

### REQ-SEC-008 Accountable append-only audit

Record login/logout/admission, user/role changes, capture request/outcome/retry/
cancel, editorial/review, collection/tag changes, export, publish/revoke, archive
and operational actions. Audit includes actor/resource/correlation/time and bounded
safe details, never tokens/raw secrets. Audit/business mutations are transactional;
operator activities use a defined durable recording/reconciliation path. Application
roles shall not update/delete audit history. Host DB administrators remain trusted.

## Threat scenarios and design outputs

Prioritize malicious destination/redirect/DNS, page escape/egress, role/session
bypass, guessed file IDs, stale public caches, forged batch confirmation, receipt
resource fetch, filename/CSV injection and evidence tampering. Complete a threat/
control/test table before enabling hostile public Internet capture. Security
controls are required in V0; independent review breadth grows before production.

Bootstrap admin with a documented operator command using a verified identity;
never promote the first arbitrary registrant. DEC-11 resolves disablement, session
invalidation, audit access and the last-admin recovery path. Acceptance:
ACC-01/02/04/05/06/07/08/09/10/11/12.
