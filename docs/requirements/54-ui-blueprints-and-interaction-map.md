# UI blueprints and interaction map

Date: 2026-11-09. Design revision: 0.10. Status: **selected UI direction and
interactive synthetic mockups; runtime implementation/qualification pending**.
Owners: product/UX, evidence engineering, browser engineering and security.
Authority: user requested Workspace/browser UI mockups followed by a detailed
versioned implementation plan. This document refines existing requirements; it
creates no new requirement IDs or backend endpoints.

## 1. Deliverables and authority

Open the [Workspace blueprint](../../design/index.html) and the
[browser companion blueprint](../../design/extension.html) directly as local files.
They use local CSS, JavaScript and a synthetic SVG news page; there are no web fonts,
analytics, external libraries or application requests. See the
[design guide](../../design/README.md) for entry points, query parameters, previews
and reproducible checks. Keep the [original mockup](../../index.html) as historical
concept input, rather than treating either mockup as a running application.

The hierarchy is: product/security/evidence contracts and ADRs, this UI specification,
then the HTML rendering. A pretty or clickable state never overrides authorization,
profile eligibility, integrity, resource limits or a contract failure. Prototype
role/state/release controls and explanatory design notes are review tools and
shall not be shipped as product controls.

The companion page simulates extension surfaces inside a design studio. It is not
an MV3 package, does not request permissions and is not installed in a browser.
In-memory interactions reset on reload; they are not durable state. Some later
screens deliberately expose a layout and explanatory preview rather than a complete
workflow. The inventory below distinguishes those from connected simulations.

Primary inputs: [UX](06-editorial-and-ux.md), [screen/API contracts](16-screen-and-api-contracts.md),
[history](21-source-history-and-comparison.md), [context](28-investigation-context.md),
[companion architecture](34-browser-companion-architecture.md),
[protocol](35-companion-pairing-and-upload-protocol.md),
[eligibility](40-evidence-eligibility-and-provenance-policy.md),
[identity](48-future-users-roles-and-access-spaces.md) and
[protected bytes](52-protected-byte-serving-and-read-budgets.md).

## 2. Visual and information architecture

Use a quiet editorial workspace: warm near-white canvas, restrained teal actions,
fine neutral borders, serif page headings and a system sans-serif for controls/data.
Use monospace only for identifiers, digests and protocol details. Maintain a dark
palette with the same hierarchy; danger, warning and success also need text labels.
The UI shall feel like a source desk, not an analytics dashboard with unexplained
scores or an automated credibility assessment.

Selected tokens are implemented in [styles.css](../../design/styles.css):

| Token | Light direction | Dark direction / behavior |
| --- | --- | --- |
| Canvas / surface | `#f7f6f2` / `#fffefa` | `#171614` / `#201f1c` |
| Text / secondary | `#28251d` / `#66655e` | `#eeede7` / `#b6b3a9` |
| Primary / subtle fill | `#01696f` / `#e2eeea` | `#74c2ca` / `#20383a` |
| Border | `#d4d1ca` | `#49473f` |
| Radius / rhythm | 7 px controls, 12 px cards; 4/8/12/16/24/32 spacing | Same structure |
| Typography | 14 px base, 34 px page title; compact table metadata | System fonts; no remote dependency |
| Focus | Visible 3 px primary outline with offset | Never rely on hover/color alone |

Desktop: a 236 px navigation rail, a narrow context/control header, then a centered
content area. Evidence detail uses a dominant screenshot/provenance column and an
editorial/review side column. Archive tables have explicit sort and bounded paging.
At 1,100 px the detail columns stack. At 760 px the navigation becomes an explicit
menu and controls wrap. Small tables may scroll inside a labeled keyboard-focusable
region; the page itself must not overflow horizontally. Critical actions remain
available without hover. Production navigation shows only enabled capabilities;
the blueprint's expandable future-screen catalogue is design-only.

Product navigation groups:

