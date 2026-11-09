# Engineering baseline verification

Date: 2026-11-09. Environment: local checkout, Python 3.12.10. This record covers
development governance and MCP functionality; no deployment or product release.

| Check | Observed result |
| --- | --- |
| `python3 scripts/validate_workspace.py --sync` | Pass; derived ledger/inventory synchronized |
| `python3 scripts/validate_workspace.py` | Pass; schemas, ownership, dependencies, package version and bookkeeping |
| `python3 -m unittest discover -s tests -p 'test_*.py' -v` | 36 passing tests, including disposable Git baseline/commit comparisons and negative cases |
| `python3 scripts/check_docs.py` | Local Markdown links, fences, language/whitespace and project skill metadata pass |
| Skill Creator `scripts/quick_validate.py` on each local skill | All three valid |
| `python3 -m compileall -q provereno-ui/provereno scripts tests` | Python syntax passes; imports/startup are not exercised |
| `git diff --check` and staged diff check | Pass before commit |
| Codebase Memory | Three independent full indexes ready; real symbol/source retrieval, main enqueue callers and cited-path coverage checked |

Regression cases include invalid manifests, ownership overlap/gaps/transfers,
dependency cycles, planned-state violations, package drift, missing version/changelog
updates, stale derived records, historical edits, release/date discipline, invalid
Git baseline, malformed skill metadata and broken local links. Synchronization is
tested for determinism and preservation of human text/project metadata.

Runtime capture, PostgreSQL execution/locking, OAuth, browser UI/isolation, real API
requests, packaging/container builds, migrations and backup/restore were **not run**.
No pre-existing runtime suite was present. The added CI workflow has been reviewed
locally but not executed on GitHub. Runtime findings remain in
[current-state review](../04-current-state.md); MCP parser limits remain in
[the MCP runbook](codebase-memory-mcp.md).
