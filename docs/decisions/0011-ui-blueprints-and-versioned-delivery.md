# ADR-011: Adopt UI blueprints and a versioned delivery decomposition

Date: 2026-11-09. Status: **selected design and work decomposition; runtime unverified**.
Authority: user requested UI mockups for Workspace/browser companion, then a detailed
implementation plan separated by versions and grounded in existing specifications.

## Decision

Maintain reviewable local HTML/CSS/JavaScript blueprints under `design/`, separately
from the original root mockup and runtime application. Use local synthetic assets,
English copy, visible simulation labels and no remote dependencies or live data.
The UI Prototype component owns these files. The Browser Extension remains planned:
a simulated extension frame is not an installed MV3 implementation.

Select the visual/state/interaction direction in
[document 54](../requirements/54-ui-blueprints-and-interaction-map.md). Keep evidence,
editorial revision, approval, importance, personal attention and disclosure visibly
independent. Distinguish server and browser acquisition, local versus accepted
bytes, human pairing approval and explicit upload/session consent. Permissions and
profile eligibility remain server contracts, not UI-only decisions.

Adopt [document 55](../requirements/55-versioned-implementation-plan.md) as the detailed
execution decomposition of the existing 78 EWP tasks. Each has one primary milestone;
EWP-51 has independently qualified adapter subgates. F0/E0/P0 lead to a controlled
V0 pilot; R1/G1 qualify mandatory production preservation. D1–D6 package later
C/H/B/U work. Optional branches retain existing post-V0 prerequisites and may be
engineered alongside production qualification. No optional stage blocks G1.

Future product numbers in the plan are proposed packaging coordinates, not releases.
Component versions/profile versions remain independent; release/date remain null.
No calendar, individual assignment, provider choice or supported host capacity is
invented. Existing requirement/task/scenario authorities remain unchanged: 170
requirements, 78 work items and 76 runtime acceptance definitions.

## Alternatives and consequences

A hosted design service or new frontend runtime would add tooling/deployment work
before review; a self-contained local prototype can be inspected offline and
versioned alongside its contracts. Static images alone would not expose consent,
revision or recovery transitions; the connected synthetic flows make those reviewable.
Screenshots accompany the interactive source, not replace it.

The existing HTML is retained as historical concept input. New UI assets do not
activate runtime features or planned components. Detailed later forms/real browser
APIs, server authorization, accessibility qualification and every runtime evidence
gate still belong to their owning EWP implementation. A visual design mismatch
cannot silently change accepted security/evidence contracts.

## Platform sequencing amendment — 2026-11-10

[ADR-012](0012-macos-development-and-linux-qualification.md) supersedes Linux-first
implementation scheduling. Mac local implementation/acceptance and later native
Linux qualification have separate gates in document 56. Other technical/product
invariants and the original requirement/task/scenario identities remain unchanged.