- Workspace: overview, archive, new capture, CSV intake, queue and Source history.
- Investigation: comparison, annotations/tasks, search/cues, saved views and reports,
  only after the owning C/H stage is qualified and enabled.
- Automation: attention, watches and external delivery, each separately enabled.
- Administration: admission/users/devices, audit and status. Host recovery is an
  operator workflow, not a daemon-control button in the web application.

## 3. Domain state must remain visible

| Independent state | UI representation | Forbidden inference |
| --- | --- | --- |
| Job execution | Queued, capturing, retry waiting, cancellation requested, terminal result | Invented capture percentage or exactly-once execution |
| Artifact completeness | Complete/partial/failed for the named profile; required files listed | A screenshot means a complete archive or a successful production WARC |
| Provenance channel | Server, local browser, imported foreign claim; separate time bases | Client clock is trusted server time; receipt proves source truth |
| Editorial revision | Current revision, private note/tags/membership, conflict state | Editing changes original evidence bytes |
| Approval | Approved exact revision, or needs review | Approval publishes; a later edit silently changes existing projection |
| Shared importance | Normal/important, separately revisioned triage | Importance approves or acknowledges another user's event |
| Personal attention | Explicit unacknowledged/acknowledged/reopened event | Opening a page mutates acknowledgement |
| Disclosure | Private; exact public preview; active pinned projection; revoked | An export or an approved capture is automatically public |
| Derived result | Exact input digests, extractor/profile revision and known coverage | “No coverage”, error or unsupported means “unchanged”/“no match” |
| Browser spool | Local pending, consented upload, verifying, accepted receipt, expired/discarded | Local capture or session consent authorizes upload |

Partial and failed attempts stay in Source history. V0 history sorts by server
requested_at and ID; V0 archive sorts by captured_at and ID. Mixed-channel archive
semantics follow document 40: browser server-received ordering and separately
labeled client observations. Future cursors encode the actual sort basis; old and
new cursor identities are not silently mixed.

## 4. Workspace screen catalogue

Screen IDs below are UI references, not new requirement IDs. Paths such as `#new`
are mockup routes only; HTTP routes remain owned by document 16 and feature contracts.
Each screen has a role/state selector in the design header. No selector is an
access-control implementation.

