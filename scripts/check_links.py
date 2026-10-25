#!/usr/bin/env python3
"""Optional network HEAD/GET checks. Reachability is not content verification."""
import json,urllib.request,urllib.error
from pathlib import Path
root=Path(__file__).resolve().parents[1]
catalog=json.loads((root/"references/catalog.json").read_text())
for item in catalog:
    try:
        req=urllib.request.Request(item["url"],headers={"User-Agent":"DesignIntelligenceLinkCheck/1.0"},method="HEAD")
        with urllib.request.urlopen(req,timeout=8) as response:
            print(item["id"],response.status,item["url"])
    except Exception as exc:
        print(item["id"],"UNCONFIRMED",str(exc)[:120])
print("Note: link reachability is not evidence of example quality or source accuracy.")
