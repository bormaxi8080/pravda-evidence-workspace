# Future users, capability roles and evidence access spaces

Date: 2026-11-09. Status: **selected post-V0 U1/U2/U3 requirements; not implemented**.
Owner: product/identity/security/domain. Authority: explicit user request and ADR-009;
source concept sections 20/21 and the current shared admin/editor baseline.
V0 remains one shared newsroom, editor/admin, admin-only publication and no collection
ACL. The twelve IDs here add later requirements, not retroactive V0 obligations.

## Requirements

### REQ-IAM-001 Stable user identity and lifecycle in U1

User shall have stable local UUID, immutable provider issuer/subject association,
current display identity, enabled/suspended/deactivated state, permission revision
and audited lifecycle events. Renaming a provider login or email does not create
another user or transfer evidence ownership. Deactivation preserves attribution/
history and denies new operations; content is not cascade-deleted with an account.
No automatic linking across providers by matching email/display name.

### REQ-IAM-002 Controlled admission, invitations and offboarding in U1

Retain fail-closed provider/deployment admission and add explicit administrator
provisioning/invitation bound to a verified provider identity. Initial invitations
are one-time digest-backed codes with 24h expiry, communicated by an authorized
human outside this system; no new email service is implied. Admission alone grants
no unreviewed role upgrade. Offboarding revokes sessions/grants, pauses owned
automatic work, records transfer/disposition and cannot disable the last enabled
workspace administrator without the operator recovery path.

### REQ-IAM-003 Explicit versioned capability bundles in U1

Replace the single role enum through an audited migration with fixed viewer,
researcher, reviewer, publisher and workspace_admin bundles and explicit multiple
assignments. Authorization evaluates action and resource scope, not a string check
such as role!=viewer. Bundle/version changes invalidate permission revision and are
previewed; no arbitrary executable policy/custom-role language in first U1.
Workspace administration alone does not imply publication or raw evidence read.

### REQ-IAM-004 Immediate effective permission and scoped sessions in U1

Role/lifecycle changes shall affect every service, artifact, job, SSE, generated
package and companion/workload grant on its next protected operation/commit.
Long-lived streams recheck within the existing 30s bound; no forced recall of
already downloaded content is claimed. Grants are a subset of both assigned
capabilities and current scope, never a way to preserve removed authority. Record
safe permission-change audit atomically and invalidate cached decisions.

### REQ-IAM-005 Explicit review/publication separation in U1/U2

Reviewer approval and publisher publication shall be separate actions/capabilities
over exact evidence/editorial revision. Default U1 preserves current self-review
policy after migration. U2 may explicitly require reviewer != last editor and/or
publisher != reviewer per space; enabling policy validates a viable enabled team.
No silent emergency override, stale approval or implicit publisher right from
account administration. Explicit audited bundle assignment is a separate action. Operator recovery is separate, scoped and auditable.

### REQ-IAM-006 Compatible migration and recovery in U1

Dry-run effective old/new permissions before activating U1: editor maps to researcher
plus reviewer in the shared space; admin maps to workspace_admin plus researcher,
reviewer and publisher. Preserve existing approved revisions/public projections
and history rather than inventing independent past reviews. Explicit policy changes
can narrow future rights but cannot falsely claim old access was restricted. Keep
operator recovery and a tested last-admin/role-lockout migration rollback strategy.

### REQ-IAM-007 One evidence custody space in U2

Introduce AccessSpace with shared/restricted mode and explicit membership. Every
capture belongs to exactly one space; collection belongs to one space and may
contain only captures in that space. Collections remain grouping/views inside that
boundary. Multiple collection memberships never union grants across spaces. Source
URL equality cannot expose another space's existence/capture history or deduplicate
authorization away. Shared migration space preserves the old newsroom model.

### REQ-IAM-008 Scope closure across all features in U2

Enforce space scope on list/count/search/autocomplete/history, artifacts, derived
anchors/hits, jobs/SSE, report/export/import, publication, audit views and companion
context. A report/case selection cannot silently mix spaces; first U2 supports one
space per selection/package. Every input/output/dependency carries exact scope;
cache reuse checks current authority and never leaks another space through snippets,
existence, pagination counts or diagnostic details. Unsupported installed adapters
remain disabled until the complete scope path is qualified.

### REQ-IAM-009 Controlled scope moves and disclosure in U2

