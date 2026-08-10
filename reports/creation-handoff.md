# Creation Handoff

## Result

- Skill: `qiaomu-chart-report` 1.0.0
- Job: turn text/data/research/statistics into a self-contained evidence-led HTML report with pinned open-source ECharts/D3 recipes and verified desktop/mobile PNG screenshots.
- Default visual: Vercel/Geist-inspired light monochrome, explicitly chosen by the user; custom brands/themes override it.
- Canonical install path: `~/.agents/skills/qiaomu-chart-report`
- Status: renamed from `qiaomu-html-report`; prepared for public GitHub release.

## Reference skills studied

- `html-visual` (373 skills.sh installs observed 2026-08-07): learned single-file output, shared CSS tokens and accessibility basics; adapted in `SKILL.md` and `references/report-design.md`.
- `elegant-reports` (219 installs; 239 GitHub repo stars): learned explicit runtime artifact checks and HTML as a debugging surface; adapted into the audit/render gates.
- `executive-dashboard-generator` (324 installs; 242 repo stars): learned insight-first narrative and “what next” framing; adapted into the default report topology and evidence-to-action structure.
- `sn-md-to-html-report` (110 installs; 4,913 repo stars): learned plan-before-HTML, fact-strength preservation and content-shaped layout; adapted into `report-plan.md`, evidence boundaries and review rules.
- `AntV chart-visualization` (5,500 installs): learned broad chart taxonomy and input contracts; adapted into a relationship-first matrix while rejecting the default remote API upload.
- `ByteDance DeerFlow chart-visualization` (2,100 installs): learned per-chart parameter references; adapted into progressive reference loading.
- `OpenAI visualization-strategy-and-critique` (first-party trust anchor): learned static-screenshot survival, mobile sibling strategy and novelty-with-meaning; adapted into complex-chart gates.
- `ECharts visualization guide` (SkillsMP repo 3,161 stars): learned declarative advanced chart patterns; adapted to pinned ECharts 6.1.0 with offline embedding and readiness gates.

## Absorbed and rejected

- Keep: single-file delivery, insight-first narrative, plan-before-code, relationship-first chart selection and runtime verification.
- Adapt: offline-first instead of CDN/API-first; ECharts default plus D3 specialist adapter; editorial report by default instead of dashboard by default; deterministic gates plus human screenshot inspection.
- Reject: mandatory dark/interactive UI, fixed dashboard templates, routine dual-axis charts, unsupported forecasts, random exotic-chart selection and user-data upload to chart APIs.
- Invent: typed evidence ledger, 13 reusable recipes, pinned vendor integrity, chart-ready screenshot gate, semantic chart audit and required dual-viewport handoff.

## Advantages and evidence

- **Design advantage:** full evidence-to-screenshot workflow is encoded in one package.
- **Design advantage:** strong boundaries prevent overlap with apps, marketing pages, covers/cards and existing-page screenshots.
- **Validated advantage:** package validator and trigger eval pass; recorded fixture audit and local Chrome rendering pass.
- **Validated advantage:** gallery audit passes with 13/13 semantic chart containers; Chrome reports 13/13 ready on desktop and mobile with no captured runtime errors.
- **Validated advantage:** ECharts/D3 vendor hashes and license evidence pass.
- **Validated advantage:** both default fixtures pass the `vercel-monochrome` audit with required tokens present and legacy cream/green/red defaults absent; screenshots were regenerated and opened.
- **Validated correction:** language-aware display tokens separate Latin (`1.02`) and CJK (`1.12`) leading; the audit rejects CJK display leading below `1.08`, and both Chinese fixtures pass desktop/mobile visual review.
- **Validated correction:** monochrome now applies only to the webpage shell. Chart recipes use an eight-color data palette plus fixed positive/negative semantic colors, while labels, shapes, decals and ordering remain redundant encodings. The regenerated 13-chart gallery passes desktop/mobile runtime and visual review.
- **Validated correction:** global ECharts `aria.decal` is disabled, so the default categorical, heatmap, hierarchy and flow fills render without automatic hatching. A static gate rejects re-enabling the global decal; texture remains opt-in per chart.
- **Hypothesis:** the paired screenshot gate will reduce mobile/report layout failures; provider-backed comparison and human blind review are missing evidence.

## Verification and limits

- Package validation: see local command output and `reports/trigger-eval.json`.
- Runtime fixture: `reports/fixture-audit.json`, `fixture-desktop.png`, `fixture-mobile.png`.
- Excluded permissions: default network access, user browser Profile/Cookies, arbitrary file browsing and uploads.
- Missing evidence: independent statistical review, human blind review, provider-backed runs and cross-platform/cross-browser runtime.
