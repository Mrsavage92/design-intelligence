#!/usr/bin/env python3
"""Resolve library paths through a native skill symlink or Windows junction."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[4]
resources = {
    "readme": "README.md",
    "methodology": "docs/research-protocol.md",
    "router": "routing/routes.json",
    "catalogue": "references/catalog.json",
    "route_command": "scripts/route.py",
    "findings_template": "research-findings/TEMPLATE.md",
    "findings_index": "research-findings/index.json",
    "patterns_index": "patterns/index.json",
}
missing = [name for name in resources.values() if not (root / name).is_file()]
if missing:
    raise SystemExit("Library unavailable. Link this skill from the complete canonical checkout; see docs/installation.md. Missing: " + ", ".join(missing))
print(json.dumps({"library_root": str(root), "resources": {key: str(root / value) for key, value in resources.items()}}, indent=2))
