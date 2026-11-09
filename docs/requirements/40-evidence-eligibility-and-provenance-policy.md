# Evidence eligibility, provenance and consent policy

Date: 2026-11-09. Status: **selected refinement; no policy implementation**.
Owner: evidence/security/backend. Authority: ADR-008. Refines REQ-DAT-001/003/005,
REQ-EVD-001/002/005/008, REQ-CMP-001/003, REQ-MON-006, REQ-RPT-002/003/004,
REQ-XCH-003/005 and REQ-BAE-001/003/005/006. No new requirement IDs are introduced.

## Independent decision inputs

An input can be byte-valid and complete under its declared profile while unsuitable
for a particular operation. Evaluate these dimensions separately:

- Acquisition: server-observed pipeline facts; client-submitted collector claims;
  foreign imported claims; legacy unknown. A foreign package describing a server
  does not make the receiving installation its witness.
- Inventory/completeness: exact known profile and required artifacts, complete/
  partial/failed status. An HTTP 404 may be complete evidence of that response.
- Integrity/availability: verified input hashes/manifest and currently present bytes;
  corruption/missing/purged/unsupported are different reasons.
- Intent/editorial: explicit collection/rationale, current editorial revision/review,
  independent triage, selected annotation/report revision and disclosure consent.
- Authority/readiness: current actor/resource permission, operation capability,
  profile adapter, qualified environment, capacity and current dependency fence.

Authorization is checked before descriptive diagnostics. Missing/foreign/private
resources retain the generic 404/denial policy; a capability endpoint cannot become
a way to enumerate evidence, annotation bodies or personal query definitions.

## Purpose-specific eligibility matrix

Each "qualified" cell requires its owning stage and exact adapter/version; the table
does not enable a capability just by naming it.

| Evidence class | Private inspection/originals | Private package | C1/H1/H2/H3 processing | C3 automatic content baseline | Public publication |
| --- | --- | --- | --- | --- | --- |
| Complete verified local server V0 | Authorized screenshot/metadata and attachment reads | Qualified workspace-export-v0/1 | Qualified supported inputs/anchors and exact limits; each stage checks its own purpose | Only local eligible HTTP 2xx, supported meaningful text, current watch/profile epoch | Admin, approved editorial revision, exact projection and integrity checks |
| Complete verified server error page | Same, with recorded HTTP/status warnings | Same profile without hiding error outcome | Manual comparison/reference may be valid; never infer article deletion/truth from status | Ineligible as first C3 article baseline; technical event, prior baseline retained | Only same explicit core checks/disclosure; no automatic publication from a status event |
| Partial or failed server capture | Metadata and individually verified retained artifacts with warnings | No complete export profile; no silent successful incomplete package | Only specifically supported references; no invented anchors/complete input | Ineligible | Ineligible |
| Legacy unknown/import | Known verified retained originals plus unknown/migration caveats | No V0 relabel; packaged legacy export requires its own qualified contract | Unsupported unless a named adapter proves the required input/profile | Ineligible by default | Ineligible; old-link policy in document 17 remains |
| Accepted browser viewport/page | Private verified bytes, client/time/fidelity labels | Qualified workspace-browser-export/1 | Each browser C/H adapter has an independent subgate; viewport cannot supply missing MHTML text | Ineligible in selected B stages | Ineligible in selected B stages, even after editorial approval |
| Accepted H4 foreign evidence | Private origin_imported data, current local permission | Explicit own-native package/export with preserved claims and qualified adapter | Exact supported profile/byte/provenance adapter required | Ineligible by default | Ineligible by default; no imported public flag/role grant |
| Unknown profile, purged or corrupt required input | Safe diagnosis only; individually valid unrelated artifacts follow their own permissions | Block incomplete/unsupported claim | Block affected operation; distinguish unsupported, corruption and cache loss | Ineligible | Block affected serving/creation under integrity/removal policy |

Reports distinguish a citation-only reference from included original bytes. A
partial/foreign reference can be displayed only with its actual status and selected
profile's support; it cannot become a verified quote or included complete original
by removing a warning. C4's first payload remains minimal application-event metadata;
neither publication nor a successful report permits new content-bearing delivery.

## Shared decision contract

Application services expose an internal versioned decision, not a new public
authorization endpoint. Inputs: operation, actor/permission revision, resource IDs,
exact profile/manifest/artifact/revision refs, effective feature revision and current
dependency epoch. Output: allowed/blocked/unavailable/pending_qualification plus
bounded reason codes, required action and the checked revision set.

Selected reason families: authorization_denied, profile_unsupported,
adapter_unqualified, input_incomplete, input_missing, integrity_failed,
dependency_removed, annotation_retracted, stale_revision, disclosure_required,
resource_limit, feature_disabled, restore_hold. Map to existing HTTP envelopes;
do not replace an authorization denial with a detailed profile leak. Never include
raw note/query/page bodies, bearer material or storage paths in reasons/logs.

Admission stores exact selection/consent and the applicable policy version; claim,
commit and every protected download recheck current authority/fences. A previous
allowed decision is not a bearer capability. Policy updates can block future use
without rehashing original evidence or rewriting old receipts as newly qualified.
Unknown purpose/profile/version fails closed. Same service is used by SSR, web API,
companion intake, workers, verifier/export and relevant publication asset paths.

## Time basis and imported identity

| Channel | Immutable observed/claimed times | Default mixed archive basis |
| --- | --- | --- |
| Local server | Actual request/navigation/finalization under stated host-clock scope | Preserve existing server captured_at semantics |
| Browser | Original client interval/clock claim; separate server requested/received/verified/accepted | Server received_at; client future clock cannot reorder default archive |
| Foreign/legacy | Preserved historical claims or null/unknown, plus local import time | Explicit server import-time basis where selected; never overwrite claimed/unknown capture time |

Expose time_basis and archive_sort_at in the mixed-stage DTO/cursor version. In
V0 the existing captured_at order is unchanged. Source history remains server
requested_at/ID descending; imported unknown request time is labeled unknown,
not fabricated from migration. Date filters name their basis; changing it resets
the cursor. Null historical times use explicit deterministic placement/ID tie-breaks.
Foreign IDs are namespaced/mapped, not authentication or authority over local objects.

## B2 recording versus approved upload

Freeze an observation descriptor at local acquisition: client observation ID,
session ID/acquisition epoch, artifact inventory digest, capture interval and context.
Register only that minimal digest/ID descriptor with the server while the acquisition
lease is active, under the disclosed session-control consent. No original/page body
is sent at registration. Upload approval separately pins the registered descriptor/
destination/inclusions and consent revision; it may occur after recording stops.
Stop/pause/lease expiry fences **new acquisition/registration**; it does not erase
registered historical observations or the explicit keep-approved-uploads decision.

After stop/expiry, an explicitly approved upload of a previously registered observation
can finish only if its stored descriptor/consent is unchanged, upload is still unaccepted/non-cancelled and current
actor/grant authority is valid. A valid re-pair/adoption follows document 35. It
cannot claim a new observation under the stopped epoch. Missing linkage/changed
inventory or missing consent fails; historical valid linkage does not fail merely
because recording is no longer active. Unregistered offline local bytes require
explicit manual B1 review/new intent; they cannot become registered B2 history
after the epoch stopped. Their original session claim remains unverified. Grant revoke, actor disable, explicit upload
cancel or removal fence still blocks finalizer commit. Server does not attest that
a client truthfully observed the claimed interval.

See documents 41–43 for dependency closure, resource/rollout and SYS verification.
