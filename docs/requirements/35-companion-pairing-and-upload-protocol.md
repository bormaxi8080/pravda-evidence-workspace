# Companion identity, authorization and resumable intake

Date: 2026-11-09. Status: **selected B0/B1 protocol design; unimplemented**.
Owner: API/security/backend. Authority: ADR-007. Applies alongside, not instead of,
the same-origin cookie/CSRF API in document 16. No OpenAPI/collection exists for
these endpoints yet; EWP-42 creates authoritative schemas and generated client types.
Pairing uses the device-approval pattern referenced in the platform review, without
claiming a general-purpose OAuth server or changing GitHub admission.

## Requirements

### REQ-BCP-001 Human-approved bounded pairing

Pair only with an explicitly configured TLS origin and its advertised instance ID.
An expiring random secret device code is kept in the trusted extension session;
the short user code is entered on the Workspace's logged-in approval page. Show
instance/account, matching confirmation phrase, requested scopes and untrusted
device label. Approval requires enabled editor/admin, normal CSRF and explicit
confirmation. Never put device/access secrets in URLs, browser history, page DOM,
logs, notification text or content-script messages. Denial/expiry cannot grant access.

### REQ-BCP-002 Narrow revocable credentials

Issue opaque 256-bit random bearer tokens with 15min lifetime, actor, device-grant,
instance security epoch and selected scope set. Store only token digests server-side
and use trusted-context storage.session client-side; no persistent refresh token or
Workspace/GitHub cookie. Every operation rechecks actor enabled/admission/role,
grant status/expiry, instance epoch, scope and resource ownership. CORS/extension ID
are additional controls, never authentication or proof of collector authenticity.

### REQ-BCP-003 Fixed-origin transport and isolated privilege

Use only exact configured HTTPS origin, fixed versioned paths, credentials=omit,
Authorization header and redirect=error. Never follow an upload URL supplied by a
source page, capability response or redirect; no presigned third-party storage URL.
Server validates configured extension-origin allowlist when Origin is present;
null/disallowed origins fail, and missing Origin never bypasses bearer checks.
No wildcard credentialed CORS, TLS bypass, HTTP fallback or cookie-auth fallback.

### REQ-BCP-004 Owned resumable immutable upload slots

Create a bounded upload intent with client_capture_id, selected profile/context and
declared immutable artifact inventory/size/SHA-256. Reserve capacity before intake.
Allocate sequential per-artifact offsets and accept bounded chunks with exact hash,
offset and length. Replaying identical bytes at an already committed offset is safe;
conflicting/out-of-order bytes fail without overwriting accepted content. Durable
status, not the client's last response, determines committed offsets after a crash.

### REQ-BCP-005 Fenced verification and at most one accepted result

Finalize only a complete uploaded inventory matching its pinned request digest;
enqueue isolated validation under normal admission. Recompute hashes, validate
profile/MIME/bounds and promote through fenced staging/DB finalization. A client
finalize call or 202 is not success. Return ready only with one accepted capture ID
and server verification/receipt digest. Retry/lost response cannot create a second
capture or fetch a live URL; cancellation/revoke before acceptance fences completion.

### REQ-BCP-006 Negotiated contracts and explicit failure

Advertise protocol/profile/schema versions, enabled modes, safe effective limits and
supported package versions before pairing/submission. Reject unknown versions/fields,
unsupported required artifacts, oversize input and stale context with typed errors.
The companion API cannot publish, approve, enumerate arbitrary evidence, change
users/roles, create watches, export an archive or execute a remote capture command
without a fresh local user action. Server flags cannot enlarge browser permissions.

## Routes, principals and scopes

Prefix `/api/companion/v1`. Resource IDs are UUIDs; short code uses eight unambiguous
characters. JSON is UTF-8; control bodies <=256 KiB with unknown fields rejected.
Capabilities never include bearer material, internal hosts/paths or deployment secrets.

