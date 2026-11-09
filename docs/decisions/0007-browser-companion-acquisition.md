# ADR-007: Select a staged browser companion and acquisition channel

Date: 2026-11-09. Status: **selected design; implementation/qualification pending**.
Authority: explicit user request to design the browser extension, update system
planning and commit documentation. Sources: concept sections 5.2/36, ADR-006 and
[platform review](../reference/browser-extension-platform-review.md).

## Decision

Select an independently versioned Chromium Manifest V3/TypeScript companion with
three post-V0 stages: B0 explicit URL handoff to the existing server capture service;
B1 explicit local viewport/optional MHTML capture and verified upload; B2 bounded
same-origin, foreground-tab assisted sessions. The 70-requirement V0 and baseline
production release do not acquire a dependency on an installed extension.

Supersede ADR-006's blanket browser-companion deferral only for these selected
stages. User cookies/password stores, hidden/background-tab capture, arbitrary
cross-origin recording, native file downloads/EXIF, mobile and vendor case adapters
remain deferred. Existing authenticated page pixels/MHTML can be preserved in B1
without exporting cookies or replaying the user's login on the server.

Keep server acquisition and browser submission distinct. B0 creates a new public-
target server observation; B1/B2 create client-submitted evidence under new profiles,
client-claimed times and independent server receipt/verification. Client checksums,
extension IDs and pairing do not attest page truth, genuine software or trusted time.
Do not relabel browser submissions as server Playwright captures or H4 case imports.

Use a dedicated narrow bearer API, human-approved expiring device pairing and
revocable short-lived credentials. The extension never receives Workspace cookies,
GitHub tokens, admin/publication authority or arbitrary private-evidence read access.
Validate uploads offline in quarantine and reuse trusted fenced finalization.

## Ownership and alternatives

Reserve Browser Extension at 0.0.0 with its manifest only and future path
`browser-extension/`; activate at 0.1.0 when real source/build/checks are introduced.
Application owns server pairing/intake/domain services; Evidence Contracts will own
actual DTO/profile schemas; Deployment owns quotas/TLS/isolation. No existing artifact
depends on the planned component. Documentation changes do not bump Application.

Reject sharing the browser's Workspace session cookie, persistent broad API keys,
all-sites permissions and an always-running service worker. Reject treating DOM
serialization as an original HTTP response or claiming PNG/MHTML are simultaneous.
Select narrow resumable upload rather than a native helper or WebSocket byte stream.

## Consequences and verification

Add 24 later-stage requirements, B-ACC-01–12 and EWP-41–52 in documents 34–38.
Current totals: 158 requirements, 70 V0 / 88 later, and 52 assignable tasks.
Pairing/permission races, wrong-tab snapshots, lost grants, untrusted bytes, offline
recovery, revoke/restore, resource bounds and build/distribution need actual evidence.
B0 can ship independently; B1 does not wait for H1–H4, C1 or B2. Optional annotation,
search/report/transfer adapters depend on the corresponding qualified H/C stages.

Signing/store approval, browser compatibility and suitable support budgets remain
qualification work. No code, executable schema, package, public store listing,
deployment, vendor compatibility or runtime success is created by this decision.
