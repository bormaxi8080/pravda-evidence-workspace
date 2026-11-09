# Hunchly functional comparison and Workspace adoption

Reviewed: 2026-11-09. Status: **official-documentation research; product not installed
or tested**. Owner: product/evidence/engineering. Public sources describe vendor
behavior; Workspace choices below are our design inferences, not verified Hunchly
implementation details. No source code, branded assets, case data or product access
was obtained. Earlier help articles and the 2018 evidence guide are dated references.

## Source register and edition caveat

| Source | Documented observation and limit |
| --- | --- |
| [Product overview](https://hunch.ly/) | Describes capture while browsing, URL/time/hash collection, organization/search and reports; marketing reliability/legal language is not our acceptance evidence |
| [Basic edition, updated 2026-08-25](https://support.hunch.ly/article/130-hunchly-basic) | Lists notes/tags/selectors/tasks/case exports, one-case limit, and unavailable Report Builder/regex/custom extractors/automation/data tab; do not attribute every function to every edition |
| [Selectors](https://support.hunch.ly/article/18-2-setting-up-your-first-selector) | Documents tracking names/addresses/keywords across pages and filtering history; these are research terms, not CSS extraction regions |
| [Regex selectors](https://support.hunch.ly/article/114-selectors-using-regular-expressions-regex) | Documents version-specific regular-expression matching; our initial research cues remain bounded literals |
| [Notes](https://support.hunch.ly/article/23-5-using-notes-in-hunchly) | Describes viewport screenshot plus explanatory text and using notes in reports |
| [Important/history filters](https://support.hunch.ly/article/20-4-hunchly-marking-pages-as-important-and-history-filtering) | Describes importance filtering with tags, terms and keywords |
| [Review screen](https://support.hunch.ly/article/27-9-using-the-page-review-screen) | Lists notes, details/data/path, page export and movement through filtered history |
| [Case tasks](https://support.hunch.ly/article/28-10-using-case-to-do-lists) | Documents case-scoped work ideas and default task lists |
| [Reports](https://support.hunch.ly/article/31-12-building-reports) | Describes assembling ordered report elements and organization identity; availability is edition-dependent |
| [Case export/import](https://support.hunch.ly/article/30-11-exporting-cases) | Documents full/selective export and import; no usable interchange schema/compatibility proof was established here |
| [Attachments](https://support.hunch.ly/article/25-7-working-with-attachments) | Describes file attachment hashing and origin tracking, including manual versus downloaded input |
| [Photos](https://support.hunch.ly/article/24-6-working-with-photos) | Describes photo-page linkage, hashes, EXIF and captions; this is not a Workspace native-media implementation |
| [Data extractors, updated 2025-04-21](https://support.hunch.ly/article/26-8-understanding-hunchly-data-extractors) | Documents page-linked extracted observations and warns older video examples are outdated; no particular current-site extractor was tested |
| [Facebook compatibility](https://support.hunch.ly/article/64-facebook) | Documents missing material on virtualized timelines and manual viewport-note approaches; reinforces fidelity limits rather than universal capture guarantees |
| [Cloud workspace](https://support.hunch.ly/article/113-3-hunchly-cloud-workspace-features) | Documents persistent/ephemeral sessions and file transfer; our one-newsroom self-hosted model remains unchanged |
| [Evidence Guide, revision 1.0 dated 2018-10-17](https://hunch.ly/resources/Hunchly%20Evidence%20Guide.pdf) | Describes MHTML, SHA-256, local GPG signatures and deletion records, including limitations of hashes and locally controlled signing keys; not proof of current feature behavior or legal admissibility |

The reviewed pages contain videos, but only accessible written descriptions/PDF
text were examined. No hands-on UI, browser extension, cloud isolation, retention,
export contents or cryptographic implementation was validated. No pricing or edition
entitlement is made a Workspace dependency.

## Comparison against our actual and planned scope

| Concern | Hunchly documented approach | Workspace source / selected design | Adoption |
| --- | --- | --- | --- |
| Capture context | Browser-led research and case association | Current source is a server Playwright prototype; isolated server capture selected for V0 | Preserve explicit requested context; do not claim server saw the operator's authenticated tab |
| Organization | Cases, tags, important pages | Existing collections/tags; shared archive with no collection ACLs | Use Collection as investigation grouping; add explicit context/importance in H0/V0 |
| Notes | Source-linked notes and screenshots | Existing capture-level freeform note; immutable original evidence selected | H1 anchored text/crop annotations as separate revisioned derivatives |
| Finding evidence | Selector hits, history filters and extracted values | V0 URL/title filters; C1 offline text derivation selected | H2 private full-text search and research cues, separate from CSS/noise profiles |
| Reporting | Ordered findings/notes into reports | Current ZIP receipt; selected verified capture/export profiles | H3 frozen selective narrative report with exact citations and separate disclosure preview |
| Transfer | Full/selective case exports/import | Existing private capture export; no case interchange implementation | H4 own verified bounded transfer profile; no claimed Hunchly format compatibility |
| Provenance and integrity | Hash/signature/deletion narrative in dated guide | SHA-256/manifests, audit and purge ledger selected, unimplemented | Refine provenance/assertion distinctions and preserve independent byte verification; optional signing remains deferred |
| Images/attachments | Page-linked media/origin/metadata | PNG/MHTML HTML profile; native formats deferred | Extend deferred media design without fabricating native files as HTML captures |
| Browser/cloud automation | Product-specific browser/cloud workflow | Controlled public-target server capture, no cookies/auto browsing in V0 | Keep browser companion/credentialed capture as a separate future acquisition contract |

changedetection.io contributed change observation, filters, scheduling and delivery.
Hunchly contributes research context, evidence-linked findings and selective handoff.
Workspace remains a self-hosted editorial evidence lifecycle; research assistance
does not become automatic truth assessment, an unrestricted crawler or a new SaaS.

## Recommended/selected boundaries

ADR-006 selects two bounded H0 refinements for V0: explicit collection/rationale
context at submission and a shared importance flag independent of review. H1–H4
then add annotation/work context, search/cues, reports and transfer under explicit
stage requirements. Source history, C1–C4 and production qualification stay intact.

Important distinctions: research cue versus CSS selector; importance versus approval;
task completion versus review; observed acquisition metadata versus user assertions;
frozen report versus changing case view; byte verification versus legal authenticity.
An explanatory note or cropped screenshot cannot silently replace original bytes.

We select original implementations of product ideas using our existing services.
No code/API/format reverse engineering, Hunchly dependency, brand reuse, direct
compatibility or vendor-equivalent assurance is claimed. See
[requirements 28–33](../requirements/28-investigation-context.md) and
[handoff/acceptance](../requirements/33-investigation-roadmap-and-acceptance.md).
