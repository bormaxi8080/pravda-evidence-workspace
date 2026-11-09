# changedetection.io: source review and adoption recommendations

Reviewed: 2026-11-09. Owner: engineering/product. Status: **source-based research;
recommendations for Evidence Workspace, no upstream code imported or executed**.
Repository: [dgtlmoon/changedetection.io](https://github.com/dgtlmoon/changedetection.io).
Pinned source: [c01f1546417a2fb34eb5add32b35ca56002e248c](https://github.com/dgtlmoon/changedetection.io/tree/c01f1546417a2fb34eb5add32b35ca56002e248c),
the observed master commit, dated 2026-11-08. Observations below concern this snapshot,
not all historical versions or a tested production deployment.

## Review method and boundaries

Read upstream README, LICENSE/NOTICE, repository tree, fetcher capabilities, watch
history, text/image processors, diff rendering, notification handling, scheduling
and targeted regression tests through the GitHub connector. Checked existing
Workspace requirements and prototype source locally. No upstream installation,
benchmark, security audit, live notification, or account/credential use occurred.
Performance claims in upstream descriptions are not adopted as measurements.

## What is present in the inspected source

| Area | Observed source | Evidence and limitation |
| --- | --- | --- |
| Product functions | [README](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/README.md) | Documents watches, selectors, browser steps, comparison, schedules, notifications, PDF/JSON handling and optional AI; feature descriptions alone are not runtime verification |
| Fetcher capabilities | [content_fetchers/base.py](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/changedetectionio/content_fetchers/base.py#L10-L29) | Typed flags identify screenshots, browser steps, element positioning and original PDF support |
| Processing pipeline | [text_json_diff/processor.py](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/changedetectionio/processors/text_json_diff/processor.py#L511-L694) | Separate extraction, ignore/trigger logic, config fingerprint and normalized-content comparison; includes MD5-based change fingerprints |
| Text comparison | [diff module](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/changedetectionio/diff/__init__.py#L424-L455) | Supports added/removed/replaced content, context, word-level output and normalization options |
| History and attention | [Watch model](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/changedetectionio/model/Watch.py#L340-L350) | Tracks last-viewed versus newest history; history storage is watch/file-oriented and is not our capture/publication data model |
| Image comparison | [image processor](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/changedetectionio/processors/image_ssim_diff/processor.py#L146-L220) | Establishes baseline, compares screenshot outputs with configurable thresholds/cropping and isolated processing calls; do not infer implementation from directory name alone |
| Notification boundary | [notification service](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/changedetectionio/notification_service.py), [handler](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/changedetectionio/notification/handler.py#L306-L410) | Queues/formats change context and uses Apprise; provider delivery was not tested |
| Schedule time semantics | [time_handler.py](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/changedetectionio/time_handler.py), [timezone regressions](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/changedetectionio/tests/test_scheduler_timezone_regressions.py) | Timezone-aware windows and tests for bad configuration affecting scheduling; regression examples are reusable design lessons |

## Adoption matrix

The original review recommendations below are now adopted through ADR-005 and
requirements 20–26, except deferred investigations in document 27. The first-version
addition is explicit Source history; automatic comparison/watch/delivery stays in
later stages. These are Workspace design choices, not upstream guarantees.

| Idea | Workspace use | Recommended stage | Adaptation required |
| --- | --- | --- | --- |
| Fetcher capability descriptors | Display actual engine-supported options and reject unsupported capture conditions | V0 design/implementation | One descriptor behind CaptureEngine; no plugin market or extra engines required |
| Capture history timeline | Show previous captures of a Source, preserving independent capture identity | V0, using existing source/capture model | Missing/failed attempts are visible; no automatic dedupe/deletion of unchanged captures |
| Text comparison | Let an editor compare two stored captures and inspect additions/removals with context | First optional post-V0 increment | Versioned offline extraction; comparison is derived analysis, not original evidence |
| Ignore/select rules | Suppress menus/timestamps/banners in a comparison, focus on article content | After basic comparison | Preserve originals; explicit profile revision, raw versus filtered views, missing-selector outcome |
| Profile fingerprint invalidation | Recompute comparison when extraction/normalization rules change | With comparison | Cache key includes input artifact hashes, extractor/algorithm versions and full effective profile |
| Reviewed/unread changes | Give each editor an attention queue distinct from evidence approval | After comparison | Per-user acknowledgement via POST; merely viewing a page cannot approve or publish it |
| Recheck schedules and pause | Observe selected sources at bounded intervals with visible next run | Optional monitoring phase | Durable due jobs, one run per source, timezone/DST policy, quotas, pause/backoff, no catch-up storm |
| Failure diagnostics | Distinguish missing selector, unavailable origin and unchanged content | V0 errors; richer monitoring later | Failed extraction is unknown/error, never "no change" or "deleted" without evidence |
| Internal alerts, then notifications | Tell reviewers that a source needs attention | Internal first; external opt-in later | Durable outbox, minimal payload, destination approval, retry/deduplication; no implicit disclosure |
| Screenshot comparison | Help inspect layout/image changes | Later optional increment | Fix viewport/locale/engine context; isolated pixel processing; no semantic truth score |
| PDF/JSON source profiles | Preserve and compare a public document or structured response | Later separate artifact profiles | Native original bytes plus bounded extraction; incompatible with pretending every source is HTML/MHTML |
| Visual selector | Assist configuring a focus region | Later, after profile UX | Use safe screenshot/element metadata; never render hostile archived HTML in the trusted app origin |
| Global/tag defaults | Reuse common monitor settings | Later only if real usage warrants it | Avoid hidden inheritance: show/pin effective profile, owner and revision |

## Concepts to keep separate

Availability observation asks whether an origin is reachable. Content comparison
asks how two captured representations differ. A schedule decides when to run.
Evidence Capture preserves bytes/provenance. An alert requests human attention.
Review approves a revision; Publication grants public access. None implies another.

For example: a rule ignores a rotating timestamp while the article changes. Keep
both original captures; store extraction/profile/input digests; show a derived diff;
create an internal change event if warranted; never rewrite evidence or publish it
automatically. The same-original-byte shortcut can avoid repeated analysis, but an
explicit editor capture request still creates its own provenance-bearing capture.

## Implementation-level lessons

1. Copy the pipeline boundary idea, not the whole monitoring application: acquire,
   preserve, derive/extract, compare, evaluate rules, enqueue notifications separately.
2. Pin effective configuration. Upstream checks both raw content and filter state
   before skipping processing; our comparison cache must also include extractor and
   algorithm versions. A changed rule with unchanged source bytes is a new analysis.
3. Keep selector absence/empty output distinct from stability. Upstream has explicit
   missing-filter handling and tests; Workspace must prevent a disappearance from
   turning into a reassuring unchanged result.
4. Keep notification failure independent from capture/evidence success. Use our
   durable PostgreSQL outbox, not a second truth source or request-thread delivery.
5. Review test scenarios as design references, then write Workspace behavior tests.
   Do not claim the upstream tests ran or that passing them proves our isolation.

Relevant tests: [ignore-text](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/changedetectionio/tests/test_ignore_text.py),
[trigger interaction](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/changedetectionio/tests/test_trigger.py),
[missing-filter notification](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/changedetectionio/tests/test_filter_failure_notification.py),
[diff patch XSS regression](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/changedetectionio/tests/test_diff_download_patch_xss.py).

## Reuse choices and exclusions

Recommended now: adopt ideas and write interfaces/tests within the existing Python
architecture. Later evaluate focused dependency reuse (for example Apprise behind
a narrow notification adapter), based on actual needs, dependency/license inventory
and security/resource tests. A direct changedetection.io runtime dependency, fork,
sidecar synchronization or wholesale module transplant is not selected.

Do not adopt consumer price/restock tracking, arbitrary browser login workflows,
custom JavaScript execution, unrestricted proxies, user plugins or external AI
summaries into V0. Do not transplant MD5 change fingerprints as forensic digests,
watch-history pruning as evidence retention, or shared watched-state as editorial
approval. These choices would conflict with Workspace boundaries.

## License and attribution evidence

The inspected [LICENSE](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/LICENSE)
is Apache-2.0. Its redistribution section specifies license/notice retention and
modified-file notices. The repository's
[NOTICE](https://github.com/dgtlmoon/changedetection.io/blob/c01f1546417a2fb34eb5add32b35ca56002e248c/NOTICE)
reserves brand assets and identifies separate dependency licensing. This review
imports no code, assets, tests or dependencies. Any later code reuse needs an
exact-file provenance/dependency inventory and retained applicable notices; it is
not automatically cleared by this research. Workspace's own license is unchanged.

## Workspace follow-up

The selected continuation is routed through the
[adopted roadmap](../requirements/20-change-monitoring-proposal.md), detailed in
requirements 21–25, and mapped to acceptance/tickets in document 26. Advanced
investigations remain document 27. V0 now has 68 requirements including history;
39 later-stage requirements do not become V0 gates or replace evidence/recovery work.
