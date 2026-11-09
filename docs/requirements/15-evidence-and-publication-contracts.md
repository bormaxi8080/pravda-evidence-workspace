# Evidence, finalization, publication and export contracts

Date: 2026-11-09. Status: **selected design, not implemented or qualified**.
Owner: evidence/publication lead. Refines REQ-EVD-001–008, REQ-ARC-005/006,
REQ-DAT-003–008 and REQ-SEC-005–008. See ADR-003/004 and document 13.

## Profile definitions

`workspace-capture-v0/1` requires valid non-empty `evidence/screenshot.png`,
`evidence/page.mhtml`, `metadata/capture.json` and `manifest.json`. MHTML must be
a bounded valid archive from the selected engine, not just any non-empty file.
Metadata records actual conditions/provenance and capture warnings. No WARC field
is invented; `deferred_formats` explicitly identifies WARC. PDF is not a capture artifact.

`workspace-export-v0/1` requires a copy of that capture set under `capture/`,
`export.json`, `receipt.html`, `manifest.json`, `SHA256SUMS`, `README.txt`.
`include_pdf=true` makes PDF required for this particular export; absence is a failure.
`include_editorial=false` and `include_actor=false` are defaults. Explicit inclusion
pins an editorial revision and applies requester permission at creation and download.

## Byte and inventory rules

All JSON profile objects: UTF-8 without BOM; keys sorted in Unicode codepoint order;
no insignificant spaces; one final LF; reject duplicate keys, NaN/infinity and floating
point fields. Strings/booleans/null/integers/arrays/objects only. Do not normalize
original URL/content strings during serialization. New timestamps are UTC RFC3339
strings with recorded precision; unknown legacy values are null plus provenance notes.
This is a project serialization contract, not a claim of implementing a general
canonical JSON standard. Exact bytes are preserved and SHA-256 hashed once finalized.

The manifest has `profile`, `capture_id`, `attempt_id`, `artifacts`, `warnings` and
`deferred_formats`. Each artifact lists `path`, `kind`, `mime_type`, `size_bytes`,
`sha256`; entries sort by ASCII relative path. It inventories PNG/MHTML/metadata,
not itself. Capture DB stores manifest size/hash separately. Raw path/url/headers
stay private; profile validation bounds each field and header inventory.

Checksum file syntax: 64 lowercase hex, two ASCII spaces, normalized relative path,
LF. No absolute paths, backslashes, dot segments, symlinks, duplicate member paths
or case-colliding portable archive names. Export manifest inventories every package
file except itself and SHA256SUMS. SHA256SUMS covers all files including both capture
and export manifests, except SHA256SUMS itself. Verifier checks profile-required
inventory and digest coverage, not merely whatever a supplied checksum list names.

No export changes the original capture manifest. Export time/editorial revision/
receipt versions are recorded in export.json. The receipt explains missing V0 WARC
and the limits of hashes/time claims. Repeated export can legitimately have a new
timestamp/package hash; original capture bytes and their hashes remain identical.

## Metadata disclosure and provenance

Record exact private requested/final URLs, main-document status, redirect chain,
request/start/navigation/end/finalization times, engine/browser version, viewport,
locale/timezone, capture options/condition result, artifact outcomes and warnings.
Store an allowlisted response header set for content type/cache/last-modified/etag
and bounded informational fields; exclude Authorization, Cookie, Set-Cookie and
credential/token-bearing headers. Sensitive URL queries remain private. Any omitted
metadata is recorded as omitted by policy, not falsely complete raw network capture.

## Finalization protocol and crash cases

1. Current worker creates DB finalization intent with attempt/generation, target
   immutable namespace and candidate inventory; runner output remains untrusted.
2. Validate/copy bounded regular files into trusted staging, compute actual hashes,
   write metadata/manifest, flush required file/directory state for selected filesystem.
3. Persist the trusted computed inventory/manifest digest on the intent, then
   atomically rename that complete directory to a generation-specific final path
   on the same volume. No overwrite or reuse of another attempt's directory.
4. Lock current job/capture, verify lease/generation/cancel/requester, then set selected
   attempt/artifact/manifest refs, terminal event and audit in one DB transaction.
5. If commit response is ambiguous, query durable state/idempotency before returning
   success or recapturing. Reconciliation can accept only a valid current intent.

| Crash point | Recovery action |
| --- | --- |
| Before intent/copy | Failed attempt; quarantine/expire incomplete staging |
| During write/validation | Keep incomplete state; never finalize empty or truncated bytes |
| After promotion, before DB commit | Reconcile recorded intent + bytes + lease/cancel; otherwise orphan/quarantine |
| After commit, before reply/event delivery | Return stored terminal state on replay; do not create another capture |
| Stale generation promotes late output | It cannot update selected refs; quarantine its unique namespace |
| Later byte corruption/missing files | Record integrity finding, deny complete exports/new publication; suspend affected public serving until resolved |

