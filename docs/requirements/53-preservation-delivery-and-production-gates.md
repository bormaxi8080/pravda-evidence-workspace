# Preservation delivery, verification and production gates

Date: 2026-11-09. Status: **selected implementation plan; no runtime task completed**.
Owner: evidence/capture/rendering/security/operator. Authority: ADR-010.
Documents 50–52 refine the existing 170 requirements: 70 V0 / 100 later. This pass
adds six tasks and eight integration scenarios, bringing totals to 78/76. No new
product requirement, production release, working recorder or public replay is implied.

## Stage and transition rules

| State/input | Selected behavior |
| --- | --- |
| V0 deployment | Existing PNG/MHTML profile and optional PDF; protected byte delivery still required by existing integrity/access contracts |
| Production recording candidate | Qualification-only controlled fixtures and strict engine/2 contract; no production claim before all evidence gates |
| Qualified production mode | Default new server intent requires the production profile/WARC, complete export requires safe PDF; no automatic fallback to prototype |
| Existing complete/partial V0, client or imported capture | Keep immutable profile/bytes/unknowns; no wrapper, new PDF or app version upgrades its historical fidelity |
| Queued old intent during mode transition | Retain its pinned profile/default snapshot; hold/cancel or explicitly process under supported legacy policy, never silently recapture/upgrade it |
| Unsupported reader/client/optional adapter | Fail or explicitly disable affected capability; original archive remains private under its supported profile, no hidden compatibility bypass |

Switching the default is an operator-reviewed config/schema/client compatibility
operation after migration/rehearsal; completed records and idempotent replay retain
their original profile. An old browser companion/client must display the actual
selected server profile or fail negotiation before submission. Public raw WARC/
PDF/package serving is not added; existing screenshot publication rules remain.

## Assignable tasks

| Ticket | Dependencies / owner | Bounded deliverable | Completion evidence |
| --- | --- | --- | --- |
| EWP-73 Recorder/fidelity feasibility | EWP-16/62; capture/evidence/security | Controlled same-attempt recording spike, existing-engine-first evaluation, explicit observation/header/coverage policy, pinned candidate comparison and provider disposition | PRD-ACC-01/02/04; real browser/recording/egress/resource and MHTML/PNG correlation evidence, or production blocked |
| EWP-74 Production profile/engine/verifier contracts | EWP-73/02/53; evidence/API | Actual production capture/export and engine/2 schemas, WARC association/byte/inventory checks, structured verifier errors and negative fixtures | PRD-ACC-01/03/08; exact profile/version/self-hash/parser/digest cases, no historical relabel |
| EWP-75 Recording adapter and replay qualification | EWP-74/08/62; capture/deployment | One qualified recorder-backed engine, bounded recording/validation/finalization, offline independent replay test harness and capability descriptors | PRD-ACC-01–04/08; real same-attempt/timeout/truncation/SSRF/reader proof, no source fallback or unqualified dual provider |
| EWP-76 Safe receipt PDF and production export | EWP-13/61; evidence/rendering/security | Controlled ReceiptModel/template/font assets, isolated renderer/PDF validator, required-output inventory and independent package verifier | PRD-ACC-03/05/06/08; filesystem/URL/attachment/CPU/memory/layout/Unicode/required-PDF failures and real exported bytes |
| EWP-77 Protected read/snapshot authority | EWP-06/54/55; application/security | Shared pre-header integrity snapshot, owned read reservations/transfer leases, root/permission/revoke checks and safe whole-file/proxy behavior | PRD-ACC-07 plus ACC/SYS access/removal; real file substitution, slow clients, lease/deadline, no heavy-slot deadlock |
| EWP-78 Production format/recovery dossier | EWP-68/75/76/77; evidence/operator | Versioned producer/independent-reader fixture results, profile-mode migration, exact export verification and clean restore/replay/PDF/resource evidence | Applicable PRD-ACC-01–08 plus ACC-12 and existing OPS/SYS gates; source/artifact/fixture identities, actual support scope/limitations |

EWP-77 is the actual-core read-contract refinement before EWP-12/13; it knows only
implemented V0 profiles until later adapters qualify. It does not depend on WARC,
PDF or EWP-73–76. EWP-17 uses EWP-75/76/78 for its already required production
format delta while retaining availability/automated-operations work. EWP-78 never
depends on EWP-17/18, so production gates remain acyclic. C/H/B/U completion is
not a prerequisite of V0 or baseline production.

## Controlled fixture corpus

Use deterministic synthetic request graphs and captured byte expectations: redirect
to HTML with CSS/font/image; repeated URL/query order; binary and encoded response;
HTTP error; blocked private subresource; cached/service-worker/opaque disposition;
streaming/connection loss; huge/invalid/truncated archive; long/RTL/Unicode receipt;
mutation/revoke during file snapshot/transfer. Keep control-server observations
separate from recorder claims, enabling detection of missing/changed exchange bytes.

No live newsroom account/page/secret is a fixture. Store small expected examples in
the future owning test component and retain large actual artifacts only in controlled
evidence storage outside Git/MCP. Capture profile IDs/intervals/record IDs/transform
policy/fixture version and exact tools/host/network conditions in each result.

### PRD-ACC-01 Same-attempt WARC and scope

