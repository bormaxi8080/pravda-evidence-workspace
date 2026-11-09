# Browser-submitted evidence profiles and verification

Date: 2026-11-09. Status: **selected B1 design; not implemented or verified**.
Owner: evidence/browser/backend. Authority: ADR-007; refines the separate acquisition
boundary in document 32 without changing existing V0 server capture profiles.

## Requirements

### REQ-BAE-001 Distinct complete profiles

Define workspace-browser-viewport/1 (PNG + client acquisition metadata) and
workspace-browser-page/1 (the same plus MHTML). A user selects one before acquisition;
required output failure is failed/partial, never silent downgrade. Complete means
the selected inventory passed checks, not a complete page/network/history. Neither
profile claims full-page PNG, WARC, raw HTTP response or the server runner identity.

### REQ-BAE-002 Same-target consistency and honest fidelity

Pin tab/window, top-frame document/navigation generation and URL before capture;
check focus/active tab, grant and measurements before/after PNG and optional MHTML.
Observe activation/navigation events throughout. On mismatch or unprovable identity,
discard the candidate as interrupted and require a new explicit attempt. No server
repair. Even stable IDs cannot prove the DOM remained unchanged: record separate
acquisition intervals and non-atomic/mutable-page caveats. Do not claim iframe,
virtualized timeline, unloaded content or background-state completeness.

### REQ-BAE-003 Separate client claims and server observations

Record acquisition_channel=browser_companion, claimed browser/extension version,
source URL/title, client start/end times, viewport/scroll/zoom/device-pixel ratio,
selected profile, permission/capture warnings and client artifact hashes. Label
these as collector claims. Independently record authenticated submitter/grant,
server received/verified/accepted UTC times, recomputed hashes and verifier version.
Clock discrepancy is a warning, not correction of the original claimed timestamp.
Do not fabricate response status/headers, cookie state, source authorship or time trust.

### REQ-BAE-004 Hostile bytes and bounded offline validation

Treat a paired client as an untrusted collector. Intake quarantines declared slots,
checks lengths/hashes/PNG dimensions, validates bounded metadata and MHTML structure
offline, and never executes or resolves archived HTML/resources/URLs. Reject fake
MIME, decompression bombs, malicious images, paths, links and undeclared artifacts.
Only a trusted controller writes accepted namespaces and an acceptance manifest.
Validation failure yields a diagnosable private result, never a complete capture.

### REQ-BAE-005 Integration without inherited authority

Accepted submissions create private Capture/Artifact/context records with
origin_client_submitted and unreviewed state. They appear in Source history with
channel/profile/fidelity labels and preserve repeated versions. They cannot become
automatic watch baselines, inherit a public link or claim local server witnessing.
Initial B1 permits private inspection/export only; public publication requires a
later explicit browser-profile disclosure/security qualification. Editor triage and
notes use existing revision rules, independent of original byte identity.

### REQ-BAE-006 Independent export and exact derivative inputs

Provide workspace-browser-export/1 with unchanged original submitted files,
original client inventory and separate server acceptance/verifier manifest/receipt.
Independent verification distinguishes byte match from collector/time assertions.
Later H1 crops may anchor original viewport pixels; text quotes require exact
qualified C1-derived text rather than a live DOM selection. H2/H3/H4 adapters check
actual supported profiles and preserve channel/trust labels; unsupported input
fails explicitly. No upgrade silently rewrites an original browser capture profile.

## Inventory and timing model

Original submitted bytes: `evidence/viewport.png`, optional `evidence/page.mhtml`,
`metadata/browser-acquisition.json`. Preserve exact UTF-8 metadata bytes and their
digest. Client inventory uses fixed relative paths/kinds/sizes/SHA-256; no arbitrary
filename or self-hashing manifest field. The server creates its own canonical
acceptance manifest referencing every submitted file, client inventory and separate
server receipt. It does not edit the submitted JSON to add a trusted actor/time.

Receipt records provenance_scope=client_claimed and verification_scope=received_bytes,
server actor/grant/epoch/profile/verifier, verification outcome and source-normalization
version. Server accepts opaque local tab/window/document identifiers only as bounded
diagnostic claims, not proof of the browser session. No full user agent fingerprint,
OS username, local path, cookies, network credentials or browsing-history database.

For each browser API record started_at/finished_at and monotonic elapsed_ms; record
wall-clock times as timezone-aware client claims. PNG coordinates are output image
pixels; CSS viewport/zoom is contextual measurement and must not be assumed to map
1:1. Unsupported measurement is unknown. Two unchanged URLs alone are insufficient
for tab/document identity. Same-document SPA changes may still occur during capture;
the receipt always states the acquisition is non-atomic.

Use an on-demand isolated-world top-frame probe with a capture nonce, the
scripting InjectionResult.documentId and frameId=0, plus event generation, never injected page-authored selectors/scripts. Do
not read form values, passwords, storage or hidden fields as metadata. Those values
may nevertheless appear in original pixels/MHTML: users must review the scope and
keep it private. Preview cannot promise an automated secret scrub.