| UI ID / mockup route | First target | Content and primary action | State coverage / owner tasks |
| --- | --- | --- | --- |
| UI-W01 `#admission` | V0 | Admitted GitHub sign-in, local return, policy explanation | Ready, denied, expired, provider failure; EWP-05/06 |
| UI-W02 `#dashboard` | V0 | Counts with completeness, recent sources, review/queue overview | Ready, first use, loading, offline; EWP-09/10/67 |
| UI-W03 `#archive` | V0 | Title/URL, collection/importance filters, date order, completeness/review/private labels | Ready, no matches, loading, denied; working synthetic filter; EWP-10/31 |
| UI-W04 `#new` | V0 | Public HTTP(S) URL, collection, private rationale, independent importance | Ready, invalid URL, full queue, offline; connected synthetic queue flow; EWP-09/31 |
| UI-W05 `#batch` | V0 | CSV validation, duplicate disposition, accepted selection and atomic confirmation | Selected fixture, row preview, stale token, insufficient capacity; EWP-11/31 |
| UI-W06 `#queue` | V0 | Intent, last confirmed phase, attempt, cancellation/retry and reconnect context | Queued/running, empty, failed, reconnecting; EWP-07/55 |
| UI-W07 `#capture` | V0 | Evidence/provenance/artifacts/history tabs, editorial revision, review and triage | Complete, partial, failed, conflict, denied; connected synthetic edits/review; EWP-08/10/31/77 |
| UI-W08 `#source` | V0 | Ordered attempts including identical/partial/failed; later ordered pair comparison | Ready, empty, unavailable attempt; EWP-10/21 |
| UI-W09 `#publication` | V0 | Exact pinned public preview, audience, exclusions and distinct confirmation | Needs approval, approved, active, revoked, denied; EWP-12/77 |
| UI-W10 `#public` | V0 | Inert screenshot, source/provenance/profile/digest only | Visible projection or generic unavailable; EWP-12/77 |
| UI-W11 `#export` | V0; production inventory at 1.0 | Profile, exact pinned inputs, disclosure options, job and verifier | Preview, queued, failed, expired; historic V0/production mismatch; EWP-13/76/77 |
| UI-W12 `#settings` | V0 | Service status, queue/temp limits, backup/restore evidence, membership and audit | Ready, degraded, denied; EWP-05/65/67/72 |
| UI-W13 `#compare` | C1 / 1.1 | Ordered pair, supported inputs, escaped difference and derivation identity | Changed, identical, unsupported, failed; layout/fixture preview; EWP-19–21 |
| UI-W14 `#investigation` | H1 / 1.1 | Exact quote/crop context, assertion revisions, task and saved view | Ready, unavailable anchor, conflict; layout preview; EWP-32/33 |
| UI-W15 `#attention` | C2 / 1.2 | Personal event and explicit acknowledge/reopen | New, empty, failure; connected synthetic acknowledgement; EWP-23 |
| UI-W16 `#profiles` | C2 / 1.2 | Supported literal text rules, raw/filtered preview, new immutable revision | Ready, invalid rule, failed preview; layout preview; EWP-22 |
| UI-W17 `#search` | H2 / 1.2 | Private corpus search, exact source spans, coverage and literal cue draft | Hit, no hit, no coverage; fixture preview; EWP-34/35 |
| UI-W18 `#reports` | H3 / 1.3 | Frozen ordered selection, disclosure profile, dependency and preview | Ready, missing input, failed render; layout preview; EWP-36/37 |
| UI-W19 `#transfer` | H4 / 1.3 | Own-native selection export and quarantined admin import disposition | Preview, anomalies, denied; layout preview; EWP-38/39 |
| UI-W20 `#watches` | C3 / 1.4 | Owner/source/interval/window, baseline, epoch, quota, pause/resume | Active, paused, quota, restore hold; synthetic pause/resume; EWP-24–26 |
| UI-W21 `#delivery` | C4 / 1.5 | Approved destination, owner opt-in, exact minimal payload and finite attempt state | Queued, acceptance uncertain, expired, denied; preview; EWP-27–29 |
| UI-W22 `#pairing` | B0 / 1.1 | Exact origin, manually entered code/phrase, scopes, human approval and owned devices | Pending, approved once, expired, denied; synthetic approval; EWP-43–45 |
| UI-W23 `#access` | U2 / 1.5; U1 subset at 1.3 | Separate role bundles, lifecycle, one-space custody, scoped move, later U3 | Ready, denied, conflict; conceptual role/space preview; EWP-69–71 |

The access screen combines an explanatory U1 panel with a later U2 panel. The U1
product milestone implements user/bundle/lifecycle controls without exposing spaces.
This blueprint is not yet a complete set of U1 forms, group pickers, audit filters,
report editors or operator procedures. Before their implementation, the owning EWP
ticket adds field-level screen cases using this direction and existing contracts.

## 5. Core Workspace interaction contracts

### 5.1 Capture, batch and durable feedback

1. Enter the original public URL; identify server acquisition and anonymous access.
   Validate syntax in the client for feedback, then authoritatively validate the
   network destination on the server. The mockup's small URL check is not SSRF policy.
2. Select collections and optional private rationale up to 2,048 characters; freeze
   submission context. Show importance as a separate choice.
3. Submit once with current CSRF/session and idempotency identity. Distinguish rejected,
   pending response and accepted intent. Disable repeated submission while resolving
   the same request; a lost response reconciles the intent rather than creating another.
4. On admission show server job ID and state; reconcile durable SSE sequences after
   reconnect. Do not equate a notification transport connection with job completion.
5. A queue-full/offline response preserves the draft. A failed attempt retains its
   reason without interpreting timeout/403/404 as proof of source deletion.
