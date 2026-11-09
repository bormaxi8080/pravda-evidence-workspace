# Companion local lifecycle, privacy, release and operations

Date: 2026-11-09. Status: **selected B0–B2 design; unimplemented**.
Owner: browser/security/operations. Authority: ADR-007 and documents 34–36.
Limits below are engineering starting values, not measured supported capacity.

## Requirements

### REQ-BLC-001 Bounded explicit local retention

Store evidence in extension-origin IndexedDB, never storage.sync, page localStorage
or ordinary downloads. Journals record item ID, original instance/account/context,
profile, inventory digest, consent, staged slots, offsets and disposition. Admission
checks actual quota and selected spool cap; no unlimitedStorage permission or silent
eviction of pending evidence. UI exposes retained bytes, expiry and explicit discard.
Browser-managed storage is not claimed encrypted against a local/profile attacker.

### REQ-BLC-002 Session pause, stop and scope fencing

B2 shall bind a visible session to one tab/window/source origin/collection/profile
with generation/revision and expiry. Pause/stop, context switch, grant/token loss,
focus loss and cross-origin navigation fence pending acquisition before persisting
or transmitting output. Returning to the tab never silently resumes. B2 automatic
snapshots remain local and require explicit item/batch disclosure review before
upload; recording consent is not general outbound-send authority.

### REQ-BLC-003 Recovery without duplicate or phantom captures

On worker restart reconcile staged inventories and durable server status before
retry. Browser restart/update clears session credentials and recording consent;
pending items remain needs_reconnect/review, never recapture the current page to
replace missing bytes. Accepted receipt identity prevents duplicate upload/acceptance.
Corrupt local state is quarantined/unavailable with actionable disposition, not
presented as a server-stored success. Expired server upload needs reviewed new intent.

### REQ-BLC-004 Private content and attack-surface boundaries

No collection while incognito, on denied schemes/known local targets/Workspace
itself or outside the selected tab scope. No cookie/password extraction, keystroke
logging, passive history, credential replay, third-party analytics or remote code.
Keep page/URL/note data out of general logs; validate all typed message senders and
escape every preview. Explain that authenticated pixels/MHTML may contain secrets
despite these restrictions; submission is private and cannot automatically publish.

### REQ-BLC-005 Controlled build, identity and compatibility

Produce reproducible reviewed MV3 bundles with locked dependencies, source revision,
artifact hashes, supported protocol/profile range and package identity. Development,
managed deployment and public store builds have separate IDs/allowlists and evidence.
Server rejects unsupported versions without deleting pending bytes. Update/schema
migration pauses recording, validates storage transactionally and never widens
permissions or uploads old content automatically. Distribution/release is separately
authorized and needs current store/privacy/security review; no listing is created now.

### REQ-BLC-006 Revocation, restore and incident operations

Users/admins can revoke grants and inspect safe device/upload status. Every chunk,
finalization and status read enforces current grant/actor authority. Revoke fences
unaccepted intake, releases reservations and purges quarantine under bounded cleanup;
it does not erase accepted evidence. Restore rotates instance security epoch,
invalidates tokens/pairings and holds intake/automatic work until reconciliation,
deletion-ledger replay and deliberate re-pairing. Never revalidate old bearer tokens
by restoring an older DB snapshot.

## Local state machine and retention

```text
idle -> acquiring -> staged -> awaiting_upload_consent -> uploading
                                                    -> waiting_network
uploading -> awaiting_server_validation -> accepted -> local_bytes_removed
nonterminal -> interrupted / needs_reconnect / failed / discarded / expired
```

One local writer/capture slot uses a journal generation. All transitions commit
atomically with inventory/consent references. A local success marker follows complete
staging; a server success marker follows a ready receipt whose hashes match local
inventory. Hash mismatch blocks success and keeps explicit failure state. During
recovery, partial IndexedDB writes cannot masquerade as a complete local inventory.

Selected spool: 100 MiB and at most 20 retained items per browser profile, including
partial/candidate bytes; reserve before a copy and reject overflow. Browser quota
may be lower: handle QuotaExceededError without dropping another item. Retain
unaccepted bytes at most 24h, show warning and expire explicitly; cleanup runs on
worker/UI startup and periodic alarm when possible, not an exact deletion deadline
while Chrome is closed. On return, expired bytes are not displayed/uploaded and
are removed before normal work. Accepted bytes are removed after verified receipt;
minimal receipt/status IDs last at most seven days, subject to explicit clear.