| Operation | Principal/input | Result / consequential behavior |
| --- | --- | --- |
| GET `/capabilities` | No bearer; rate-limited safe instance metadata | 200 instance_id, protocol=companion/1, profiles, flags, limits, min/max client versions |
| POST `/pairings` | No bearer; approved package client_id, claimed label/version, requested scopes | 201 pairing_id, secret device_code, user_code, phrase, fixed verification_uri, expires_in=300, interval=5 |
| POST `/pairings/token` | device_code in body, never query; rate/expiry checked | 202 authorization_pending; 429 slow_down; denied/expired fail; first approved exchange 200 access_token/token_type/expires_in/scopes/grant_id |
| GET `/connection` | Valid token | Own account/grant/capabilities/expiry only; no session cookie |
| GET `/collections` | collections:read | Bounded IDs/names for existing shared collections, not evidence bodies or private saved views |
| POST `/capture-intents` | capture:create + key; B0 URL/options/context | 202 existing server capture/job IDs; existing SSRF/default ports/queue rules unchanged |
| GET `/capture-intents/{id}` | status:own + current requester ownership | Safe own outcome and relative private UI link; no raw artifact read |
| POST `/uploads` | upload:create + key; B1 inventory/context/client_capture_id | 201 upload ID, revision, expiry, fixed artifact slot IDs; reserves declared bytes |
| GET `/uploads/{id}` | status:own + upload ownership | State/revision, durable committed offsets, verification errors or ready receipt |
| PUT `/uploads/{id}/artifacts/{slot_id}` | upload:write + ownership; offset/length/chunk SHA-256 | 200 durable offset; byte replay safe; conflicting overlap/out-of-order 409 |
| POST `/uploads/{id}/finalize` | upload:finalize + key, expected_revision, inventory digest | 202 validation/job IDs or replay of prior result; incomplete 409 |
| POST `/uploads/{id}/cancel` | upload:cancel + expected_revision | 200/202 cancellation, accepted terminal result 409; no capture purge |
| POST `/disconnect` | Own valid token/grant | Revoke current grant, fence pending acceptance, idempotent explicit action |

The web UI uses its existing cookie/CSRF routes to approve/deny pairings and list/
revoke grants (`/api/v1/companion-grants`, POST `/{id}/revoke`). Editors manage only
their own grants; admin may revoke any. Pairing does not let a user choose another
actor. B2 adds scoped session start/stop/status and bounded event metadata only
after its separate gate; upload authority remains per approved item.

Default B0 scopes: collections:read, capture:create, status:own. B1 additionally
requests upload:create/write/finalize/cancel through renewed explicit approval.
No scope aliases to admin or unrestricted `/api/v1`. User disabling or admission
suspension immediately denies each new protected operation and finalizer commit.

## Pairing, expiration and reconnect behavior

Device codes are cryptographically random (at least 256 bits), stored as digests;
user-code lookup is digest-based with a unique pending code and bounded attempts.
Selected limits: five starts/hour per browser-install hint, 300/hour per source IP,
1,000 starts/hour and 100 pending intents per instance,
five failed approval-code entries/10min per IP/account, at most ten grants/user.
Install hint is not authentication; abuse controls also use global capacity/IP.
Poll no faster than 5s; slow_down increases delay by 5s, never busy-loops. UI displays
the configured origin, requires manually entering the displayed code and matching
phrase, and explains that an unsolicited pairing request must not be approved.

Pairing states: pending -> approved -> consumed, or denied/expired. Approval cannot
be reused; concurrent exchanges have one winner. If the token response is lost,
the consumed intent does not mint another token: user re-pairs and revokes the
orphaned grant; its token also expires within 15min. No secret replay cache needed.
Expiry/restart requires interactive reconnect, not a persistent hidden refresh key.

Re-pairing as the same enabled actor may explicitly adopt the actor's existing
unaccepted upload after checking destination/inventory/expiry and recording grant
transition. Another actor/instance cannot adopt it. This is a reviewed resume,
not trust in the installation UUID. Rejected/revoked uploads cannot be adopted;
user must make a new approved intent for retained local bytes. Logout from the web
does not silently revoke a separate device grant; UI offers revoke-all connections.

## Byte protocol and limits

Artifacts use fixed slot paths, never client filesystem names. PUT carries binary
bytes, X-Upload-Offset, Content-Length and X-Chunk-SHA256. The browser supplies
Content-Length from the bounded Blob/body; extension code does not set a forbidden
request header. Chunk size is 1 MiB except
the final shorter chunk; offsets are multiples of 1 MiB except the terminal size.
HEAD/content encoding/compressed transfer tricks cannot bypass byte accounting;
request decompression is disabled for these binary endpoints. Hash each stored
chunk and whole artifact independently; acknowledge only after durable commit of
bytes/offset, with reconciliation for bytes written before a DB crash.

