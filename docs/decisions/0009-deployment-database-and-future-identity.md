# ADR-009: Specify operational deployment and future access boundaries

Date: 2026-11-09. Status: **selected design; implementation/qualification pending**.
Authority: user requested technical requirements, Docker/database/deployment/
maintenance detail and future roles/users. Sources: concept sections 20/22–29,
ADR-002–008 and [primary/static review](../reference/deployment-and-database-platform-review.md).

## Decision

Retain one newsroom/host, Python 3.12, PostgreSQL 16, SSR/Compose and the initial
4 CPU/8 GiB/40 GiB free-storage qualification budget from ADR-002. It is a test
envelope, not measured minimum capacity. Pin exact supported build/image/OS/Compose/
browser identities when tested. V0 still has admin/editor and shared evidence.

Specify immutable role-specific image targets, private DB/internal services,
separate edge/control/egress boundaries, explicit mounts/secrets, finite resource
budgets, schema migration gate and operator installation/update/recovery procedures.
Use a bounded host-trusted job launcher to instantiate per-job browser/offline
containers; only that operator boundary may access the container daemon. Web,
worker, browser and decoder containers get no Docker socket. Launcher accepts
fixed policy/job IDs, never arbitrary commands/images/host mounts/privileged flags.
This selects a mechanism for the existing isolated-runner contract, not a second
capture engine. EWP-01 must prove it or reopen the topology without enabling unsafe capture.

Select PostgreSQL ownership/runtime/migration separation, bounded connection/query
budgets, explicit indexes/locking/migrations, accepted-byte-aware backups and routine
maintenance. No create_all upgrade authority, concurrent incompatible major upgrade,
DB-only disaster recovery guarantee or implicit zero-downtime claim.

For later versions select U1 account lifecycle and fixed capability bundles; U2
one AccessSpace custody boundary per capture with restricted-space collections;
U3 qualified federation/non-interactive identities. Collections remain organizational
groups inside one space, not union-based grants across multiple evidence spaces.
One installation remains one newsroom; no SaaS tenancy, guest public archive or
protection from the trusted host/DB operator is introduced.

Future roles: viewer, researcher, reviewer, publisher and workspace_admin, combined
explicitly. Workspace administration does not silently grant restricted evidence
read/publication. Legacy migration preserves existing effective editor/admin powers
in the shared space; stronger review separation is an explicit policy gate, not
retroactive invented approval. OIDC/service grants stay separate from browser
companion tokens and database roles.

## Delivery and scope

Documents 44–47 refine existing technical requirements; document 48 adds 12
later-stage REQ-IAM requirements, with acceptance/tasks in 49. Current totals:
170 requirements (70 V0 / 100 later), 72 tasks and 68 scenario definitions.
EWP-61–68 refine core build/DB/deploy/operations; EWP-69–71 implement U1–U3 later;
EWP-72 is handoff for the actual supported feature set. No U stage becomes a V0
or baseline production prerequisite. Runtime components stay unchanged by prose.

Specification advances only; no Docker/SQL/config/runtime file, secret, account,
role grant, backup, deployment or store listing is created. All capacity, isolation,
restore, permission and protocol assertions require actual stage evidence later.

## Platform sequencing amendment — 2026-11-10

[ADR-012](0012-macos-development-and-linux-qualification.md) supersedes Linux-first
implementation scheduling. Mac local implementation/acceptance and later native
Linux qualification have separate gates in document 56. Other technical/product
invariants and the original requirement/task/scenario identities remain unchanged.
