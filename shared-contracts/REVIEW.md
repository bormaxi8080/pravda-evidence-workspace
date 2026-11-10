# LOC-4 / EWP-02: inventory slice review

Source baseline: `f8b328cf0b287f1e15ea53a51582d56bc33b0fcb` (design revision 0.10).
Branch: `chore/LOC-4-workspace`. Dedicated worktree: the LOC-4 execution workspace.
Deliverables: [contract and limits](README.md), [manifest schema](schemas/workspace-capture-v0-1.schema.json),
[fixtures and fingerprints](fixtures/identity.json), [verifier](validate.py),
[behavior checks](tests/test_inventory.py). Evidence Contracts is 0.1.0 development;
Governance is 0.1.3 for explicit planned-component test fixtures.

## Validation evidence

Environment: Darwin arm64, Python 3.12.10, standard library only. No container,
browser, database, external API runtime, image or investigation data was used.
Fixture version/seed: 1 / `loc4-inventory-1`; grammar-only synthetic bytes with
SHA-256 identities recorded in fixtures/identity.json and complete.manifest.json.

Commands and observed outcomes:

```text
python3 scripts/validate_workspace.py --sync
PASS: derived ledger and Unreleased inventory synchronized
python3 scripts/validate_workspace.py
PASS: ownership/dependency/version/docs/governance checks
python3 -m unittest discover -s tests -p 'test_*.py' -v
PASS: 36 tests
python3 -m unittest discover -s shared-contracts/tests -p 'test_*.py' -v
PASS: 6 tests with positive and adversarial subcases
git diff --check
PASS
```

The first governance run failed 5 of 36 tests because planned-state checks used
the live Evidence Contracts manifest. Explicit synthetic planned fixtures fixed
those failures without changing validator behavior. The subsequent run passed.
Independent Draft 2020-12 validation was unavailable: system Python lacked
`jsonschema`; pip installation of 4.23.0 in a disposable /private/tmp virtualenv
was denied by the sandbox PyPI network allowlist. No access change was attempted.

## Coverage and limits

Covered: exact complete inventory, unknown profile/version, omitted required output,
missing member bytes, same-size byte tampering, size mismatch, self-hash exclusion,
manifest reference digest changes, ordering/duplicate/path/unknown-field rejection,
positive integer and string bounds, canonical byte/null semantics and schema identity.
Partial/failed acquisition result contracts are outside this complete-inventory slice.
The local schema evaluator covers only the checked-in vocabulary and is not an
independent full JSON Schema engine. Full decoder/filesystem/isolation/authorization,
recovery and selected Linux x86_64 qualification are untested and not claimed.

Compatibility/recovery: no runtime consumers, production data, migration or historical
capture relabeling. Product release/date remain null. Unknown versions fail closed.
Future producers must not adopt this profile until its bounds and schema are accepted.
No push, merge, release, deployment or upstream integration is included.

Next action: human review of this admitted slice, including proposed 64 KiB manifest
and warning limits. Acceptance allows continuation with remaining core metadata,
export/legacy, engine request/result/job/events and API DTO/OpenAPI contracts.
The whole EWP remains open until all deliverables, acceptance and integration gates
are satisfied. A passing inventory check does not qualify browser capture integrity.

## Delivery restriction

Staging explicit paths failed: Git could not create the worktree's `index.lock`
(`Operation not permitted`). No commit was created. The staged whitespace command
returned no errors, but there was no staged change to review; it is not staged
content verification. Changes remain in the authorized worktree and review bundle.
The operator must restore ordinary Git index write access in this managed worktree
before the reviewed changes can be staged and committed. No permission bypass or
alternate Git index was attempted.
