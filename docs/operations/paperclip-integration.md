# Paperclip local main integration

The operator authorized project agents to integrate accepted tasks into local
`main` on 2026-11-11. This standing authorization covers the local merge after
whole-package human acceptance and successful required checks. Read this policy
from the canonical main checkout when a retained task branch has older rules.

## Task delivery

1. Implement and commit in the assigned isolated task worktree. Return the entire
   package and actual evidence for its existing human review.
2. After acceptance, read the current local `main` tip. Merge it into the task
   branch when needed. Preserve accepted source ancestry and user changes.
3. Resolve routine conflicts in the task worktree. Combine Unreleased entries,
   preserve newer platform requirements, reconcile affected component versions
   above their integrated baselines and regenerate the ledger/inventory. Ask for
   a decision only when conflict resolution changes accepted product behavior or
   an unresolved requirement. Revalidate the combined tree and commit it.
4. From the clean task worktree, invoke the canonical helper with full hashes.

   ```sh
   python3 /Volumes/Transcend/workspace/projects/osint/provereno/pravda-evidence-workspace/scripts/integrate_main.py --source <tested-task-head> --expected-main <validated-main-tip>
   ```

   The helper locks the integration operation, checks clean main/task trees and
   the expected main tip, and performs `git merge --ff-only`. A busy lock or an
   advanced main requires retrying with fresh state and applicable validation.
   Preserve a dirty main checkout and report its actual changes for resolution.
5. Verify source ancestry, resulting main identity and cleanliness. Record the
   integrated commit in Paperclip and refresh the canonical CodeBase index.
   Existing human-only final status controls still govern the review verdict.

Accepted feature prerequisites may also be integrated into the task's own branch.
If resolution changes accepted runtime or contract semantics, return those changes
for review before integration. Routine version and changelog reconciliation uses
the standing local merge authorization.

## Local execution profile

The installed original Codex launcher verifies the task worktree registration,
branch and canonical Git identity. It grants main writes to versioned top-level
paths present in main or the task and to exact main index/ref/reflog/coordination
files. It retains the active task's Git access and the approved Docker/loopback
connection. New tracked top-level paths become available on the next invocation.
An already running session needs a fresh invocation after a profile change.

The profile's common Git configuration and other worktrees' metadata remain
read-only. The integration lock coordinates cooperating project agents. These
filesystem grants provide write capability, while the acceptance and clean-tree
rules govern how agents use it. Pushing, releases, tags and deployment require
their own operator instruction.
