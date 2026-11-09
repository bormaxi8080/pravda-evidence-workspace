# Comparison profiles and per-user attention requirements

Date: 2026-11-09. Status: **selected C2 design; implementation pending**.
Owner: product/evidence/UX. Depends on qualified C1, ADR-005 and document 21.
This stage adapts selective comparison and attention ideas; original evidence and
editorial Review/Publication remain independent.

## Versioned focus and noise profiles

### REQ-PRF-001 Immutable explicit profile revisions

Profile edits shall create immutable revisions with owner/actor/time, display name,
parent revision, algorithm/extractor compatibility, full effective options and SHA-256
fingerprint. Existing runs pin their revision forever. First C2 has explicit per-run/
per-watch selection and instance default copied at creation; tags/collections cannot
silently change effective processing. Preview/draft never changes active watches.

### REQ-PRF-002 Restricted deterministic rules

C2 shall support a bounded main-content include selector, bounded exclude selectors,
literal line-ignore rules and explicit whitespace/case options. Defaults preserve
case, punctuation and line order. No arbitrary JS, executable templates, user plugins,
regex, XPath/jq or implicit alphabetical sorting/deduplication in the first release.
Allow only a documented bounded CSS subset implemented offline; validate rules at
save and evaluation. Unsupported syntax fails explicitly, not via a different engine.

### REQ-PRF-003 Preview raw and filtered representations

Preview shall run against explicitly selected stored captures, show pre-profile
escaped extracted text versus filtered text, removed-region/line counts, effective
rules and warnings. This "raw" view is safe text before focus/noise rules, never
executed original HTML. Show that excluded regions can contain editorially relevant
changes. Profile acceptance requires a useful matched content region on the fixtures.

### REQ-PRF-004 Missing/empty/error semantics

An include selector with zero matches, ambiguous unsupported selection, empty
meaningful result, failed parser or exceeded bound shall yield incomparable/failed
with a typed code. Zero matching exclude selectors may be a visible warning, not
success evidence that a region disappeared. Ignoring all text cannot declare a stable
source. Failures preserve previous watch baseline and create diagnostic attention,
not a false unchanged/content-deleted event.

### REQ-PRF-005 Configuration changes invalidate analysis, not evidence

Recompute when any effective profile/extractor/version/limits value changes even
if original bytes match. Keep old runs inspectable. Manual reanalysis under a new
profile is labeled reanalysis and creates no automatic source-change notification.
Applying a new profile to a watch increments its epoch and clears active comparison
baseline until a new complete eligible capture establishes that epoch. Old-epoch
results cannot advance a new baseline or send a new-epoch event.

### REQ-PRF-006 Bound profile lifecycle and disclosure

Use expected_revision/idempotency for profile commands. Referenced revisions cannot
be physically deleted; archive them to prevent new assignments. Store rule text
privately because selectors/literals may reveal investigation context. Exporting a
comparison is a separate explicitly authorized derived report; profile/rule text
and extracted content never enter ordinary public evidence projections automatically.
Routine referenced-profile archive is distinct from operator emergency removal:
authorized purge may remove sensitive profile/rule bodies and mark their revisions
unavailable with minimal safe tombstones. Dependent analyses then cannot rebuild;
the system must not infer or regenerate removed rule text from live sources.

## Per-user attention

### REQ-ATT-001 Attention events separate from evidence review

ChangeEvent shall identify trigger type (`comparison_saved`, `content_changed`,
`analysis_failed`, `watch_paused`, `baseline_established`) and exact source/run or
watch occurrence/epoch. C2 supports explicit "Add to attention" for a selected run
and diagnostic events for requested analysis failures; automatic source-change/watch
events start only with C3. Persist the event transactionally with its explicit
command or accepted diagnostic/watch result. It requests
attention; it does not approve/reject a capture, change editorial revision or create
a Publication. C2 manual reanalysis can be revisited without a new automatic change event.

### REQ-ATT-002 Explicit personal acknowledgement

UserAttention shall be unique(user_id,event_id). Acknowledge/reopen uses an explicit
authorized idempotent POST and records time/actor. GET/list/view does not acknowledge.
One person's acknowledgement does not mark the event read for all editors, advance
a watch baseline, cancel retries or approve evidence. No team-wide bulk acknowledgement
or assignment workflow is implied by C2.

### REQ-ATT-003 Bounded inbox and clear provenance

Provide an internal paged inbox with event kind/time/source-safe label, unseen/
acknowledged filter, link to exact comparison/capture and diagnostic next action.
Separate technical failures from content changes. Counts reflect each current
user's attention state; no heuristic "viewed after newest timestamp" updates on GET.
Unknown/expired derived output shows rebuild/unavailable rather than fabricated diff.

### REQ-ATT-004 Permissions and dependency disposition

Reauthorize inbox/detail/acknowledgement and input links. Disabled users lose access;
events remain auditable. Emergency purge invalidates dependent runs/events/payloads
before further display/delivery and retains minimal non-sensitive tombstones.
Archiving a watch/profile does not erase already preserved evidence or acknowledge
events for others. External delivery policy remains separate from inbox permission.

## Profile UX and examples

Case A: article text changes while menu/date rotates. Both original captures remain;
raw extracted view shows all observed text; focused diff suppresses declared noise
and records exact rules. No hidden edit is made to screenshot/MHTML.

Case B: article selector disappears. Show `selector_missing`, leave monitoring
baseline intact, record failure attention. Do not send "unchanged" or claim the
article was deleted solely from extraction failure.

Case C: editor changes ignore rule and reruns the same pair. Create a new analysis
key/revision; label reanalysis. Applying it to a watch starts a new epoch and first
future complete capture establishes baseline without a content-change alert.

Case D: two editors open the same diff. Neither is auto-acknowledged; one explicitly
acknowledges and the other's personal queue remains unchanged. Evidence review and
publication statuses are unaffected by both actions.
