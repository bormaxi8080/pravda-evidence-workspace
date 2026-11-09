# ADR-003: Select evidence profiles and publication projections

Date: 2026-11-09. Status: **selected engineering baseline; implementation unverified**.
Scope authority: continued documentation/design work. Covers DEC-04/05/12 for V0;
production WARC fidelity and service objectives remain qualification/design work.

## Decision

Select `workspace-capture-v0/1`: required PNG, MHTML and capture metadata JSON,
an immutable capture manifest and SHA-256 references. Export uses a separate
`workspace-export-v0/1` inventory with HTML receipt, export metadata, the original
capture inventory and SHA256SUMS. PDF is optional through an explicit profile
option; missing required output fails rather than silently downgrading the profile.
No production-WARC claim may be attached to historical V0 bytes.

Manifest serialization, inventory boundaries, limits and failure behavior are
defined in document 15. Manifests never contain their own digest; export-time
editorial/probe/receipt data never rewrites the capture manifest.

Publication requires complete/integrity-valid evidence plus an approved editorial
revision and explicit admin action. Pin the screenshot and allowlisted metadata.
V0 does not publicly serve MHTML, private manifests, exports, notes, raw headers or
internal usernames. Unsafe screenshot/URL disclosure means keep private; redacting
original evidence bytes is not an authorized shortcut.

Serve publication assets only through active publication authorization, with
no-store and no direct evidence-directory proxy access. Revoked slugs stay revoked;
republishing creates a new slug. Already copied content cannot be recalled.

## Alternatives and consequences

A mutable public boolean cannot capture reviewed projection/history/revocation.
Public export of full private metadata risks disclosure and is excluded from V0.
Adding receipts to the original manifest would confuse capture/export times and
create hash cycles if self-digests were included. Keep the two inventories separate.

WARC is still mandatory before production release, with its fidelity/replay contract
specified in EWP-17. Production PDF and measured operational objectives are separate
gates. The selected V0 profile does not claim legal authenticity or trusted time.

## Verification obligations

ACC-01/04/05/06/07/09/10 must prove completeness, immutable originals, transactional
review/publication, byte tampering detection, proxy withdrawal and clean recovery.
No such runtime result is claimed by this decision record.
