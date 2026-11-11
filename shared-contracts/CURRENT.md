# EWP-02 implementation review

Status: proposed machine-readable core contracts; whole-package human acceptance
and integration pending. Source baseline f8b328cf0b287f1e15ea53a51582d56bc33b0fcb,
design revision 0.10. The first capture inventory slice was accepted separately
on 2026-11-10. Its schema and original fixture identities remain unchanged.

## Authority and coverage

| Catalogue | Authority | Producer / consumers | Materialized coverage |
| --- | --- | --- | --- |
| CTR-01 | Accepted capture schema; build_core.py | Trusted finalizer / verifier, export, migration | Complete V0 capture metadata, capture inventory, export options/manifest, legacy unknown provenance |
| CTR-02 | build_engine.py; build_core.py | Controller, runner, job service / finalizer, status, SSE | Engine request/result; job, attempt and safe durable event DTOs |
| CTR-03 | build_api.py | Future cookie API / SSR services, generated documentation | Core capture/editorial/triage/review/retry, jobs, CSV preview/batch, collections/tags, publication/revocation, exports, archive, audit, status and user operations |

Generated representations: schemas/, openapi/core-commands.openapi.json and
synthetic fixtures. Their definitions are generated from the Python authorities;
no independent hand-maintained DTO/OpenAPI field definitions exist.
contract-index.json records corpus fingerprints. Build scripts support --check.
New unknown versions/fields fail closed; incompatible shapes need explicit new
versions and reviewed adapters, never relabeling historical evidence.

Pure validation modules perform additional invariants that JSON shape alone cannot
establish. core.py checks temporal order, disclosure flags, legacy notes, retry/
terminal semantics, exact export inventory, capture identity, trusted metadata links,
manifest self-exclusion and SHA256SUMS coverage of both manifests. It checks every
required member rather than trusting a caller-supplied subset. Inputs are bounded
in-memory mappings; no supplied filename is opened or interpreted as instructions.
The two base64 export fixtures preserve original capture byte identities inside
both default and PDF-selected synthetic packages. Their tiny PDF/MHTML/PNG grammar
samples do not prove format decoding, rendering or browser capture fidelity.

api.py accepts ordinary UTF-8 JSON with duplicate/type checks and rejects unknown
fields. Evidence profile and engine messages use the documented canonical bytes.
Request defaults: load condition, export false inclusions, list limit 25. Explicit
export wire booleans pin the effective selection. Publication fields, metadata
headers and diagnostic fields are closed allowlists. Unknown legacy times/actors
stay null with notes; legacy records cannot claim local complete/publication status.
SSE data uses JobEvent, with transport ID job_uuid:sequence; reset requires fetching
the authoritative job snapshot. This component does not implement transport replay.

## Proposed details requiring whole-package review

New wire field names and DTO versions, cookie name workspace_session, error field
allowlist, explicit export flags, 1 MiB DTO cap, export array cap 12, metadata/engine
header/redirect limits, namespace syntax, legacy inventory bound 3, viewport/ID/
revision bounds, list/collection bounds and safe status projection are implementation
choices for review before any runtime producer adoption. They are not new accepted
architecture decisions. The selected design authorities remain documents 13–17/43.
Public viewer/OAuth protocol/SSR route implementations and future companion,
production recording, C/H/U contracts remain owned by their separate packages.

API schemas describe permission and CSRF/idempotency requirements; they do not
implement current access decisions. envelope() is an executable error example over
trusted middleware facts, not an authorization service. Stale revisions, role,
resource ownership, idempotency replay/conflict, current lease/fences and database
transaction races need service/runtime tests. No passing schema example proves them.

## Verification and limits

Run the component checks listed in components/evidence-contracts/component.json.
Fixture identities: loc4-inventory-1, loc4-engine-1, loc4-core-1, synthetic grammar only.
The standard-library schema evaluator covers the checked-in vocabulary only.
Independent full JSON Schema/OpenAPI validation is unavailable (jsonschema absent;
the earlier installation attempt was denied by the PyPI sandbox allowlist).
No install or external access change was attempted on continuation.

No live DB, browser, hostile decoder, ZIP extraction, receipt renderer, network,
OAuth provider, recovery or selected Linux x86_64 qualification ran. Current evidence
is Darwin arm64/Python 3.12.10, with no runtime consumer/dependency, real data,
migration, product release, push, merge or deployment. Publication remains explicit;
archived active content is data. Product release/date remain null.
The earlier Git permission failure is preserved in REVIEW.md as historical failed
evidence. Ordinary explicit staging succeeded after the operator repair.

Next action: whole-package contract review, resolve proposed wire details, then
integrate through the agreed base. EWP-02 cannot be closed before acceptance and
integration. Runtime consumers must pass their own authorization, integrity,
filesystem, isolation and recovery gates.
