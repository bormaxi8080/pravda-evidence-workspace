# Production preservation, WARC scope and replay qualification

Date: 2026-11-09. Status: **selected production contract; recorder not qualified**.
Owner: capture/evidence/security. Authority: ADR-010. Refines REQ-EVD-001/002/003/
004/007/008, REQ-ARC-003, REQ-SCP-003 and ACC-12; no new requirement IDs.
Sources: existing concept production obligations and the primary review.

## Profile and byte boundary

workspace-capture-production/1 requires `evidence/screenshot.png`,
`evidence/page.mhtml`, `evidence/network.warc.gz`, `metadata/capture.json`,
`metadata/recording.json` and `manifest.json`. WARC is captured during that same
attempt/browser session as the PNG/MHTML. Sequential artifact generation is
non-atomic and has individual intervals. A separate later navigation, MHTML wrapper
or independently fetched response cannot substitute for a missing recording.

The capture manifest inventories exact PNG/MHTML/WARC/metadata bytes, excluding
itself, under document 15's byte/path/checksum rules. Record original profile,
engine/browser/recorder/contract/policy identities and actual intervals. No PDF
receipt is added to the capture manifest; it is an export-time derivative.

First WARC contract uses a self-contained WARC 1.1 stream with per-record gzip
members and declared record inventory. No external revisits, dedup references,
segmented logical records, remote WARC dependency or arbitrary archive nesting.
If the provider produces another container, extract through a qualified bounded
adapter and preserve declared source/transform identity; an opaque WACZ cannot be
renamed network.warc.gz. Source/licensing and actual parser interoperability remain
implementation gates, not inferred from a filename or successful gzip decode.

## Acquisition scope and completeness

One explicit public HTTP(S) navigation, selected V0 conditions/viewport/environment
and existing egress policy remain the source scope. No recursive crawl, login,
cookie import, scrolling behavior or platform automation is enabled to get WARC.
Recording begins before navigation and ends at a recorded boundary within the
120s attempt deadline. Browser-generated later activity is not silently claimed
to have been preserved. Requests outside supported method/protocol/scope are
explicitly denied or classified by the pinned policy, never executed to repair replay.

| Exchange class | Selected completeness rule |
| --- | --- |
| Main document and redirect chain | Required matching request/response records, observed URL/status and complete retained response body; missing/truncated/ambiguous required records make the profile non-complete |
| Supported HTTP(S) resources observed before boundary | Record response/association or explicit failed/blocked disposition. A lost/unknown body within declared required scope is non-complete, not silently omitted |
| Known policy-blocked/unsupported protocol, streaming, WebSocket or boundary-in-flight activity | Explicit category/count/reason and warning; cannot be called complete traffic or proof of page absence. Required navigation failure still blocks completion |
| Browser-generated/opaque/cache/service-worker content without verifiable recording | Mark source/observation layer unknown/unsupported as applicable; do not fabricate wire bytes or treat a replay hit as acquisition proof |

Policy eligibility is fixed before capture and cannot relabel a failed exchange as
excluded afterward. A complete preserved HTTP error page remains error-page evidence,
not a normal article or C3 baseline. All completed-with-policy-exclusions views
show their scope; unknown coverage never becomes "all resources captured".

## Record/content provenance

Record IDs, types, target references, times, lengths and associations must parse
under the selected WARC contract. Check record block/payload digest semantics as
appropriate and retain whole-file SHA-256 separately; these are different byte
domains. The adapter records the exact supported digest encoding/algorithm and
rejects unknown algorithms rather than rewriting an asserted digest silently.

metadata/recording.json includes recorder/version, observation_layer (for example
browser-observed or proxy-observed), reconstruction/normalization policy, navigation
record IDs, exchange counts/dispositions, truncation/error diagnostics, time boundary
and supported replay scope. Raw HTTP/2 framing, TLS packets and host clock trust are
not implied by a reconstructed archival HTTP representation.

Apply the selected sensitive-header omission policy before retained output becomes
immutable; record omitted field categories without secret values. Changed transfer/
content encodings and computed lengths are explicit transformations, not original
raw headers. The exact retained transformed bytes are what the WARC/profile hashes
verify. No post-finalization "sanitizing" mutation; unsuitable disclosure stays private.

## Engine contract and provider qualification

capture-engine/2 adds requested_capture_profile, recording_policy_revision,
recorder capability/version, required output inventory and recording dispositions
to the fixed generation/deadline/network/resource contract. Unknown required fields/
profile/capabilities fail before navigation. Controller and runner materialize strict
schemas together; v1 cannot silently accept v2 fields. One attempt is owned by one
qualified provider; fallback produces no fabricated same-attempt completion.

EWP-73 first investigates a recorder-backed existing Playwright adapter. A separately
pinned Browsertrix candidate must independently meet PNG/MHTML/recording, condition,
timing, sandbox/egress and output limits; its docs are not proof. If neither qualifies,
record the blocker and keep production feature disabled. No parallel deployment,
new browser behaviors or provider profile is installed by this specification.

## Bounded validation and failure

Initial WARC ceilings: 100 MiB stored file, 256 MiB total decompressed record data,
64 MiB per record block, 10,000 records and 64 KiB per WARC/HTTP header section;
strict lengths, finite nesting and no external reference resolution. These coexist
with the existing 100 MiB artifact/250 MiB whole-attempt caps, disk reserve and one
heavy permit. Aggregate PNG/MHTML/WARC may exceed the total even if individually
valid: fail explicitly, never remove one required artifact or silently raise a cap.

Parse/validate in a no-network isolated 512 MiB/30s worker with streaming bounded
decode, record/association/digest checks and exact EOF/member inventory. A pipeline
that cannot safely enforce these bounds does not qualify. The existing
120s whole-attempt deadline includes recording flush, validation and finalization:
initial phase ceilings are 80s acquisition (including the 60s navigation cap),
30s validation and 10s trusted promotion/commit. Do not add hidden post-deadline
verification time. Each phase is visible/fenced; no complete result precedes them.

Validation/promotion still requires current generation/actor/fences and complete
inventory. A valid WARC with missing PNG/MHTML or corrupt metadata is non-complete.
No schema migration adds WARC to historic captures. Existing V0/browser/foreign
profiles retain their own inspection/export and purpose eligibility.

## Independent replay test boundary

Replay is qualification/inspection tooling, not an active-content viewer in the
Workspace origin. Use one explicit verified capture package in an isolated browser/
replay service without app cookies, DB/final-store write access or external network.
Disable live/remote archive fallback; missing resources fail visibly, never fetch
today's page. Do not index another space/capture into a shared guessed replay URL.

Qualify at least one independently pinned reader (pywb is a candidate) with controlled
redirect/CSS/font/binary/query/Unicode fixtures and expected payload/coverage assertions.
Record replay tool/browser/environment, misses and differences. Pixel similarity
alone is not fidelity/truth and animation/time differences do not rewrite originals.
General website replay remains bounded/limited; supported fixture success is not
universal social-platform, cache or full-history preservation.

EWP-73/74/75 and PRD-ACC-01–04 in document 53 turn these contracts into actual proof.
