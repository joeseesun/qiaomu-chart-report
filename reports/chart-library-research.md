# Open-Source Chart Research

- Researched at: 2026-08-07
- Queries: `advanced data visualization charts`; `interactive chart gallery html report`; `echarts d3 visualization`
- Sources: skills.sh, SkillsMP, canonical GitHub source, official project documentation, npm registry metadata
- Rating evidence: unavailable; installs and repository stars are not ratings

## Skill prior art

| Candidate | Signal observed 2026-08-07 | Learned | Adapted into | Rejected |
|---|---|---|---|---|
| [AntV chart-visualization](https://github.com/antvis/chart-visualization-skills/tree/master/skills/chart-visualization) | 5,500 skills.sh installs; repo 455 stars; MIT | Broad chart taxonomy and explicit input shapes | Chart selection matrix and recipe data contracts | Remote API upload, returned image URL, dual axes as a routine option |
| [ByteDance DeerFlow chart-visualization](https://github.com/bytedance/deer-flow/tree/main/skills/public/chart-visualization) | 2,100 skills.sh installs; repo 79,474 stars; MIT | Per-chart reference routing and parameter extraction before generation | Progressive reference loading in `open-source-chart-system.md` | URL-only result and framework-bound generator |
| [OpenAI visualization-strategy-and-critique](https://github.com/openai/plugins/tree/main/plugins/build-web-data-visualization/skills/visualization-strategy-and-critique) | 3 skills.sh installs; first-party trust anchor; repo 4,969 stars | One focal question, static-screenshot survival, mobile as sibling strategy, novelty must carry meaning | Interesting-chart gate, one-complex-chart budget, mobile fallback and screenshot critique | Large platform-specific routing tree outside this skill's report scope |
| [ECharts visualization guide](https://github.com/brycewang-stanford/Auto-Empirical-Research-Skills/tree/main/skills/43-wentorai-research-plugins/skills/analysis/dataviz/echarts-visualization-guide) | SkillsMP repo 3,161 stars; source inspected | Declarative ECharts options, resize, interactive research charts and PNG export | Pinned offline ECharts recipes and resize observers | CDN-only ECharts 5 snippet, generic academic theme, no chart-ready screenshot gate |

skills.sh returned no parseable candidates for one query (`echarts d3 visualization`); this is recorded as missing catalog evidence in `chart-prior-art-candidates.json`.

## Library comparison

| Library | Version verified | GitHub stars observed | License | Decision |
|---|---:|---:|---|---|
| [Apache ECharts](https://github.com/apache/echarts) | 6.1.0 | 66,996 | Apache-2.0 | Bundle as default engine: broad types, declarative options, SVG/Canvas, ARIA and responsive support |
| [D3](https://github.com/d3/d3) | 7.9.0 | 113,371 | ISC | Bundle as specialist adapter for chord, beeswarm and ridgeline recipes |
| [Observable Plot](https://github.com/observablehq/plot) | 0.6.17 | 5,344 | ISC | Document as concise exploratory alternative; do not bundle because it overlaps D3 and adds runtime weight |
| [Vega-Lite](https://github.com/vega/vega-lite) | 6.4.3 | 5,440 | BSD-3-Clause | Document as JSON-grammar alternative; do not bundle because complex styling and runtime size do not fit the single-file default |
| [AntV G2](https://github.com/antvis/G2) | 5.4.8 | 12,580 | MIT | Document as grammar alternative; do not create a second default engine beside ECharts |

Mutable metrics and versions were checked on 2026-08-07. npm metadata reported the same versions and licenses. Stars indicate repository attention, not output quality.

## Keep / adapt / reject / invent

### Keep

- Relationship-first selection and explicit data shapes.
- Declarative chart configuration where it reduces fragile custom geometry.
- Mobile and static screenshot as first-class outcomes.

### Adapt

- Convert remote/API chart generation to pinned offline runtimes embedded only when used.
- Convert a type list into a matrix with data preconditions, misuse cases and mobile fallback.
- Convert generic examples into Qiaomu-themed recipes that inherit report CSS tokens and direct-label rules.

### Reject

- Uploading user data to a chart API by default.
- Loading every candidate library or CDN in every report.
- Selecting Sankey, chord, radar, river or force layouts only because they look novel.
- Treating tooltip-only values or desktop-only interaction as complete evidence.

### Invent

- 13 reusable, source-visible recipes across comparison, distribution, time, hierarchy, flow and multivariate exploration.
- `embed_chart_lib.py` for single-file offline embedding of only selected runtimes.
- `verify_vendor.py` with pinned SHA-256 and bundled licenses.
- Screenshot renderer readiness contract: all chart containers must reach `data-chart-ready=true` with no captured runtime error.
- Static audit contract: every chart requires ARIA, a figure wrapper and figcaption.

## Advantages and evidence

- **Design advantage:** this package joins chart choice, data validity, offline runtime, reusable recipes, accessibility, mobile degradation and screenshot readiness in one report workflow.
- **Validated advantage:** `chart-gallery.html` renders 13/13 charts with no captured runtime errors; audit reports 13/13 semantic containers and no remote resources.
- **Validated advantage:** pinned ECharts and D3 SHA-256 plus license files pass `verify_vendor.py`.
- **Hypothesis:** a relationship-first recipe system should yield more varied and clearer reports than a basic bar/line/pie shortlist, but provider-backed comparison and independent preference testing are missing evidence.

## Missing evidence

- No public user-rating/review fields for the inspected skills.
- No provider-backed baseline vs upgraded-skill run.
- No independent human blind review.
- No Firefox/Safari/Windows/Linux runtime verification.
- Synthetic gallery data does not validate real-dataset statistical correctness.