Moving evidence between spaces is an explicit bounded preview/revisioned command
requiring move authority in both scopes, dependency/publication/disclosure review
and an audited migration plan. Freeze/fence affected writes, invalidate old scoped
grants/caches/exports and preserve original byte/provenance identity. Active public
projection requires explicit revoke/disposition before narrowing scope. No ordinary
collection edit or copy grants private access. First U2 has no bulk unreviewed
cross-space move or reusable package carrying imported ACL grants.

### REQ-IAM-010 Groups and delegated management in U2

Flat groups may assign existing role bundles within spaces under explicit bounded
membership/grant revisions. No nested/recursive groups or implicit domain-based
membership. A delegated space steward manages only approved memberships/capability
subsets there, not deployment admins, service credentials or self-escalation beyond
that delegation. Restricted-space membership is explicit for workspace_admin too;
administrative oversight can view safe policy/audit metadata without opening content.

### REQ-IAM-011 Qualified identity federation in U3

Select one configured OIDC issuer per deployment as an optional future provider,
with verified issuer/subject/audience/state/nonce and code-flow protection under
reviewed current standards. Explicitly link existing identities only after proving
control of the existing account and new provider or the operator recovery procedure.
Provider groups map through reviewed local rules, never direct admin/publisher claims.
Provider outage fails closed; no login-domain/email-match fallback or automatic
tenant creation. Stronger privileged-action step-up needs actual provider support/
tests and cannot be inferred from opening another OAuth redirect.

### REQ-IAM-012 Separate workload identities in U3

Non-interactive automation uses dedicated disabled-by-default service principals,
responsible enabled human owner, exact operation/space scopes, expiry, rotation and
revocation. First scope is capture-intent submission and own status only; no review,
publication, user management, broad archive export or browser login/session token.
Server authorizes current principal/owner/scope at every admission/finalization;
owner disablement pauses automation. No service credential is imported through a
case package, browser extension or DB role. Protocol/lifetime/key handling must be
materialized/qualified before enabling this stage, not advertised as working OAuth.

## Default U1 capability matrix

| Capability | Viewer | Researcher | Reviewer | Publisher | Workspace admin |
| --- | --- | --- | --- | --- | --- |
| Inspect authorized metadata/screenshot | Yes | Yes | Yes | Yes | Only with separately assigned content role/scope |
| Download raw originals / private export | No by default | Yes | Yes for review | Only with researcher/reviewer also assigned | No implicit right |
| Capture, organize and edit research context | No | Yes | No unless researcher also assigned | No unless researcher also assigned | No implicit right |
| Review exact revision | No | No unless reviewer also assigned | Yes | No unless reviewer also assigned | No implicit right |
| Publish/revoke qualified approved projection | No | No | No | Yes, allowed scope/policy | No implicit right |
| Accounts, fixed-role assignments, safe security policy/audit | No | No | No | No | Yes, explicit audited changes |
| Host/DB backup, daemon, emergency purge/recovery | No | No | No | No | Not an application role; operator procedure |

These are application capabilities, independent of PostgreSQL login roles. App
admin may explicitly assign itself an allowed bundle under policy/audit; the fact
of being admin is never a hidden content bypass. Workspace/DB/host operators still
control the installation; restricted spaces do not promise cryptographic secrecy
against that trusted operator. No local-password/MFA service is introduced in U1.
GitHub reconnect alone is not proof of a new MFA/user-presence challenge.

## Space model, defaults and migration

AccessSpace: UUID, name, mode, state, policy/revision and created/updated actors/times.
SpaceMembership and group grants bind enabled principal, space and bundle revisions.
Every capture, collection, job input/output and derived selection has a canonical
space association; enforce cross-scope invariants with application checks and
composite DB relationships. App-level defaults are deny absent an effective grant.

Existing data maps to one default shared space only after reviewed migration. Do
not mark old collections restricted or backfill fictional historic privacy. User
selects active space explicitly on capture/CSV/companion submission; stale/deleted/
changed space returns conflict, never silently falls back to shared. Source listing/
history is filtered to authorized captures; global canonical URL reuse is internal
and cannot reveal existence through API/count/dedup messages.

Initial U2 caps to qualify: 50 active spaces, 100 flat groups, 100 memberships/group,
100 records per previewed grant/move command, existing 25/100 paging. Use bounded
effective-role computation and no uncontrolled recursive inheritance. A restricted
space can publish only through explicit publisher capability/disclosure policy;
public slug access reveals only the approved projection, never membership/context.

