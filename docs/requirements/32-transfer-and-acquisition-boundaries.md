# Investigation transfer and acquisition boundaries

Date: 2026-11-09. Status: **selected H4 Workspace-native transfer; other acquisition
paths deferred**. Owner: evidence/security/operations. Hunchly official materials
document case/file workflows, but no vendor interchange parser/compatibility is selected.

## Requirements

### REQ-XCH-001 Explicit bounded Workspace-native selection

H4 shall export/import a versioned investigation selection through
`workspace-case-transfer/1`: selected captures/original inventories, collection
metadata, explicitly selected annotation/task/view context and mapping/provenance.
Preview and freeze selection/inclusion/omissions. Full means complete selected
dataset under this profile, not all DB rows, hidden cases or an installation backup.
No OAuth/session/provider/delivery secrets, ACL grants, active watches/destinations
or automatic publication authority may be included or restored.

### REQ-XCH-002 Quarantine and independent validation

Import is admin-initiated, streamed into private quarantine and processed offline
under archive/file/JSON/decode/time/storage limits. Validate profile/schema, expected
inventory, paths, duplicates, MIME and exact sizes/digests; reject traversal, links,
executable migrations and undeclared files. Unknown format/version or mismatch fails
with report and no accepted business records. A manifest assertion is not a trusted
instruction. No automatic source fetch or vendor converter execution.

### REQ-XCH-003 Namespace mapping and provenance preservation

Map source-instance/foreign IDs to new local IDs with an explicit repeat-import
policy; do not overwrite local evidence or infer trust from UUID equality. Preserve
original byte/manifest digests, claimed capture metadata and separate local import
event/time/verifier outcome. Identity/actor strings are foreign claims, never enabled
local users/roles. Imported task assignees stay unmapped until explicit local
selection; imported saved views are disabled/private to the accepting local owner
until supported-query and sharing review. Verified package bytes do not prove capture authorship/time/truth.
Report URL/name/normalization collisions before accepting selected mappings.

### REQ-XCH-004 Atomic review and safe acceptance

After validation, show a bounded mapping/disclosure/anomaly preview; acceptance
uses actor-bound preview digest/revision and idempotency with transactional records.
Imported records remain private, origin_imported, and unreviewed; publication/watch
baseline/delivery authority is not imported. Rerunning the same accepted import is
a replay; a conflicting namespace/input digest requires explicit new import scope.
No partly accepted case may appear successful if promoted bytes/DB commit fail;
use staged finalization/reconciliation and preserve a clear quarantine disposition.

### REQ-XCH-005 Compatibility, purge and restore truth

Own native profile validation is not claimed Hunchly compatibility. Only a later
documented/tested adapter may import vendor formats. Preserve origin distinctions
in search/report/comparison and block unsupported imported profiles rather than
relabel as local complete captures. Purge invalidates dependent outputs; restore
reapplies deletion state and leaves automatic work disabled. Imported views/tasks/
context cannot execute queries/actions beyond current reviewed supported contracts.

## Initial transfer model and limits

TransferRun stores UUID, direction, profile, frozen selection/input digest, source
instance reference, owner/admin, quarantine/staging namespace, namespace map, anomaly
report, acceptance revision, state and byte/result digests. States: uploaded,
validating, review_required, accepting, completed, rejected, failed, cancelled.
No unknown package body is parsed in the request-serving process.

Initial caps: 25 captures; 512 MiB compressed input AND cumulative decoded package,
1,000 members, 1 MiB per JSON manifest/record and 16 MiB metadata total; reject nested
archives except explicitly declared verified evidence-package members under separate
bounded unpack accounting. Every actual streamed byte counts, not trusted ZIP headers.
One import/export slot, 512 MiB worker memory, 120s execution deadline and existing
disk reserve. Exceeding caps requests a smaller explicit selection; no silent slicing.

POST `/api/v1/case-transfers` exports a reviewed selection for editor/admin under
existing evidence access. POST `/api/v1/case-imports` is admin-only upload; GET
`/{id}/preview` is private; POST `/{id}/accept` pins preview revision/digest and key.
Downloads/status/maps expose safe fields only. Accepted foreign actor names remain
provenance strings; operator bootstrap/session/admission is unrelated.

First H4 permits read/analysis of accepted supported imported bytes with explicit
origin warning and current permissions. Imported material is ineligible as an
automatic watch baseline or public publication by default. A later deliberate
review/import-trust policy must qualify any broader use; importing a "published"
flag does not activate a link. Comparison eligibility still checks actual supported
profile/completeness/integrity; unknown legacy/native profiles remain unsupported.

## Deferred acquisition paths and fidelity

V0/H0–H4 do not passively collect an investigator's browsing, cookies, downloads or
authenticated sessions. A future browser companion must have explicit per-session/
case consent, visible pause, scoped permissions, origin/collector identity, transport
authentication, partial-upload/replay and protected local buffering/purge semantics.
Client-supplied bytes require a distinct acquisition profile and untrusted-input
validation; server recapture remains a separate capture with its own time/environment.

Viewport snapshots and full-page archives preserve different observations. Dynamic/
virtualized pages can omit earlier off-screen material; neither a tall screenshot
nor successful navigation proves exhaustive history. Record viewport/scroll scope,
limitations and partial outcomes honestly rather than promising all social content.
Native attachment/photo/EXIF extraction belongs to separately qualified original-
format profiles in document 27, with source linkage and metadata-location disclosure.

Optional signatures/trusted time remain future trust/custody design, not a replacement
for manifests, audit, independent verification or known limitations. Do not infer
identity/trusted capture time from a locally controlled key or use court-ready
marketing as a product/legal guarantee.
