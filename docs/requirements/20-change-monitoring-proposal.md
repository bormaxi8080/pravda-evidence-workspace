# Optional comparison and source-monitoring proposal

Date: 2026-11-09. Status: **candidate post-V0 extension; no feature adoption or
implementation claim**. Owner: product/evidence lead. Origin: user-requested
[changedetection.io review](../reference/changedetection-io-review.md).
The 67 mandatory baseline requirements and V0 exit scope are unchanged.

## Product case

A newsroom wants to see what changed between two preserved versions of a source,
avoid reviewing navigation/timestamp noise, and later learn that a watched source
may need another capture. Comparison helps editorial attention; it does not
determine truth, prove who changed a page or approve publication automatically.

## Proposed increments

| Increment | Included outcome | Prerequisites / explicit exclusions |
| --- | --- | --- |
| C1 Manual comparison | Source timeline, select two stored captures, escaped line/word diff, input/provenance links | Qualified immutable capture/storage/permissions; no live fetch, schedule or external notification |
| C2 Focus and noise profiles | Versioned include/exclude regions and literal-ignore rules, preview, raw/filtered comparison, per-user attention acknowledgement | C1; bounded offline parser, missing-selector semantics; no arbitrary JS/jq/plugin execution |
| C3 Durable watches | Opt-in source schedule/pause, bounded capture slots/quotas, internal change events and attention queue | C1/2 + stable recovery/security/operations; no catch-up storm or silent recapture |
| C4 Delivery and formats | Opt-in destinations with outbox; later visual diff and native PDF/JSON profiles | C3 + disclosure/egress/secret policy, separate format contracts and operational evidence |

Recommend C1 first after V0 qualification. C2/C3 require a separate scope decision;
C4 is later. These are product suggestions, not dependencies of EWP-01–16.

## Candidate objects and states

- ComparisonProfileRevision: immutable include/exclude/ignore/order/normalization
  options, extractor/algorithm versions, caps and effective fingerprint. No hidden
  tag/global inheritance in the first increment; future inheritance pins resolved values.
- DerivedRepresentation: input artifact SHA-256, extractor/profile/version, bounded
  text/structure output, output digest and warnings. Original evidence is unchanged.
- ComparisonRun: exact left/right capture/artifact hashes, profile/algorithm versions,
  result changed/unchanged/incomparable/failed, changed fragments and diagnostics.
- SourceWatch: source ID, enabled/paused, owner, frequency, timezone/window, next due,
  quota, profile revision, last observation/result and failure/backoff state.
- ChangeEvent: comparison/watch identity and input refs, internal attention state.
  UserAttention stores per-user acknowledgement separately from editorial review.
- NotificationIntent/DeliveryAttempt: destination secret reference, permitted payload
  class, dedupe key, retry/expiry and delivered/failed/revoked outcome.

An OriginObservation is availability only. It is not a ComparisonRun or an accepted
Capture. HTTP 304/header checks do not create a fictional new complete browser
capture. An explicit editor capture request is preserved even if byte-identical to
an earlier one; comparison caching can save analysis work without deleting history.

## Candidate acceptance rules

### CAND-01 Reproducible comparison, immutable originals

Compare only authorized stored artifacts offline. Record both input hashes plus
extractor, algorithm and profile revisions. Cache identity includes all those
values, not just URLs or current profile name. Changed profile reprocesses unchanged
inputs. Equal normalized text does not assert binary identity or semantic equivalence.
Display which transformations were applied and link to originals/provenance.

### CAND-02 Bounded extraction and noise filtering

Start with escaped text/line comparison and literal ignore rules; add CSS focus only
with bounded safe extraction. Do not execute archived scripts or fetch resources.
Missing selector, parser failure, truncation and zero meaningful text yield explicit
incomparable/error, not unchanged. Rules suppress attention, not preservation. Give
raw versus filtered views; highlight that omitted regions may contain relevant changes.
Regex/advanced query languages require separate complexity/time/sandbox qualification.

### CAND-03 Attention is per-user and separate from approval

Show new comparison events in an internal queue. Viewing a diff is not review approval,
publication or a global team acknowledgement. Use an explicit idempotent POST to
acknowledge a particular event for a particular user. No action changes source bytes
or invalidates another user's attention state. No mutation occurs on ordinary GET.

### CAND-04 Safe scheduling and recovery

Default watches disabled; explicit authorized opt-in selects scope, interval/window,
quota and retention policy. Persist due times in UTC and named timezone for windows;
define DST missing/repeated-hour behavior and bounded jitter. A bad watch pauses
itself and cannot stop global scheduling. Coalesce missed checks to at most one
pending occurrence per watch, revalidate owner/policy and network controls, and
respect installation capture capacity. Paused watches preserve existing evidence.

### CAND-05 Notification is an explicit disclosure decision

Start with internal alerts. External delivery is opt-in, admin-approved, destination-
allowlisted and secret-referenced, with a durable transactional outbox. Default
payload contains minimal event/status plus an approved authenticated-app link;
no notes, raw URL queries, diffs, screenshots or evidence attachments without
separate explicit payload permission. Delivery failure never rolls back evidence.
Reauthorize before send/retry, bound retry/expiry/deduplication and protect egress.
Evaluate Apprise behind an adapter later; do not expose arbitrary provider URLs
or templates as unrestricted outbound execution.

### CAND-06 Visual/native-format extensions preserve meaning

Visual diff requires compatible viewport/locale/browser context and explicit crop/
threshold/version data; differences are not a truth score. Native PDF/JSON inputs
need their own original-byte/artifact profiles and bounded parsers. Do not create
placeholder MHTML/PNG to force them into the HTML V0 success profile. Visual selector
UX uses inert screenshot/element metadata rather than executing an archive in-app.

## Candidate verification before adoption

| Scenario | Required evidence |
| --- | --- |
| MON-ACC-01 | Changed article versus rotating clock/menu; originals unchanged; filter/profile version change recomputes same bytes |
| MON-ACC-02 | Selector disappears, parser/limit failure, reordered text, empty result and mismatched contexts are explicit, not stable by default |
| MON-ACC-03 | Two users acknowledge independently; review/publication unchanged; unauthorized diff/input access denied; rendered diff/patch XSS payload inert |
| MON-ACC-04 | Timezone/DST/bad configuration, restart/missed schedule, quota/paused owner and duplicate due claims do not stop other watches or flood capture |
| MON-ACC-05 | Destination revoked/disabled between intent and send, provider outage, repeated retries and content-bearing payload denial preserve privacy/evidence |
| MON-ACC-06 | Native PDF/JSON/visual-profile inputs verify as their actual format and declare extraction/fidelity limits |

Existing ACC-01–12 remain baseline requirements; these MON scenarios are not
reported as executed or added as V0 release gates. Adopted extension work will
introduce its own requirement IDs, component contract changes and migration/evidence
gates through a separately bounded implementation stage.
