"""Exercise local integration against real disposable Git worktrees."""
import fcntl
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from integrate_main import git, integrate


class MainIntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.main = Path(self.temp.name) / "main"
        self.task = Path(self.temp.name) / "task"
        subprocess.run(["git", "init", "-q", "-b", "main", str(self.main)], check=True)
        git(self.main, "config", "user.email", "synthetic@example.invalid")
        git(self.main, "config", "user.name", "Synthetic integration test")
        (self.main / "base.txt").write_text("base\n")
        git(self.main, "add", "base.txt")
        git(self.main, "commit", "-qm", "test: create base")
        self.base = git(self.main, "rev-parse", "HEAD")
        git(self.main, "worktree", "add", "-qb", "task", str(self.task))
        (self.task / "feature.txt").write_text("accepted feature\n")
        git(self.task, "add", "feature.txt")
        git(self.task, "commit", "-qm", "test: add accepted feature")
        self.source = git(self.task, "rev-parse", "HEAD")

    def test_fast_forward_and_repeat_preserve_exact_source(self):
        self.assertEqual(integrate(self.task, self.source, self.base), self.source)
        self.assertEqual((self.main / "feature.txt").read_text(), "accepted feature\n")
        self.assertEqual(integrate(self.task, self.source, self.base), self.source)
        self.assertEqual(git(self.main, "status", "--porcelain=v1"), "")

    def test_dirty_main_is_preserved(self):
        (self.main / "base.txt").write_text("operator change\n")
        with self.assertRaisesRegex(ValueError, "Main has local changes"):
            integrate(self.task, self.source, self.base)
        self.assertEqual(git(self.main, "rev-parse", "HEAD"), self.base)
        self.assertEqual((self.main / "base.txt").read_text(), "operator change\n")

    def test_advanced_main_requires_fresh_validation(self):
        (self.main / "new.txt").write_text("another integrated task\n")
        git(self.main, "add", "new.txt")
        git(self.main, "commit", "-qm", "test: advance main")
        current = git(self.main, "rev-parse", "HEAD")
        with self.assertRaisesRegex(ValueError, "Main advanced"):
            integrate(self.task, self.source, self.base)
        self.assertEqual(git(self.main, "rev-parse", "HEAD"), current)
        with self.assertRaises(subprocess.CalledProcessError):
            integrate(self.task, self.source, current)
        self.assertEqual(git(self.main, "rev-parse", "HEAD"), current)

    def test_concurrent_integration_lock_prevents_a_second_writer(self):
        with (self.main / ".git/paperclip-main-integration.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            with self.assertRaises(BlockingIOError):
                integrate(self.task, self.source, self.base)
        self.assertEqual(git(self.main, "rev-parse", "HEAD"), self.base)

    def test_uncommitted_task_changes_prevent_integration(self):
        (self.task / "feature.txt").write_text("unreviewed edit\n")
        with self.assertRaisesRegex(ValueError, "task must be clean"):
            integrate(self.task, self.source, self.base)
        self.assertEqual(git(self.main, "rev-parse", "HEAD"), self.base)