Reject browser/internal/file/blob/data/extension URLs and embedded credentials;
block literal loopback/private/link-local addresses and known local hostnames and
the paired Workspace origin. DNS resolution/locality and server response metadata
are not attested by browser intake; do not execute a source lookup/fetch to fill
them in. V0 server-origin SSRF controls remain separate and unchanged. A manipulated
collector can forge URL claims: no claim-validation result becomes source identity trust.

## Selected initial limits and failure behavior

| Limit | Initial selected value / behavior |
| --- | --- |
| PNG | 10 MiB, 10 million pixels; inspect dimensions before decoding; no silent resize/crop |
| MHTML | 32 MiB; missing/unsupported required MHTML fails page profile |
| Metadata / total submission | 256 KiB metadata, 48 MiB total including inventories/overhead |
| Local acquisition | 15s coordination deadline, one in-flight candidate; ignore/discard late output |
| Server validation | One slot, 30s, 512 MiB process memory, bounded 64 MiB decoded MHTML resources in aggregate |
| Private export | Existing 512 MiB spool/package and 120s deadline; own profile/verifier required |

Browser APIs may allocate/generate output before returning its Blob/data URL and may
not support cancellation. Product caps bound retained/converted/uploaded bytes, not
Chrome's internal renderer memory. Check Blob size before conversion/copy, bound
base64 decoding/PNG allocation, invalidate generation at deadline and discard late
results. EWP-41 must measure hostile/large-page behavior; if safe operation cannot
be qualified, disable the page profile rather than promise an unenforceable bound.

PNG-required failure creates no successful viewport capture. MHTML success with
PNG failure cannot be relabeled complete; retain a failed local diagnostic only
under explicit user disposition. Network loss after staging never causes recapture.
No transcoding/thumbnail replaces the original PNG. Derived previews have separate
encoding/hash and cannot be exported as the submitted original.

## Domain and eligibility

Add logical CompanionGrant, PairingIntent, BrowserUpload/ArtifactSlot,
BrowserAcquisition and B2 ResearchSession/Observation records. Upload state is
created -> uploading -> uploaded -> validating -> finalizing -> accepted; terminal
alternatives cancelled/expired/rejected/failed retain minimal safe diagnostics.
Capture becomes visible as accepted evidence only after finalization; no successful
capture exists merely because an upload slot was reserved. Failed submissions can
have their own status without polluting Source history with fictional acquisitions.

Initial EditorialRevision/context is pinned at intent/admission; worker completion
never overwrites later edits. Collection disappearance before acceptance is an
explicit context conflict, not reassignment to an unrelated collection. Original
requested context remains distinct from current membership. Importance defaults normal.

Profile-specific UI shows verified bytes/client-claimed observation, original viewport
scope and missing formats. Existing server export/review/publish code must fail
closed on unknown browser profiles until its adapter is qualified. Browser export
is a new contract, not a new optional member hidden in workspace-export-v0/1.

Accepted immutable evidence survives disconnect/cancellation of a later session.
Purge is an operator policy with dependencies; grants/retries cannot delete already
accepted evidence. Source URL identity follows document 14 while preserving the
exact claimed URL; channel labels prevent treating it as independently confirmed origin.

## Portable package and archive-time adapter

The browser-export profile contains the exact accepted set under capture/
(original evidence/metadata, client-inventory.json, server-receipt.json and
manifest.json), plus receipt.html, export-manifest.json, SHA256SUMS and README.txt.
Capture manifest hashes its referenced files, never itself. Export manifest lists
exact included paths/sizes/digests excluding itself and SHA256SUMS; SHA256SUMS
covers every package file except itself. Use the existing canonical JSON/byte/path
rules and independent verifier; duplicate/undeclared/path-traversal entries fail.
A rendered receipt references claims and server checks without changing original
bytes or asserting trusted capture time.

The mixed archive adapter uses a server-controlled archive_sort_at: retain existing
server captured_at semantics for server evidence, and use server received_at for
browser submissions. Browser client-claimed time is separately labeled and cannot
push a record into the future or reorder the default archive. Version mixed-stage
cursors/date-filter semantics explicitly; UI names the actual time basis. Source
history remains server requested_at/ID descending, with browser intake intent time
versus claimed observation time displayed separately. No legacy V0 record is
rewritten to a client timestamp. EWP-48 qualifies paging/date/source behavior.

## Integrated policy/serialization refinement

ADR-008/documents 40–43 govern purpose-specific profile eligibility, dependent-copy
removal, aggregate capacity and exact contract fixtures. A valid 24 MiB browser
MHTML can pass this 32 MiB intake cap yet exceed C1's 16 MiB analysis cap: keep the
original valid and show analysis unsupported-by-limit, never invalidate the capture
or silently truncate text. Each H/C adapter applies its own supported-input budget.

Use the project JSON integer/string/boolean/null rules for new profile fields:
zoom_milli and device_pixel_ratio_milli are positive integer thousandths with
explicit measurement precision/rounding, not JSON floats or exact pixel-coordinate
truth. Optional raw measured decimal claims, if retained, are bounded decimal
strings under the schema. Crop anchors always use verified original PNG pixels.
Original submitted JSON bytes remain unchanged after acceptance; no server rewrite
of client metadata to normalize a previously accepted record.
