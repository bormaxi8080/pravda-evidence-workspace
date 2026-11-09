# Adopted comparison and monitoring roadmap

Date: 2026-11-09. Revision: 0.4. Status: **adopted into staged design; implementation pending**.
Owner: product/evidence/engineering. The user explicitly requested adoption of
changedetection.io ideas into the first-version/future implementation documentation.
[ADR-005](../decisions/0005-adopt-comparison-and-monitoring.md) records that decision.
The existing filename is retained for links; the former candidate proposal is
superseded by the normative stage requirements linked below.

## What adoption means

Adopt the useful product/engineering ideas in Workspace's own domain and trust
model. Preserve original evidence, private access, review and explicit publication.
No upstream code, assets, runtime service or transport dependency is imported.
The [pinned source review](../reference/changedetection-io-review.md) remains evidence
for upstream observations; these stage choices are our design decisions.

## Selected stages

| Stage | Selected behavior | Authoritative documents |
| --- | --- | --- |
| C0 / V0 | Paged authorized Source history; existing engine capabilities shown honestly | [21 History/comparison](21-source-history-and-comparison.md), original V0 capture contracts |
| C1 after V0 | Manual ordered stored-capture comparison, offline derivation, safe diff and exact identity | [21 History/comparison](21-source-history-and-comparison.md) |
| C2 | Immutable focus/noise profile revisions, previews and explicit personal attention | [22 Profiles/attention](22-profiles-and-editorial-attention.md) |
| C3 | Opt-in durable watches, UTC/window scheduling, quotas/epochs/baselines and internal events | [23 Watches/scheduling](23-watches-and-scheduling.md) |
| C4 | Explicit disclosure permissions, minimal payload, durable outbox and restricted delivery | [24 Notifications](24-notifications-and-delivery.md) |
| Deferred evaluation | Visual diff, native PDF/JSON, visual selector, inheritance and more transports | [27 Later boundaries](27-advanced-format-and-reuse-boundaries.md) |

Shared API/resource/storage/migration/restore contracts are in
[document 25](25-extension-contracts-and-operations.md). Complete requirement/scenario
coverage and EWP-19–30 are in [document 26](26-adoption-roadmap-and-acceptance.md).
These stages are selected roadmap work, not optional placeholders; they are not
implemented features or automatic additions to the V0 release gate.

## First-version boundary

V0 now explicitly includes REQ-HIS-001: Source history using existing records,
including failed/partial requests and identical manual captures. The original 67
requirements remain stable, so V0 has 68 applicable requirements. Comparison,
profiles, watches and delivery add 39 selected later-stage requirements. Total
selected requirements are 107; no later-stage gate is silently imposed on V0.

C1 starts after qualified V0. Production WARC/PDF/security/recovery remain mandatory
and independent; comparison delivery cannot excuse their omission. No calendar,
public release number or production qualification is claimed by stage labels.

## Former candidate mapping

| Former label | Current normative home |
| --- | --- |
| CAND-01 Reproducible comparison | REQ-CMP-001–008 and REQ-EXT-001/002/005 |
| CAND-02 Bounded extraction/noise | REQ-CMP-002/004/005 and REQ-PRF-001–006 |
| CAND-03 Personal attention | REQ-ATT-001–004 |
| CAND-04 Scheduling/recovery | REQ-MON-001–008 and REQ-EXT-003/004/005 |
| CAND-05 Delivery permission | REQ-NTF-001–007 |
| CAND-06 Visual/native formats | Deferred document 27; not a mandatory C0–C4 requirement |

MON-ACC-01–06 labels are retained and expanded in document 26; MON-ACC-07–12 add
history, cache/cancel, epoch/baseline, restore and deployed-capacity coverage.
Definitions appear once in that acceptance document, not in competing copies here.
