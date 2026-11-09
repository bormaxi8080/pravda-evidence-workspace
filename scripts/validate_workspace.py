#!/usr/bin/env python3
"""Validate component ownership, versions, changelog, and English documentation.

--sync regenerates the version map and the bounded Unreleased inventory table.
Manifest commands are descriptive metadata; this tool never evaluates them.
"""

# Adapted from The OA; see docs/reference/theoa-tooling-license.txt.

from __future__ import annotations

import argparse
import ast
from datetime import date
from fnmatch import fnmatchcase
import json
from pathlib import Path
import re
import subprocess
import sys
import tomllib

from check_docs import check as check_docs


START = "<!-- component-versions:start -->"
END = "<!-- component-versions:end -->"
BOOKKEEPING = {"CHANGELOG.md", "release/versions.json"}


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def schema_errors(value, schema: dict, location: str) -> list[str]:
    """Evaluate the JSON Schema keywords used by the two checked-in schemas."""
    errors = []
    types = {"object": dict, "array": list, "string": str, "null": type(None)}
    expected = schema.get("type")
    if expected:
        allowed = expected if isinstance(expected, list) else [expected]
        if not any(isinstance(value, types[kind]) for kind in allowed):
            return [f"{location}: expected {' or '.join(allowed)}"]
    if "const" in schema and (type(value) is not type(schema["const"]) or value != schema["const"]):
        errors.append(f"{location}: invalid constant")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{location}: value not allowed")
    if isinstance(value, dict):
        properties = schema.get("properties", {})
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{location}: missing {key}")
        if len(value) < schema.get("minProperties", 0):
            errors.append(f"{location}: too few properties")
        for key, item in value.items():
            errors.extend(schema_errors(key, schema.get("propertyNames", {}), f"{location}.{key}"))
            extra = schema.get("additionalProperties", {})
            if key in properties:
                errors.extend(schema_errors(item, properties[key], f"{location}.{key}"))
            elif extra is False:
                errors.append(f"{location}: unknown property {key}")
            elif isinstance(extra, dict):
                errors.extend(schema_errors(item, extra, f"{location}.{key}"))
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{location}: too few items")
        if schema.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in value}) != len(value):
            errors.append(f"{location}: duplicate items")
        for index, item in enumerate(value):
            errors.extend(schema_errors(item, schema.get("items", {}), f"{location}[{index}]"))
    if isinstance(value, str):
        if len(value.strip()) < schema.get("minLength", 0):
            errors.append(f"{location}: empty value")
        if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
            errors.append(f"{location}: invalid format")
    return errors


def load_manifests(root: Path) -> tuple[dict, list[str]]:
    schema = read_json(root / "release/component.schema.json")
    manifests, errors = {}, []
    for path in sorted((root / "components").glob("*/component.json")):
        item = read_json(path)
        issues = schema_errors(item, schema, path.relative_to(root).as_posix())
        errors.extend(issues)
        if issues:
            continue
        name = item["name"]
        if name in manifests or path.parent.name != name:
            errors.append(f"{path.relative_to(root)}: duplicate or mismatched component name")
        manifests[name] = item
    if not manifests:
        errors.append("components: no valid manifests")
    return manifests, errors


def safe_path(value: str) -> bool:
    return bool(value) and not value.startswith(("/", "~")) and "\\" not in value and not any(
        part in {"", ".", ".."} for part in value.rstrip("/").split("/")
    )


def owners(path: str, manifests: dict) -> list[str]:
    return [name for name, item in manifests.items() if any(fnmatchcase(path, pattern) for pattern in item["owned_paths"])]


