# ADR-005: Adopt staged comparison and monitoring design

Date: 2026-11-09. Status: **selected documentation/roadmap decision; implementation pending**.
Authority: the user explicitly requested adoption of changedetection.io ideas into
project documentation, considering the first version and later implementation.
Source evidence remains the [pinned upstream review](../reference/changedetection-io-review.md).
This decision adopts product/engineering ideas, not upstream code, services or assets.

## Decision and release boundary

Adopt C0 source history and engine-capability clarity into V0. Source history is
an authorized paged view of existing Source/Capture records, including partial/
failed outcomes; it adds no automatic capture, new engine or change-detection claim.
The original 67 requirements stay stable; REQ-HIS-001 makes this V0 behavior explicit.

Select the following staged roadmap beyond qualified V0:

- C1: manual offline comparison of two stored complete HTML captures.
- C2: immutable focus/noise profiles and per-user acknowledgement of internal events.
- C3: disabled-by-default opt-in watches with durable scheduling and internal alerts.
- C4: opt-in external delivery through a restricted durable outbox/transport adapter.

These are selected requirements for their respective stages, not optional prose
suggestions or additional V0 release gates. Each stage still needs implementation,
assignment and qualification. Stage labels are not SemVer/product releases.
Visual diff, native PDF/JSON preservation, interactive visual selection, profile
inheritance and additional transports remain separately deferred designs.

## Architectural consequences

Keep capture, derivation, comparison, watch occurrence, change event, acknowledgement,
notification and publication separate. Only capture owns original bytes. Derived
results pin exact input hashes, extractor/algorithm/profile revisions and limits.
Filter failure is an explicit error/incomparable outcome. Profile edits establish
a new monitoring epoch; they do not masquerade as a source edit or retroactively
rewrite earlier comparison/event history.

Use existing modular Python/PostgreSQL/jobs/storage/authorization boundaries. Add
bounded worker job types and additive schema contracts when their stage starts;
do not make changedetection.io a runtime sidecar or a second system of record.
Retain all manually requested captures even when bytes match. Reuse analysis only
when the complete derivation key matches and access/integrity checks still pass.

External delivery is an explicit disclosure permission, never an automatic extension
of editorial access. Notifications do not publish evidence or change review state.
Production WARC/PDF/security/recovery obligations remain independently mandatory;
the comparison roadmap cannot be used to postpone them.

## Alternatives and verification

A wholesale application transplant introduces incompatible watch/history/storage
authority and unnecessary operational coupling. Putting schedules/notifications in
V0 would enlarge its qualification surface. Purely retaining a candidate list no
longer meets the user's instruction to adopt and detail the ideas. Staged adoption
keeps a bounded first version and a concrete extension path.

Documents 21–26 define requirements, APIs, limits, acceptance coverage and tickets.
No runtime acceptance result or upstream dependency/license clearance is fabricated.
