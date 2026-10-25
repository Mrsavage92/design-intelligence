---
id: research-20261025-saas-pricing-integration
reviewed_utc: 2026-10-25
project: design-intelligence-integration-test
source_url: https://linear.app/pricing
access_method: live-firecrawl-markdown-maxAge-0
evidence_level: E1
status: reviewed-with-limitations
---
# SaaS pricing research integration test

## Decision and audience

Hypothetical B2B collaboration SaaS for small teams deciding between a free and paid plan. The research question is how a pricing page can explain eligibility, limitations and next steps. This tests the library, not a redesign of any existing project. Audience, baseline conversion, actual pricing model, brand and customer feedback are assumptions or unknown. No target repository, analytics access or customer data was supplied.

Route used: `Review a SaaS pricing page for small teams choosing a subscription tier`. The deterministic router selects pricing, with pricing/trust/ux-research categories. Catalogue galleries and vendor commentary are discovery leads; the test instead retrieves original product pages identified through live search. It does not need every research category or an analytics integration.

## Direct observations and provenance

All three first-party pages were retrieved on **2026-10-25 UTC** through Firecrawl `firecrawl_scrape`, requesting Markdown with `maxAge: 0`; each returned HTTP 200. These are dated E1 content observations, not design-performance validation. Exact access receipts are retained by the local integration report.

| Original source | Direct content observations | Retrieval identifier |
| --- | --- | --- |
| [Linear pricing](https://linear.app/pricing) | Free, Basic, Business and Enterprise sections; self-service start links and an Enterprise sales link; yearly billing text; a detailed feature comparison follows. | `01a171c6-f0e6-73dd-ad82-346bddc03724` |
| [Slack pricing](https://slack.com/pricing) | Free, Pro, Business+ and Enterprise+ sections; free-plan limits; monthly/annual wording; a temporary offer with eligibility terms; enterprise sales link and feature comparison. | `01a171c6-f4cc-760d-ad2e-668ab0a45017` |
| [Notion pricing](https://www.notion.com/pricing) | Plans described for individuals, small teams, growing businesses and larger organizations; signup and enterprise sales paths; grouped plan sections and a longer comparison. | `01a171c6-f880-760c-ab5b-f53e5b6ae963` |

## Inferences and uncertainty

Self-service entry alongside an enterprise contact path recurs in three independent product examples. That supports an E2 convention for this narrow content pattern, not evidence that it improves conversion. Billing clarity and disclosed limits are reasonable hypotheses to assess with target users. Vendor trust logos, recommendation badges and performance wording are not independently verified outcomes.

Extraction has limitations: Linear's animated numeric text is duplicated in Markdown, and feature-table states can lose spatial relationships. Prices are deliberately not adopted from this output. No screenshot, billing-toggle interaction, checkout, mobile viewport, screen reader, keyboard, contrast or measured performance test ran. The locale and any personalization may differ from another visitor's experience. A successful fresh-fetch request does not guarantee globally uniform content.

## Counterexamples

Notion's text groups plan content into audience-oriented sections rather than requiring a single flat four-card layout. Slack's promotional detail adds eligibility and expiry considerations. These examples argue against blindly copying a supposedly universal pricing layout or unexplained discount treatment.

## Applicability and original adaptation

Option A: concise tier summaries with the target product's real limits, billing unit/cadence and one appropriate next step per tier; place a detailed comparison below. Appropriate if customer interviews indicate clear plan segments; risks include hiding important limits in the summary.

Option B: a short use-case guide before the tier comparison, if teams struggle to identify their needs. This costs more reading time and requires real audience evidence; it should not recommend a paid tier without a defensible reason. Keep the existing page if project evidence does not justify a change.

Reuse the principle, not competitor copy, screenshots, assets or plan economics. The target product's existing design system and specialist skills govern implementation. On mobile, validate readable comparison alternatives; use semantic headings, explicit link labels and keyboard-accessible controls. These are future checks, not completed tests.

## Measurement hypothesis

Hypothesis: explicit plan eligibility and billing disclosure may reduce plan-selection confusion. Before testing, define eligible visitor segments, baseline window, pricing-view and plan-start events, completion denominator, support-confusion and refund guardrails, sample size and experiment duration. No uplift, revenue change, causal result or E4 target-product validation is claimed.

## Implementation outcome and lessons

Status: **not implemented**. No existing project was changed. Live search and fresh page retrieval worked; the installed skill/router can support a focused evidence record with limitations. The example shows why copied skill folders need a reliable canonical-library path and why text retrieval must be distinguished from visual/interaction inspection.

## Source restrictions and next review

Public page content was summarized; no proprietary images, logo files, full pages, credentials or customer data are stored in Git. Recheck original pages before consequential reuse, especially offer terms, billing text and plan limits. Findings belong to this integration-test context, not an existing product's validated customer knowledge.