A move keeps original capture/manifest bytes unchanged: access metadata is not
rewritten capture provenance. Dependent report snapshots/packages keep their original
scope provenance but old server downloads are unavailable until a new authorized
selection is created. Previously downloaded originals cannot be recalled. If a full
atomic scope/dependency/publication transition cannot be established, deny the move;
no halfway exposure. Normal in-space collection edit remains ordinary editorial revision.

First U2 records at most five explicit stewards/space under a revisioned delegation.
Scope-move authority requires that delegation plus researcher/content authority in
both source and destination; workspace_admin alone is insufficient. Delegated grants
cannot assign deployment administration or widen their own approved subset. Changes
to current publisher/reviewer grants affect future commands, not silent rewriting
or reactivation of historical public projections; incident withdrawal remains explicit.

Transport setup/secret administration remains a deployment/workspace-admin capability,
separate from research content access. An enabled C4 binding additionally requires
current authorized watch ownership/scope and approved disclosure policy. H4 imports
cannot carry role/membership grants, H3 selection stays in one scope, and user-attention
acknowledgement stays personal. Every enabled adapter's literal old admin/editor
checks must be migrated to the reviewed capability/scope service before U activation.

## Identity UX/API and authority boundary

Future screens: user list/lifecycle, invitation approval, effective-permission preview,
own sessions/grants, role assignment history, space switch/membership/group admin,
review-separation policy and scope-move preview. Show actual effective actions and
why a change narrows access; no ambiguous superuser checkbox.

Cookie/CSRF web commands use expected permission/policy revisions and safe audit;
queries remain read-only. Materialize typed DTOs for user lifecycle/roles, invitation
redeem, space/group membership, scope-move preview/confirm and identity linking in
EWP-69–71. Browser API gains only negotiated scoped context fields/adapters; no
existing token expands rights when U stages turn on. Unknown client/scope version
fails rather than writing an unscoped capture into restricted deployment.

U2 migration must cover every enabled C/H/B adapter, download/public projection and
operational path; unsupported optional modules may be explicitly disabled, not a
reason to weaken isolation. First U1/U2 remain one newsroom, not multi-tenant SaaS.
OPS-ACC-09–12 and the IAM matrix in document 49 define stage gates.

## U3 technical protocol boundary to materialize

OIDC code flow uses PKCE S256, exact registered redirect/issuer/audience checks,
state/nonce and verified signed token expiry/algorithm/key rules. Discovery/JWKS
comes only from the configured trusted issuer/TLS/control-plane policy, never an
arbitrary token URL/jku. Test bounded key caching/rotation and failure; unverified
claims cannot select an issuer, account, space or role. An explicitly configured
internal identity provider is a control-plane exception, not a private-source
capture/SSRF bypass. Materialize exact provider/library/config compatibility before
claiming conformance to the primary OIDC/OAuth sources.

First workload protocol is separately versioned under /api/workload/v1. A one-time
shown random 256-bit service credential has at most seven-day expiry, digest-only
server storage and tested rotation/revocation. It can mint opaque 15min operation/
space-bound bearer tokens; no persistent refresh token or interactive-session reuse.
Secret exchange is body/header over fixed TLS, never URL, browser content or logs.
Client ID, IP or host placement alone never authenticates a caller. Every request
checks current principal, responsible enabled owner, permission revision and exact
capture:create/status:own scope. Creation/rotation needs an authorized administrator
and explicit space delegation; publisher/reviewer/admin capabilities cannot be requested.

This is a selected bounded Workspace protocol, not an implemented OAuth client-
credentials server. Schema/endpoints/rate limits/negative examples and library/key
handling are EWP-71 deliverables; until qualified, workload endpoints remain disabled.
Credential expiry pauses rather than secretly impersonating a user. Browser tokens,
web cookies and DB passwords are rejected on this protocol, and workload tokens
are rejected on arbitrary web/companion routes.

U3 audit/intent actors use a typed user-or-service reference plus separate responsible
human owner. Extend requester constraints explicitly for a valid service principal;
do not impersonate the owner, create a fake human account or mark service activity
as legacy unknown. Original human actor IDs/history remain unchanged.

Effective U2 permission preview includes all surviving direct and flat-group grant
paths within the selected space. Removing one path is not claimed to remove access
if another approved path still grants it; disabled principal/removed resource/root
fence remains a deny. This computation is bounded/versioned and intersects purpose/
profile policy, not merely the union of named roles.
