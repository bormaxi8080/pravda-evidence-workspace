# Project prompt starters

These are reusable task requests, not another policy source or product AI feature.
Read [AGENTS.md](../../AGENTS.md); project rules and actual user authorization apply.
Replace bracketed task inputs with the requested scope. Skills are under `.agents/skills/`.

## Orient or resume

```text
Use $evidence-orient for pravda-evidence-workspace. Read the project instructions,
vision, current-state review, versions and Unreleased. Verify the matching MCP
root/status. For [topic], identify current source behavior, target proposals,
contradictions, affected components and the next unresolved decision. Cite paths.
```

## Design a specification

```text
Use $evidence-spec to create/revise the implementation specification for [scope].
Ground requirements in the concepts and source review. Record decisions separately
from proposals. Include contracts, permissions, failure/recovery, migration limits,
acceptance scenarios and open questions. Update Specification and Unreleased.
```

## Derive the detailed plan

```text
Use $evidence-spec to derive a dependency-ordered implementation plan from [accepted
specifications]. For each stage give scope, prerequisites, artifacts, component
impact, compatibility/migrations, verification and completion gates. Surface missing
decisions before committing to dates. Do not implement runtime code in this task.
```

## Implement a bounded stage

```text
Implement [stage] from [accepted specification]. Read applicable instructions and
use $evidence-deliver. Preserve evidence/privacy invariants, add behavior-focused
checks, update docs and affected versions, validate and report actual evidence.
Follow the user's existing commit authorization; do not infer a release or push.
```

## Review before delivery

```text
Use $evidence-deliver to review [diff or stage] for requirement coverage, source
truth, permissions, evidence integrity, recovery, compatibility and version/changelog
consistency. Run applicable checks, report concrete findings with paths and state
what remains unverified. Do not rewrite unrelated work.
```

## Current platform instruction

Use MAC-DEV and [document 56](../requirements/56-macos-development-and-linux-qualification.md)
for current tickets. Implement/test on this Mac; preserve real local evidence and
move native-target-only qualification to the linked Linux iteration. A missing
local dependency/access path needs a concrete Mac bootstrap handoff, not a request
for a Linux machine. Human review, upstream integration and release boundaries remain.
