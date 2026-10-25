#!/usr/bin/env python3
"""Search the source catalogue locally by keyword."""
import json,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
items=json.loads((root/"references/catalog.json").read_text(encoding="utf-8"))
query=" ".join(sys.argv[1:]).lower()
for item in items:
    if not query or query in " ".join(str(v) for v in item.values()).lower():
        print(f'{item["name"]} | {item["category"]} | {item["url"]} | {item["status"]}')
