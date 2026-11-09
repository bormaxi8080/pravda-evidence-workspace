# ADR-010: Specify production preservation and protected byte delivery

Date: 2026-11-09. Status: **selected contract/refinement; implementation unverified**.
Authority: user requested continued specification development. Sources: REQ-EVD-001–008,
ADR-003/008/009 and [primary review](../reference/preservation-rendering-and-replay-review.md).

## Decision

Select workspace-capture-production/1 with same-attempt PNG/MHTML/HTTP WARC plus
capture/recording metadata and manifest. Select workspace-export-production/1 with
the exact capture set, separate export metadata/manifest, HTML and required PDF
receipt, checksums and verification guide. Old V0/browser/foreign packages never
gain a production label from app upgrade or generated wrappers.

WARC scope is the recorded HTTP representation of one anonymous public navigation
under explicit policy/deadline, not packet/TLS history, all future page activity or
universal replay. Record collector observation layer, transformed header/body rules,
omissions and incomplete exchanges. Main navigation/redirect coverage is mandatory;
unknown or lost required response bytes fail/partial the requested profile.

Introduce strict capture-engine/2 recording negotiation and validated WARC output.
First qualify recorder-backed existing Playwright integration; a pinned Browsertrix
adapter is an alternative candidate only. Do not select a runtime provider based
on documentation alone. EWP-73 records the actual qualified choice or explicitly
blocks production; no silent second capture/engine/profile fallback is permitted.

Render receipt PDFs from controlled escaped data and approved bounded local assets
inside an offline isolated process. Production export requires PDF; V0 optional
behavior remains explicit. Independent verification separates container/inventory/
digest consistency from provenance, replay quality and legal/time assertions.

Select a protected read plane that verifies bytes before success headers, accounts
snapshot/stream resources globally and rechecks authority/fences. Large preverified
spools are not unbounded web work. Slow readers hold transfer/spool capacity, not
the heavy compute permit; cancellation/expiry releases only their own resources.

## Scope and consequences

Documents 50–53 refine the existing 170 requirement IDs and add EWP-73–78 and
PRD-ACC-01–08: 78 tasks, 76 scenarios. V0 remains 70 requirements; its byte-serving
subset is the implementation of existing integrity/access requirements. Actual WARC,
required PDF and replay stay production gates, not hidden V0 requirements. U/C/H/B
features remain optional later branches and do not delay baseline production.

Only Specification advances. No runtime schema/component/dependency, capture,
PDF, replay service, deployment or release is created. Production provider/resource/
interoperability/security qualification remains pending. Empirical failure reopens
the recorder choice without waiving the preservation contract.