6. CSV follows select → validate → duplicate decisions → actor-bound preview →
   atomic confirm. Show rejected rows and admitted selection explicitly; previewing
   creates no jobs. Expired previews require regeneration, not confirmation bypass.

### 5.2 Evidence and editorial work

Evidence defaults to a static screenshot, never archived active markup. Tabs expose
original profile, original/submitted/final URL, channel, time basis, completeness,
artifact inventory and immutable history. Original attachments use protected-byte
serving, not direct guessed filesystem links. The mockup digest is deliberately
abbreviated/illustrative and cannot be used as a real checksum.

Saving editorial changes uses expected_revision. On conflict retain the draft,
show current versus edited values and require deliberate reconciliation. Do not
blindly retry a write against the latest revision. Approval pins a revision; a
subsequent editorial edit clears approval for new publication. Importance retains
its separate revision and cannot invalidate approval or mutate personal attention.
A worker finishing a queued capture cannot overwrite editorial edits or request
context. The blueprint currently demonstrates the conflict message, not a full
side-by-side revision merge editor.

### 5.3 Publication and revocation

Both V0 roles may read/edit/review/export within the shared newsroom. Only admin may
publish/revoke, archive or view administrative audit/users. The product shall omit
an action the role cannot perform and still enforce authorization on every HTTP
path; the mockup's role selector simply previews the denial boundary.

Publication requires purpose-specific eligible evidence, the exact approved revision,
admin authority, an exact preview and an explicit action. The screenshot and selected
metadata are visible; notes, rationale, memberships, raw packages and usernames are
excluded. A second confirmation describes the audience and pinned revision. No
GET publishes/revokes. A changed input or approval conflicts instead of silently
publishing a different projection. Existing public content does not change when
private context is edited. Republishing creates a new slug.

Revoke confirms what can be withdrawn. New slug/asset requests must be denied under
current authority and generation checks, with no-store handling. An unavailable
public view does not reveal private title, reason or record existence. Previously
downloaded copies cannot be recalled. Runtime race/stream/cache proof belongs to
EWP-12/77, not the HTML dialog.

### 5.4 Exports, production and operators

The UI selects a named profile and exact disclosure before generation, then displays
queued/running/complete/failed/expired state. A required output failure cannot
produce a download advertised as complete. V0 has PNG/MHTML/metadata/manifest and
HTML receipt; explicitly requested optional PDF still has required-output semantics.
Production new captures add actual same-attempt WARC/recording metadata; production
exports require safe PDF. Old V0/browser/foreign artifacts are never relabeled or
repaired by a wrapper. The blueprint intentionally blocks the production export of
its historical V0 fixture; it does not simulate a qualified production capture.

Status screens show safe health, actual last-success/failure timestamps, effective
feature state and links to operator guidance. Backup presence is separate from a
successful clean restore drill. No invented RPO/RTO, stable host support, production
status or green backup can be inferred from a synthetic card. Destructive maintenance
requires its already specified operator authority and exact closure preview.

## 6. Browser extension surfaces

| UI ID / surface | Stage | Essential contents and decisions |
| --- | --- | --- |
| UI-B01 / options + unpaired popup | B0 | Exact HTTPS workspace origin, bounded pairing start, no secret URL, support/profile information |
| UI-B02 / pending popup + UI-W22 | B0 | Human code and matching phrase, expiry, exact origin and scopes; manual entry in admitted web session |
| UI-B03 / action popup / URL mode | B0 | Public URL, collection/rationale, server observation warning, explicit intent, own status |
| UI-B04 / action popup / this-tab mode | B1 | Target title/URL, viewport PNG versus page profile choice, fidelity warning, manual local capture |
| UI-B05 / local review | B1 | Actual local preview/inventory, client time claim, spool age/size, selected bytes and separate upload consent |
| UI-B06 / upload + receipt | B1 | Confirmed byte/chunk progress, reconciliation, verifying versus accepted capture, owned receipt |
| UI-B07 / side panel | B2 | One tab/origin, visible recording badge, elapsed time/limits, pause/stop, pending item review |
| UI-B08 / recovery | B1/B2 | Offline/expired token, quota, target mismatch, interrupted worker, stopped or unregistered descriptor |
| UI-B09 / options / disconnect | B0+ | Device revoke, scoped grant status, local storage/expiry, no auto-resume and deliberate discard |

