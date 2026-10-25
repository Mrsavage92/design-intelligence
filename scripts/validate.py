#!/usr/bin/env python3
"""Validate maintained structures offline; does not certify website content or behavior."""
import json
import re
from datetime import date
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
GRADES = {"E0", "E1", "E2", "E3", "E4"}
REQUIRED = [
    "README.md", "AGENTS.md", "CLAUDE.md", "references/catalog.json", "routing/routes.json",
    ".agents/skills/design-research/SKILL.md", ".claude/skills/design-research/SKILL.md",
    ".agents/skills/design-research/scripts/context.py", "docs/research-protocol.md",
    "docs/installation.md", "docs/governance.md", "docs/measurement.md",
    "docs/evaluation-rubric.md", "scripts/route.py", "scripts/install_codex.py",
    "tests/benchmark-cases.json", "research-findings/TEMPLATE.md", "patterns/TEMPLATE.md",
    "project-context/TEMPLATE.md", "research-findings/index.json", "patterns/index.json",
]


def validate(root=ROOT):
    errors = []
    for name in REQUIRED:
        if not (root / name).is_file():
            errors.append(f"Missing {name}")
    if errors:
        return errors

    def read(name):
        return json.loads((root / name).read_text(encoding="utf-8"))

    def https(value):
        return isinstance(value, str) and urlparse(value).scheme == "https" and bool(urlparse(value).netloc)

    def unique(records, field, label):
        values = [record.get(field) for record in records]
        if any(not isinstance(value, str) or not value for value in values):
            errors.append(f"{label}: missing {field}")
        elif len(values) != len(set(values)):
            errors.append(f"{label}: duplicate {field}")

    catalog, routes = read("references/catalog.json"), read("routing/routes.json")
    if not isinstance(catalog, list) or not catalog or not all(isinstance(item, dict) for item in catalog):
        return ["Catalogue must be a nonempty list of objects"]
    unique(catalog, "id", "Catalogue")
    unique(catalog, "url", "Catalogue")
    for item in catalog:
        if not https(item.get("url")) or item.get("evidence_level") not in GRADES:
            errors.append(f"Invalid URL or grade: {item.get('id')}")
        if not all(item.get(key) for key in ("name", "category", "status", "note")) or "last_checked_utc" not in item:
            errors.append(f"Incomplete catalogue entry: {item.get('id')}")
        if item.get("status") == "unverified" and item.get("evidence_level") != "E0":
            errors.append(f"Unverified lead must remain E0: {item.get('id')}")
        if item.get("last_checked_utc") is not None:
            try:
                date.fromisoformat(item["last_checked_utc"])
            except (ValueError, TypeError):
                errors.append(f"Invalid source check date: {item.get('id')}")
        if item.get("evidence_level") != "E0" and not item.get("last_checked_utc"):
            errors.append(f"Observed source needs a date: {item.get('id')}")
    categories = {item.get("category") for item in catalog}
    if not isinstance(routes, dict) or not routes:
        return errors + ["Routes must be a nonempty object"]
    for route, values in routes.items():
        if not isinstance(values, list) or not values or any(value not in categories for value in values):
            errors.append(f"Unknown or empty categories in route {route}")
    from route import KEYWORDS
    if set(KEYWORDS) != set(routes):
        errors.append("Router keyword names and configured routes differ")
    for skill in (".agents", ".claude"):
        text = (root / skill / "skills/design-research/SKILL.md").read_text(encoding="utf-8")
        if not text.startswith("---\n") or not re.search(r"^name: design-research$", text, re.M) or not re.search(r"^description: .+", text, re.M):
            errors.append(f"Invalid skill metadata: {skill}")
    cases = read("tests/benchmark-cases.json")
    unique(cases, "id", "Benchmarks")
    for case in cases:
        if not case.get("prompt") or not case.get("expected"):
            errors.append(f"Incomplete benchmark: {case.get('id')}")
        if "route" in case and case["route"] not in routes:
            errors.append(f"Unknown benchmark route: {case.get('id')}")
    for folder in ("research-findings", "patterns"):
        entries = read(f"{folder}/index.json")
        unique(entries, "id", f"{folder} index")
        indexed = set()
        for item in entries:
            path = (root / item.get("path", "")).resolve()
            indexed.add(path)
            if not path.is_relative_to((root / folder).resolve()) or not path.is_file() or path.suffix != ".md":
                errors.append(f"Missing or unsafe index path: {item.get('path')}")
                continue
            text = path.read_text(encoding="utf-8")
            for field in ("id", "evidence_level", "reviewed_utc"):
                if f"{field}: {item.get(field)}" not in text:
                    errors.append(f"Index metadata differs from {item['path']}: {field}")
            try:
                date.fromisoformat(item.get("reviewed_utc", ""))
            except (ValueError, TypeError):
                errors.append(f"Invalid reviewed date: {item.get('id')}")
            if item.get("evidence_level") not in GRADES:
                errors.append(f"Invalid indexed evidence grade: {item.get('id')}")
            if folder == "research-findings" and (not item.get("project") or not item.get("source_urls") or not all(https(url) and url in text for url in item.get("source_urls", []))):
                errors.append(f"Missing project or traceable sources: {item.get('id')}")
        for path in (root / folder).rglob("*.md"):
            if path.name != "TEMPLATE.md" and path.resolve() not in indexed:
                errors.append(f"Unindexed record: {path.relative_to(root)}")
    return errors


def main():
    try:
        errors = validate()
    except (ValueError, TypeError, KeyError, OSError, AttributeError) as error:
        errors = [f"Malformed library data: {error}"]
    if errors:
        raise SystemExit("FAIL:\n" + "\n".join(errors))
    print("PASS: catalogue, route coverage, skill metadata, required resources, benchmarks and finding/pattern indexes")


if __name__ == "__main__":
    main()
