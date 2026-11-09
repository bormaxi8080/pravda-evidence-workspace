# Evidence-linked notes, quotes, crops and research trails

Date: 2026-11-09. Status: **selected H1 design; not implemented**.
Owner: evidence/UX/backend. Depends on qualified C1 extraction/provenance and core
artifact integrity. Hunchly notes/review are product inspiration; our annotations
refer to stored evidence, not an investigator's live browser viewport.

## Requirements

### REQ-ANN-001 Versioned linked annotations

Annotations shall have UUID, capture/artifact references, author/time, revision,
type=`comment|text_quote|image_region`, body and active/retracted state. Create/edit/
retract are explicit authorized commands with conflict detection/audit. Preserve
prior revisions; do not overwrite original evidence or claim a comment is captured
source text. Existing V0 capture-level notes migrate as comments with legacy context,
not invented historical anchors. Private annotations are never public by default.

### REQ-ANN-002 Verifiable text anchors

A text quote shall pin exact input artifact SHA-256, supported DerivedRepresentation
ID/hash, extractor/version and UTF-8 byte span with quote bytes/digest. Validate
boundaries and exact match; repeated strings require the selected occurrence, never
"first current match". A changed extractor/source cannot silently relocate the quote.
If no verified match exists, save only an explicitly user-asserted comment, not a
verified source quote. Cues/findings and editorial assertions remain separate objects.

### REQ-ANN-003 Screenshot regions are derived output

An image region shall reference the verified original PNG hash/dimensions and
integer x/y/width/height in original image pixels. Convert displayed scale to those
coordinates and validate bounds. Crop generation uses a bounded controlled offline
decoder and records derivative encoding/version/hash; original PNG stays unchanged.
Show full-context link and crop label. Crop time is annotation time, not a new
browser capture time; viewport/URL provenance remains that of the original capture.

### REQ-ANN-004 Explicit observation versus assertion trail

Record whether a link/reason is user-asserted, recorded by the capture pipeline or
imported/unknown. Optional related capture/collection links need a bounded relation
type/reason and actor/time. Do not infer that one pasted URL was reached from another,
that a shared extracted value proves ownership, or that server recapture equals
what an authenticated browser user saw. No unrestricted browsing graph is introduced.

### REQ-ANN-005 Stable report references and correction behavior

Reports pin exact annotation revision and original/derivative hashes. Editing a
note creates a new revision; it does not rewrite a completed report or change source
digests. Retracted/purged/unsupported anchors cannot silently float to latest text
or be omitted from a newly generated report while claiming completeness. Require
new explicit report selection/revision or fail with actionable missing-dependency
reason. Previously downloaded reports cannot be recalled by editing a note.

### REQ-ANN-006 Privacy, bounds and emergency removal

Authorize every note/body/quote/crop read and dependent export. Apply bounded body,
anchor and image-resource caps; escape source/editor text and never run archived
DOM to create anchors. Ordinary retract preserves revision history; operator purge
may remove sensitive bodies/crops and invalidate dependent reports/indexes/hits.
Keep minimal safe tombstones and replay deletion ledger on restore before serving.
No original byte replacement, automatic publication or external-send permission follows.

## Selected first contract

AnnotationRevision includes immutable anchor descriptor, body<=8,192 chars and
source/assertion type; maximum 200 active annotations/capture and 16 KiB quote UTF-8.
First H1 supports only one contiguous quote or one rectangular image region per
annotation. No freehand editing/redaction of original evidence, video/time anchors,
OCR assumptions, native PDF annotations or HTML iframe viewer.

Rectangles require x,y>=0, width,height>0 and contained image bounds. Crop target
is PNG, <=5 MiB output, <=10 million pixels, one decoding slot, 30s/512 MiB worker
budget. Do not silently resize to pass; explicit derived resize would need another
transform contract. General original PNG may still use larger V0 capture limits.

POST `/api/v1/captures/{id}/annotations` supplies type/body/anchor and idempotency;
PATCH `/api/v1/annotations/{id}` and POST `/retract` require expected_revision.
GET `/annotations/{id}` and `/crop` reauthorize capture/dependency integrity and
use no-store. Quote preview returns escaped extracted text plus exact span/hash.
An unsupported/purged derivation is unavailable, not a request to fetch the live URL.

Annotation changes have their own revisions. They never change the capture's
approved editorial revision/public projection automatically; a report has its own
selection review and no annotation is eligible for public inclusion merely because
its source capture was published. Minimal safe audit stores IDs/revisions/actions,
not whole note/quote bodies in general telemetry.

Anchor dependencies pin the exact derivation/transform version and required bytes
under the bounded dependency/cache policy in document 25. Annotations are not
ordinary disposable LRU cache entries; deny new pinned output when capacity is
exhausted rather than silently evict a referenced anchor. General source purge
still overrides pins. Migrating capture notes preserves their legacy revision/
approval history and records the mapping; it cannot invent past annotation authors
or let subsequent capture-editorial edits bypass the existing review contract.
