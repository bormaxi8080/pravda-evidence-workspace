# Contributing

Read [AGENTS.md](AGENTS.md) and [engineering rules](docs/02-engineering-rules.md).
The repository contains a working-source prototype and a future production concept.
Neither source presence nor a package number is runtime verification.

## Change workflow

1. Inspect Git status, instructions, affected components and the matching MCP index.
2. Identify current behavior, requested outcome, compatibility and relevant evidence.
3. Complete the authorized change; maintain related docs and acceptance criteria.
4. Increment each affected component once and add a human-readable Unreleased entry.
5. Run `python3 scripts/validate_workspace.py --sync`, then required/targeted checks.
6. Review diffs, stage explicit paths and commit when authorized. Report the commit,
   checks, limitations and next unresolved decision.

Use short-lived `docs/...`, `feat/...`, `fix/...` or `chore/...` branches for normal
work. The requested initial foundation commit can use the current branch.
Do not overwrite unrelated changes, rewrite history or stage the entire workspace.

## Versions

Manifests are authoritative; [release/versions.json](release/versions.json) and
the bounded Unreleased inventory are derived. Run `--sync` after manifest edits;
it does not choose versions, run manifest commands, stage or commit.

- Patch: compatible correction, documentation or engineering iteration.
- Minor: new capability; for a pre-1.0 incompatible contract also record `BREAKING CHANGE`.
- Major: incompatible stable contract, with migration/deprecation guidance.
- Planned `0.0.0`: no implementation claim. Start at `0.1.0`, review dependencies,
  move ownership to actual files, and define executable verification.

The application manifest starts at inherited package version **1.1.0**, status
`prototype`. Do not silently reset it to 0.x. This number is separate from the
concept's target production 1.0 and the currently **null** Workspace product release.
An incompatible change to the existing 1.x package needs a major bump unless an
explicit migration/rebranding decision replaces that package contract.

Schema versions, migration IDs, design revisions, component versions and product
releases have different meanings. Bumping a version does not migrate any data.
Changing specifications normally increments Specification, not Application.
Updating only derived ledger/changelog bookkeeping does not force Governance to bump.

## Commits and releases

Paperclip task agents have standing operator authorization for local `main`
integration after whole-package acceptance and required combined-tree checks.
Resolve routine conflicts in the task branch and follow the serialized fast-forward
[integration procedure](docs/operations/paperclip-integration.md). Record the resulting
main commit in the task. Repeated merge permission requests are unnecessary once
those gates pass. Preserve the existing human review and final-verdict controls.

Use English `type(scope): imperative summary`; scope is a component ID or domain.
Types: `feat`, `fix`, `docs`, `refactor`, `test`, `build`, `ci`, `chore`, `perf`, `security`.
Explain compatibility and actual verification in the body when useful. Use `!`
and a `BREAKING CHANGE:` footer for incompatible public contracts.

Only an explicitly requested product release sets release/date, creates a tag or
publishes artifacts. The validator's `--allow-release-change` is for that operation.
Historical changelog sections are immutable; new releases prepend a dated snapshot.
A release requires source/artifact identities, component versions, migration range,
known limitations, integrity/security/recovery evidence and an upgrade plan.

## Required checks

Use Python 3.11+; the governance tools need only the standard library.

```bash
python3 scripts/validate_workspace.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
git diff --check
git diff --cached --check
```

The validator checks schemas, file ownership, dependency cycles, package versions,
derived records, version increments, release discipline and local documentation links.
It never executes command strings from manifests. `--base REF` changes the comparison
baseline for CI (a trusted branch/commit); default is `HEAD` for local edits.
Missing explicitly requested baselines fail. `--sync` preserves human changelog prose.

Follow [testing policy](docs/operations/testing.md) for runtime behavior. No runtime,
browser, API or database tests are claimed by these governance checks. Do not build
containers for documentation-only changes. Required runtime gates cannot pass on
empty/skipped suites or mock-only evidence for real database/browser guarantees.

## Platform evidence

Current changes target MAC-DEV under [document 56](docs/requirements/56-macos-development-and-linux-qualification.md).
Record host and guest architecture, actual local checks and explicit deferred-linux
obligations. Native Linux setup is not a dependency for local implementation.
Human acceptance and integration still gate task completion; production/platform
qualification and actual release remain separate.
