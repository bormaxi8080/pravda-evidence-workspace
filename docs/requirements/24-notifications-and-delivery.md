# Notification permissions, outbox and delivery requirements

Date: 2026-11-09. Status: **selected C4 design; not implemented**.
Owner: security/backend/operations. Depends on qualified internal comparison/watch
events and ADR-005. Adapts transport separation and change-alert ideas from the
pinned upstream review; no provider account, library or external send is configured.

## First delivery scope

Internal attention exists before C4. First external transport is an explicitly
approved HTTPS webhook to a fixed destination on port 443, with private credential
reference and bounded JSON payload. Email/SMTP and broader Apprise adapters are
subsequent transport evaluations; they are not working controls in initial C4.
No screenshots, raw diffs, notes, source query strings or evidence attachments in
the first payload class. Provider support/capabilities are explicit and versioned.

## Requirements

### REQ-NTF-001 Explicit destination and disclosure permission

Only admins shall create/enable/revoke destinations and payload policies; a watch
owner must explicitly bind an approved destination to that watch/revision. A user
being allowed to read evidence does not authorize sending it to a third party.
Show destination identity, allowed payload class, instance-link disclosure and
revoke effect before enablement. No default destination, inherited tag transport
or automatic external send follows capture/import/profile creation.
First C4 defaults event selection to `content_changed`; technical event kinds need
explicit approved binding policy. Baseline establishment, manual comparison saves
and profile reanalysis never trigger an automatic content-change send.

### REQ-NTF-002 Minimal versioned payload and secrets

Initial payload shall contain contract version, event/delivery IDs, safe event kind,
occurrence time, and an optional approved authenticated-app link with no bearer
token. Exclude source URL/title/notes/extracted text/diff/screenshots unless a later
explicit payload contract is adopted. Destination URL has no embedded credentials;
secrets are stored as protected references and injected only in transport headers.
Keep templates fixed/versioned; source text is never executable template content.

### REQ-NTF-003 Transactional durable outbox

Persist NotificationIntent with accepted ChangeEvent/binding decision in one DB
transaction, or record an explicit no-delivery disposition. Unique(event_id,
destination_id) prevents automatic duplicate logical intents; freeze event/input
refs, binding/policy revision, payload digest/template version and expiry. Delivery
is worker-owned outside the transaction; no network send in request/capture commit.
Capture/event success remains valid if delivery fails.
If outbox admission reaches its cap, commit an explicit capacity-denied delivery
disposition with the event and show it to permitted admins; do not roll back valid
evidence or claim a notification was queued/delivered. New retry/requeue requires
an explicit bounded policy after capacity recovers, not silent loss or infinite backlog.

### REQ-NTF-004 Reauthorization and withdrawal before send

Before claiming, sending and retrying, verify enabled admin-approved destination,
watch owner permission, current binding/policy/epoch and non-purged dependencies.
Revocation cancels unsent/retryable intents; policy revision mismatch requires a
fresh explicit disposition rather than reusing broader saved payload. Never silently
reroute to a fallback destination. A provider-accepted payload cannot be recalled;
do not describe revoke as erasing recipient copies.

### REQ-NTF-005 Bounded transport and honest uncertainty

Enforce fixed approved HTTPS target, TLS validation, public IP/redirect/egress policy,
timeouts, response/body caps and rate limits. A destination cannot become an SSRF
proxy; redirects are rejected in first C4. Separate delivery credentials/network
from browser runner. State whether the provider accepted a request; never imply
recipient receipt/read or exactly-once external delivery from an HTTP success.
If a worker loses the result after bytes may have been sent, record uncertain;
automatic replay requires a verified receiver idempotency contract, otherwise a
reviewed manual replay decision. Do not hide uncertainty as success or retry forever.

### REQ-NTF-006 Retry, expiry and delivery diagnostics

Retry eligible 408/429/5xx or known pre-send connection failures under finite
backoff/Retry-After/expiry. Other 4xx are permanent, policy denials cancel. Persist
attempt number/time, safe response classification and next action without credentials
or content-bearing response bodies in general logs. Expired/dead/uncertain intents
are visible to permitted admins and never change evidence review/publication.
Notification bursts use bounded queues/rates; no silent loss presented as delivered.

### REQ-NTF-007 Restore and purge prevent renewed disclosure

Restored destinations/bindings remain disabled and unsettled delivery intents are
held/cancelled pending operator reconciliation; never replay a backup's outbox on
startup. Reapply protected deletion/revocation ledgers before any serving/sending.
Purge dependent run/event/payload bytes as authorized, retain minimal safe disposition
and prevent rebuild from removed inputs. Historical provider acceptance is recorded
as historical, not a reason to send again. Secret restoration/rotation is explicit.

## Delivery state contract

NotificationIntent states: pending, leased, retry_wait, provider_accepted, uncertain,
failed, cancelled, expired. DeliveryAttempt is immutable after outcome. Lease fencing
protects local state but cannot retract a remote request that already crossed the
network; the sender must not promise stronger semantics than its receiver supports.

Transitions: pending/retry_wait -> leased after policy/capacity; leased -> accepted,
retry_wait, uncertain or failed; unsent/nonterminal -> cancelled on revocation; any
eligible unsent -> expired at TTL. Late replies are retained on attempt history but
cannot reactivate cancelled binding or create another accepted event. A deliberate
manual replay creates a linked new intent with explicit duplicate-risk acknowledgement;
it never edits the old delivery history.

Selected defaults to qualify: 24h intent TTL; at most five attempts with 1m/5m/30m/2h
delays; 10s connect and 30s total request deadlines; 64 KiB request and 16 KiB response
limits; one dispatch slot, at most 10 requests/minute instance and 2/minute destination.
Bound receiver Retry-After by expiry; no retry past TTL. These are design settings,
not provider delivery guarantees. Public-target restriction has no user-configurable
private-IP exception in first C4.

## Minimal payload example

```json
{"schema":"workspace-notification/1","event_id":"48816e18-6a0b-4026-9c33-a5bd0be76561","delivery_id":"4fe76fa3-c2e5-4f5a-870b-dc2066b75e55","kind":"content_changed","occurred_at":"2026-11-09T10:00:00Z"}
```

Authenticated-app links are optional because instance hostname/event identity can
itself disclose investigation activity. Destination tests use synthetic events and
are explicit authorized sends in the actual implementation; this documentation
does not authorize contacting any destination or importing a secret.
