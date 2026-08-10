from __future__ import annotations

import importlib.util
import json
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
        self.assertEqual(manifest["version"], "1.0.0")
        self.assertIn("name: qiaomu-chart-report", skill)
        self.assertIn('version: "1.0.0"', skill)

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


if __name__ == "__main__":
    unittest.main()
