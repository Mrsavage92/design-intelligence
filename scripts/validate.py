#!/usr/bin/env python3
"""Validate repository structure and catalogue without network access."""
import json
from pathlib import Path
from urllib.parse import urlparse
root = Path(__file__).resolve().parents[1]
required = ["README.md","AGENTS.md","CLAUDE.md","references/catalog.json","routing/routes.json",".agents/skills/design-research/SKILL.md",".claude/skills/design-research/SKILL.md"]
for name in required:
    assert (root / name).is_file(), f"Missing {name}"
catalog = json.loads((root / "references/catalog.json").read_text())
assert len(catalog) == 30, f"Expected 30 sources, got {len(catalog)}"
ids = [x["id"] for x in catalog]
assert len(ids) == len(set(ids)), "Duplicate IDs"
for x in catalog:
    assert urlparse(x["url"]).scheme == "https"
    assert x["evidence_level"] in ("E0","E1","E2","E3","E4")
routes = json.loads((root / "routing/routes.json").read_text())
assert len(routes) >= 10
print(f"PASS: {len(catalog)} catalogue entries, {len(routes)} research routes and required files")
