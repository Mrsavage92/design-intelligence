#!/usr/bin/env python3
"""Optional bounded reachability checks. Successful HTTP is not content verification."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def check_link(item, timeout=8):
    result = {"id": item["id"], "url": item["url"], "checked_utc": datetime.now(timezone.utc).isoformat(), "status": "unconfirmed"}
    for method in ("HEAD", "GET"):
        result["method"] = method
        try:
            headers = {"User-Agent": "DesignIntelligenceLinkCheck/1.1"}
            if method == "GET":
                headers["Range"] = "bytes=0-1023"
            request = urllib.request.Request(item["url"], headers=headers, method=method)
            with urllib.request.urlopen(request, timeout=timeout) as response:
                result.update(status="reachable", http_status=response.status, final_url=response.url)
            return result
        except urllib.error.HTTPError as error:
            if method == "HEAD" and error.code in (405, 501):
                error.close()
                continue
            result.update(http_status=error.code, error=str(error))
            error.close()
            return result
        except Exception as error:
            result["error"] = str(error)[:250]
            return result
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timeout", type=float, default=8)
    parser.add_argument("--workers", type=int, choices=range(1, 5), default=4)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.timeout <= 0 or args.timeout > 30:
        parser.error("timeout must be greater than 0 and at most 30 seconds")
    catalog = json.loads((ROOT / "references/catalog.json").read_text(encoding="utf-8"))
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        results = list(executor.map(lambda item: check_link(item, args.timeout), catalog))
    report = {"scope": "HTTP reachability only; no content, visual, quality or conversion verification", "results": results}
    encoded = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(encoded + "\n", encoding="utf-8")
    if args.json:
        print(encoded)
    else:
        for result in results:
            print(result["id"], result["status"], result.get("http_status", ""), result.get("error", result.get("final_url", "")))
        print(report["scope"])


if __name__ == "__main__":
    main()
