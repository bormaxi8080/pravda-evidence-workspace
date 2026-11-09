# Preservation, rendering and replay source review

Reviewed: 2026-11-09. Status: **primary-document research; no recorder, replay or PDF
runtime tested**. Owner: evidence/capture/security. This review informs ADR-010;
it does not import software, copy code or qualify any dependency/image version.

| Primary source | Relevant observation / limit |
| --- | --- |
| [IIPC WARC 1.1](https://iipc.github.io/warc-specifications/specifications/warc-format/warc-1.1/) | Defines record/container structure, record/block/payload distinctions, identifiers and truncation reporting. A valid container alone does not establish what an acquisition covered or that browser replay is complete. |
| [Browsertrix Crawler documentation](https://crawler.docs.browsertrix.com/) | Describes browser/CDP collection, configured crawl scope, screenshots and replay QA. Useful qualification candidate; not a drop-in proof of our single-attempt MHTML/PNG/recording, sandbox or private-export contract. |
| [pywb usage](https://pywb.readthedocs.io/en/latest/manual/usage.html) | Documents WARC replay/recording components and optional remote/fallback features. Independent replay QA must disable live/remote fallback and run outside the application security origin. |
| [WeasyPrint security](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#security) | Warns about resource exhaustion, filesystem/network access and PDF attachments with untrusted input; a URL fetcher alone is not a memory/time sandbox. Use controlled templates and an isolated finite process. |
| [RFC 9110 HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110) | Allows ignoring Range and advertising no range support; conditional/method/header handling still needs correct authorization and HTTP semantics. Transfer resumption is not implied by an artifact hash. |

Only accessible written documentation was examined. No candidate repository commit,
binary image, license compatibility, installed version, file-format conformance,
external replay interoperability or PDF safety was validated. Materializing a
dependency later requires exact source/license/SBOM/security and behavior evidence.
Vendor high-fidelity language is not our acceptance result.

## Selected interpretation

The existing V0 engine is direct Playwright without WARC; current receipt code's
presence is not a qualified safe PDF generator. The selected production gap is
actual same-attempt HTTP representation recording, clearly labeled observation/
normalization/omission scope, safe required PDF receipt and independent byte/profile
verification. A later WARC built from old MHTML cannot recreate missing exchanges.

Prefer qualification of a recorder-backed existing engine adapter first; evaluate
a separately pinned Browsertrix adapter only if needed and only through the same
contract. No dual runtime engine deployment or opaque WACZ-as-WARC substitution.
Use pywb as one replay-test candidate, not a public app viewer or an active-content
service trusted with Workspace cookies. Reader/recorder choices remain empirical
EWP-73/75 gates; failure leaves production unavailable rather than downgrading WARC.

Documents 50–53 define Workspace's own profiles, resource/permission/recovery rules
and proposed evidence gates. They refine existing requirements, not new capabilities
or runtime success. V0, browser submissions and foreign/legacy profiles keep their
original scope and byte identity.
