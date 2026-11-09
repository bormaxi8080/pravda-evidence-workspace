# Later format, UX and implementation-reuse boundaries

Date: 2026-11-09. Status: **deferred design investigations, not selected C0–C4 scope**.
Owner: evidence/product/security. These ideas remain useful follow-up from the
pinned changedetection.io review. They have no implemented feature, assigned runtime
ticket or mandatory first-version acceptance claim.

## Visual screenshot comparison

Evaluate pixel/region comparison only after C1–C4 foundations are stable. Record
input screenshots/hashes and browser/viewport/device-scale/locale/context versions.
Different viewport or animation state may invalidate comparison; resizing/cropping
is a named derived transform, never an edit to original PNG. Output needs explicit
threshold/crop/version, bounded isolated decoder/CPU/memory and meaningful fixtures.
Similarity scores cannot assert truth, semantic equivalence or evidence confidence.
Avoid choosing a library solely from an upstream directory name or speed claim.

## Native PDF and JSON sources

Design separate evidence profiles that preserve original PDF/JSON bytes and actual
HTTP provenance. PDF text extraction is offline/bounded and records page/extractor/
font/OCR limits; scans may have no machine text. JSON byte identity differs from
structural equality; specify object ordering, duplicate keys, numbers, arrays and
missing/null semantics before a structural diff. XPath/JSONPath/jq/general query
execution requires its own complexity/sandbox contract; none is implicitly enabled.

Do not manufacture HTML/MHTML/screenshots to label native files complete under the
HTML V0 profile. A preview may be derived, while original MIME bytes remain authority.
MON-ACC-06 will cover native completeness, malformed/encrypted/oversized inputs,
parser isolation and interoperability when these profiles are actually selected.

## Visual selector and interaction steps

A future selector builder may use inert screenshots plus bounded element position
metadata from an isolated runner. Never execute archived DOM in the application
origin to make selection convenient. Record selector provenance, viewport and match
ambiguity; retain textual rule preview/error handling. Browser login/cookie stores,
custom scripts and interactive automation remain outside current scope and need
explicit credential/isolation/user-consent design before reconsideration.

## Profile inheritance and reusable presets

First C2 pins explicit effective options. If later teams need organization/tag/
collection presets, define deterministic precedence, immutable resolved snapshots,
visible diff/impact preview and explicit rollout. Changing a shared preset cannot
silently rewrite past analyses or change all active watches mid-occurrence. Migration
must record which epoch/baseline each watch uses. Avoid implicit inheritance as a
way around version/permission/disclosure checks.

## Transport dependencies and code reuse

First C4 is one restricted HTTPS transport behind a narrow interface. Later evaluate
Apprise for additional channels using exact version, dependency/license inventory,
credential/egress/payload guarantees and controlled-receiver tests. SMTP/internal
relay support needs a separately approved destination-network policy; browser target
SSRF restrictions do not grant notification routes automatically.

Ideas and test scenarios can guide our architecture. Any actual code/test/asset
copy must retain applicable upstream license/attribution/modification notices and
record file/commit/dependency provenance. The current documentation imports no
upstream implementation. No brand asset reuse, runtime sidecar or storage authority
transfer is selected. Existing project license and deployment model remain unchanged.

## Conditions for adopting a deferred investigation

Record actual newsroom need, stage owner, bounded profile/API/data changes, privacy
and migration effects, compatible consumers, resource budget, acceptance fixtures
and failure/recovery plan. Promote it through a new explicit ADR/requirement/ticket
set rather than interpreting this page as blanket implementation authorization.
No deferred item may delay V0 or substitute for required production WARC/PDF/security
and restore qualification.

## Hunchly-inspired acquisition distinction

[Document 32](32-transfer-and-acquisition-boundaries.md) keeps native photos,
attachments, EXIF and browser-session acquisition separate from accepted HTML/PNG
capture and Workspace-native transfer. A file digest verifies bytes; it does not
establish the truth of EXIF, page ownership or a user's asserted origin. Future
acquisition requires a format/provenance/security contract and independent fixtures;
case import cannot silently activate these deferred capabilities.
