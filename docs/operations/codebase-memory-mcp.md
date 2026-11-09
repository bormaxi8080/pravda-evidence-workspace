# Codebase Memory MCP operations

Status: **registered, fully indexed and smoke-tested on 2026-11-09** using the
available `codebase_memory_mcp` server. No server installation or global client
configuration change was needed. This index is development tooling, not evidence
storage, a production service or a runtime dependency.

## Independent project identity

| Checkout directory | Exact MCP project ID |
| --- | --- |
| `pravda-evidence-workspace` | `pravda-evidence-workspace` |
| `Locus-Geolocation-App-provereno` | `Volumes-Transcend-workspace-projects-osint-provereno-Locus-Geolocation-App-provereno` |
| `provereno-OSINT-for-countries-V2.0` | `provereno-OSINT-for-countries-V2.0` |

The existing Locus ID was retained to avoid duplicate indexes. Each root is its
own Git checkout under the enclosing `provereno` directory. No combined root or
cross-repository intelligence links were indexed. The active project for further
work is **pravda-evidence-workspace**.

## Reproduce registration and checks

Resolve the absolute root with `git rev-parse --show-toplevel`. Call tools on the
available server, supplying actual paths rather than hardcoded developer paths:

```text
list_projects(format="json")
# Match root_path before reusing an ID.
index_repository(repo_path=<absolute-root>, name=<matching-ID>, mode="full", persistence=true)
index_status(project=<matching-ID>, diagnostics="full", format="json")
search_graph(project=<matching-ID>, name_pattern="^enqueue$", format="json")
get_code_snippet(project=<matching-ID>, qualified_name=<discovered-qn>)
trace_path(project=<matching-ID>, function_name=<discovered-qn>, direction="inbound", depth=1)
check_index_coverage(project=<matching-ID>, paths=[<cited-repository-relative-paths>])
```

The example symbol is specific to Evidence Workspace. Persistent archives are local
`.codebase-memory/graph.db.zst`, ignored by Git. They can be regenerated from source;
do not commit them. Auto-refresh may occur, but verify freshness after edits/commits.
These operations do not install or guarantee a separate filesystem watcher.

## Observed baseline verification

Initial source-only counts (before governance additions; later refreshes will differ):

| Project | Nodes / edges | Real retrieval and exact-path coverage |
| --- | --- | --- |
| Evidence Workspace | 562 / 1250 | `jobs.enqueue` source retrieved; inbound callers `create_job` and `bulk_submit`; concepts, jobs and capture metadata matched |
| Locus | 355 / 946 | `SearchEntryPointFrame` source retrieved from `src/components/SearchEntryPointFrame.tsx`; matching metadata |
| Country OSINT catalog | 154 / 269 | `appendResults` source retrieved from `site/index.html`; matching metadata |

All three returned `ready`, full indexing, no skipped files and no graph count
mismatch. `get_architecture` also returned the main project's modules/routes.
These are MCP functionality checks, not application tests.

## Parser limits and exclusions

Evidence Workspace reported partial parsing in `index.html`, the Dockerfile and
six Jinja templates (`audit`, `bulk`, `collection_detail`, `collections`,
`snapshot_detail`, `snapshots`); `provereno-ui/nginx.conf` was marked unusable for
graph parsing. Read those files directly. Locus reported a partial range at
`src/App.tsx:789`. The country catalog reported no partial/unusable parses.
These are best-effort diagnostics, not proof that other files are complete.

Reference images/assets are excluded by suffix. Git/dependency/build/local graph
state is excluded. Locus `.env.local` was reported excluded by ignore rules; its
contents were not read. Review scope/exclusions before indexing new sensitive work.
Never add captures, real investigations, credentials, exports or backups to this index.

## Daily use and fallback

Use graph discovery for symbols/relationships, `get_architecture` for structure,
`get_code_snippet` after discovering qualified names, and `query_graph` for multi-hop
questions. Prefer `rg` for exact text, configuration and coverage gaps. Verify cited
paths and current source; paginate when results are truncated. If MCP fails or is
stale, report that limitation and continue authorized work with native search.