Integrity findings are separate mutable observations and do not rewrite immutable
historical provenance or manufacture replacement bytes. Reconciliation cleanup is
operator-owned and reports every deleted temporary/orphan namespace; it never
prunes valid finalized evidence merely to recover space.

Before a successful artifact/ZIP byte response, open only the authorized regular
file and verify its trusted size/hash through a bounded spool; do not commit a
success header and discover tampering halfway through the response. Protected
storage permissions and no-follow path handling prevent a different file being
substituted between validation and serving. Export ZIP receives its own stored
digest and download verification. Integrity failure produces safe error/audit.

## Publication transaction and response contract

Input: capture ID, expected editorial revision, expected manifest digest, approved
display URL/title, optional source URL and publisher label from instance configuration.
The admin previews exactly these fields plus the pinned screenshot. Restrict source
URLs to approved HTTP(S); a redacted display URL is labeled redacted, never presented
as the exact private provenance URL. Notes, usernames, raw headers and full private
manifest are not fields of this contract.

Within one transaction, require enabled admin, approved matching revision, complete
profile, no integrity block and no other active publication. Create a unique new
slug, pinned screenshot reference/public metadata and audit. Public fields: slug,
approved title/display/source URL, capture time with precision caveat, profile,
screenshot hash/size and optional approved dated availability observation. Public
response never exposes a capture/job/storage identifier as an alternate file authority.

Every page/metadata/screenshot request resolves that slug and checks active state
and artifact availability. Apply no-store/nosniff/CSP; do not serve private files
through Nginx static aliases. Revocation commits once and is idempotent, then all
new server asset/page requests return generic 404. A known temporary storage failure
may return a generic 503 without disclosing private metadata. A new publication gets
a new slug; old revoked mappings never reactivate automatically.

## Export job and safe receipt

Request selects profile/options and evidence/editorial revision; persist export job
and idempotency with audit. Authorize again before processing and download. Use a
bounded private temporary spool and sanitized member names. Receipt renderer has
no arbitrary network access, script execution or external font/image fetch; interpolate
escaped plain fields into controlled templates. PDF requires a separate bounded
renderer process with equivalent resource/network restrictions.

On completion verify the ZIP inventory and extracted byte hashes before marking
ready. On missing required output, error rather than fallback; retain bounded safe
diagnostics. Download expires after 24 hours; expiration removes only export spool,
not capture bytes. Client receives state/code/request ID and a new-export option.
Production WARC/PDF fidelity and optional derived comparison profiles are different
contracts; neither is silently appended to historical V0 evidence.

## Private investigation-context boundary

The H0/V0 CaptureIntentContext and CaptureTriage in documents 14/28 are application
records. Collection/rationale submission context and importance do not enter
`metadata/capture.json`, the capture manifest, default exports or public metadata.
An explicit editorial export may contain the selected current editorial snapshot;
it must not silently disclose historical submission rationale, tasks, annotations,
queries or cues. Later reports/native transfer require the separate exact disclosure
profiles in documents 31/32; no V0 evidence-profile revision is implied here.

## Browser profile extension

[Document 36](36-browser-evidence-and-intake.md) defines separately versioned
workspace-browser-viewport/1, workspace-browser-page/1 and workspace-browser-export/1.
Original client bytes/inventory remain unchanged; server actor/receipt/verifier facts
have a separate manifest and time scope. They do not extend the V0 capture/export
inventory, prove HTTP/network fidelity or supply missing WARC. Initial browser
submissions are private-only; legacy generic publish/export handlers must reject
these profiles until their particular adapter/gate is qualified. H3/H4 support is
an explicit EWP-51 subgate, not automatic acceptance of all client files.

## Purpose and dependent-copy refinement

[Document 40](40-evidence-eligibility-and-provenance-policy.md) is the cross-profile
operation policy: complete/integrity-valid is necessary but not sufficient for a
baseline, particular adapter or publication. [Document 41](41-dependencies-retention-and-removal.md)
requires exact dependency/pin records and immediate root fences before deferred
cleanup. Current-read authorization, integrity and fences cover ready packages and
public assets; safe diagnosis is distinct from serving corrupt/removed content.
These controls never rewrite the original capture/export manifest or self-hash rules.

## Production profiles and protected read materialization

ADR-010/documents 50/51 now specify exact production PNG/MHTML/WARC/capture-metadata
and required PDF/export inventories, while all V0/browser/foreign identities remain
unchanged. Document 52 implements this document's pre-success hash/spool rule
through globally bounded verified snapshots and transfer leases, with current
permission/root/publication checks and no raw proxy alias. Only actual core types
are needed for V0; production parser/renderer/reader adapters need their own proof.
No original capture manifest includes its PDF receipt or a self-digest.
