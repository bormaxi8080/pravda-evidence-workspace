# Product requirements and first-prototype boundary

Date: 2026-11-09. Status: **proposed**. Owner: product lead.
Sources: concept sections 1–6, 13, 27, 32–34, 36–37; HTML mockup;
[current-state review](../04-current-state.md). Decisions: DEC-01, DEC-04, DEC-05,
DEC-06, DEC-09, DEC-12 in [decision register](12-decisions-and-risks.md).

## Product model and target users

A newsroom preserves the state of a web source at a particular time and keeps
the bytes, provenance and editorial context under its control. Editors can find
and review that evidence, selectively publish a safe representation, or export
a portable package for another reviewer. Readers see only explicitly published
material. An operator maintains the installation and its recovery path.

The initial deployment serves one mutually trusted editorial team. Admin is an
application role; host/database administrators remain a separate operational trust
boundary. There is no claim of protecting evidence from an authorized host operator.

## Proposed scope matrix

| Capability | V0 controlled pilot prototype | Production baseline from concept |
| --- | --- | --- |
| Deployment | One newsroom, one host, one DB, local volume, documented TLS | Same simple topology, qualified support/upgrade/recovery |
| Capture | Manual public HTTP(S) URL and bounded CSV, one engine implementation | Hardened adapter, documented site/format limitations |
| Jobs | Durable queue, one worker by default, retry/cancel/restart recovery | Qualified concurrency, operational recovery and throughput |
| Evidence | Required PNG, MHTML, JSON provenance, manifest, hashes | Add WARC with explicitly specified archival fidelity |
| Export | Private ZIP + HTML receipt and full checksum verification | Mandatory complete profile including WARC and PDF |
| PDF | Optional, explicitly unavailable when disabled/failing | Required and tested; silent omission forbidden |
| Editorial | Shared archive, collections, tags, notes, basic review/search | Usability-qualified complete core flow |
| Publication | Admin-only explicit publish/revoke, screenshot and safe metadata | Same baseline; editor publishing only after policy decision |
| Public downloads | Screenshot and public metadata only; raw evidence packages private | Optional explicitly approved downloads, with disclosure review |
| Monitoring | Not required for V0 exit; show unknown/not checked honestly | Bounded availability probes, timestamps and failure semantics |
| Security | Admission/RBAC/sessions, CSRF, SSRF/egress, isolation, safe files and audit required | Independent review and broader security/operational qualification |
| Operations | Clean install, migration rehearsal, manual quiesced backup/restore tested | Automated repeatable procedures, defined service objectives |
| Quality | Core happy/denied/failure/recovery scenarios | Expanded integration/security/E2E, pilots and known limitations |

The V0/production split is a new proposal. WARC and mandatory PDF are deferred
only from the controlled prototype, not deleted from the original concept.

## Requirements

### REQ-SCP-001 Independent newsroom installation

V0 shall operate as one newsroom per deployment without SaaS organizations,
billing, cross-newsroom sharing or tenant routing. All admitted editors share
internal evidence; collections organize work and do not create access-control silos.
UI shall state this model before use with different confidentiality groups.

### REQ-SCP-002 Complete bounded editorial journey

V0 shall support sign-in, URL/CSV submission, job progress, capture inspection,
organization, notes, review, private export, explicit admin publication and revocation.
An editor shall not need a terminal for those activities. Operator maintenance
may use documented CLI commands. Unsupported features shall not appear to work.

### REQ-SCP-003 Honest evidence profiles

V0 shall identify its artifact profile as a prototype profile and disclose absent
WARC/PDF. Production completeness shall be defined separately. Neither a successful
browser navigation nor an HTTP 200 alone qualifies a complete capture.
Hashes shall not be described as proof of factual truth, legal admissibility,
trusted time or authorship. A public page is a projection of evidence, not a full archive.

### REQ-SCP-004 Enforced limits and overload behavior

V0 shall validate configurable limits before accepting work where possible and
stop bounded processing when a runtime limit is reached. It shall never silently
truncate CSV rows, artifacts, exported files or results while claiming completeness.
The proposed starting limits below require review and later resource tests.

| Setting | Proposed starting value | Intended behavior at boundary |
| --- | --- | --- |
| CSV rows | 500 maximum accepted rows | Reject larger input before job creation; preview invalid/duplicate rows |
| CSV bytes | 1 MiB | Reject excessive upload/text before full parsing |
| Active browser captures | 1 per installation by default | Keep remaining jobs durable/queued; higher values require qualification |
| Pending capture jobs | 1,000 | Reject admission beyond cap; batch confirmation is all-or-nothing |
| Navigation timeout | 60 seconds | Mark attempt failure/partial with reason |
| Whole capture attempt | 120 seconds | Stop browser/processing, recover the job deterministically |
| Automatic attempts | 3 total | Retry only classified transient failures; expose exhausted result |
| Artifact size | 100 MiB per artifact; 250 MiB per attempt | Abort bounded writes and preserve diagnosable partial state |
| Interactive list size | 25 default, 100 maximum | Bound API/UI pagination; reject invalid page sizes |

Maximum screenshot dimensions, export bytes and disk-reserve threshold are blocking
configuration decisions in DEC-09. Byte limits must be enforced while streaming;
checking after a large file is fully allocated does not meet this requirement.

### REQ-SCP-005 Capture support boundaries

V0 shall support publicly reachable HTTP(S) pages within documented browser limits.
Authenticated capture, customer cookie jars, CAPTCHA solving, anti-bot bypass,
platform-specific login, recursive crawling and automatic link discovery are excluded.
A failed or unsupported source shall produce an explicit outcome, not fabricated evidence.

### REQ-SCP-006 Prototype qualification and production deferrals

V0 shall be labeled for controlled pilot use with tested limits and known gaps.
No production claim shall be made until the concept's evidence, security, recovery,
upgrade and pilot gates are met. The concept's 5–50 users and 2 GB deployment claim
are unverified assumptions; publish supported resource limits only from measurements.

## Explicit non-goals

No AI truth scoring, automatic fact-checking, research knowledge graph, Locus/country
catalog integration, full CMS, distributed crawler, multi-tenant SaaS, SSO suite,
SPA rewrite, mandatory signatures/timestamp authority, browser extension, S3 backend,
semantic diff, automatic recapture or scheduled large-scale crawling in V0.
Mobile layout and dark/light themes remain UX expectations, not separate applications.

## Acceptance and unresolved points

Verification scenarios: ACC-01/02/03/04/05/07/09/11/12 in document 10.
Scope, role/disclosure policy, hard resource ceilings and production profile must
be reviewed before implementation. Existing code is input to migration, not a
waiver of these requirements.
