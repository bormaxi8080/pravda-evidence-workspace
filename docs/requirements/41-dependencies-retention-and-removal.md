# Dependency authority, retention and emergency removal

Date: 2026-11-09. Status: **selected refinement; procedures not implemented/run**.
Owner: evidence/backend/operator. Authority: ADR-008. Refines REQ-DAT-004/006/008,
REQ-ARC-005/006, REQ-EXT-002/005, REQ-ANN-005/006, REQ-FND-005, REQ-RPT-006,
REQ-NTF-004/007, REQ-XCH-005 and REQ-BLC-006. No new retention product or legal hold.

## Authoritative objects and dependency edges

Record immutable object/revision identity, profile/algorithm and exact input hashes.
Use typed dependency edges in PostgreSQL, separate from user-asserted research links:

| Edge | Meaning | Removal consequence |
| --- | --- | --- |
| requires_input | An operation needs specific original/derived bytes and version | Missing/removed input blocks computation/rebuild; no live fetch substitution |
| embeds_content | Output contains or may reproduce input content | Source removal fences this output and includes its bytes in removal scope |
| cites_identity | Safe identifier/hash reference without copied content | Preserve only safe tombstone/history if authorized; never a working content link |
| governed_by_revision | Approval/disclosure/permission/session policy gates a command | Recheck current applicable authority; historical revision does not grant access |
| cache_of | Disposable reproducible representation | Ordinary eviction allowed only when not pinned; preserve computation identity |

Edges are written in the same business transaction as their consumer references.
No report/export/crop/search snippet/queued payload becomes ready without its input
dependency record. Unknown embedding behavior is conservative: treat as potential
content copy until qualified. Related-capture links are not executable dependency
edges; they may form research cycles without triggering recursive execution.

Maintain indexed reverse edges and affected-root/fence lookup for serving. Every
content read checks exact selected input identity, current recorded integrity/access
and the current removal fence;
stale cache/worker results cannot bypass it. Closure discovery and cleanup use
bounded pages (500 edges/page), durable cursor/visited state and idempotent jobs,
not a single unbounded recursive transaction. Newly attempted outputs referencing
a fenced root are denied before promotion. A closure page limit is a progress
boundary, never a claim that the remaining dependents do not exist.

Search reauthorizes each paged hit/snippet and labels incomplete corpus coverage
after input removal. A run's aggregate counts are not evidence that every original
is still available. Derivation upgrades produce new computation identities; pinned
old anchors do not float to the new algorithm or re-extracted matching text.

## Retention and pin inventory

| Object class | Selected existing policy / refinement |
| --- | --- |
| Accepted original artifacts/manifests, provenance, editorial/triage/annotation revisions | No automatic original purge; normal archive is non-destructive; operator emergency removal is separate |
| Computation/run/cue/profile/reference identities | Retain safe history/dependencies; removing content may leave only minimal safe tombstone |
| Unpinned C1/H-derived cache | 30-day default, shared 1 GiB bound; LRU only for unpinned disposable bytes |
| Pinned quote representation/crop/report dependency | Ordinary eviction prohibited; account referenced physical bytes once, deny exhausted capacity; no implicit original retention deletion |
| Ready private export/report spool | Existing 24h output expiry; snapshot/status may persist, supported authorized rebuild creates a new output identity when necessary |
| Browser local pending data | 24h/100 MiB/20 items; actual cleanup-on-return limitations in document 37 |
| Server pending intake/quarantine | 24h upload expiry and existing reservation cap; unaccepted bytes excluded from ordinary accepted-evidence backup |
| Job events / idempotency | Existing seven-day detailed events / 24h idempotency; terminal summaries and uniqueness references remain authoritative |
| Audit/removal/revocation history | Minimal safe accountable records under operator policy; never keep sensitive removed bodies in ordinary telemetry |

A pin has owner object/revision, referenced bytes/computation, reason and active/
released state. Referenced live annotations keep required anchor bytes pinned; a
report snapshot pins its selected dependency identities. Expiring temporary report
output releases only its output reservation, not an active annotation's anchor.
Pins derived from actual references are reconciled after crash; no anonymous orphan
pin may consume quota indefinitely without visible diagnosis/disposition. They are
storage references, not a legal preservation promise or a right to override purge.

