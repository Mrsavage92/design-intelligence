"""Deterministic regression checks; agent behavior and live browsing remain separate."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from route import route_task
from validate import validate
from install_codex import install
from check_links import check_link


class RoutingTests(unittest.TestCase):
    def test_requested_expertise(self):
        cases = {
            "Review SaaS pricing and monetisation": "pricing",
            "Improve SaaS onboarding activation": "onboarding",
            "Review landing homepage hero": "landing-page",
            "Review design systems and tokens": "design-systems",
            "Review reusable components": "components",
            "Improve accessibility and keyboard focus": "accessibility",
            "Research copywriting and messaging": "copywriting",
            "Review product analytics instrumentation": "analytics",
            "Plan an A/B test experiment": "experimentation",
            "Compare competitors": "competitive-review",
            "Improve product retention and churn": "retention",
            "Review UI UX usability": "product-design",
        }
        for task, expected in cases.items():
            with self.subTest(task=task):
                result = route_task(task)
                self.assertEqual(result["route"], expected)
                self.assertGreaterEqual(len(result["categories"]), 1)
                self.assertLessEqual(len(result["categories"]), 3)
                self.assertEqual(set(result["categories"]), {item["category"] for item in result["suggested_sources"]})

    def test_multiple_expertise_and_no_substring_fallback(self):
        result = route_task("Review pricing and onboarding accessibility")
        self.assertEqual(set(result["selected_routes"]), {"pricing", "onboarding", "accessibility"})
        self.assertEqual(len(result["categories"]), 3)
        self.assertIsNone(route_task("Plan database backup")['route'])

    def test_small_edit_has_no_external_research(self):
        result = route_task("Change CTA wording")
        self.assertEqual(result["research_depth"], "lightweight")
        self.assertEqual(result["suggested_sources"], [])

    def test_existing_manual_benchmarks_remain_distinct(self):
        cases = json.loads((ROOT / "tests/benchmark-cases.json").read_text(encoding="utf-8"))
        for case in cases:
            result = route_task(case["prompt"])
            if "route" in case:
                self.assertIn(case["route"], result["selected_routes"], case["id"])
            if case["id"] == "small-edit":
                self.assertEqual(result["research_depth"], "lightweight")


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name) / "library"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", "__pycache__", ".codebase-memory"))

    def tearDown(self):
        self.directory.cleanup()

    def test_actual_library(self):
        self.assertEqual(validate(), [])

    def test_rejects_broken_category(self):
        path = self.root / "routing/routes.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        value["pricing"] = ["nonexistent-category"]
        path.write_text(json.dumps(value), encoding="utf-8")
        self.assertTrue(any("Unknown or empty categories" in item for item in validate(self.root)))

    def test_accepts_new_catalogue_entry_without_magic_count(self):
        path = self.root / "references/catalog.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        value.append({**value[0], "id": "new-source", "url": "https://example.org/new"})
        path.write_text(json.dumps(value), encoding="utf-8")
        self.assertEqual(validate(self.root), [])

    def test_missing_resources_and_duplicate_ids_fail(self):
        (self.root / "docs/research-protocol.md").unlink()
        self.assertTrue(any("Missing docs/research-protocol.md" in item for item in validate(self.root)))
        shutil.copyfile(ROOT / "docs/research-protocol.md", self.root / "docs/research-protocol.md")
        path = self.root / "references/catalog.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        value[1]["id"] = value[0]["id"]
        path.write_text(json.dumps(value), encoding="utf-8")
        self.assertTrue(any("duplicate id" in item for item in validate(self.root)))

    def test_index_cannot_escape_record_directory(self):
        (self.root / "research-findings/index.json").write_text(json.dumps([{
            "id": "escape", "path": "README.md", "reviewed_utc": "2026-10-25", "evidence_level": "E0"
        }]), encoding="utf-8")
        self.assertTrue(any("unsafe index path" in item for item in validate(self.root)))

    def test_checks_still_run_with_python_optimization(self):
        path = self.root / "references/catalog.json"
        value = json.loads(path.read_text(encoding="utf-8"))
        value[0]["url"] = "https://"
        path.write_text(json.dumps(value), encoding="utf-8")
        result = subprocess.run([sys.executable, "-O", str(self.root / "scripts/validate.py")], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)


class InstallationTests(unittest.TestCase):
    def test_install_idempotency_and_preservation(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(os.environ, {"CODEX_HOME": str(Path(temporary) / ".codex")}):
            home = Path(temporary)
            instruction = home / "AGENTS.md"
            instruction.write_text("Keep existing instructions", encoding="utf-8")
            target = home / ".agents/skills/design-research"
            install(target, home=home)
            install(target, home=home, check=True)
            install(target, home=home)
            self.assertEqual(instruction.read_text(encoding="utf-8"), "Keep existing instructions")
            result = subprocess.run([sys.executable, str(target / "scripts/context.py")], cwd=temporary, capture_output=True, text=True, check=True)
            self.assertEqual(Path(json.loads(result.stdout)["library_root"]), ROOT)
            # Remove the link only; never recurse into the canonical checkout.
            if target.is_symlink():
                target.unlink()
            else:
                target.rmdir()

    def test_conflicting_copy_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(os.environ, {"CODEX_HOME": str(Path(temporary) / ".codex")}):
            home = Path(temporary)
            target = home / ".agents/skills/design-research"
            target.mkdir(parents=True)
            sentinel = target / "SKILL.md"
            sentinel.write_text("Existing custom skill", encoding="utf-8")
            with self.assertRaises(ValueError):
                install(target, home=home)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "Existing custom skill")

    def test_duplicate_legacy_install_is_not_created(self):
        with tempfile.TemporaryDirectory() as temporary, patch.dict(os.environ, {"CODEX_HOME": str(Path(temporary) / ".codex")}):
            home = Path(temporary)
            (home / ".codex/skills/design-research").mkdir(parents=True)
            target = home / ".agents/skills/design-research"
            with self.assertRaises(ValueError):
                install(target, home=home)
            self.assertFalse(target.exists())


class LinkTests(unittest.TestCase):
    def test_head_not_allowed_falls_back_to_get(self):
        response = unittest.mock.MagicMock()
        response.__enter__.return_value.status = 200
        response.__enter__.return_value.url = "https://example.org/final"
        with patch("urllib.request.urlopen", side_effect=[HTTPError("https://example.org", 405, "HEAD rejected", {}, None), response]) as opener:
            result = check_link({"id": "test", "url": "https://example.org"})
            self.assertEqual(result["method"], "GET")
            self.assertEqual(result["status"], "reachable")
            self.assertEqual(opener.call_count, 2)

    def test_failure_stays_unconfirmed(self):
        with patch("urllib.request.urlopen", side_effect=HTTPError("https://example.org", 404, "Missing", {}, None)):
            result = check_link({"id": "test", "url": "https://example.org"})
            self.assertEqual(result["status"], "unconfirmed")
            self.assertEqual(result["http_status"], 404)


if __name__ == "__main__":
    unittest.main()
