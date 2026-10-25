# Codex integration verification — 2026-10-25

## Scope and baseline

This run reviewed README, agent instructions and both skill manifests, all methodology/governance/measurement documents, the 30-source catalogue, routes, four original scripts, evidence templates/indexes and eight manual benchmark prompts. No existing product was redesigned. The original offline validator passed, despite accessibility and retention requests wrongly defaulting to landing-page research. The original copied-folder installation instructions did not resolve the full library from other projects.

## Installed behavior

One native user-scoped `~/.agents/skills/design-research` link points to the complete canonical GitHub checkout. The installer does not modify agent instruction files or configuration, rejects conflicts/duplicates and can verify an existing installation. On the tested Windows host it created a symbolic link; junction fallback was not exercised live. Resource resolution returned the correct absolute catalogue, methodology and routing paths from outside the checkout.

Codex CLI **0.162.1** generated the local app-server protocol schema. Two separate fresh app-server processes ran initialization and `skills/list` with `forceReload: true`, each for two unrelated working directories. All four results contained exactly one enabled `design-research`, scope `user`, and no discovery errors. No model thread, worker or turn was started. This verifies native discovery across host process restarts; it does not claim a computer reboot, desktop UI restart or automatic skill selection on a future prompt was observed. Implicit invocation remains enabled by default through the skill description.

Hashes confirmed unchanged existing global Codex/Claude instructions, the parent project's AGENTS.md and Codex configuration. This repository's AGENTS.md and CLAUDE.md remain unchanged. No project-specific instruction files were overwritten.

## Executed checks

| Check | Actual result | Boundary |
| --- | --- | --- |
| Original `scripts/validate.py` | PASS | Original checks were too shallow to establish integration. |
| Revised `scripts/validate.py` | PASS | Catalogue, route coverage, resources, metadata, benchmarks and index integrity; offline only. |
| `python -m unittest discover -s tests -v` | 15 tests PASS | Includes 12 expertise subcases and six routing expectations added to existing manual cases; does not prove their prose behaviors. |
| Built-in `skill-creator/scripts/quick_validate.py` | PASS | Initially failed because host Python lacked PyYAML; PyYAML 6.0.3 was installed only into this run's temporary work directory to execute the built-in helper. Library scripts require no third-party packages. |
| Global installer and `--check` | PASS | One link; idempotency/conflict behavior also exercised in isolated test homes. |
| Native discovery | 4/4 PASS | Two fresh metadata-only host processes, two unrelated directories each. |
| Original catalogue reachability | 24/30 reachable, 6 unconfirmed | HEAD-only results; no content/quality verification. |
| Revised checker on original URLs | 25/30 reachable, 5 unconfirmed | Material Design returned HEAD 405, then GET 206. TLS verification stayed enabled. |
| Live pricing example | 3/3 first-party page fetches HTTP 200 | Fresh Firecrawl Markdown retrieval; no UI, interaction, mobile or conversion tests. |
| Instruction preservation | 4/4 existing file hashes unchanged | Includes configuration; no claim about files outside the touched scope. |
| `git diff --check` | PASS | Whitespace integrity only. |

The live [pricing finding](../research-findings/20261025-saas-pricing-integration.md) records exact source URLs, dates, retrieval ids, observations, assumptions, counterexamples, original options, measurement hypotheses and a not-implemented outcome. A narrowly scoped [E2 recurring convention](../patterns/self-service-with-enterprise-sales.md) links those three independent examples without claiming conversion uplift. Indexes make both records discoverable and prevent silent orphaning.

## Link investigation and repair

The Python checker reported TLS certificate verification failures for Posts.design, Storybook and the original ProfitWell URL, HTTP 429 for Adfolio, and HEAD 404 for Similarweb. Fresh Firecrawl page retrieval returned content HTTP 200 for Posts.design, Storybook, Adfolio and Similarweb, so these are retained as access-method differences, not declared dead domains. The checker does not bypass TLS or automatically retry rate limits.

Firecrawl confirmed a **content HTTP 404** at `https://www.paddle.com/profitwell`. Live search found and live retrieval confirmed HTTP 200 at [Paddle's pricing-strategy guide](https://www.paddle.com/resources/pricing-strategy). Source-25 now points there with an E1 content-inspection date and vendor-advice limitation. This does not elevate vendor statements to independent outcome research. Reachability results for the old URL must not be reported as a check of its replacement.

## Remaining boundaries

The router is a bounded English keyword aid; it exposes matches and uncertainty, and cannot reliably interpret negation, implied intent or arbitrary languages. Agents still select expertise using actual project context. Large installed skill lists may be shortened by the host. Catalogue entries other than the specifically observed replacement remain discovery leads, even when their homepages are reachable.

Claude's manifest and resource-location instructions were reviewed and kept aligned; a live Claude installation/acceptance run was not performed. The Windows junction fallback and non-Windows installer path were not executed live. The remaining manual benchmark behaviors (offline honesty, injection handling, implementation quality, etc.) were not independently tested as a full behavioral suite. Desktop composer selection, mobile/accessibility/performance testing and target-product outcomes remain separate checks. This library supplies no browser, daemon, scheduler or guarantee of automatic future compliance.

The changes are intended for a dedicated pull request. Publication does not imply merge approval. No production deployment, main-branch merge, credentials, proprietary assets or private project content is part of this verification.
