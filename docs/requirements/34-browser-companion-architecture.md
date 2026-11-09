# Browser companion: product boundary and architecture

Date: 2026-11-09. Status: **selected post-V0 design; not implemented**.
Owner: browser/product/security engineering. Authority: ADR-007, current user request,
concept sections 5.2/36; [platform evidence](../reference/browser-extension-platform-review.md).
This is the browser-channel authority superseding the deferral in document 32.

## Requirements

### REQ-BRW-001 Independent staged companion

The system shall support an optional independently built/versioned Chromium MV3
companion. B0 hands off a URL; B1 preserves explicitly selected browser content;
B2 assists recording one consented tab/origin. Each has separate capability flags
and qualification. No extension is required for V0/core production operation, and
installing it cannot enable an unqualified server endpoint or evidence profile.

### REQ-BRW-002 Explicit acquisition modes

UI shall distinguish "Capture URL on server" from "Save this browser view".
B0 sends only explicit URL/options/editorial intent to the existing server pipeline;
server network policy remains mandatory and user login state is not transferred.
B1 saves a visible viewport PNG and, only when selected/supported, MHTML from the
same target tab under a separate acquisition profile. B2 follows the restricted
session contract below; no silent mode/profile fallback or server recapture retry.

### REQ-BRW-003 Visible consent and collection context

Before collection, show Workspace origin/account, collection IDs, mode/profile,
scope, rationale, inclusions and local/offline handling. Start/stop/pause are explicit
controls. No last-tab/global collection inference, install-time browsing collection
or capture caused by a web page message. A URL handed off at the user's request is
an intent, not evidence of what the tab displayed. Preserve context per item.

### REQ-BRW-004 Minimal permissions and trusted broker

B0 shall use activeTab/storage/alarms and optional permission for the configured
HTTPS Workspace host. B1 adds user-granted scripting/pageCapture only for enabled
features; B2 adds optional sidePanel. No all_urls/cookies/history/debugger/proxy/
webRequest/native helper permission. No static all-page content scripts. The trusted
worker alone selects exact-origin API paths, holds credentials and performs uploads;
page/DOM messages cannot provide fetch destinations, bearer headers or executable code.

### REQ-BRW-005 Termination-safe local execution

Persist state transitions in bounded IndexedDB, register event listeners at worker
startup and resume through durable per-item state rather than globals/keep-alive.
Transient action popup closure cannot claim success or lose an already staged item.
Capture success requires a complete staged local inventory; server success requires
the authenticated ready receipt. Browser restart/update never resumes recording
automatically; undecided acquisition becomes interrupted, not newly recaptured.

### REQ-BRW-006 Usable status, accessibility and safe commands

UI shall expose pairing, current target, local pending/error/quota, server validation,
accepted capture link and Stop/Discard/Retry actions with keyboard/focus/non-color
status. The badge/panel distinguishes recording from pending upload and permission
loss. No indication that partial/queued bytes are preserved on the server. Existing
Workspace login is required when opening private detail; an ID/deep link grants no
authority. Page text is always escaped, never rendered as extension HTML.

## Logical modules and data flow

```text
User gesture -> action popup / options / B2 side panel
                         |
                    typed local commands
                         |
              MV3 worker / permission broker
                 |                  |
         on-demand isolated     IndexedDB spool + journal
         measurement script          |
                 |          fixed HTTPS Workspace API
        selected foreground tab      |
        PNG / optional MHTML    pairing + narrow authorization
                                     |
                          quarantine / bounded verifier
                                     |
                        fenced finalizer -> DB + artifact store
                                     |
                     private capture detail / own ready receipt
```

Suggested source modules under future `browser-extension/`: platform/chrome adapter,
worker command router, capture coordinator, instance client, session controller,
spool repository/migrations, UI and generated contract types. Bundled TypeScript
with a small UI is sufficient; no SPA framework/new microservice/native daemon is
required. Application services reuse admission, audit, jobs, permissions, artifacts
and review; they do not run a browser to repair submitted bytes.

Content scripts only report bounded top-frame URL/document/viewport/scroll/zoom
measurements and selected user text when that feature is explicitly enabled. They
receive no tokens, collection search results or generic network capability. Validate
runtime sender extension ID, tab/frame/document association and request nonce. Do
not accept window.postMessage or externally_connectable commands from sites.

## B0 / B1 user journeys

1. User configures exact HTTPS Workspace origin, grants only that host and pairs
   through its normal logged-in approval screen (document 35).
2. User invokes extension on a supported public HTTP(S) tab; browser-internal,
   file/data/blob/extension, incognito, Workspace itself and syntactically identified
   local/private targets are denied by product policy, even if a browser API could technically access them.
3. User selects collection/rationale and mode. B0 sends a server intent. B1 explicitly
   selects viewport-only or viewport+MHTML, with an authenticated-content warning
   and local thumbnail/inventory review. B1 may preserve a logged-in public-origin
   view; it neither reads cookie APIs nor assures the content contains no secrets.
4. Stage immutable original bytes locally, confirm upload to the paired instance,
   transfer under limits, show validation state then open private capture detail.
   An offline saved item waits for explicit upload/resume consent after reconnect.
5. User can create an H1 annotation in Workspace after acceptance, once its adapter
   is qualified; a highlighted string from the live DOM is not already a verified
   quote from the saved MHTML.

One instance/account is active at a time. Switching either pauses work and cannot
reroute existing items. Existing staged items retain original destination/account/
collection/profile and require explicit disposition, not new implicit defaults.

## B2 assisted-session boundary

User starts a session for one foreground tab, one exact source origin and a fixed
collection/profile, with badge and side panel controls. After qualified same-origin
top-level load completion and a 2s debounce, optionally capture under the existing
activeTab grant; use at least 5s between starts, max 20 items/session, 30min session.
No scrolling, background tabs, login automation, arbitrary SPA/DOM mutation loop or
recursive link following. Explicit "Save current view" handles unsupported SPA
states/scroll positions. Duplicate navigation events coalesce, not loss of repeated
explicit user captures. Each accepted observation remains a separate Capture.

Cross-origin navigation, focus/tab switch, permission/token loss, restart/update,
unverifiable document identity or quota exhaustion immediately pauses; reactivation
needs a user gesture and scope confirmation. Session stop prevents new acquisition
and unconfirmed upload; disposition of already approved pending uploads is explicit.
No claim of complete browsing history, full social timeline or atomic DOM capture.

API floor Chrome 120; current supported stable builds need actual qualification.
Manifest permission variants, package identity, platform limits and release policy
are defined in documents 37/38. Firefox/Safari/Edge require separate qualification,
not merely a shared WebExtension label. No runtime browser dependency exists yet.

B2 automatic observations are staged locally; every upload batch needs explicit
review/consent, not merely session start. Its event source is tabs.onUpdated for
only the consented tab, plus activation/window events and on-demand probes under
the actual grant. No webNavigation or tabs-wide URL/history permission is added.
Document identity uses the scripting result documentId/top frame, not just URL;
qualification must reject unverifiable races rather than silently broaden access.
