#!/usr/bin/env python3
"""Check canonical Markdown and inactive templates without network access.

The English-language guard rejects Cyrillic; it is not natural-language detection.
This checker does not validate product claims, external links, or authorization.
"""

# Adapted from The OA; see docs/reference/theoa-tooling-license.txt.

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
HEADING = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
CYRILLIC = re.compile(r"[\u0400-\u04ff]")


def documentation_files(root: Path) -> list[Path]:
    files = {
        root / name
        for name in ("README.md", "AGENTS.md", "CONTRIBUTING.md", "CHANGELOG.md")
        if (root / name).is_file()
    }
    for directory in (root / "docs", root / ".agents", root / "shared-contracts", root / "provereno-ui"):
        if directory.is_dir():
            for current, directories, names in os.walk(directory):
                directories[:] = [name for name in directories if name not in {
                    "node_modules", ".venv", "__pycache__", ".git", ".local", "dist", "build"
                }]
                files.update(Path(current) / name for name in names
                             if name.endswith((".md", ".md.example")))
    return sorted(files)


def prose_lines(text: str, report) -> list[tuple[int, str]]:
    lines = []
    fence = None
    opened_at = None
    for number, line in enumerate(text.splitlines(), 1):
        match = FENCE.match(line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence, opened_at = marker, number
            elif marker[0] == fence[0] and len(marker) >= len(fence):
                if not line[match.end():].strip():
                    fence = None
            continue
        if fence is None:
            lines.append((number, line))
    if fence is not None:
        report(opened_at, "unclosed fenced code block")
    return lines


def heading_ids(text: str) -> set[str]:
    result = set()
    counts: dict[str, int] = {}
    for _, line in prose_lines(text, lambda *_: None):
        match = HEADING.match(line)
        if not match:
            continue
        title = re.sub(r"<[^>]*>", "", match.group(1)).lower()
        slug = re.sub(r"[^\w\- ]", "", title).replace(" ", "-")
        count = counts.get(slug, 0)
        counts[slug] = count + 1
        result.add(f"{slug}-{count}" if count else slug)
    return result


def check(root: Path) -> tuple[list[str], int, int, int]:
    errors: list[str] = []
    documents = documentation_files(root)
    links = 0
    examples = sorted((root / "docs").rglob("*.json.example"))
    for path in documents:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(root)

        def report(number, message):
            errors.append(f"{relative}:{number}: {message}")

        if not text.endswith("\n"):
            report(1, "missing final newline")
        for number, line in enumerate(text.splitlines(), 1):
            if CYRILLIC.search(line):
                report(number, "Cyrillic text in canonical English documentation")
            if line.rstrip() != line:
                report(number, "trailing whitespace")

        for number, line in prose_lines(text, report):
            for match in LINK.finditer(line):
                destination = match.group(1).strip()
                if destination.startswith("<"):
                    destination = destination[1:].split(">", 1)[0]
                else:
                    destination = destination.split(maxsplit=1)[0]
                parsed = urlsplit(destination)
                if parsed.scheme or parsed.netloc:
                    continue
                links += 1
                target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
                if not target.exists():
                    report(number, f"missing local target: {destination}")
                elif parsed.fragment and (target.suffix == ".md" or target.name.endswith(".md.example")):
                    if unquote(parsed.fragment) not in heading_ids(target.read_text(encoding="utf-8")):
                        report(number, f"missing local heading: {destination}")

    for path in examples:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (ValueError, UnicodeError) as error:
            errors.append(f"{path.relative_to(root)}: invalid JSON example: {error}")
    for skill in sorted((root / ".agents/skills").glob("*/SKILL.md")):
        text = skill.read_text(encoding="utf-8")
        front = re.match(r"\A---\nname: ([a-z0-9]+(?:-[a-z0-9]+)*)\ndescription: ([^\n]+)\n---\n", text)
        if not front or front.group(1) != skill.parent.name or not front.group(2).strip():
            errors.append(f"{skill.relative_to(root)}: invalid project skill frontmatter/name")
    return errors, len(documents), links, len(examples)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    if not (root / "README.md").is_file():
        parser.error("root must contain README.md")
    errors, documents, links, examples = check(root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"OK: {documents} Markdown documents/templates, {links} local links, {examples} JSON examples.")
    print("Cyrillic guard, code fences, whitespace, and local targets passed; external URLs and runtime security were not checked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