Popup intent is 360 px wide, side panel 384 px in the blueprint; both adapt to the
actual available surface. The options page is responsive. Avoid long prose inside
critical controls: concise description plus expandable fidelity/privacy detail in
the implementation. A popup closure must not be treated as a durable stop or upload
success; the service worker/journal owns transitions. Side-panel status is backed
by the coordinator, not a timer local to the panel.

### 6.1 Pairing and B0

Accept exactly one approved HTTPS origin, default port 443, with no path/query/
credentials. Display it throughout pairing. The human enters the code and matches
the phrase in an admitted Workspace session. The design uses `DEMO 42` and
`quiet river`; these are non-secret fixtures, not real credentials. Pending/approved/
consumed/denied/expired states remain distinct; polling is bounded by the server.
Only one successful token exchange consumes an approval. Lost-token response needs
re-pairing and old-grant revocation, not a hidden replay cache.

The 15-minute bearer lives in session storage; no persistent refresh token. B0 grants
collections:read, capture:create and status:own only. Explicit later approval adds
owned upload/session scopes. B0 sends a URL for a new server visit, never the current
DOM, browser login or cookies. It is useful independently of local acquisition.

### 6.2 B1 manual bytes and failure states

A gesture pins target tab/window/document generation. Choose
workspace-browser-viewport/1 or workspace-browser-page/1 before capture. PNG is the
visible viewport; page profile additionally requires MHTML. Optional availability
at selection time does not allow silent downgrade after a chosen required MHTML
fails. Recheck target/focus/grant around each acquisition; mismatch discards the
uncertain candidate and requires a new deliberate attempt.

Local preview shows actual selected bytes and sensitive-content warning. Explicit
upload consent is separate from capture. Keep 100 MiB/20-item/24-hour spool limits;
full storage refuses/pauses rather than silently evicting pending evidence. User
may deliberately discard local items; this is not server evidence deletion.

Uploads show real confirmed byte progress only: 1 MiB chunks, owned offset/hash
reconciliation and no invented percent for server verification. Token expiry or
connection loss retains local state and requires current authority; accepted bytes
produce exactly one fenced record and an owned receipt. Receipt labels server
received_at separately from untrusted client time. Server hashes verify submitted
bytes, not that they faithfully represent a site. Browser records are private,
baseline-publication-ineligible and not watch baselines.

### 6.3 B2 assisted session and stop semantics

Start/resume requires a gesture, reviewed tab/origin boundaries, activeTab authority
and a current server lease. Bound collection to one foreground tab/origin, 30 minutes,
20 observations, 5 seconds between starts and 2-second debounce. Display 60-second
lease/30-second heartbeat status without exposing a secret. Cross-origin navigation,
focus loss, token failure and restart pause collection; never silently resume.

Register a minimal descriptor only during the active lease; it includes no page
URL/body. Local snapshots remain pending until an explicit batch-upload review.
Stopping ends collection authority but does not erase a historically registered
descriptor: registered items may later receive deliberate upload approval under a
current grant. An offline/unregistered item cannot register retroactively into a
stopped session. The UI offers a new explicit manual B1 review while retaining the
unverified session claim. It never silently converts or server-recaptures the item.

## 7. Later-stage UX closure

- C1/C2: ordered eligible inputs, raw versus filtered output, immutable fingerprints,
  parser budget errors, no-coverage and reprocessing labels. Unsupported visual/AI/
  selector features are absent. Personal acknowledge/reopen is explicit POST intent.
