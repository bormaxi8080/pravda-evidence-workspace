# Evidence Contracts

Component: Evidence Contracts 0.1.0 (development). Catalogue: CTR-01 / EWP-02.
Authority: [evidence contract](../docs/requirements/15-evidence-and-publication-contracts.md)
and [catalogue](../docs/requirements/43-contract-catalog-and-delivery-gates.md).
See [current implementation coverage and review limits](CURRENT.md). The original
inventory slice below was accepted separately; EWP-02 acceptance remains pending.

The authoritative [JSON Schema](schemas/workspace-capture-v0-1.schema.json) freezes
`workspace-capture-v0/1` complete manifest shape. Producer: future trusted capture
finalizer; consumers: future integrity checker/exporter/import reader. No runtime
consumer is connected. The schema fingerprint is in [fixture identity](fixtures/identity.json).
No secondary DTO or OpenAPI representation is maintained for this slice.

Required package: `evidence/page.mhtml`, `evidence/screenshot.png`,
`metadata/capture.json`, `manifest.json`. The three manifest entries occur in
ASCII path order with exact path/kind/MIME, positive size and lowercase SHA-256.
The manifest excludes itself. Its exact size/hash is returned separately for a
future database record; the fixture identity demonstrates that external reference.
No checksum file belongs to this capture profile. WARC is explicitly deferred;
PDF is outside the capture inventory. Unknown profiles/versions/fields are denied;
there is no fallback, invented output or implicit conversion of old evidence.
Changes to required inventory require a new profile version and reviewed adapters.

JSON bytes are UTF-8 without BOM, sorted Unicode codepoint keys, compact separators
and exactly one LF. Duplicate keys, floats, NaN/infinity and invalid Unicode are
rejected. Original string normalization is forbidden. Missing required fields fail;
null is never a replacement for a required ID/hash/output. Canonical JSON supports
explicit null for unknown legacy metadata, with provenance notes, as the synthetic
metadata example shows. Detailed provenance/metadata DTOs remain for the next slice;
this inventory verifier checks metadata canonical bytes, not its domain completeness.
Warnings are bounded to 64 strings of 1–1024 characters. The review-slice manifest
cap is 64 KiB; selected artifact/attempt caps are 100/250 MiB. These new field bounds
are proposed contract detail for acceptance before any producer adoption.

Run with Python 3.11+ and the standard library:

```bash
python3 -m unittest discover -s shared-contracts/tests -p 'test_*.py' -v
```

`validate.py` evaluates only the schema vocabulary used here and rejects unknown
keywords. It is not a general JSON Schema validator. Independent full Draft 2020-12
validation is unavailable in this environment: `jsonschema` is absent and installing
4.23.0 was blocked by the sandbox's PyPI network allowlist. No dependency was added.

Fixtures are tiny synthetic grammar samples encoded in `members.json`, not live
captures. Their positive and negative manifests are committed as actual canonical
JSON. Tests cover exact inventory, missing files, digest/size tampering, self-hash
exclusion, path/order/duplicate/unknown-field rejection, byte encoding and bounds.
The verifier accepts an in-memory name-to-bytes mapping and never opens those names.
It does not validate PNG/MHTML decoding, hostile filesystem objects, authorization,
network/browser isolation or capture fidelity. Real controlled-browser output and
trusted finalizer checks remain separate mandatory runtime gates.

The remaining profile, engine/job/event and API DTO/OpenAPI contracts are now
materialized; see CURRENT.md for coverage, proposed details and qualification limits.
Whole-package acceptance and integration are required before closing EWP-02.

## Engine continuation after inventory acceptance

The inventory slice was accepted through LOC-4's human review card on 2026-11-10.
Its manifest schema and existing fixture identities remain unchanged.

CTR-02 now includes `capture-engine/1` request/result definitions in
[build_engine.py](build_engine.py), generated [request schema](schemas/capture-engine-1-request.schema.json)
and [result schema](schemas/capture-engine-1-result.schema.json), and
[synthetic examples/fingerprints](fixtures/engine/identity.json).
`python3 shared-contracts/build_engine.py --check` checks deterministic generation.
The Python definitions are the single authority for these generated representations.
[engine.py](engine.py) additionally checks cross-field and request/result relationships.
Future producers: controller/isolated runner; consumers: controller/trusted finalizer.
No runtime consumer is connected. Unknown versions are rejected without fallback;
new incompatible wire shapes require a new contract version and reviewed adapters.

Requests pin IDs/generation, opaque job-only authorization, deadline, exact URL,
condition/options, caps, temporary namespace and network policy. Locale/timezone
are explicit effective values, not inferred defaults. Results retain status and
filtered headers, actual options, timestamps, errors and output digest hints.
A complete HTTP error response is allowed; eligibility remains a separate policy.
Complete requires both PNG/MHTML output descriptors and satisfied readiness.
Partial requires an output and an error; failed cannot claim retained output;
cancelled is distinct. Final metadata/manifest are trusted-finalizer outputs,
not runner output descriptors. Digest hints never establish accepted integrity.

Additional proposed bounds: engine message 256 KiB, redirect inventory 32,
engine/browser version 128 characters, four allowlisted response-header values
4,096 characters each; omitted allowlisted values are explicit null. URL syntax
checks enforce credentials/default ports and UTF-8 byte bounds, but do not resolve
DNS or establish public-address policy. Namespace syntax grants no filesystem
access. Host launcher authorization, current DB lease, clock/deadline authority,
network policy enforcement, descriptor decoding and finalizer validation remain
runtime gates. Additional core contracts and their current limits are in CURRENT.md.
