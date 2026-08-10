# Fixture Visual Review

- Reviewed at: 2026-08-07
- Reviewer role: package author; not an independent blind reviewer
- Desktop: opened `fixture-desktop.png`; hierarchy, full-width use, chart labels, table, source and limitations are visible; no overlap or clipping observed.
- Mobile first pass: failed because the horizontally scrollable table hid two columns in the static screenshot.
- Fix: converted the mobile table into per-month semantic field grids while keeping the desktop table unchanged.
- Mobile second pass: opened `fixture-mobile.png`; all five monthly fields are visible, no page-level horizontal overflow, chart labels remain readable, and no overlap or clipping observed.
- Result: author visual check passed for the recorded fixture.
- Chart gallery desktop first pass: all 13 charts rendered, but the D3 chord SVG used `height:auto`, exceeded its fixed container and pushed labels toward the caption/footer.
- Chart gallery fix: D3 SVG recipes now obey both container width and height with `preserveAspectRatio`.
- Chart gallery desktop second pass: opened `chart-gallery-desktop.png`; 13 charts are contained, captions remain separated, and no clipping or overlap was observed.
- Chart gallery mobile: opened `chart-gallery-mobile.png`; one-column reading order, chart containers and captions remain inside the 390px viewport. Dense advanced charts are intentionally examples; real reports must apply the documented mobile fallback when labels or decision context require it.
- Missing evidence: independent blind review, real-device review, Windows/Linux, Firefox/Safari and accessibility-tool testing.
- Vercel-monochrome revision: regenerated and opened the quarterly desktop/mobile screenshots and the chart-gallery desktop screenshot. The previous cream background, serif hero and green/red chart palette are gone; white/near-black/gray hierarchy, sans-serif headings, 1px borders, small radii and grayscale charts are visible. No overlap, clipping or horizontal overflow was observed.
- CJK title-leading correction: the initial Vercel-style `.98` display leading was too tight for multi-line Chinese. The default now uses language-aware tokens: Latin `1.02`, CJK `1.12` (audit floor `1.08`). Regenerated quarterly and gallery screenshots were opened at 1440px and 390px; title lines have visible separation with no glyph collision, clipping or new horizontal overflow.
- Chart-color correction: regenerated and opened `chart-gallery-desktop.png` and `chart-gallery-mobile.png`. The page shell remains white/near-black/gray, while data marks now use a coherent blue/orange/green/red/purple/cyan palette. Waterfall uses stable positive/negative colors; the calendar uses a sequential blue scale. All 13 charts remain contained and readable, with no runtime error, overlap, clipping or page-level horizontal overflow.
- Solid-fill correction: removed the global ECharts decal overlay and regenerated both gallery screenshots. Bar, heatmap, sunburst, treemap and theme-river fills now render as clean color fields without diagonal or dotted hatching. Desktop and mobile inspection found no regression in hierarchy, containment or label readability.
