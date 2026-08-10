# Prior-Art Research

> 2026-08-07 chart-system upgrade: see `chart-library-research.md` and `chart-prior-art-candidates.json` for the additional open-source library and advanced-chart investigation.

- Researched at: 2026-08-07
- Queries: `html report visualization`; `data visualization dashboard report`; `webpage screenshot html`
- Catalogs: skills.sh, SkillsMP, canonical GitHub source
- Rating evidence: unavailable; installs and repository stars are not ratings

| Candidate | Why shortlisted | skills.sh installs | GitHub repo stars | Trust / maintenance | Adopt | Reject | License |
|---|---|---:|---:|---|---|---|---|
| [html-visual](https://github.com/2ykwang/agent-skills/tree/main/skills/html-visual) | Closest general single-file HTML visualization workflow | 373 | 17 | Source inspected; pushed 2026-08-04 | Single-file output, CSS tokens, responsive/a11y checks | Default dark mode, mandatory interaction, routine CDN use, no screenshot gate | MIT |
| [elegant-reports](https://github.com/jdrhyne/agent-skills/tree/main/skills/elegant-reports) | Report production and HTML-debugging specialist | 219 | 239 | Source inspected; repo security-scanning claim visible; pushed 2026-06-29 | Template reuse discipline, explicit runtime validation, inspect intermediate HTML | External Nutrient API/PDF path and Nordic style lock-in | MIT |
| [executive-dashboard-generator](https://github.com/OneWave-AI/claude-skills/tree/main/executive-dashboard-generator) | Strong insight-first reporting workflow | 324 | 242 | Source and reporting references inspected; pushed 2026-07-15 | “So what / what next”, data discovery, trend/outlier checks, direct status language | Fixed executive template, speculative projections, dual-axis recommendation, dashboard as universal default | MIT |
| [sn-md-to-html-report](https://github.com/OpenSenseNova/SenseNova-Skills/tree/main/skills/sn-md-to-html-report) | Closest editorial HTML-report design specialist and high-attention trust anchor | 110 | 4,913 | Source and design-contract/review references inspected; pushed 2026-07-28 | Plan-before-HTML, fact-strength preservation, content-shaped layout, visual review angles | Long mandatory brainstorm for every task, handcrafted-only chart restriction, no deterministic screenshot tool | MIT |

Mutable metrics were observed on 2026-08-07. skills.sh installs measure ecosystem adoption. GitHub stars measure repository attention, not skill-specific quality. SkillsMP search results were used for breadth; no inspected candidate exposed verifiable user ratings or reviews.

## Contribution ledger

### Keep

- Single-file HTML and shared visual tokens from `html-visual`.
- Insight-first narrative and explicit recommendations from `executive-dashboard-generator`.
- Plan-before-HTML, fact-strength preservation and content-shaped layout from `sn-md-to-html-report`.
- Runtime artifact verification and intermediate HTML inspection discipline from `elegant-reports`.

### Adapt

- Replace generic “dashboard” with a decision between editorial report and monitoring dashboard.
- Replace CDN-first visualization with offline-first inline HTML/CSS/SVG and user-authorized remote exceptions.
- Turn visual review guidance into a two-part gate: deterministic static audit plus real desktop/mobile browser screenshots.
- Add a typed evidence ledger so computed metrics, interpretation and recommendations do not collapse into one claim type.

### Reject

- Mandatory dark/light toggle and interaction for every output: many reports are better static, printable and focused.
- Universal KPI-card grid and fixed executive template: they encourage equal-weight content and placeholder thinking.
- Dual-axis charts and probability scenarios without data support: high risk of misleading encoding or invented confidence.
- Third-party PDF/API dependency: outside the requested HTML + screenshot job and adds a data-boundary cost.
- A long multi-direction visual brainstorm for all cases: valuable for bespoke editorial work but disproportionate for routine statistical reporting.

### Invent

- Dependency-free Chrome DevTools Protocol renderer with isolated temporary Profile, full-page capture, selector capture and height guard.
- Static report audit for semantic structure, offline resource boundary, placeholders, media semantics, evidence language and responsive/print fallbacks.
- Required paired desktop/mobile screenshots plus manual visual-open gate.
- A clear near-neighbor router separating report artifacts from app/landing-page development, covers/cards and existing-page screenshots.

## Created skill advantages

- **Design advantage:** compared with the inspected candidates, the package explicitly owns the full `evidence -> plan -> HTML -> audit -> desktop/mobile screenshot -> visual inspection` loop.
- **Design advantage:** the evidence ledger separates source facts, computed metrics, interpretations, recommendations and missing evidence.
- **Validated advantage:** the recorded fixture passes the static audit and renders PNG screenshots through a local isolated Chrome process; see `reports/fixture-audit.json` and the two fixture PNGs.
- **Hypothesis:** the evidence ledger and dual-viewport gate should reduce misleading claims and responsive regressions, but provider-backed A/B comparison and human blind review are missing evidence.

## Missing evidence

- No user-rating/review signal was available for the inspected candidates.
- No provider-backed trigger or output comparison.
- No independent human blind review.
- No Windows/Linux, Firefox or Safari runtime verification.
- Fixture data is synthetic and does not prove statistical correctness on a real dataset.
