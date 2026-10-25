#!/usr/bin/env python3
"""Simple deterministic research source router. Not an AI recommendation engine."""
import json
import sys
from pathlib import Path
root = Path(__file__).resolve().parents[1]
routes = json.loads((root/"routing/routes.json").read_text())
catalog = json.loads((root/"references/catalog.json").read_text())
task = " ".join(sys.argv[1:]).lower()
keywords = {"pricing":["pricing","plan","subscription"],"onboarding":["onboard","activation","signup"],"landing-page":["landing","homepage","hero"],"dashboard":["dashboard","admin","interface"],"navigation":["navigation","navbar","menu"],"email":["email","newsletter"],"advertising":["advert","campaign","ad "],"social-preview":["social","open graph"],"experimentation":["experiment","ab test","conversion"],"competitive-review":["competitor","competitive"],"presentation":["presentation","pitch","deck"]}
matches = [key for key,words in keywords.items() if any(word in task for word in words)]
selected = matches[0] if matches else "landing-page"
cats = routes[selected]
print(json.dumps({"route":selected,"categories":cats,"suggested_sources":[x for x in catalog if x["category"] in cats][:10],"note":"All URLs are discovery leads until live verified."},indent=2))