def registry_errors(manifests: dict, files: list[str]) -> list[str]:
    errors = []
    for name, item in manifests.items():
        if item["$schema"] != "../../release/component.schema.json":
            errors.append(f"{name}: incorrect schema reference")
        for pattern in item["owned_paths"]:
            if not safe_path(pattern):
                errors.append(f"{name}: unsafe owned path")
        planned_path = item["planned_path"]
        if planned_path is not None and (not safe_path(planned_path) or not planned_path.endswith("/")):
            errors.append(f"{name}: unsafe planned path")
        manifest_path = f"components/{name}/component.json"
        if owners(manifest_path, manifests) != [name]:
            errors.append(f"{name}: manifest must have exactly its own owner")
        if item["status"] == "planned":
            if item["version"] != "0.0.0" or item["checks"] or planned_path is None:
                errors.append(f"{name}: planned components need reserved 0.0.0, a future path, and no claimed checks")
            if any(path.startswith(planned_path or "\0") for path in files):
                errors.append(f"{name}: planned component contains implementation files")
            if item["owned_paths"] != [manifest_path]:
                errors.append(f"{name}: planned component may own only its manifest")
        elif item["version"] == "0.0.0" or not item["checks"]:
            errors.append(f"{name}: existing components need a version and checks")
        for dependency in item["depends_on"]:
            if dependency not in manifests:
                errors.append(f"{name}: unknown dependency {dependency}")
            elif item["status"] != "planned" and manifests[dependency]["status"] == "planned":
                errors.append(f"{name}: existing artifact depends on a planned component")

    visiting, visited = set(), set()

    def visit(name):
        if name in visiting:
            errors.append(f"{name}: component dependency cycle")
            return
        if name in visited or name not in manifests:
            return
        visiting.add(name)
        for dependency in manifests[name]["depends_on"]:
            visit(dependency)
        visiting.remove(name)
        visited.add(name)

    for name in manifests:
        visit(name)
    for path in files:
        found = owners(path, manifests)
        if len(found) != 1:
            errors.append(f"{path}: expected one owner, found {len(found)}")
    return errors


def package_errors(root: Path, manifests: dict, files: list[str]) -> list[str]:
    """Check declarative package/runtime versions without executing project code."""
    errors = []
    for relative in files:
        path = root / relative
        version = None
        if path.name == "pyproject.toml":
            version = tomllib.loads(path.read_text()).get("project", {}).get("version")
        elif path.name in {"package.json", "package-lock.json"}:
            data = read_json(path)
            version = data.get("version")
            if path.name == "package-lock.json" and data.get("packages", {}).get("", {}).get("version") != version:
                errors.append(f"{relative}: lockfile root package version differs")
        elif path.name == "__init__.py":
            for node in ast.parse(path.read_text()).body:
                if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "__version__" for t in node.targets):
                    version = ast.literal_eval(node.value)
        elif relative == "shared-contracts/openapi.json":
            version = read_json(path).get("info", {}).get("version")
        if version is not None:
            found = owners(relative, manifests)
            if len(found) == 1 and version != manifests[found[0]]["version"]:
                errors.append(f"{relative}: package/runtime version differs from {found[0]} manifest")
    return errors


def version_map(manifests: dict) -> dict:
    return {name: manifests[name]["version"] for name in sorted(manifests)}


def version_table(manifests: dict, project: dict) -> str:
    lines = ["| Component | Version | Status |", "| --- | --- | --- |"]
    release = project["release"] or "None"
    lines.append(f"| Product release | `{release}` | {project['stage']} |")
    for name in sorted(manifests):
        item = manifests[name]
        lines.append(f"| {item['display_name']} (`{name}`) | `{item['version']}` | {item['status']} |")
    return "\n".join(lines)


def replace_inventory(changelog: str, table: str) -> str:
    if changelog.count(START) != 1 or changelog.count(END) != 1:
        raise ValueError("CHANGELOG.md: exactly one inventory marker pair is required")
    start = changelog.index(START)
    end = changelog.index(END)
    unreleased = changelog.index("## [Unreleased]")
    next_section = re.search(r"^## \[", changelog[unreleased + len("## [Unreleased]"):], re.M)
    boundary = unreleased + len("## [Unreleased]") + next_section.start() if next_section else len(changelog)
    if not unreleased < start < end < boundary:
        raise ValueError("CHANGELOG.md: inventory must belong to Unreleased")
    return changelog[:start] + START + "\n" + table + "\n" + changelog[end:]


def historical_sections(changelog: str) -> str:
    match = re.search(r"^## \[(?!Unreleased\])", changelog, re.M)
    return changelog[match.start():] if match else ""


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, check=False)


def git_inventory(root: Path) -> list[str]:
    result = git(root, "ls-files", "--cached", "--others", "--exclude-standard", "-z")
    if result.returncode:
        raise ValueError("cannot obtain the current Git inventory")
    return sorted({path for path in result.stdout.split("\0") if path and (root / path).is_file()})


def baseline_errors(previous: dict, ledger: dict, manifests: dict, changed: list[str],
                    old_history: str, new_history: str, allow_release: bool = False,
                    previous_manifests: dict | None = None) -> list[str]:
    errors = []
    if not allow_release and any(previous["project"][key] != ledger["project"][key] for key in ("release", "release_date")):
        errors.append("product release changed outside an explicit release operation")
    if old_history and not new_history.endswith(old_history):
        errors.append("historical changelog sections were modified")
    for name, old in previous["components"].items():
        if name not in manifests:
            errors.append(f"{name}: component removal needs an explicit retirement/migration workflow")
            continue
        current = manifests[name]
        before = tuple(map(int, old.split(".")))
        after = tuple(map(int, current["version"].split(".")))
        if after < before:
            errors.append(f"{name}: component version regressed")
        affected = any(path not in BOOKKEEPING and
                       name in set(owners(path, manifests) + owners(path, previous_manifests or manifests))
                       for path in changed)
        if affected and current["status"] != "planned" and after <= before:
            errors.append(f"{name}: changed component needs a version increment")
    return errors


