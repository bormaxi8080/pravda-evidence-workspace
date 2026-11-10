"""Exercise delivery gates in a disposable Git repository and skill/link failures."""

from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_workspace as workspace


class GitDeliveryTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="evidence-git-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for directory in ("release", "components"):
            shutil.copytree(ROOT / directory, self.root / directory)
        # Minimal synthetic documentation; never copy real captures or credentials.
        (self.root / "README.md").write_text("# Synthetic baseline\n")
        changelog = "# Changelog\n\n## [Unreleased]\n\n" + workspace.START + "\n" + workspace.END + "\n\nInitial baseline.\n"
        (self.root / "CHANGELOG.md").write_text(changelog)
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Synthetic Fixture")
        # Establish a commit so default HEAD exists, then establish governance.
        self.git("add", "README.md")
        self.git("-c", "core.hooksPath=/dev/null", "commit", "-qm", "Initial fixture")
        self.assertEqual(workspace.validate(self.root, sync=True), [])
        self.git("add", ".")
        self.git("-c", "core.hooksPath=/dev/null", "commit", "-qm", "Establish governance")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args], check=True,
                              capture_output=True, text=True).stdout.strip()

    def update_specification(self, version=None, changelog=True):
        path = self.root / "components/specification/component.json"
        manifest = json.loads(path.read_text())
        if version is None:
            major, minor, patch = map(int, manifest["version"].split("."))
            version = f"{major}.{minor}.{patch + 1}"
        manifest["version"] = version
        path.write_text(json.dumps(manifest, indent=2) + "\n")
        if changelog:
            path = self.root / "CHANGELOG.md"
            path.write_text(path.read_text() + "\nClarify synthetic requirements.\n")

    def test_unversioned_document_change_fails_against_real_git(self):
        (self.root / "README.md").write_text("# Changed synthetic requirements\n")
        errors = "\n".join(workspace.validate(self.root))
        self.assertIn("specification: changed component needs a version increment", errors)
        self.assertIn("human-readable changelog entry", errors)

    def test_valid_change_passes_and_explicit_base_survives_commit(self):
        baseline = self.git("rev-parse", "HEAD")
        (self.root / "README.md").write_text("# Changed synthetic requirements\n")
        self.update_specification()
        self.assertEqual(workspace.validate(self.root, sync=True), [])
        self.git("add", ".")
        self.git("-c", "core.hooksPath=/dev/null", "commit", "-qm", "Clarify requirements")
        self.assertEqual(workspace.validate(self.root, base=baseline), [])

    def test_version_bump_without_human_entry_fails(self):
        self.update_specification(changelog=False)
        self.assertIn("human-readable changelog entry", "\n".join(workspace.validate(self.root, sync=True)))

    def test_missing_explicit_base_fails(self):
        self.assertIn("cannot resolve Git baseline", "\n".join(workspace.validate(self.root, base="missing-fixture-ref")))

    def test_schema_errors_do_not_rewrite_derived_files(self):
        before = (self.root / "release/versions.json").read_bytes()
        path = self.root / "components/specification/component.json"
        path.write_text('{"invalid": true}\n')
        self.assertTrue(workspace.validate(self.root, sync=True))
        self.assertEqual(before, (self.root / "release/versions.json").read_bytes())


class AdditionalInvariantTests(unittest.TestCase):
    def test_deleted_or_transferred_file_affects_previous_owner(self):
        manifests, errors = workspace.load_manifests(ROOT)
        self.assertEqual(errors, [])
        previous_manifests = deepcopy(manifests)
        previous = workspace.read_json(ROOT / "release/versions.json")
        manifests["specification"]["owned_paths"].remove("README.md")
        manifests["governance"]["owned_paths"].append("README.md")
        errors = workspace.baseline_errors(previous, previous, manifests, ["README.md"], "", "",
                                           previous_manifests=previous_manifests)
        self.assertTrue(any("specification: changed component needs" in issue for issue in errors))
        self.assertTrue(any("governance: changed component needs" in issue for issue in errors))

    def test_planned_component_cannot_own_other_artifacts(self):
        manifests, _ = workspace.load_manifests(ROOT)
        manifests["evidence-contracts"].update(status="planned", version="0.0.0",
                                              planned_path="shared-contracts/", checks=[])
        manifests["evidence-contracts"]["owned_paths"].append("README.md")
        self.assertIn("planned component may own only its manifest", "\n".join(workspace.registry_errors(manifests, [])))

    def test_skill_name_mismatch_and_broken_link_fail(self):
        with tempfile.TemporaryDirectory(prefix="evidence-docs-") as temporary:
            root = Path(temporary)
            skill = root / ".agents/skills/evidence-orient/SKILL.md"
            skill.parent.mkdir(parents=True)
            skill.write_text("---\nname: wrong-name\ndescription: Synthetic fixture.\n---\n\n[missing](missing.md)\n")
            errors, _, _, _ = workspace.check_docs(root)
            self.assertTrue(any("frontmatter/name" in issue for issue in errors))
            self.assertTrue(any("missing local target" in issue for issue in errors))

    def test_inventory_only_change_is_not_a_human_entry(self):
        before = "## [Unreleased]\n" + workspace.START + "\nold table\n" + workspace.END + "\nHuman note.\n"
        after = workspace.replace_inventory(before, "new table")
        self.assertEqual(workspace.human_changelog(before), workspace.human_changelog(after))


if __name__ == "__main__":
    unittest.main()
