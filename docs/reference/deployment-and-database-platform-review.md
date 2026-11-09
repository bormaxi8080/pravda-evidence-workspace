# Deployment and database platform review

Reviewed: 2026-11-09. Status: **official-documentation/static-source review; no build,
database or deployment test executed**. Owner: deployment/database/security.

## Local source findings

At source reviewed for this pass, `provereno-ui/docker-compose.yml` declares only
web/db, publishes PostgreSQL on host port 5434 and web on 8080, and contains literal
development DB credentials. It does not instantiate the selected worker, scheduler,
edge, egress policy or isolated job runner. Its DB healthcheck is not application
schema/readiness evidence. The Dockerfile uses Python 3.13, installs before copying
the package source, includes Chromium in the web image and has no USER declaration.
The package build backend/installability remains unqualified. No .env, live secret,
investigation data, database volume or running daemon was inspected.

These observations refine [the source baseline](../04-current-state.md); they are
not proof of an exposed live instance. Selected Python 3.12/PostgreSQL 16 and
process isolation remain design targets until implementation/qualification.

## Primary-source register

| Source | Relevant fact / design implication |
| --- | --- |
| [Compose startup order](https://docs.docker.com/compose/how-tos/startup-order/) | Container start is not readiness; service_healthy and service_completed_successfully support dependency gates. Application retries/schema checks remain necessary. |
| [Compose secrets](https://docs.docker.com/compose/how-tos/use-secrets/) | Secrets can be explicitly granted as service-mounted files. Host file access and backup/rotation still need operator policy; this is not a general secret vault. |
| [Docker build practices](https://docs.docker.com/build/building/best-practices/) | Multi-stage builds, small runtime content and pinned bases support controlled artifacts. Record tested digests rather than depend on a moving tag. |
| [Playwright Python Docker guidance](https://playwright.dev/python/docs/docker) | The published image is described as testing/development oriented and not recommended as-is for untrusted sites; root disables Chromium sandbox. Qualify a dedicated user/sandbox/seccomp/egress boundary rather than copying a trusted-test command. |
| [PostgreSQL 16 backup](https://www.postgresql.org/docs/16/backup.html) | SQL dump, filesystem backup and continuous archiving have different assumptions. Choose and test the exact DB-plus-artifact consistency boundary. |
| [pg_dump](https://www.postgresql.org/docs/16/app-pgdump.html) | A DB dump can be consistent while writes continue, but it covers one database and not global roles or separate artifact files. It is not by itself a coherent Workspace backup. |
| [PostgreSQL connection settings](https://www.postgresql.org/docs/16/runtime-config-connection.html) | Connection/reserve limits are server configuration. Budget pooled and dedicated connections explicitly instead of multiplying process-local defaults. |
| [Routine vacuuming](https://www.postgresql.org/docs/16/routine-vacuuming.html) | Maintenance includes vacuum/statistics/wraparound control; VACUUM FULL takes an exclusive table lock. Routine operations must not blindly schedule it online. |
| [Explicit locking](https://www.postgresql.org/docs/16/explicit-locking.html) | Lock modes/conflicts and advisory locks have different purposes. Use migration serialization separately from ordinary row-level work and bounded lock waits. |
| [Row security](https://www.postgresql.org/docs/16/ddl-rowsecurity.html) | RLS can restrict rows, but owners/superusers/BYPASSRLS have important exceptions. SQL policy alone cannot authorize filesystem/report/publication paths. |
| [OpenID Connect Core](https://openid.net/specs/openid-connect-core-1_0.html) and [RFC 9700](https://www.rfc-editor.org/rfc/rfc9700) | Future federation needs verified identity/claims and reviewed code-flow security; these standards do not implement local role mapping or prove provider step-up support. |

Docker firewall documentation could not be retrieved during this pass; no particular
backend/rule behavior is claimed from it. Actual host forwarding, bridge reachability,
IPv4/IPv6/DNS/UDP bypass and Docker-published ports require live qualification under
document 44. No example firewall command is represented as tested.

## Selected scope

Documents 44–47 refine the existing one-host technical requirements. Document 48
selects future application identity/AccessSpace policy; database roles are different
principals, not copies of user-facing roles. PostgreSQL RLS is defense-in-depth
evaluation for a future qualified migration, not an implemented V0 feature or a
substitute for application authorization. No upgrade to another PostgreSQL major,
automatic HA, public deployment or current software-version guarantee is inferred.
