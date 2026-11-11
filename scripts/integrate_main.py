#!/usr/bin/env python3
"""Serialize a tested, accepted task's fast-forward into the local main checkout."""
import argparse
import fcntl
from pathlib import Path
import re
import subprocess


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", "-C", str(root), *args], text=True).strip()


def integrate(task: Path, source: str, expected_main: str) -> str:
    for commit in (source, expected_main):
        if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", commit):
            raise ValueError("Use full commit hashes for source and expected main")
    common = Path(git(task, "rev-parse", "--path-format=absolute", "--git-common-dir"))
    main = common.parent
    if common.name != ".git" or not (main / ".git").is_dir():
        raise ValueError("A canonical main checkout with a .git directory is required")
    with (common / "paperclip-main-integration.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if git(main, "branch", "--show-current") != "main":
            raise ValueError("The canonical checkout must be on main")
        if git(main, "status", "--porcelain=v1"):
            raise ValueError("Main has local changes. Preserve them before integration")
        current = git(main, "rev-parse", "HEAD")
        if current == source:
            return current
        if current != expected_main:
            raise ValueError("Main advanced. Integrate its new tip into the task and revalidate")
        if git(task, "rev-parse", "HEAD") != source or git(task, "status", "--porcelain=v1"):
            raise ValueError("The task must be clean at the tested source commit")
        subprocess.run(["git", "-C", str(main), "merge-base", "--is-ancestor",
                        current, source], check=True)
        subprocess.run(["git", "-C", str(main), "merge", "--ff-only", source], check=True)
        result = git(main, "rev-parse", "HEAD")
        if result != source or git(main, "status", "--porcelain=v1"):
            raise RuntimeError("Verify main after the incomplete integration")
        return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, help="Full accepted and tested task HEAD")
    parser.add_argument("--expected-main", required=True, help="Full main tip used for validation")
    args = parser.parse_args()
    try:
        print(integrate(Path.cwd(), args.source, args.expected_main))
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"Integration stopped: {error}\n")
