# ADR-006: Select evidence-linked research context and handoff

Date: 2026-11-09. Status: **selected staged design; implementation unverified**.
Authority: user requested Hunchly comparison, adoption recommendations and continued
requirement development. Evidence: [official-source review](../reference/hunchly-comparison.md).
This selects Workspace behavior, not a copy or compatibility claim for a vendor product.

## Decision

Keep existing Collection as the investigation grouping, without a second Case model
or collection-level access isolation in V0. Add two H0 requirements to V0: an explicit
collection/rationale submission context and an independent shared importance flag.
Neither grants public access, implies truth/review approval or mutates captured bytes.

After qualified V0/C1, select H1 linked revisioned annotations/tasks/saved views;
H2 private content search and literal research cues; H3 frozen selective reports;
H4 verified Workspace-native case transfer. Research cues are not comparison CSS
selectors and cannot silently alter C2 filters or C3 watch epochs. Use existing
PostgreSQL/jobs/storage/permission and profile contracts, not new microservices.

Annotations and reports pin original artifact and derivative/annotation revisions.
Reports have explicit reference-only versus original-evidence inclusions and their
own inventory/disclosure preview. Import validates untrusted packages in quarantine,
remaps foreign identities and never imports grants/publications/session or delivery
authority. Hunchly interchange compatibility is not selected without a real contract.

## Scope, alternatives and consequences

The original 107 requirements remain stable; add 27 stage requirements: two H0/V0,
25 later-stage. Total 134, with 70 applicable to V0 and 64 later-stage. EWP-31 adds
V0 context/importance qualification before EWP-15; H1–H4 use EWP-32–40. Existing
production WARC/PDF/security/recovery and C1–C4 gates remain independently mandatory.

Do not include passive browsing capture, user cookie import, automatic downloads,
EXIF/native attachment ingestion, arbitrary regex/custom extractors, legal-certainty
claims, graph integration or local/cloud account emulation in V0. Those need their
own acquisition/format/security evidence. A server recapture is a new observation,
not proof of what was in an investigator's tab or session.

Importance is triage, not a capture editorial approval revision. Private request
rationale is not automatic export/public metadata. A research task is not an
implementation ticket or evidence review. Derived quotes/crops remain distinguishable
from original capture. Public publication remains a separate deliberate command.

## Verification and unresolved implementation work

Requirements 28–33 specify field/permission/limit/state/API and acceptance details.
No reviewer sign-off, running product test, vendor code/asset import, supported
interchange or runtime feature is claimed by this document. Unsupported/partial
extraction, stale annotation/report selection, removed inputs, import collisions,
and restore/purge must be qualified before enabling their stage.

## Subsequent browser decision

[ADR-007](0007-browser-companion-acquisition.md) supersedes the blanket companion
deferral for selected B0–B2 only. Cookie/credential replay, hidden all-sites capture
and unsupported native/media/trust paths remain deferred. ADR-006's H0–H4 scope
and historical counts above remain unchanged; the current registry is document 38.