## Events with deliberately different effects

| Event | Serving/computation behavior | Forbidden conflation |
| --- | --- | --- |
| Editorial or annotation edit | New revision; old report snapshot stays pinned; future capture publication follows editorial rules | Replacing original bytes or rewriting old report selection |
| Annotation retract | Historical revision labeled retracted; blocks new report generation using it; existing exact output remains historical with warning unless removed | Treating ordinary retract as assured erasure of previous downloads |
| Cache eviction | Exact result may be unavailable/rebuilt from same supported retained inputs | Invalidating original capture/review or silently changing algorithm/hash |
| Original corruption/missing bytes | Fence dependent verified-content operations; preserve finding/original expected hash | Relabeling as successful eviction or overwriting from live URL |
| Public revoke | Deny old public slug/assets; retain authorized private evidence | Deleting private original or granting access through an old export link |
| Actor/grant disable/revoke | Deny that principal's operations; accepted shared evidence remains private under current access | Treating a user-specific denial as physical evidence deletion |
| Operator content removal | Root fence, dependent-copy cleanup, minimal tombstone and restore-ledger replay | Allowing cache/hold/pin to resurrect or continue serving sensitive content |

Retraction alone is not a purge fence. Purge/missing/corrupt required dependencies
block affected ready downloads and new renders; safe status may explain why. A
different independent artifact can remain available only if its dependency path
and permissions are actually unaffected. Downloaded/recipient/offline copies cannot
be recalled by a local state transition.

## Emergency removal transaction and crash protocol

This implements the already required operator procedure, not a general editor UI.
Require reviewed exact IDs/revisions and a dry-run dependency/inclusion report,
reason, operator identity, current backup/replica/disclosure limitations and intended
scope. No automatic expansion from a user-supplied filesystem path or URL search.

1. Establish a durable maintenance/serving hold. Append and flush a minimal removal
   intent to the protected ledger kept outside ordinary restored application data.
2. Commit DB root fences/removal epoch, disable affected publication assets and
   cancel/fence dependent jobs/exports/intents. Only then acknowledge containment.
   Ledger and DB are not claimed to be one distributed atomic transaction: if either
   step is ambiguous/unavailable, keep the serving hold and reconcile before reopening.
3. Walk reverse dependency pages, mark affected copies unavailable and remove only
   approved namespaces/records under exact inventory checks. Late finalizers recheck
   fences and cannot promote content after removal won.
4. Reconcile physical bytes, pins, reservations and tombstones, report failed/unreachable
   copies and safe closure counts. A partial cleanup is explicitly partial; root
   fences remain effective even while later pages or backup handling are pending.
5. Reapply ledger on every restore before protected serving, rebuilding or outbound
   work; reject restoration if the authoritative ledger cannot be obtained/verified.

Every step is retry-safe. Tombstones include opaque IDs, removal generation,
action/time/operator reference and safe reason code, not removed note bodies/URLs.
For sensitive identifiers even hashes/labels may need minimization under the
operator's exact scope. Do not claim immutable audit history justifies retaining
unnecessary removed content. Protected ledger access/inventory is separately audited.

B2 acquisition stop does not create a root content-removal fence; upload consent
uses document 40. Grant revoke still blocks unaccepted intake. Browser/server
cleanup reports distinguish accepted evidence, pending quarantine, local spool,
downloaded reports, backup copies and recipient-held content.

## Acceptance boundary

V0 covers actual capture/export/publication dependencies and emergency removal.
C/H/B edges are added with their feature migrations and tested before enablement,
not fabricated in a V0 DB. SYS-ACC-02/03/04/08 in document 43 extend existing core,
MON/HUN/B recovery/purge tests. No cleanup/restore or sensitive-data deletion has
been performed by this documentation pass.

Integrity/removal/cache-loss state has an explicit cause and verification identity.
A newly detected corruption blocks affected consumers without changing the expected
original hash; verified recovery from an authorized matching backup needs recorded
operator reconciliation. A removal fence cannot be lifted merely because bytes
reappear. Generators/verifiers recompute materialized byte hashes; read checks must
not pretend that existence or an old passing hash proves unknown new bytes valid.
This design does not promise detection of every latent disk error before a bounded
integrity scan or protection against the trusted host operator changing storage.
