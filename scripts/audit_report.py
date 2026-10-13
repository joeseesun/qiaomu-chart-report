#!/usr/bin/env python3
"""Static audit for a self-contained HTML report."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import urlparse


PLACEHOLDERS = [
    r"\bTODO\b",
    r"\bTBD\b",
    r"lorem ipsum",
    r"\{\{[^{}]+\}\}",
    r"\[[A-Z][A-Z _-]{2,}\]",
]


NUMBER_TOKEN = re.compile(r"(?<![\w.#-])-?\d[\d,]*(?:\.\d+)?%?")


def _numeric_values(text: str) -> list[tuple[float, int, bool]]:
    values = []
    for token in NUMBER_TOKEN.findall(text):
        percent = token.endswith("%")
        raw = token.rstrip("%").replace(",", "")
        try:
            value = float(raw)
        except ValueError:
            continue
        decimals = len(raw.split(".")[1]) if "." in raw else 0
        values.append((value, decimals, percent))
    return values


def _is_trivial_number(value: float, decimals: int, percent: bool) -> bool:
    if percent:
        return False
    if decimals == 0 and 0 <= value <= 12:
        return True  # section numbers, small counts, months
    if decimals == 0 and 1900 <= value <= 2100:
        return True  # years
    return False


def number_provenance(markup: str, data_paths: list[Path]) -> dict[str, object]:
    """Every non-trivial number shown in the report should exist in the data or metrics files."""
    visible = re.sub(r"<(script|style)\b[^>]*>.*?</\1>", " ", markup, flags=re.I | re.S)
    visible = re.sub(r"<[^>]+>", " ", visible)
    shown = [item for item in _numeric_values(visible) if not _is_trivial_number(*item)]
    source: list[float] = []
    for data_path in data_paths:
        source.extend(value for value, _, _ in _numeric_values(data_path.read_text(encoding="utf-8", errors="replace")))

    def matches(value: float, decimals: int, percent: bool) -> bool:
        tolerance = 0.5 * 10 ** (-decimals) + 1e-9
        candidates = [value, value / 100] if percent else [value]
        for target in candidates:
            scale_tolerance = tolerance / 100 if (percent and target != value) else tolerance
            if any(abs(item - target) <= scale_tolerance for item in source):
                return True
        return False

    unmatched = sorted({f"{v:g}{'%' if pct else ''}" for v, d, pct in shown if not matches(v, d, pct)})
    return {"data_files": [str(path) for path in data_paths], "checked": len(shown), "unmatched": unmatched}


def occurrences(pattern: str, text: str, flags: int = re.I | re.S) -> int:
    return len(re.findall(pattern, text, flags))


def remote_urls(text: str) -> list[str]:
    urls: set[str] = set()
    for raw in re.findall(r'''(?:src|href)\s*=\s*["']([^"']+)["']''', text, re.I):
        parsed = urlparse(raw.strip())
        if parsed.scheme in {"http", "https"}:
            urls.add(raw.strip())
    for raw in re.findall(r'''url\(\s*["']?([^"')]+)''', text, re.I):
        parsed = urlparse(raw.strip())
        if parsed.scheme in {"http", "https"}:
            urls.add(raw.strip())
    return sorted(urls)


def section_heading_alignment_violations(markup: str) -> dict[str, object]:
    """Find section-heading CSS that breaks the default shared left edge."""
    css = "\n".join(re.findall(r"<style\b[^>]*>(.*?)</style>", markup, re.I | re.S))
    fixed_leading_columns: list[str] = []
    non_left_alignment: list[str] = []
    section_head_selector = re.compile(
        r"(?:\.q-section-head\b|\.section-head\b|\[data-qiaomu-section-head(?:\]|[=\s]))",
        re.I,
    )
    fixed_first_column = re.compile(
        r"^\s*(?:"
        r"\d+(?:\.\d+)?(?:px|rem|em|vw)|"
        r"minmax\(\s*\d+(?:\.\d+)?(?:px|rem|em|vw)\s*,[^)]+\)"
        r")\s+",
        re.I,
    )
    for selector, declarations in re.findall(r"([^{}]+)\{([^{}]*)\}", css, re.S):
        selector = selector.strip()
        if not section_head_selector.search(selector):
            continue
        columns_match = re.search(r"grid-template-columns\s*:\s*([^;]+)", declarations, re.I)
        if columns_match and fixed_first_column.search(columns_match.group(1)):
            fixed_leading_columns.append(f"{selector}: {columns_match.group(1).strip()}")
        alignment_match = re.search(r"text-align\s*:\s*(center|right|end)\b", declarations, re.I)
        if alignment_match:
            non_left_alignment.append(f"{selector}: {alignment_match.group(1).lower()}")
    return {
        "fixed_leading_column_rules": fixed_leading_columns,
        "non_left_text_rules": non_left_alignment,
    }


def audit(
    path: Path,
    allow_remote: bool,
    data_paths: list[Path] | None = None,
    strict_numbers: bool = False,
) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    lower = text.lower()
    markup = re.sub(r"<script\b[^>]*>.*?</script>", "<script></script>", text, flags=re.I | re.S)
    markup_lower = markup.lower()
    errors: list[str] = []
    warnings: list[str] = []
    checks: dict[str, object] = {}

    required = {
        "doctype": bool(re.search(r"<!doctype\s+html", text, re.I)),
        "lang": bool(re.search(r"<html\b[^>]*\blang\s*=", text, re.I)),
        "viewport": bool(re.search(r"<meta\b[^>]*name=[\"']viewport[\"']", text, re.I)),
        "title": bool(re.search(r"<title>\s*[^<\s][^<]*</title>", text, re.I)),
        "main": bool(re.search(r"<main\b", text, re.I)),
        "css_tokens": ":root" in lower and "--" in text,
    }
    checks["required_structure"] = required
    for name, passed in required.items():
        if not passed:
            errors.append(f"missing required structure: {name}")

    h1_count = occurrences(r"<h1\b", text)
    checks["h1_count"] = h1_count
    if h1_count != 1:
        errors.append(f"expected exactly one h1, found {h1_count}")

    remote = remote_urls(markup)
    checks["remote_resources"] = remote
    if remote and not allow_remote:
        errors.append(f"remote resources are disabled by default: {len(remote)} found")
    elif remote:
        warnings.append(f"authorized remote resources remain runtime dependencies: {len(remote)}")

    placeholders = sorted(
        {pattern for pattern in PLACEHOLDERS if re.search(pattern, markup, re.I)}
    )
    checks["placeholder_patterns"] = placeholders
    if placeholders:
        errors.append(f"unfinished placeholder patterns found: {len(placeholders)}")

    img_count = occurrences(r"<img\b", markup)
    img_alt_count = occurrences(r"<img\b[^>]*\balt\s*=", markup)
    checks["images"] = {"count": img_count, "with_alt": img_alt_count}
    if img_alt_count != img_count:
        errors.append(f"all images need alt attributes: {img_alt_count}/{img_count}")

    svg_count = occurrences(r"<svg\b", markup)
    accessible_svg = occurrences(r"<svg\b[^>]*(?:aria-label|aria-labelledby|aria-hidden|role\s*=)", markup)
    checks["svg"] = {"count": svg_count, "with_semantics": accessible_svg}
    if accessible_svg != svg_count:
        warnings.append(f"SVG semantics incomplete: {accessible_svg}/{svg_count}")

    chart_tags = re.findall(
        r"<[^>]+\sdata-qiaomu-chart(?:\s*=\s*(?:\"[^\"]*\"|'[^']*'|[^\s>]+))?(?=\s|>)[^>]*>",
        markup,
        re.I,
    )
    chart_semantics = sum(
        1 for tag in chart_tags if re.search(r"\b(?:aria-label|aria-labelledby|role)\s*=", tag, re.I)
    )
    chart_figures = occurrences(r"<figure\b[^>]*\bdata-qiaomu-chart-figure", markup)
    checks["charts"] = {
        "count": len(chart_tags),
        "with_semantics": chart_semantics,
        "chart_figures": chart_figures,
        "runtime_ready_hook": "__QIAOMU_CHARTS_READY__" in text,
    }
    if chart_semantics != len(chart_tags):
        errors.append(f"chart containers need role/ARIA semantics: {chart_semantics}/{len(chart_tags)}")
    if chart_tags and chart_figures < len(chart_tags):
        errors.append(f"chart containers need data-qiaomu-chart-figure wrappers: {chart_figures}/{len(chart_tags)}")
    if chart_tags and "__QIAOMU_CHARTS_READY__" not in text:
        warnings.append("chart report has no __QIAOMU_CHARTS_READY__ screenshot readiness hook")

    table_count = occurrences(r"<table\b", markup)
    caption_count = occurrences(r"<caption\b", markup)
    checks["tables"] = {"count": table_count, "with_caption": caption_count}
    if table_count and caption_count < table_count:
        warnings.append(f"tables without captions: {table_count - caption_count}")

    has_reduced_motion = "prefers-reduced-motion" in lower
    has_print = "@media print" in lower
    checks["responsive_and_print"] = {
        "reduced_motion": has_reduced_motion,
        "print_styles": has_print,
        "media_queries": occurrences(r"@media\b", text),
    }
    if not has_reduced_motion:
        warnings.append("missing prefers-reduced-motion handling")
    if not has_print:
        warnings.append("missing print styles")
    if "overflow-x: hidden" in markup_lower or "overflow-x:hidden" in markup_lower:
        warnings.append("global overflow-x:hidden can conceal layout defects")

    style_match = re.search(r"\bdata-qiaomu-style\s*=\s*[\"']([^\"']+)[\"']", markup, re.I)
    style_profile = style_match.group(1) if style_match else None
    style_checks: dict[str, object] = {"profile": style_profile}
    if style_profile is None:
        warnings.append("missing data-qiaomu-style profile; default should be vercel-monochrome")
    elif style_profile == "vercel-monochrome":
        required_style_values = ["#ffffff", "#171717", "#666666", "#eaeaea"]
        missing_style_values = [value for value in required_style_values if value not in markup_lower]
        forbidden_default_values = ["#f3f0e9", "#f0eee8", "#fffdf8", "#ca4d2f", "#2c6b62"]
        found_forbidden = [value for value in forbidden_default_values if value in markup_lower]
        style_checks.update({"missing_required_values": missing_style_values, "forbidden_default_values": found_forbidden})
        if missing_style_values:
            errors.append(f"vercel-monochrome profile missing required tokens: {', '.join(missing_style_values)}")
        if found_forbidden:
            errors.append(f"vercel-monochrome profile contains legacy default colors: {', '.join(found_forbidden)}")
        html_lang_match = re.search(r"<html\b[^>]*\blang\s*=\s*[\"']([^\"']+)", markup, re.I)
        html_lang = html_lang_match.group(1).lower() if html_lang_match else ""
        cjk_document = html_lang.startswith(("zh", "ja", "ko"))
        cjk_leading_match = re.search(r"--display-leading-cjk\s*:\s*([0-9.]+)", markup, re.I)
        cjk_leading = float(cjk_leading_match.group(1)) if cjk_leading_match else None
        cjk_selector_uses_token = bool(re.search(
            r":(?:where\([^{}]*(?:lang\(zh\)|lang\(ja\)|lang\(ko\))[^{}]*\)|lang\((?:zh|ja|ko)\))[^{}]*\{[^{}]*line-height\s*:\s*var\(--display-leading-cjk\)",
            markup,
            re.I | re.S,
        ))
        style_checks["cjk_display_leading"] = {
            "document_is_cjk": cjk_document,
            "token": cjk_leading,
            "language_selector_uses_token": cjk_selector_uses_token,
        }
        if cjk_document and (cjk_leading is None or cjk_leading < 1.08):
            errors.append("CJK display title leading must use --display-leading-cjk at 1.08 or above")
        if cjk_document and not cjk_selector_uses_token:
            errors.append("CJK display title needs a language-aware selector using --display-leading-cjk")
        section_alignment = section_heading_alignment_violations(markup)
        section_alignment["policy"] = "section labels sit above headings; hero, headings, descriptions and primary content share a left edge"
        style_checks["section_heading_alignment"] = section_alignment
        if section_alignment["fixed_leading_column_rules"]:
            errors.append("section headings must share the primary left edge; fixed leading section-head columns are forbidden")
        if section_alignment["non_left_text_rules"]:
            errors.append("section heading containers must remain left-aligned by default")
        chart_palette = re.findall(r"--chart-[1-8]\s*:\s*(#[0-9a-f]{6})", markup_lower)
        colorful_chart_tokens = []
        for value in chart_palette:
            red, green, blue = int(value[1:3], 16), int(value[3:5], 16), int(value[5:7], 16)
            if max(red, green, blue) - min(red, green, blue) >= 24:
                colorful_chart_tokens.append(value)
        style_checks["chart_color_separation"] = {
            "chart_count": len(chart_tags),
            "palette_tokens": chart_palette,
            "colorful_tokens": colorful_chart_tokens,
            "page_shell_remains_monochrome": not found_forbidden,
        }
        if chart_tags and len(set(colorful_chart_tokens)) < 4:
            errors.append("chart reports need at least four distinct non-neutral --chart-N palette tokens; monochrome applies to the page shell, not the data layer")
        global_decal_enabled = bool(re.search(
            r"aria\s*:\s*\{\s*enabled\s*:\s*true\s*,\s*decal\s*:\s*\{\s*show\s*:\s*true",
            text,
            re.I | re.S,
        ))
        style_checks["solid_chart_fill"] = {
            "global_aria_decal_enabled": global_decal_enabled,
            "default_fill_policy": "solid",
        }
        if chart_tags and global_decal_enabled:
            errors.append("global ECharts aria.decal must be disabled; default chart fills should be solid and texture is opt-in per chart")
    checks["style_profile"] = style_checks

    has_source = bool(re.search(r"source|来源|数据源", text, re.I))
    has_limit = bool(re.search(r"limitation|missing evidence|限制|局限|缺失", text, re.I))
    checks["evidence_language"] = {"source": has_source, "limitations": has_limit}
    if not has_source:
        warnings.append("no visible source/data-source language detected")
    if not has_limit:
        warnings.append("no limitations or missing-evidence language detected")

    if data_paths:
        provenance = number_provenance(markup, data_paths)
        checks["number_provenance"] = provenance
        if provenance["unmatched"]:
            message = (
                f"numbers shown without a source in data/metrics files: {len(provenance['unmatched'])} "
                f"({', '.join(provenance['unmatched'][:8])})"
            )
            (errors if strict_numbers else warnings).append(message)

    return {
        "ok": not errors,
        "file": str(path),
        "bytes": path.stat().st_size,
        "errors": errors,
        "warnings": warnings,
        "checks": checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="HTML report to audit")
    parser.add_argument("--allow-remote", action="store_true", help="Allow remote HTTP(S) assets")
    parser.add_argument("--json-output", type=Path, help="Optional JSON report path")
    parser.add_argument("--data", type=Path, action="append", default=[], help="Data or computed-metrics file every shown number must come from (repeatable)")
    parser.add_argument("--strict-numbers", action="store_true", help="Fail instead of warn when a shown number has no source")
    args = parser.parse_args()

    if not args.html.is_file():
        parser.error(f"HTML file not found: {args.html}")
    for data_path in args.data:
        if not data_path.is_file():
            parser.error(f"data file not found: {data_path}")
    result = audit(args.html, args.allow_remote, args.data, args.strict_numbers)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    if not result["ok"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
