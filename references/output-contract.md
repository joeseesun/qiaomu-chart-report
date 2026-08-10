# 交付契约

## Required artifacts

```text
output/
├── report-plan.md
├── report.html
├── report-desktop.png
├── report-mobile.png
└── audit.json
```

文件名可按主题改写，但五类产物都要存在。用户明确只要某一种截图时可减少 PNG 变体；不得省略 HTML 和审计结果。

## HTML contract

- 单文件、自包含、可离线打开；远程资源必须是用户授权的例外。
- `<!doctype html>`、`lang`、viewport、非空 title、唯一 h1、main 区域。
- CSS tokens 管理颜色、字号、间距、边界和宽度。
- 默认 `<html data-qiaomu-style="vercel-monochrome">`，使用 `assets/styles/vercel-monochrome.css` 的黑白 tokens；自定义主题必须显式写成其他 profile 并在计划中说明。
- 统计口径、单位、日期、来源和 missing evidence 可见。
- 图表有语义标签或文本/表格替代；无伪造数字和占位符。
- 复杂图使用内置固定版本 runtime 与 recipes；只嵌入实际需要的 ECharts/D3，调用 `QiaomuCharts.ready()`。
- 每个 `data-qiaomu-chart` 容器位于 `data-qiaomu-chart-figure` 中，具有 role/ARIA 与 figcaption。
- 桌面与移动布局均无页面级横向滚动。

## Screenshot contract

- PNG 来自真实 Chrome/Chromium 渲染，默认 full-page。
- 默认桌面 1440×900、移动 390×844、DPR 1；用户指定设备时遵从用户。
- 截图前等待 `document.fonts.ready`、图片加载和可选等待时间。
- 图表页面还必须等待 `window.__QIAOMU_CHARTS_READY__`；ready 数量与图表容器数量不一致时截图失败。
- 交付前人工打开检查；静态审计不能替代视觉验收。

## Final handoff

报告：

- 结论与受众用途
- 数据范围、计算口径和限制
- HTML、桌面截图、移动截图、计划、审计文件的绝对路径
- 审计结果与人工检查结果
- 外部依赖、未验证项和 `missing evidence`

不要声称统计正确、跨浏览器兼容或审美优秀，除非有对应证据。
