# Preserved-content search, research cues and extracted observations

Date: 2026-11-09. Status: **selected H2 design; not implemented**.
Owner: evidence/search/backend. Origin: Hunchly documented keyword/selectors/data
workflow, adapted to our offline derivation and shared newsroom authorization.
Depends on qualified C1/H1; no search cluster, public search or AI inference is added.

## Terminology and scope

ResearchCue means a literal term an investigator wants to locate (name/address/
other string). ComparisonProfile CSS selector means a region used for extraction/
noise handling. They are different models/APIs; cue edits never change C2 profiles,
C3 epochs or preserved bytes. Literal hits and extracted observations are leads,
not verified identities, relationships, factual claims or editorial approval.

## Requirements

### REQ-FND-001 Private explicit corpus search

H2 shall search supported preserved capture text with optional collection/source/
date/importance filters and bounded paging. Reuse PostgreSQL plus versioned offline
derived text; preserve V0 URL/title query behavior. Content search is a named scope,
not a silent expansion of that query. Annotation-text search is an explicit separate
scope and labels user commentary versus source text. No live fetch or external
service receives search terms. Reauthorize all results/snippets/input links.

### REQ-FND-002 Coverage and version-aware indexing

Index exact capture/artifact/derivation hashes and extractor/index version, one record
per capture version. Expose eligible/indexed/failed/unsupported coverage for the
selected corpus; unavailable or partial indexing cannot imply absence of evidence.
Rebuild with durable bounded jobs and do not reset review/publication. Deduplicated
display may group results by Source, but retains capture IDs/version counts and
does not delete repeated/identical captures. Private saved-view definitions are not
automatically indexed as shared source text.

### REQ-FND-003 Versioned literal research cues

Collection-scoped ResearchCue revisions shall record name, literal value, match mode,
author/time and active/archived state. First H2 supports literal case-sensitive and
explicit Unicode-casefold matching only, with versioned normalization and original
offset mapping. No arbitrary regex/query execution, custom scripts or automatic
person/entity creation. Referenced cue revisions remain stable for prior results.
Values may be sensitive and stay out of ordinary public/export/notification metadata.

### REQ-FND-004 Auditable source-linked hits

CueHit shall pin cue revision, capture/artifact/representation hashes, exact UTF-8
span/quote digest, algorithm version and search-run outcome. Validate mapped spans
against original derived bytes even under casefold expansions. Repeated matches
retain occurrence identity; unsupported text/overflow is explicit incomplete coverage,
not no hits. Preserve raw source context link; never treat a match as proof that a
named person owns a page or that two sites have a real-world relationship.

### REQ-FND-005 Reanalysis, privacy and attention boundaries

Cue edits/reindexing create a new analysis with scope/version/time and no invented
historical hit timestamp. GET/search does not acknowledge events, change importance,
approve review, publish, enable watches or send C4 notifications. An investigator
may explicitly save a hit as an H1 annotation with verified anchor; the hit remains
a derived observation. Input/cue purge invalidates affected indexes/snippets/hits
before serving or export, and restore replays deletion state before rebuilding.

### REQ-FND-006 Bounded built-in observations, not an ontology

A subsequent H2 increment may enable maintained offline email/IP candidate extractors
under explicit extractor profiles. Preserve exact source span/hash, normalized
candidate, extractor version and caveats. No network resolution, enrichment, identity
merge, automatic graph edge or proof-of-ownership assertion. Built-in parser output
is a proposed observation for research review, distinct from manual assertions.
Unsupported source types, malformed candidates and bounds remain visible. First
literal-cue/search release does not pretend these extractors are already enabled.

## Initial contracts and limits

ResearchCue has UUID, collection_id, revision, name<=128 chars, value<=256 chars,
mode=`literal|casefold_literal`, actor/time and archived flag. Start with at most
100 active cues/collection and 100 cue definitions per explicit analysis run.
CueHit and SearchRun preserve completed/partial/failed status, input corpus snapshot,
index/algorithm versions, exact candidate offsets and coverage diagnostics.

POST `/api/v1/evidence-searches` creates a bounded query/corpus intent or returns
known coverage with a search ID; GET `/{id}/results` pages stable snapshot results.
POST/PATCH `/api/v1/research-cues` or `/{id}` creates revisions with expected_revision;
POST `/{id}/analyze` selects stored captures and an idempotency key. It cannot
fetch a URL. GET cue hits respects same internal evidence permissions. Search uses
a versioned plain term/phrase grammar, not unrestricted SQL/regex/JS.

Default page 25/max100; query<=512 chars; representation cap 2 MiB UTF-8 as C1;
max500 hits per artifact/run and 10,000 total hits/run. On cap mark coverage partial
with explicit next action; never claim a complete case scan or silently lose hits.
Analysis uses existing one-slot offline worker/deadline/memory/temp limits and
global admission cap. Storage/index quotas must be enforced without pruning originals.

Base full-text derivation uses the named unfiltered archive-text extractor, not
C2's focused/ignored view; search coverage labels its actual text scope. Raw HTML
resources/script contents are not promised as visible-text coverage. Existing live
query views and frozen report corpus snapshots remain visibly different.

Corpus admission resolves explicit capture IDs and representation eligibility into
the SearchRun snapshot. Process bounded pages under durable jobs rather than load
an unbounded collection in memory. Deadline/quota interruption records processed/
unprocessed counts and partial status; changing membership needs a new run. Use
the existing 1 GiB derived cache budget for cached analysis bytes; keep authoritative
run/cue/annotation references, deny exhausted pinned capacity and rebuild disposable
indexes only from verified retained inputs. Retained corpus/index size and rebuild
time require qualification before enabling H2 on a larger installation.
