#!/usr/bin/env python3
"""Bounded keyword routing with explicit uncertainty; no AI or network dependency."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KEYWORDS = {
    "pricing": [r"pricing", r"subscription", r"moneti[sz]ation", r"billing", r"price tiers?"],
    "onboarding": [r"onboard\w*", r"activation", r"sign[ -]?up", r"first[ -]run"],
    "landing-page": [r"landing", r"homepage", r"hero"],
    "dashboard": [r"dashboard", r"admin", r"interface"],
    "navigation": [r"navigation", r"navbar", r"menu"],
    "email": [r"email", r"newsletter"],
    "advertising": [r"advert\w*", r"campaign", r"ads?"],
    "social-preview": [r"social preview", r"open graph"],
    "experimentation": [r"experiment\w*", r"a[ /-]?b test\w*", r"conversion"],
    "competitive-review": [r"competitor\w*", r"competitive"],
    "presentation": [r"presentation", r"pitch", r"deck"],
    "accessibility": [r"accessibility", r"accessible", r"wcag", r"screen reader", r"keyboard", r"focus"],
    "design-systems": [r"design system\w*", r"design tokens?", r"typography", r"spacing"],
    "components": [r"components?", r"buttons?", r"forms?", r"modals?"],
    "copywriting": [r"copywriting", r"messaging", r"microcopy", r"wording", r"headlines?", r"cta"],
    "analytics": [r"analytics", r"instrumentation", r"funnels?", r"cohorts?", r"metrics?"],
    "retention": [r"retention", r"churn", r"engagement", r"growth", r"re[ -]?activation"],
    "product-design": [r"ui", r"ux", r"product design", r"usability"],
    "performance": [r"performance", r"core web vitals", r"page speed"],
}


def route_task(task, root=ROOT):
    routes = json.loads((root / "routing/routes.json").read_text(encoding="utf-8"))
    catalog = json.loads((root / "references/catalog.json").read_text(encoding="utf-8"))
    text = task.lower()
    matches = []
    for name, words in KEYWORDS.items():
        score = sum(bool(re.search(r"\b(?:" + word + r")\b", text)) for word in words)
        if score:
            matches.append((name, score))
    matches.sort(key=lambda match: -match[1])
    lightweight = bool(re.search(r"\b(change|replace|fix|correct)\b", text)) and bool(
        re.search(r"\b(typo|wording|label|cta)\b", text)
    ) and not re.search(r"\b(research|redesign|compare|test|experiment)\b", text)
    selected = [] if lightweight else [name for name, _ in matches[:3]]
    categories = []
    for name in selected:
        if routes[name][0] not in categories:
            categories.append(routes[name][0])
    for name in selected:
        for category in routes[name]:
            if category not in categories and len(categories) < 3:
                categories.append(category)
    sources = []
    groups = [[item for item in catalog if item["category"] == category] for category in categories]
    for index in range(max((len(group) for group in groups), default=0)):
        for group in groups:
            if index < len(group) and len(sources) < 10:
                sources.append(group[index])
    return {
        "route": selected[0] if selected else None,
        "matched_routes": [name for name, _ in matches],
        "selected_routes": selected,
        "categories": categories,
        "suggested_sources": sources,
        "research_depth": "lightweight" if lightweight else "focused" if selected else "needs-context",
        "reason": "Exact small edit: use project context; external research is optional." if lightweight
        else "Keyword matches require project-context review; ties are not confidence scores." if selected
        else "No supported task signal: inspect context or choose a route explicitly; no landing-page default.",
        "note": "Catalogue entries are discovery leads. Consult original sources and record access limitations.",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task", nargs="+")
    args = parser.parse_args()
    print(json.dumps(route_task(" ".join(args.task)), indent=2))


if __name__ == "__main__":
    main()
