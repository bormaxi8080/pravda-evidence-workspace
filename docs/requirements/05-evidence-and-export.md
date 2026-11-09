# Evidence preservation, integrity and export requirements

Date: 2026-11-09. Status: **selected evidence design; implementation pending**. Owner: evidence/domain lead.
Sources: concept sections 6.3–6.4, 14–17, 24, 34.2/34.5;
current `capture.py`, `forensic.py`, `routers/export.py`.
Decisions: DEC-04, DEC-05, DEC-08, DEC-09, DEC-12.

## Artifact profiles

Selected profile IDs, serialization/inventory and finalization rules are specified
in [document 15](15-evidence-and-publication-contracts.md). Machine-readable schema
implementation remains EWP-02 and does not change planned component status here.

| Artifact | V0 complete profile | Production complete profile |
| --- | --- | --- |
| Screenshot PNG | Required | Required |
| MHTML | Required | Required |
| Capture metadata JSON | Required | Required |
| Evidence manifest and checksums | Required | Required |
| WARC/WARC.GZ | Explicitly absent/deferred | Required with defined fidelity |
| HTML receipt | Required in export | Required in export |
| PDF receipt | Optional and explicitly reported | Required in complete export |

Capture evidence and later generated export packages have distinct manifests.
Receipts, editorial snapshots and origin observations produced later cannot be
silently added to the immutable capture manifest as if captured at the same time.

## Requirements

### REQ-EVD-001 Completeness before success

Validate all artifacts required by the selected profile: presence, non-empty valid
format, bounded size and readable final location. Record missing/partial artifacts
as a non-complete outcome. A profile ID/version and warnings shall appear in the
capture detail/export. No code path may silently omit required output after failure.

### REQ-EVD-002 Immutable bytes and accurate provenance

Store exact output bytes before computing digests. Capture metadata shall include
requested/final URL, relevant HTTP metadata, redirect history, real capture/engine/
browser timing/options, condition outcome and errors/warnings. Unknown values remain
explicitly unknown. Browser locale/timezone and viewport are provenance, not settings
to be guessed later. Sensitive request/response headers require a documented policy;
exclude credentials/session material from ordinary metadata and all public projections.

### REQ-EVD-003 Unambiguous hashes without self-reference

SHA-256 shall cover exact stored bytes. The capture manifest lists required evidence
and provenance metadata using normalized relative paths, MIME, sizes and digests;
it does not list its own digest. Persist the exact deterministic UTF-8 manifest
bytes and store their SHA-256 in the capture record. Use the selected JSON serialization/field ordering in document 15; validate it
when materializing the schema/verifier. A checksum file may include the
manifest plus listed files, but never its own checksum. The export manifest/checksum
layer separately includes receipts and any export-time metadata.

### REQ-EVD-004 Bounded immutable storage and reconciliation

Use per-attempt staging and per-capture immutable final namespaces with validated
storage keys. Enforce byte/disk limits while writing; do not overwrite an existing
finalized key. On missing/corrupt bytes, report failed verification and prevent
new publication/export as a complete profile. Reconciliation identifies temporary
orphans and DB/filesystem disagreements; cleanup must not erase finalized evidence.

### REQ-EVD-005 Portable self-describing private export

Authorized V0 editors/admins shall request a bounded ZIP containing original
evidence, capture metadata/manifest, export metadata/manifest, HTML receipt and
SHA256SUMS. Include a plain verification guide, profile, omissions, export time
and any explicitly included editorial revision. Private notes are included only
through an explicit choice; default export excludes internal notes/user identity.
Do not derive archive member names from untrusted URLs or allow traversal/symlinks.

Export either returns a verified complete selected profile or an explicit failure;
a separately named partial diagnostic package, if offered later, cannot masquerade
as complete evidence. Large exports use a job and bounded temporary storage rather
than unlimited in-memory ZIP creation. Record requester and actual export outcome.

### REQ-EVD-006 Safe receipts and optional PDF behavior

Receipts shall escape all source/editorial strings, use controlled local assets
and include URL/display identity, times, profile, files/digests and verification
instructions. Receipt rendering must not fetch arbitrary resources or execute
archive scripts. If PDF is disabled or fails in V0, expose the omission and reason;
if a client requested a PDF-required profile, fail that export. Production complete
export requires a successful safe PDF. Never retain the current silent exception behavior.

### REQ-EVD-007 Explicit WARC fidelity and future compatibility

Before production WARC implementation, specify whether it captures network responses,
browser output/resources or another archival representation, which exchanges are
covered, truncation/error semantics and replay/interoperability expectations. Do not
label an MHTML wrapper as a full network recording. V0 exports shall advertise no
WARC. Adding WARC later requires a new artifact/profile contract and compatibility
test; it cannot retrospectively manufacture missing historical traffic.

### REQ-EVD-008 Verification must detect more than checksum mismatch

Provide an implementation-stage verifier that checks required inventory, normalized
paths, duplicate members, sizes, digests, profile/schema support and unreadable or
missing files. It shall reject unsupported profiles explicitly, not declare success
on an empty checksum list. Verification output shall distinguish internal consistency
from external authenticity/trusted capture time. Verify an exported package outside
the original installation using only its contents and documented tools.

## Illustrative package structure

```text
evidence-<capture-id>.zip
  README.txt
  evidence/screenshot.png
  evidence/page.mhtml
  metadata/capture.json
  integrity/capture-manifest.json
  receipt.html
  receipt.pdf                 # optional in V0, required in production profile
  export.json
  manifest.json               # export inventory; excludes itself
  SHA256SUMS                  # covers export manifest and contents, not itself
```

Production adds WARC at an explicitly named path. This illustration is not a
released file-format schema. Acceptance: ACC-01/04/05/07/09/10/12.

## Detailed selected design

See [the baseline register](13-selected-v0-baseline.md),
[contracts and operator procedures](README.md) and
[assignable work packages](18-assignable-work-packages.md).
Implementation/qualification remain pending; source presence is not test evidence.

## Selected production refinement

ADR-010/documents 50–53 select workspace-capture-production/1 and
workspace-export-production/1, same-attempt HTTP representation recording, explicit
scope/omissions, safe required receipt PDF and independent verification/replay.
The existing V0 profiles are unchanged. A network.warc.gz filename, later MHTML
conversion or PDF generation cannot establish missing historic traffic/fidelity.
Protected pre-header byte validation and read budgets are specified in document 52;
its core subset applies before V0 qualification without requiring production formats.
