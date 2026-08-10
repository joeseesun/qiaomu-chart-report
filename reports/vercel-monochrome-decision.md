# Vercel-Inspired Monochrome Default

- Decided at: 2026-08-07
- Decision authority: explicit user preference
- Scope: default HTML styling in `qiaomu-chart-report`; user-specified brands/themes override it

## Primary references

- [Vercel Geist introduction](https://vercel.com/geist/introduction): high-contrast color system, grid and Geist Sans/Mono as core foundations.
- [Geist colors](https://examples.vercel.com/geist/colors): two background levels, component background steps, border steps and accessible text/icon steps.
- [Geist typography](https://examples.vercel.com/geist/typography): coordinated size, line-height, letter-spacing and weight roles; mono/tabular styles for technical labels and numbers.
- [Vercel Web Interface Guidelines](https://vercel.com/design/guidelines): visible focus, redundant status cues, tabular numbers, crisp borders and accessible charts.
- [Geist font](https://github.com/vercel/geist-font): open font reference; generated reports use an offline-safe system stack unless a font asset is explicitly embedded.

## Keep / adapt / reject / invent

- **Keep:** high-contrast neutral hierarchy, background 1/2 distinction, tight sans-serif display type, tabular/mono numbers, crisp borders and grid discipline.
- **Adapt:** use Chinese system UI fallbacks when Geist is not embedded; translate component-system rules into a static editorial/data-report surface; loosen CJK display leading instead of copying Latin typography metrics.
- **Reject:** Vercel Logo/triangle, brand copy, exact page recreation, framework-specific components, automatic dark toggle and arbitrary brand mimicry.
- **Invent:** `data-qiaomu-style="vercel-monochrome"` profile plus audit gates that require core monochrome tokens, reject the previous cream/green/red defaults, and enforce language-aware CJK display leading.

## Default contract

- White `#ffffff` page and surfaces; near-black `#171717` primary text.
- Gray `#666666` secondary text and `#eaeaea` borders.
- Sans-serif hero with controlled negative letter-spacing; Latin display leading defaults to `1.02`, while CJK defaults to `1.12` and may not fall below the `1.08` audit floor. “Tight” must never mean vertically cramped.
- 8px radius, no heavy shadow, no colorful card wall.
- The webpage shell remains monochrome, but charts have an independent data-color layer: categorical palettes, sequential scales and fixed positive/negative semantic colors are allowed by default. Labels, shapes, line styles, textures or ordering must reinforce color.
- Explicit user theme/brand/reference always overrides this default.

## Evidence

- `fixture-desktop.png` and `fixture-mobile.png` were regenerated and opened after the change.
- `chart-gallery-desktop.png` was regenerated and opened; all 13 recipes use the monochrome series and remain legible.
- Both HTML fixtures pass the style-profile audit with no missing required values and no forbidden legacy colors.
- Both Chinese fixtures pass the CJK leading gate and were re-rendered at desktop and mobile widths after the correction.
- The regenerated gallery passes the chart-color separation gate: eight non-neutral chart tokens are present while the page shell retains its monochrome tokens.
- The gallery also passes the solid-fill gate: ECharts ARIA remains enabled, but global decal textures are disabled; accessibility redundancy comes from labels, shapes, line styles, ordering and textual summaries unless a specific chart explicitly opts into texture.

## Missing evidence

- No independent blind preference comparison.
- Geist font is not embedded by default; exact Vercel typography is not claimed.
- Cross-browser and Windows/Linux visual comparison remain missing evidence.