Record a controlled main/redirect/resource graph, PNG and MHTML with one attempt/
generation/provider. Compare fixture server observations to declared recording
inventory, headers/body transforms and boundary. A later refetch, MHTML wrapper,
opaque container rename or missing required exchange cannot qualify production.
Record actual scope/exclusions rather than universal traffic/replay claims.

### PRD-ACC-02 Deadline, omissions and failure semantics

Exercise navigation timeout, recorded boundary, blocked/unsupported protocol,
in-flight streaming, lost main body, truncated resource and provider crash. Declared
pre-capture policy cannot be rewritten afterward to hide failure. Required lost/
unknown bytes are non-complete; known exclusions are visible. Aggregate 120s and
artifact/record limits hold; no second capture/engine fallback fabricates success.

### PRD-ACC-03 Structural and independent package verification

Tamper lengths/member paths/record IDs/digests, duplicate required members, omit
PDF/WARC, add undeclared output and expand nested compression beyond caps. Reject
empty checksum success and unknown profiles. Independently verify actual exported
original bytes and exact capture/export inventories outside Workspace, without
network or session. Structural consistency does not assert time/authorship/truth.

### PRD-ACC-04 Offline replay and recorder isolation

Replay one verified package with an independently pinned reader in an isolated
origin/browser with external/live/archive fallback disabled. Controlled resource
misses remain visible, not filled by today's site. Compare expected content/
resource assertions under recorded replay conditions; screenshot similarity alone
cannot pass. Test recorder/replayer cannot reach app credentials, DB, host or another
scope. Replay never becomes an active HTML viewer in the app origin.

### PRD-ACC-05 Renderer containment and output safety

Use malicious-looking source strings, CSS/HTML/URI/file/SVG/attachment attempts,
oversize values and long layout. Only escaped typed content/fixed templates and
declared assets resolve. Real offline non-root process limits/kill and no-network/
filesystem-secret checks hold. A custom fetcher or syntactic PDF prefix alone cannot
pass. Validate page/output limits and the no-active-action/attachment contract.

### PRD-ACC-06 Required PDF and readable receipt

V0 optional-disabled, V0 explicitly PDF-required and production export produce their
declared success/failure, never silent omission. Render/inspect fixture pages with
Unicode/RTL, long URLs/digests and page breaks; exact required fields and warnings
are readable without clipped/missing content. PDF export time/hash is distinct from
capture time/original digests; no self-hash loop, PDF/A/signature or legal claim.

### PRD-ACC-07 Protected read correctness and shared capacity

Change file/path/bytes during validation; revoke publication/scope/principal or
remove a root before headers and during streaming; stall/disconnect multiple clients.
No invalid pre-header success, unauthorized HEAD/conditional/range bypass, direct
proxy alias or mutable-path switch. Bound read snapshots/transfers/temp and release
compute before slow clients; no sole-heavy-permit deadlock. Record started-transfer
partial-byte limits honestly. This applies to actual V0 reads without requiring WARC.

### PRD-ACC-08 Profile migration, recovery and truthful readiness

Switch production default with old queued/completed V0/browser/foreign records and
unsupported readers/clients. Preserve original profiles and pinned idempotent intent.
Restore accepted WARC/PDF manifests/dependencies with newer removal ledger, validate
exact bytes and prove no automatic replay/recapture/publication. Effective production
readiness requires actual qualified recorder/renderer/parser/environment scope,
not a document, version bump or unrelated green metadata check.

## Refinement coverage and release evidence

| Existing requirement IDs | Detailed contract | Planned scenarios |
| --- | --- | --- |
| REQ-EVD-001, REQ-EVD-002, REQ-EVD-007, REQ-ARC-003, REQ-SCP-003 | 50 acquisition/profile/scope | PRD-ACC-01, PRD-ACC-02, PRD-ACC-04, PRD-ACC-08 |
| REQ-EVD-003, REQ-EVD-005, REQ-EVD-006, REQ-EVD-008, REQ-SEC-007 | 51 receipts/export/verifier | PRD-ACC-03, PRD-ACC-05, PRD-ACC-06, PRD-ACC-08 |
| REQ-ARC-005, REQ-ARC-006, REQ-EVD-004, REQ-SEC-002, REQ-SEC-006, REQ-API-005, REQ-EXT-003 | 52 protected read/resource authority | PRD-ACC-07, PRD-ACC-08 |
| REQ-OPS-004, REQ-OPS-005, REQ-OPS-008, REQ-EXT-005 | 53 compatibility/restore/handoff | PRD-ACC-03, PRD-ACC-04, PRD-ACC-08 |

Complete 170-ID coverage stays in 10/26/33/38/49; this matrix refines existing IDs
only. Add CTR-17 production capture/export/engine/2/recording schemas, CTR-18 safe
ReceiptModel/PDF/verifier result, and CTR-19 ReadSnapshot/TransferLease to the future
catalogue. Materialize exact versions/examples before their producers; no empty
schema file or new planned-component activation is created by this prose.

Each gate records source/binary/profile/schema/policy/fixture hashes, exact command/
environment/times/outcome, independent tool identity, safe failure references and
limits. Record actual provider selection or the unresolved feasibility blocker.
Required tests cannot pass by empty/skipped/mocked-only evidence. The existing 36
governance tests establish neither recording fidelity nor safe rendering/recovery.
Release/tag/store/deployment remain separate authorized operations after mandatory
format/security/operations/pilot conditions, with no invented reviewer sign-off.