- H1/H2: source text versus editorial assertion is visibly separate. Quote/crop
  anchors pin exact bytes/coordinates/derivation; missing anchors cannot reattach
  themselves. Search shows corpus coverage before claiming no matches. Cues are
  literal/casefold matching; extractor observations do not assert identity or truth.
- H3/H4: report preview freezes disclosure/order/revisions. Missing/retracted inputs
  block or require explicit supported disposition. Imports begin quarantined and
  cannot import local users, roles, publication authority or active automation.
- C3/C4: show owner, baseline, due slot, window/time zone, quota, epoch and restore
  hold. No backlog storm or failed-attempt baseline. Distinguish delivery queued,
  rejected, expired and acceptance uncertain. Minimal payload preview and owner
  opt-in precede external work; replay is a new explicit authorized action.
- U1/U2/U3: separate capability bundles from workspace administration. U1 migrates
  old effective rights explicitly. U2 shows exactly one custody space, scoped
  membership and move/revocation closure; collections do not become ACLs. U3 shows
  configured issuer/subject linking and separate workload principals. No email
  auto-link, implicit fresh MFA or service publication/admin privilege.

## 8. Accessibility and interaction acceptance

Implementation target follows existing REQ-UX requirements and document 16. Verify
with keyboard and supported assistive technology, not visual inspection alone.

1. Logical landmarks/headings, descriptive labels, skip link and visible focus. An
   in-product tab implementation supports roving focus/arrow keys and associated
   panel labels; the blueprint's native buttons are an initial tab illustration.
2. Dialog focus enters the dialog, remains contained, closes with Escape and returns
   to the trigger. Confirmation names entity, revision, audience and consequences.
3. Errors are associated with fields and summarized at the form; durable success/
   failure does not depend on a disappearing toast. Pending writes expose busy state.
4. Contrast, zoom, reduced motion, long source text and narrow windows are tested.
   Never communicate acquisition/review/privacy using color alone. Raw untrusted
   strings are escaped, including title, rationale and receipt fields.
5. Loading is a loading state; offline is a stale confirmed view with timestamp and
   reconciliation action. Conflict retains a draft. Empty, denied, purged and
   unavailable do not leak private counts or imply nonexistent evidence.
6. Real profiles/capabilities determine product controls. No URL query, role switch
   or hidden button can confer access. Validate all server/file/SSE/export paths
   with allowed/denied accounts and current generations.

## 9. Review checklist and actual evidence

Design checks are named `UI-QA` to avoid confusing them with the 76 existing runtime
acceptance scenarios. They introduce no new EWP tasks or normative product IDs.

| Check | Review evidence | Runtime counterpart still required |
| --- | --- | --- |
| UI-QA-01 Core flow | Local capture/CSV → queue, detail tabs, editorial save/review | Real DB/browser/SSE/CSRF/idempotency; ACC/HUN core |
| UI-QA-02 Disclosure | Consent, admin-only action preview, pinned text, revoke explanation | Real permission/revoke/cache/stream races; EWP-12/77 |
| UI-QA-03 Independent state | Editing clears approval; importance does not | Concurrent expected_revision/triage transactions |
| UI-QA-04 Companion consent | Pair pending/approved; local review → explicit upload → receipt | Real MV3 grants/worker death/upload/finalizer; B-ACC |
| UI-QA-05 Session boundary | Explicit resume, pause/stop, unregistered manual review | Actual focus/origin/lease/restart and descriptor proof |
| UI-QA-06 Layout | Desktop/mobile, light/dark, internal table scrolling, no page overflow | Supported browser/assistive-tech/zoom/contrast qualification |
| UI-QA-07 Honest scope | Synthetic labels, future stage gates, profile/time distinctions | Real effective-feature descriptors and compatibility matrix |

The reproducible design smoke script and screenshots are in `design/`. The exact
run and limitations are recorded in its guide. Runtime security, accessibility
certification, OAuth, Docker/PG, WARC/PDF, extension packaging and restore proof
remain absent from this design change. The
[versioned plan](55-versioned-implementation-plan.md) assigns those gates.
