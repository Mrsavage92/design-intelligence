# Design Intelligence v3

Shared evidence-first research library for Claude Code and Codex. GitHub is the source of truth. The resource catalogue is a discovery index, **not evidence that sources have been inspected or that designs convert**.

## Workflow
1. Read `routing/routes.json` to choose relevant specialist domains.
2. Inspect the target project's code, users, product constraints and metrics.
3. Browse actual primary sources and specific examples when browser access exists.
4. Record exact URLs, dates, observations, limitations and evidence grades.
5. Compare options and design an original solution. Respect accessibility and mobile usability.
6. Implement only when requested; run tests and record actual results.
7. Save findings in `research-findings/`, promote corroborated patterns into `patterns/`.

## Evidence grades
E0 = bookmark or unvisited lead. E1 = directly observed dated example. E2 = recurring pattern across independent examples. E3 = relevant research or measured outcomes with limitations. E4 = validated in the target product. Gallery appearance alone never proves conversion.

## Contents
`references/catalog.json`: 30 discovery sources. `routing/routes.json`: specialist router. `docs/`: methodology, governance, evaluation and measurement. `.agents/skills/` and `.claude/skills/`: agent skills. `scripts/`: local tools. `tests/`: acceptance tests.

## Status
This is an initial GitHub publication of the v3 methodology. Source URLs require individual live verification; agent integration and end-to-end benchmarks remain outstanding. Do not claim those are complete.

## Global use and verification

See [installation](docs/installation.md) for the native user-scoped Codex link and prerequisites. Resolve the canonical library through the discovered skill path so it works from unrelated projects. The installer preserves instructions and rejects conflicts. The [router](routing/README.md) covers product/design/growth tasks with bounded research and explicit uncertainty. See [persistent findings](docs/governance.md) for indexed, source-traceable learning without another service.

Run `python scripts/validate.py` and `python -m unittest discover -s tests -v`. Existing benchmark prompts specify manual behaviors; deterministic tests and HTTP reachability do not establish that all agents, browsers or future sessions have passed them. Dated integration evidence belongs in research findings and verification reports; the initial-publication status above describes the original baseline.
