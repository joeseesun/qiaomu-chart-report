from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_audit_module():
    path = ROOT / "scripts" / "audit_report.py"
    spec = importlib.util.spec_from_file_location("qiaomu_chart_report_audit", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load audit_report.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ChartReportRegressionTests(unittest.TestCase):
    def test_identity_is_consistent(self) -> None:
        manifest = json.loads((ROOT / "manifest.json").read_text(encoding="utf-8"))
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertEqual(manifest["name"], "qiaomu-chart-report")
        self.assertEqual(manifest["version"], "1.1.0")
        self.assertIn("name: qiaomu-chart-report", skill)
        self.assertIn('version: "1.1.0"', skill)

    def test_number_provenance_flags_numbers_missing_from_data(self) -> None:
        audit_module = load_audit_module()
        html = (
            "<!doctype html><html lang=\"zh\"><head><meta name=\"viewport\" content=\"width=device-width\">"
            "<title>t</title><style>:root{--a:1}</style></head><body><main><h1>2025 年收入 1,234.5 万</h1>"
            "<p>同比增长 18.2%，第 3 节；客单价 87 元。</p></main></body></html>"
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            page = Path(temp_dir) / "r.html"
            page.write_text(html, encoding="utf-8")
            data = Path(temp_dir) / "metrics.json"
            data.write_text('{"revenue": 1234.47, "growth": 0.1817}', encoding="utf-8")
            loose = audit_module.audit(page, allow_remote=False, data_paths=[data])
            strict = audit_module.audit(page, allow_remote=False, data_paths=[data], strict_numbers=True)
        self.assertEqual(loose["checks"]["number_provenance"]["unmatched"], ["87"])
        self.assertTrue(any("without a source" in w for w in loose["warnings"]))
        self.assertTrue(any("without a source" in e for e in strict["errors"]))

    def test_default_chart_fills_disable_global_decal(self) -> None:
        recipes = (ROOT / "assets" / "chart-recipes.js").read_text(encoding="utf-8")
        self.assertIn("decal: { show: false }", recipes)
        self.assertNotIn("decal: { show: true }", recipes)

    def test_gallery_passes_color_and_solid_fill_gates(self) -> None:
        audit_module = load_audit_module()
        result = audit_module.audit(ROOT / "reports" / "chart-gallery.html", allow_remote=False)
        self.assertTrue(result["ok"], result["errors"])
        style = result["checks"]["style_profile"]
        self.assertGreaterEqual(len(set(style["chart_color_separation"]["colorful_tokens"])), 4)
        self.assertFalse(style["solid_chart_fill"]["global_aria_decal_enabled"])

    def test_default_section_heading_style_uses_shared_left_edge(self) -> None:
        css = (ROOT / "assets" / "styles" / "vercel-monochrome.css").read_text(encoding="utf-8")
        self.assertIn(".q-section-head { display: grid; grid-template-columns: minmax(0, 1fr); gap: 8px;", css)
        self.assertNotRegex(css, r"\.q-section-head\s*\{[^}]*grid-template-columns\s*:\s*(?:\d+px|minmax\(\s*\d+px)")

    def test_quarterly_fixture_passes_section_heading_alignment_gate(self) -> None:
        audit_module = load_audit_module()
        result = audit_module.audit(ROOT / "evals" / "fixtures" / "quarterly-report.html", allow_remote=False)
        self.assertTrue(result["ok"], result["errors"])
        alignment = result["checks"]["style_profile"]["section_heading_alignment"]
        self.assertEqual(alignment["fixed_leading_column_rules"], [])
        self.assertEqual(alignment["non_left_text_rules"], [])

    def test_audit_rejects_fixed_leading_section_heading_column(self) -> None:
        audit_module = load_audit_module()
        fixture = (ROOT / "evals" / "fixtures" / "quarterly-report.html").read_text(encoding="utf-8")
        broken = fixture.replace(
            "grid-template-columns: minmax(0, 1fr); gap: 8px; margin-bottom: 30px;",
            "grid-template-columns: 190px 1fr; gap: 24px; margin-bottom: 30px;",
            1,
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "broken-alignment.html"
            path.write_text(broken, encoding="utf-8")
            result = audit_module.audit(path, allow_remote=False)
        self.assertFalse(result["ok"])
        self.assertIn(
            "section headings must share the primary left edge; fixed leading section-head columns are forbidden",
            result["errors"],
        )

    def test_audit_rejects_centered_section_heading_container(self) -> None:
        audit_module = load_audit_module()
        fixture = (ROOT / "evals" / "fixtures" / "quarterly-report.html").read_text(encoding="utf-8")
        broken = fixture.replace(
            "gap: 8px; margin-bottom: 30px;",
            "gap: 8px; margin-bottom: 30px; text-align: center;",
            1,
        )
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "centered-heading.html"
            path.write_text(broken, encoding="utf-8")
            result = audit_module.audit(path, allow_remote=False)
        self.assertFalse(result["ok"])
        self.assertIn("section heading containers must remain left-aligned by default", result["errors"])


if __name__ == "__main__":
    unittest.main()
