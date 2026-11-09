---
name: evidence-spec
description: Create Evidence Workspace implementation specifications or dependency-ordered plans from its concepts and current source, with explicit decisions and verification gates.
---

# Specify Evidence Workspace

Read AGENTS.md and the documents relevant to the requested scope. Use
`docs/05-next-design-phase.md` for the documentation brief and
`docs/reference/specification-template.md` for a starting structure.

Trace each requirement to concept sections, user decisions or source findings.
Separate prototype behavior, target recommendations and accepted ADRs. Preserve
stable IDs and record contradictions instead of silently choosing a new contract.
Do not import The OA's SaaS/AI scope.

Specify byte/provenance immutability versus editable editorial context, private/public
access, state transitions, partial results, retry/crash recovery and migrations
where relevant. WARC fidelity, capture-engine choice, durable queue, publication/cache
withdrawal and prototype-data migration need explicit decisions before dependent work.

Use observable acceptance cases, including denied access and recovery. A plan follows
specifications and dependencies; each stage needs real deliverables and evidence gates.
Mark unknown capacity/dates and unresolved choices. Use synthetic examples and do not
claim tests ran merely because they are specified.

Update Specification/version and Unreleased for changed documents; planned contracts
remain 0.0.0 until implemented. Implement runtime code only if the actual task includes it.
