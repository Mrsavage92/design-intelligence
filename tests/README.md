# Benchmark suite
Cases are manual acceptance prompts. Run them independently in both Claude Code and Codex, record observed behavior and failures. Passing a JSON schema check does not demonstrate that the agents can browse, reason or implement correctly.

Run deterministic regression checks with Python 3.10+:

```text
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/check_links.py --output link-check.json
```

The unit suite covers the requested expertise routes, multi-domain and lightweight/unknown tasks, non-overwriting/idempotent installation, link resolution from another CWD, duplicate install rejection, missing resources, malformed route references, growing catalogues, index containment and validation under `python -O`. Link checks use at most four workers and fall back to bounded GET only for HEAD 405/501. Results retain timestamps and redirects without modifying catalogue evidence grades. Non-2xx, TLS errors and rate limits stay unconfirmed; no TLS bypass is used. Exit zero means the check executed, not that every URL is reachable. Link output is an artifact, not a measured quality or conversion score.

Manual scenarios in `acceptance.md` and `benchmark-cases.json` still require actual agent/tool execution. Optional `route` fields support automated routing assertions; their prose expectations remain manual. Keep raw host-discovery receipts and live retrieval identifiers locally, and commit only public-safe findings and a dated summary. A fresh native host `skills/list` check verifies metadata discovery without invoking an extra model session; it does not prove autonomous behavior on every future task.