def human_changelog(text: str) -> str:
    """Remove generated inventory; a table-only edit is not a change description."""
    return re.sub(re.escape(START) + r".*?" + re.escape(END), "", text, flags=re.S)


def validate(root: Path, sync: bool = False, allow_release: bool = False,
             base: str = "HEAD") -> list[str]:
    if git(root, "rev-parse", "--verify", f"{base}^{{commit}}").returncode:
        return [f"cannot resolve Git baseline: {base}"]
    manifests, errors = load_manifests(root)
    if errors:
        return errors
    files = git_inventory(root)
    errors.extend(registry_errors(manifests, files))
    errors.extend(package_errors(root, manifests, files))
    ledger_path = root / "release/versions.json"
    ledger = read_json(ledger_path)
    errors.extend(schema_errors(ledger, read_json(root / "release/versions.schema.json"), "release/versions.json"))
    if errors:
        return errors
    if ledger["$schema"] != "./versions.schema.json":
        errors.append("release/versions.json: incorrect schema reference")
    project = ledger["project"]
    if project["stage"] == "design" and project["release"] is not None:
        errors.append("design-stage project cannot claim a software release")
    if (project["release"] is None) != (project["release_date"] is None):
        errors.append("project release and date must both be set or both be null")
    if project["release_date"] is not None:
        try:
            date.fromisoformat(project["release_date"])
        except ValueError:
            errors.append("invalid release calendar date")
    changelog_path = root / "CHANGELOG.md"
    changelog = changelog_path.read_text(encoding="utf-8")
    expected = replace_inventory(changelog, version_table(manifests, project))
    if sync and not errors:
        ledger["components"] = version_map(manifests)
        ledger_path.write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
        changelog_path.write_text(expected, encoding="utf-8")
        changelog = expected
    if ledger["components"] != version_map(manifests):
        errors.append("version ledger differs from manifests; run --sync")
    if changelog != expected:
        errors.append("Unreleased component table is stale; run --sync")
    prior = git(root, "show", f"{base}:release/versions.json")
    if prior.returncode == 0:
        previous = json.loads(prior.stdout)
        diff = git(root, "diff", "--name-only", base, "-z")
        untracked = git(root, "ls-files", "--others", "--exclude-standard", "-z")
        if diff.returncode or untracked.returncode:
            errors.append(f"cannot inspect changes against {base}")
        else:
            changed = sorted(set(filter(None, (diff.stdout + untracked.stdout).split("\0"))))
            old_log = git(root, "show", f"{base}:CHANGELOG.md")
            previous_manifests = {}
            for name in previous["components"]:
                old_manifest = git(root, "show", f"{base}:components/{name}/component.json")
                if old_manifest.returncode:
                    errors.append(f"{name}: cannot read baseline manifest")
                else:
                    previous_manifests[name] = json.loads(old_manifest.stdout)
            errors.extend(baseline_errors(previous, ledger, manifests, changed,
                                         historical_sections(old_log.stdout), historical_sections(changelog),
                                         allow_release, previous_manifests))
            if any(path not in BOOKKEEPING for path in changed) and human_changelog(old_log.stdout) == human_changelog(changelog):
                errors.append("changed artifacts need a human-readable changelog entry")
    doc_errors, _, _, _ = check_docs(root)
    errors.extend(doc_errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--sync", action="store_true", help="regenerate derived inventory; does not bump versions, stage, or commit")
    parser.add_argument("--allow-release-change", action="store_true", help="only for an explicitly authorized release operation")
    parser.add_argument("--base", default="HEAD", help="trusted comparison commit/ref; defaults to HEAD for local edits")
    args = parser.parse_args()
    try:
        errors = validate(args.root.resolve(), args.sync, args.allow_release_change, args.base)
    except (OSError, ValueError, KeyError, TypeError) as error:
        errors = [str(error)]
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print("OK: component schemas, ownership, dependencies, versions, Unreleased inventory, baseline discipline, and documentation.")
    print("Manifest checks are metadata; application security and runtime/browser tests were not run by this command.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
