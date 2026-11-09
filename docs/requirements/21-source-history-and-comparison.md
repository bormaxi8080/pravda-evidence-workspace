# Source history and stored-capture comparison requirements

Date: 2026-11-09. Status: **selected staged design; not implemented**.
Owner: product/evidence/backend. Stages: C0 in V0; C1 after qualified V0.
Authority: ADR-005; origin: [upstream review](../reference/changedetection-io-review.md).
Acceptance/assignment: [document 26](26-adoption-roadmap-and-acceptance.md).

## C0: first-version history

### REQ-HIS-001 Authorized source history in V0

V0 shall provide an authenticated Source history view listing its Captures with
ID, request/capture times, outcome, profile, requester-safe display, review/publication
state and link to detail. Show failed/partial/cancelled requests rather than only
successful captures. Page at the existing 25/100 bounds, descending requested_at
then UUID; unknown legacy capture time is explicitly unknown. Do not infer change
or deletion from a new capture, and never merge byte-identical requests automatically.
Timeline GET is read-only; visibility is the existing shared newsroom policy.

The capture detail links back to Source history and previous/next records under
the same authorization. Capability descriptions reuse REQ-ARC-003; disabled engine
options explain why they are unavailable. V0 exposes no working Compare/Watch/Notify
controls until their stage exists. There is no public Source history endpoint.

## C1: comparison semantics

### REQ-CMP-001 Explicit authorized pair selection

An editor/admin shall choose ordered left/right complete, integrity-valid captures
of the same Source, using supported HTML capture profiles. Default UI selects the
previous eligible complete capture and current capture; never silently swap a pair.
Show reversed temporal order as such. Reject identical capture IDs, mixed sources,
unsupported/legacy-only profiles and missing evidence with specific safe reasons.
No previous eligible capture means no baseline, not "unchanged". Requesting comparison
shall not navigate to the live source or create a new capture.

### REQ-CMP-002 Bounded offline derived representation

Extract a text representation from the preserved MHTML main HTML document in an
isolated offline worker with no network, cookies or privileged DB credentials.
Decode only the required MIME parts under explicit size/part/depth limits; reject
ambiguous/missing main-document selection. Ignore script/style and non-content
metadata by a versioned algorithm, never execute scripts or fetch references.
Describe output as archived-DOM text; do not claim it equals all visually rendered
text, CSS visibility, shadow DOM or a complete replay. Preserve original bytes.

### REQ-CMP-003 Reproducible analysis identity

Comparison identity shall include ordered input artifact IDs/SHA-256 values, profile
revision/fingerprint, extractor/algorithm versions, normalization options, limits
version and output format. Derived representation carries its own digest and warnings.
Same key may reuse a verified result; changed extraction/profile/options creates a
new run. Recheck current authorization/integrity on cache access. Never use URL,
latest-capture pointer or MD5 alone as evidence/analysis identity.

### REQ-CMP-004 Exact outcome vocabulary

Terminal comparison outcomes shall be `changed`, `unchanged`, `incomparable` or
`failed`. Preserve diagnostic reason and input/provenance refs. `unchanged` means
equal derived representation under this exact profile/algorithm; include a separate
raw-byte-equality flag. It does not establish factual truth or semantic equivalence.
Limit/truncation/parser/selector failure or empty meaningful text cannot become
unchanged or a complete diff.

### REQ-CMP-005 Safe understandable diff

Provide escaped line comparison with optional bounded word highlighting and context,
separate added/removed fragments and links to both capture details. Keep original
chronology, options, changed-fragment counts and normalization warnings visible.
Never inject archived markup into the application origin. Bound output/segment
counts and return an explicit limit failure rather than silently dropping changes.
No percentage/similarity value is presented as an evidence-confidence score.

### REQ-CMP-006 Durable jobs, cancellation and independent failure

Use existing durable job/lease/cancel/event machinery with comparison-specific
limits and one analysis slot. Persist run intent before acknowledgement. Cancellation,
parser crash and stale generation cannot overwrite a successful run or alter source
captures. Do not hold web requests or DB locks while parsing/diffing. Failure affects
derived analysis only; capture, review, publication and original export stay intact.

### REQ-CMP-007 Integrity and retention of derived results

Store derived bytes/inventory in a separate protected namespace, never in the original
capture manifest. Reference input dependencies explicitly so purge/restore can remove
or invalidate dependent analysis. Cached output can be rebuilt only when referenced
inputs/versions exist; rebuilt bytes must not falsely reuse a prior run identity
when versions changed. Keep run metadata/status even after cache output expires.

### REQ-CMP-008 History and baseline do not imply change publication

A manual comparison can be saved/revisited internally but shall not automatically
create a watch, send external data, approve review or publish either capture/diff.
Repeated comparison of the same pair/key returns its logical result, not duplicate
attention events. Monitoring later owns explicit baseline advancement and event
creation. Manual editor capture requests remain separate records even if bytes match.

## Concrete user flow and data

Source history -> select two eligible captures -> confirm left/right/profile ->
durable analysis job -> text/provenance/warnings -> return to either original.
Screens include no-baseline, incompatible input, queued/running, cancelled, partial
extraction, limit failure, changed/unchanged and expired-cache rebuild states.

DerivedRepresentation stores input artifact/hash, extractor/version/options digest,
output hash/key/size, completion time and warnings. ComparisonRun stores ordered
capture/representation refs, profile revision, analysis key, job/generation, outcome,
result artifact digest, safe diagnostics and creation/completion times. DB uniqueness
protects a logical idempotent request; input order remains significant.

Main-document selection, text line breaking and whitespace normalization are frozen
as a named extractor release with synthetic MHTML fixtures before C1 ships. Default
preserves case/punctuation/order and normalizes line endings to LF; no alphabetic
sorting or deduplication. Implementation must document its exact DOM-to-text rules.
Materializing this algorithm is an explicit C1 deliverable, not a claimed existing parser.