No long-term credential in local IndexedDB/storage.local. Tokens/device codes reside
only in trusted storage.session with restricted access level; content scripts never
receive them. Nonsecret origin/instance ID/preferences may persist locally, with
clear-instance cleanup. Clearing browsing history is not a reliable spool purge;
provide explicit "Clear local pending evidence" and distinguish server retention.
Uninstall/disable and host/profile backups cannot be treated as provable erasure.

## Race and cancellation table

| Trigger | Required result |
| --- | --- |
| User switches tab/window during acquisition | Invalidate generation; discard candidate; no wrong-tab upload |
| Tab navigates/same URL new document | Compare document/event generations; abort if changed/unprovable |
| B2 cross-origin or activeTab loss | Pause with origin/grant explanation; user gesture required |
| User changes instance/account/collection | Stop current session; old items keep pinned destination/context |
| User stops while upload pending | No new acquisition; offer keep approved uploads or cancel unaccepted items explicitly |
| User revokes while finalizer runs | Transaction/fencing decides one winner; revoke before acceptance blocks commit; accepted bytes remain private |
| Last upload/finalize reply lost | Query owned durable status and offsets; never create another capture blindly |
| Token expires mid-upload | Stop requests, preserve local bytes, explicit re-pair/adoption review |
| Server rejects integrity/profile | No auto resend/recapture under another profile; explicit diagnostic/disposition |
| Update/worker death before staging | Interrupted state, no invented files; fresh capture requires user action |

Sensitive candidate bytes should be discarded as soon as an acquisition scope check
fails; cleanup must invalidate stale callbacks so they cannot resurrect discarded
objects. A compromised client can bypass its own UI, so server trust remains limited
to authorized received bytes. Local guardrails are not cryptographic attestation.

## Deployment and incident procedures to implement

Server flags default off: companion_api_enabled, browser_intake_enabled and
assisted_session_enabled. B0 can be enabled without browser intake; B1 requires
qualified profiles/quarantine/export; B2 requires its recording gate. Configure exact
extension IDs/origins and HTTPS canonical origin; reject Host/proxy-header confusion.
Do not grant every development ID in production. Validate quota/deadline settings.

Maintenance stops new reservations, drains/fences validation and reconciles slot
bytes with DB offsets/intents. Pending quarantine is temporary and excluded from
ordinary evidence backups; backup preserves safe metadata and accepted files.
After restore, pending uploads become interrupted/unresumable unless byte inventory
is explicitly restored and verified. Clients make new reviewed intents if necessary;
never claim restoration of discarded unaccepted bytes. Accepted originals, manifests,
receipt/channel/context and dependency maps are part of coherent evidence backup.

Security epoch is rotated as a mandatory restore/bootstrap operation before serving;
it is not copied unchanged from a historical snapshot. Incident revoke-all also
rotates epoch and stops intake. A lost browser cannot be remotely wiped by server
revocation; tell the operator which data may remain on the device/downloads/backups.
Emergency purge covers original and derived server bytes, report/search caches,
quarantine and deletion ledger; clients delete local dependencies on next authorized
contact where possible, without promising removal from an offline compromised client.

Monitor reservation/spool bytes, orphan slot age, upload/validation outcomes, permission
loss, paired/revoked/expired counts, protocol mismatches and cleanup results. Metrics
must not contain source URL/query, titles, notes, screenshots, bearer/device secrets
or persistent cross-installation tracking IDs. Audit IDs/actions/revisions/bytes,
not full evidence bodies. Endpoint and parser failure cannot leak local host paths.

Release checks: real-browser permission/worker lifecycle tests; controlled authenticated
fixture without real accounts; reproducible build/dependency scan; denial/message/XSS/
wrong-tab/upload crash tests; real DB/filesystem reconciliation and clean restore;
user-facing privacy/retention/permission descriptions. Store approval/signing and
cross-browser compatibility remain unavailable until actually performed.

B2 requires the 60s control lease in document 35 in addition to its 30min scope
limit; renewal failure or late worker wake pauses local recording. A local offline
manual B1 save can retain explicitly consented bytes within spool/TTL limits, but
cannot claim current server authority or upload until interactive reconnect/review.
No raw MHTML preview is rendered in the extension or Workspace: thumbnail/escaped
metadata only, with original files as protected attachments.
