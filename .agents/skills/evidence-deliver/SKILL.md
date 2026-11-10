---
name: evidence-deliver
description: Prepare or review an Evidence Workspace change for delivery with component ownership, version and changelog consistency, relevant checks and truthful verification evidence.
---

# Deliver an Evidence Workspace change

Read AGENTS.md, CONTRIBUTING.md and affected manifests. Identify the change's
observable outcome and consumer/migration impact. Preserve unrelated user work.

Increment each affected existing component once per coherent change. Keep inherited
application package versions aligned; requirement edits do not bump runtime by
association. Preserve null product release/date for routine changes. Add a meaningful
Unreleased entry, then run `python3 scripts/validate_workspace.py --sync`.

Run required governance checks and behavior-specific evidence from
`docs/operations/testing.md`. Metadata/schema success is not runtime security,
browser, OAuth, queue or restore proof. Report unavailable checks and remaining risks.

Inspect the diff and explicit staged paths, then run `git diff --cached --check`.
Commit only within actual task/session authorization. A commit grants no push,
tagging, publishing or deployment authority. Refresh/check the matching MCP index
after changes and keep graph/runtime artifacts ignored.

Return what changed, actual check results, limitations and commit identity if created.


For current work record MAC-DEV host/guest identities and required local results.
Use `docs/requirements/56-macos-development-and-linux-qualification.md` to separate
native Linux obligations. Accepted/integrated Mac implementation can close its lane
ticket without claiming production or Linux qualification; skipped local gates cannot.
