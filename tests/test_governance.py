"""Exercise repository invariants and failure paths, without application claims."""

# Adapted from The OA; see docs/reference/theoa-tooling-license.txt.

from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import validate_workspace as workspace


def planned_contract_fixture(manifests):
    """Keep planned-state tests independent of live component activation."""
    manifests["evidence-contracts"].update(
        version="0.0.0", status="planned", runtime="none",
        planned_path="shared-contracts/",
        owned_paths=["components/evidence-contracts/component.json"], checks=[])


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.manifests, errors = workspace.load_manifests(ROOT)
        self.assertEqual(errors, [])
        self.files = [f"components/{name}/component.json" for name in self.manifests]

    def issues(self):
        return "\n".join(workspace.registry_errors(self.manifests, self.files))

    def test_current_registry_has_valid_ownership_and_dependencies(self):
        self.assertEqual(self.issues(), "")

    def test_schema_rejects_unknown_fields(self):
        manifest = {**self.manifests["application"], "unreviewed": True}
        errors = workspace.schema_errors(manifest, workspace.read_json(ROOT / "release/component.schema.json"), "application")
        self.assertIn("unknown property unreviewed", "\n".join(errors))

    def test_schema_rejects_malformed_versions(self):
        manifest = {**self.manifests["application"], "version": "1.2"}
        errors = workspace.schema_errors(manifest, workspace.read_json(ROOT / "release/component.schema.json"), "application")
        self.assertTrue(any("version" in error for error in errors))

    def test_planned_version_is_reserved(self):
        planned_contract_fixture(self.manifests)
        self.manifests["evidence-contracts"]["version"] = "0.1.0"
        self.assertIn("planned components need reserved 0.0.0", self.issues())

    def test_planned_component_cannot_claim_existing_code(self):
        planned_contract_fixture(self.manifests)
        self.files.append("shared-contracts/schema.json")
        self.assertIn("planned component contains implementation files", self.issues())

    def test_new_file_needs_an_owner(self):
        self.files.append("unregistered/new-file.py")
        self.assertIn("expected one owner, found 0", self.issues())

    def test_two_components_cannot_own_one_file(self):
        self.manifests["governance"]["owned_paths"].append("README.md")
        self.files.append("README.md")
        self.assertIn("expected one owner, found 2", self.issues())

    def test_paths_cannot_escape_checkout(self):
        self.manifests["application"]["owned_paths"].append("../other/**")
        self.assertIn("unsafe owned path", self.issues())

    def test_unknown_dependency_is_rejected(self):
        self.manifests["application"]["depends_on"].append("foreign-package")
        self.assertIn("unknown dependency", self.issues())

    def test_dependency_cycle_is_rejected(self):
        self.manifests["application"]["depends_on"].append("deployment")
        self.assertIn("dependency cycle", self.issues())

    def test_existing_component_cannot_depend_on_planned_runtime(self):
        planned_contract_fixture(self.manifests)
        self.manifests["governance"]["depends_on"].append("evidence-contracts")
        self.assertIn("existing artifact depends on a planned component", self.issues())


class DocumentationDiscoveryTests(unittest.TestCase):
    def test_runtime_guides_are_checked_but_installed_dependencies_are_not(self):
        with tempfile.TemporaryDirectory(prefix="evidence-docs-") as directory:
            root = Path(directory)
            (root / "README.md").write_text("# Synthetic fixture\n")
            (root / "provereno-ui/node_modules/dependency").mkdir(parents=True)
            (root / "provereno-ui/node_modules/dependency/README.md").write_text("missing final newline")
            (root / "provereno-ui/README.md").write_text("missing final newline")
            errors, documents, _, _ = workspace.check_docs(root)
            self.assertEqual(documents, 2)
            self.assertTrue(any("provereno-ui/README.md" in error for error in errors))
            self.assertFalse(any("node_modules" in error for error in errors))


class BaselineTests(unittest.TestCase):
    def setUp(self):
        self.manifests, _ = workspace.load_manifests(ROOT)
        self.previous = workspace.read_json(ROOT / "release/versions.json")
        self.current = deepcopy(self.previous)

    def issues(self, changed=None, old_history="", new_history="", allow_release=False):
        return "\n".join(workspace.baseline_errors(
            self.previous, self.current, self.manifests, changed or [],
            old_history, new_history, allow_release))

    def test_requirements_change_needs_specification_bump(self):
        self.assertIn("specification: changed component needs", self.issues(["docs/01-vision.md"]))

    def test_incremented_component_is_accepted(self):
        parts = list(map(int, self.previous["components"]["specification"].split(".")))
        parts[2] += 1
        self.manifests["specification"]["version"] = ".".join(map(str, parts))
        self.assertEqual(self.issues(["docs/01-vision.md"]), "")

    def test_shared_bookkeeping_does_not_bump_governance(self):
        self.assertEqual(self.issues(["release/versions.json", "CHANGELOG.md"]), "")

    def test_version_cannot_regress(self):
        self.manifests["specification"]["version"] = "0.0.1"
        self.assertIn("component version regressed", self.issues())

    def test_planned_metadata_does_not_claim_implementation_version(self):
        planned_contract_fixture(self.manifests)
        self.previous["components"]["evidence-contracts"] = "0.0.0"
        self.current["components"]["evidence-contracts"] = "0.0.0"
        self.assertEqual(self.issues(["components/evidence-contracts/component.json"]), "")

    def test_normal_work_cannot_change_product_release(self):
        self.current["project"]["release"] = "0.1.0-alpha.1"
        self.current["project"]["release_date"] = "2026-11-01"
        self.assertIn("product release changed", self.issues())
        self.assertEqual(self.issues(allow_release=True), "")

    def test_component_retirement_cannot_happen_silently(self):
        del self.manifests["application"]
        self.assertIn("component removal needs an explicit retirement", self.issues())

    def test_historical_release_cannot_be_rewritten(self):
        self.assertIn("historical changelog sections were modified",
                      self.issues(old_history="## [0.1.0]\nOriginal\n", new_history="## [0.1.0]\nChanged\n"))

    def test_new_release_can_prepend_unchanged_history(self):
        history = "## [0.1.0]\nOriginal\n"
        self.assertEqual(self.issues(old_history=history, new_history="## [0.2.0]\nNew\n" + history), "")


class SynchronizationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="evidence-governance-")
        self.root = Path(self.temporary.name)
        shutil.copytree(ROOT / "components", self.root / "components")
        shutil.copytree(ROOT / "release", self.root / "release")
        shutil.copyfile(ROOT / "CHANGELOG.md", self.root / "CHANGELOG.md")
        (self.root / "README.md").write_text("# Fixture\n", encoding="utf-8")
        self.files = [p.relative_to(self.root).as_posix() for p in self.root.rglob("*") if p.is_file()]
        self.inventory = patch.object(workspace, "git_inventory", return_value=self.files)
        self.git = patch.object(workspace, "git", side_effect=lambda root, *args:
                                subprocess.CompletedProcess([], 0 if args[0] == "rev-parse" else 128, "", ""))
        self.inventory.start()
        self.git.start()
        self.addCleanup(self.inventory.stop)
        self.addCleanup(self.git.stop)
        self.addCleanup(self.temporary.cleanup)

    def test_package_version_drift_is_rejected_without_execution(self):
        package = self.root / "provereno-ui/pyproject.toml"
        package.parent.mkdir()
        package.write_text('[project]\nversion="9.0.0"\n')
        self.assertIn("package/runtime version differs", "\n".join(
            workspace.package_errors(self.root, workspace.load_manifests(self.root)[0], ["provereno-ui/pyproject.toml"])))
        package.write_text('[project]\nversion="'+workspace.load_manifests(self.root)[0]['application']['version']+'"\n')
        self.assertEqual(workspace.package_errors(self.root, workspace.load_manifests(self.root)[0], ["provereno-ui/pyproject.toml"]), [])

    def test_stale_ledger_is_rejected(self):
        path = self.root / "release/versions.json"
        ledger = workspace.read_json(path)
        ledger["components"]["application"] = "9.0.0"
        path.write_text(json.dumps(ledger), encoding="utf-8")
        self.assertIn("version ledger differs", "\n".join(workspace.validate(self.root)))

    def test_sync_is_deterministic_and_preserves_human_text(self):
        ledger_path = self.root / "release/versions.json"
        ledger = workspace.read_json(ledger_path)
        project = deepcopy(ledger["project"])
        ledger["components"]["application"] = "9.0.0"
        ledger_path.write_text(json.dumps(ledger), encoding="utf-8")
        log_path = self.root / "CHANGELOG.md"
        log_path.write_text(log_path.read_text() + "\nHuman-authored note.\n", encoding="utf-8")
        self.assertEqual(workspace.validate(self.root, sync=True), [])
        snapshot = (ledger_path.read_bytes(), log_path.read_bytes())
        self.assertEqual(workspace.validate(self.root, sync=True), [])
        self.assertEqual(snapshot, (ledger_path.read_bytes(), log_path.read_bytes()))
        self.assertEqual(workspace.read_json(ledger_path)["project"], project)
        self.assertIn("Human-authored note.", log_path.read_text())

    def test_stale_changelog_inventory_is_rejected(self):
        path = self.root / "CHANGELOG.md"
        path.write_text(workspace.replace_inventory(path.read_text(), "stale table"), encoding="utf-8")
        self.assertIn("Unreleased component table is stale", "\n".join(workspace.validate(self.root)))

    def test_inventory_cannot_be_written_into_history(self):
        log = "## [Unreleased]\n\n## [0.1.0]\n" + workspace.START + "\n" + workspace.END + "\n"
        with self.assertRaisesRegex(ValueError, "inventory must belong to Unreleased"):
            workspace.replace_inventory(log, "table")

    def test_release_requires_a_real_calendar_date(self):
        path = self.root / "release/versions.json"
        ledger = workspace.read_json(path)
        ledger["project"].update(release="0.1.0-alpha.1", release_date="2026-02-30")
        path.write_text(json.dumps(ledger), encoding="utf-8")
        self.assertIn("invalid release calendar date", "\n".join(workspace.validate(self.root)))


if __name__ == "__main__":
    unittest.main()
