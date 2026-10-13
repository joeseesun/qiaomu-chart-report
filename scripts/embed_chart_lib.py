#!/usr/bin/env python3
"""Inline pinned chart libraries and Qiaomu recipes into an HTML template."""

from __future__ import annotations

import argparse
from pathlib import Path


TOKENS = {
    "echarts": "<!-- QIAOMU_VENDOR:ECHARTS -->",
    "d3": "<!-- QIAOMU_VENDOR:D3 -->",
    "recipes": "<!-- QIAOMU_CHART_RECIPES -->",
    "style": "<!-- QIAOMU_STYLE:VERCEL_MONOCHROME -->",
}


def script_tag(source: str, label: str) -> str:
    safe = source.replace("</script", "<\\/script")
    return f'<script data-qiaomu-vendor="{label}">\n{safe}\n</script>'


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("template", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--libraries", default="echarts,d3", help="Comma-separated: echarts,d3")
    args = parser.parse_args()

    skill_dir = Path(__file__).resolve().parent.parent
    sources = {
        "echarts": skill_dir / "assets/vendor/echarts-6.1.0/echarts.min.js",
        "d3": skill_dir / "assets/vendor/d3-7.9.0/d3.min.js",
        "recipes": skill_dir / "assets/chart-recipes.js",
        "style": skill_dir / "assets/styles/vercel-monochrome.css",
    }
    selected = {item.strip() for item in args.libraries.split(",") if item.strip()}
    unknown = selected - {"echarts", "d3"}
    if unknown:
        parser.error(f"unknown libraries: {', '.join(sorted(unknown))}")
    if not args.template.is_file():
        parser.error(f"template not found: {args.template}")

    html = args.template.read_text(encoding="utf-8")
    for name in ("echarts", "d3"):
        marker = TOKENS[name]
        if marker not in html and name in selected:
            parser.error(f"template missing token: {marker}")
        replacement = script_tag(sources[name].read_text(encoding="utf-8"), name) if name in selected else ""
        html = html.replace(marker, replacement)
    if TOKENS["recipes"] not in html:
        parser.error(f"template missing token: {TOKENS['recipes']}")
    html = html.replace(TOKENS["recipes"], script_tag(sources["recipes"].read_text(encoding="utf-8"), "qiaomu-recipes"))
    if TOKENS["style"] in html:
        css = sources["style"].read_text(encoding="utf-8").replace("</style", "<\\/style")
        html = html.replace(TOKENS["style"], f'<style data-qiaomu-style="vercel-monochrome">\n{css}\n</style>')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8")
    print(f"wrote {args.output.resolve()} ({args.output.stat().st_size} bytes; libraries={','.join(sorted(selected))})")


if __name__ == "__main__":
    main()