Idempotency key is actor+instance+operation scoped for 24h. Unique
(instance_id,actor_id,client_capture_id) plus immutable request digest prevents
duplicate acceptance across new grants. Same ID/different inventory conflicts;
ordinary repeated intentional capture gets a new client_capture_id. Chunks also
serialize concurrent writers to a slot. Finalization locks current upload/grant
state and uses a generation; integrity/permission/cancel checks apply at commit.

Upload TTL: 24h, five open uploads/grant, 20/actor, 1 GiB quarantined/reserved per
instance, one active validator slot, global pending-job cap 1,000 and existing disk
reserve. Individual profile caps are in document 36. Limit grants cannot reserve
unbounded space by multiplying users; reservation is installation-wide. Selected
HTTP request timeout 20s/chunk, client retry max five transient attempts with
1/2/4/8/16s delays and 0–20% jitter; then visible stalled state. Honor Retry-After.

Error envelope follows document 16. 401 expired/revoked -> stop and reconnect;
403 scope/actor/admission -> stop; 404 hides missing/foreign IDs; 409 offset/revision/
digest/state -> reconcile; 410 upload_expired -> explicit new intent; 413 quota/size;
422 unsupported profile/policy; 429 throttle; 503 dependency/storage -> bounded retry.
After uncertain finalize, query status before retry. All responses no-store; access
logs redact auth/device codes and URL bodies. OPTIONS/preflight grants no authority.

No bearer token, upload ID or reference URL can authorize arbitrary egress by the
server. B1 source URLs are validated as provenance strings and never dereferenced;
B0 server fetching uses its existing network boundary. Pairing-host access is a
user-selected control-plane exception, not permission to ingest internal source tabs.

First connection configuration is an HTTPS origin on port 443 without an application
subpath. Non-default ports/path-prefix installations need a later tested adapter;
never strip or rewrite a supplied URL silently. Host permission covers the whole
host, so the broker separately enforces the fixed API paths and exact origin.
Only unexpired/non-revoked grants count toward ten active grants/user; a grant in
this first protocol expires with its issued 15min token and retains safe audit
history. Reconnection creates a newly approved grant, not a refreshed hidden token.

## B2 session control extension

B2 explicitly requests session:own in pairing approval. POST `/sessions` takes
client_session_id, source_origin, collection_ids, selected profile and requested
caps; creates a private control session/epoch, not a remote instruction to capture.
GET `/sessions/{id}` reads own safe state; POST `/{id}/heartbeat`, `/pause`, `/resume`
and `/stop` require ownership/current revision or session epoch as appropriate.
Start/resume originates only from an explicit extension UI gesture. No server
queue entry or webpage message may cause the client to start recording.

Selected session lease is 60s, renewed at most every 30s while the selected tab
is foreground and consent remains active. Client pauses immediately on a failed
renewal and no later than local lease expiry; server revoke cannot guarantee
instant offline-device erasure. If wake/timer timing cannot preserve the lease,
pause rather than keep the worker alive artificially. Heartbeat carries state/
counts only, not unselected page URLs/content. Navigational observations stay local
until reviewed upload. Linked uploads pin session_id/epoch/observation_id but use
their own upload consent and ownership; accepted capture history is not erased by
session stop. No more than one active session/grant and one local session/profile.

A stopped/revoked session cannot register a new acquisition observation. ADR-008/
document 40 clarifies historical linkage: a descriptor registered while its acquisition
lease was active can be explicitly upload-approved after stop; current upload/grant/
actor authority and keep/cancel disposition still gate finalization. Historical valid
linkage does not require recording to remain active. Unknown/changed linkage or
new registration under a stopped epoch fails; it cannot invent history. Server
records control actions and registered/accepted observation references, not an
unbounded page-visit trail. Session status never grants publication rights.

B2 POST `/sessions/{id}/observations` registers client observation ID, epoch, fixed
artifact-inventory/context digest and claimed acquisition interval under the active
lease, ownership and idempotency checks. It sends no page URL/body/original bytes;
this minimal registration is disclosed in session consent. Own bounded status can
resolve lost acknowledgement. Registration freezes the descriptor; it is not upload
consent, server receipt of original bytes or attestation of the client clock. After
stop, a matching registered descriptor may receive explicit item/batch upload approval.
An offline/unregistered local item cannot be inserted retroactively into that epoch:
retain it for explicit manual B1 review/new intent with an unverified historical
session claim, preserving original bytes/metadata rather than fabricating B2 proof.
Grant/session revoke still rejects continuation; no automatic fallback or recapture.
