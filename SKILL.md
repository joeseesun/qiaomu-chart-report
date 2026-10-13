---
name: qiaomu-chart-report
description: |
  将文本、Markdown、CSV/JSON/表格数据、研究材料或统计结果制作成自包含 HTML 可视化网页、数据故事和统计报告，并渲染为经过检查的桌面端与移动端 PNG 截图。适用于“生成 HTML 报告”“把数据做成网页”“统计报告可视化”“网页化分析”“做一个清晰表达的单页网页”“有趣/高级图表”“桑基图、旭日图、蜂群图、山脊图、弦图、排名变化图”“HTML dashboard/report”“生成网页和截图”等请求。内置离线 Apache ECharts 与 D3、可复用复杂图表 recipes、事实可追溯、结论先行、图表语义选择、编辑式信息层级、响应式降级和真实浏览器截图。不要用于完整网站/应用开发、营销落地页、HTML 封面/信息卡、幻灯片、仅分析数据而不需要网页交付、只截取现有网页，或用一台会动的实物机器讲解“某个系统/算法如何运作”的等距交互图（交给 anatomy）。
metadata:
  author: Qiaomu
  version: "1.1.0"
---

# Qiaomu Chart Report

把信息做成一份能读、能核对、能分享的单文件 HTML 报告，并交付真实浏览器截图。页面不是“数据堆成仪表盘”，而是一条从结论到证据的阅读路径。

## Mandatory Workflow

1. 把当前 `SKILL.md` 所在目录记为 `SKILL_DIR`，读 [Vercel 式黑白默认视觉](references/vercel-monochrome-style.md)、[报告设计与图表规则](references/report-design.md) 和 [交付契约](references/output-contract.md)。只要任务包含图表，再读 [开源图表系统](references/open-source-chart-system.md)。
2. 确认受众、用途、输入、时间范围、单位、统计口径和输出目录。信息足够时直接执行；只有缺失会改变结论或统计口径时才询问。
3. 先做证据账本：区分 `source fact / computed metric / interpretation / recommendation / missing evidence`。不得把推断伪装成原始事实，也不得补造数字。
4. 计算必须可复核。优先使用项目已有脚本或合适的数据工具；保留公式、筛选条件、分母、日期和单位。发现数据质量问题时在页面里显式披露。
5. 写一个紧凑的 `report-plan.md`：核心结论、受众动作、章节顺序、每张图回答的问题、响应式降级、证据与限制。视觉默认锁定为 `vercel-monochrome`；只有用户明确指定其他品牌、主题或参考图时才覆盖，并记录覆盖原因。
6. 生成自包含 HTML：语义 HTML、内联 CSS、必要的内联 JS/SVG；默认不依赖 CDN、远程字体或网络资源。以 `assets/styles/vercel-monochrome.css` 为默认 token 和组件基准，在 `<html>` 写 `data-qiaomu-style="vercel-monochrome"`，整页只有一个视觉系统。
7. 每张图只回答一个问题，标题写结论，图形展示证据。先在开源图表矩阵中匹配数据关系：普通图和多数高级图用 ECharts recipe；弦图、蜂群、山脊等特殊布局才用 D3 recipe。复杂图必须通过“有趣门禁”和移动端降级，不得从图库里随机挑一个炫技。
8. 默认从 `assets/chart-recipes.js` 复用图表配置，不重复手写脆弱布局。HTML 模板保留 vendor 占位符，再按需嵌入固定版本：

```bash
python3 "$SKILL_DIR/scripts/embed_chart_lib.py" report.template.html report.html --libraries echarts
# 只有使用 D3 recipe 时：
python3 "$SKILL_DIR/scripts/embed_chart_lib.py" report.template.html report.html --libraries echarts,d3
```

9. 图表必须有标签、单位、来源/口径、figure/figcaption 和文本替代；颜色不是唯一编码。调用 `QiaomuCharts.ready()`，让截图器等待所有图表完成。没有数据关系时用文字、表格或简图，不强行画图。
10. 运行静态审计：

```bash
python3 "$SKILL_DIR/scripts/audit_report.py" report.html --json-output audit.json \
  --data data.csv --data metrics.json --strict-numbers
```

`--data` 传原始数据和计算指标文件（派生数字先写进 `metrics.json`，不要只出现在正文里）；页面上每个非平凡数字都必须能在其中找到（按显示精度四舍五入、百分比可对应小数）。`--strict-numbers` 让未找到来源的数字直接失败；交付前把 `number_provenance.unmatched` 清到 0。

11. 用临时、隔离的 Chrome/Chromium Profile 渲染桌面和移动截图：

```bash
node "$SKILL_DIR/scripts/render_html.mjs" report.html report-desktop.png --width 1440 --height 900 --full-page
node "$SKILL_DIR/scripts/render_html.mjs" report.html report-mobile.png --width 390 --height 844 --full-page
```

12. 必须打开两张 PNG 做真实视觉检查。先检查 Hero、章节编号、章节标题、正文与主要容器是否共享预期左边线；复杂图再检查标签碰撞、图形守恒、tooltip 依赖和静态截图可理解性。修复横向滚动、裁切、重叠、孤行、标签拥挤、图例歧义、文字过密、对比度和移动端降级问题，再重新审计与截图。
13. 交付 `report-plan.md`、HTML、桌面 PNG、移动 PNG 和 `audit.json`。说明数据口径、图表 runtime、已验证项与 `missing evidence`；不能只交源码或声称“应该正常”。

## Decision Rules

- 默认视觉是 Vercel / Geist 启发的浅色黑白：白底、近黑文字、灰阶层级、无衬线紧凑排版、12 列网格、1px 细边框、8px 小圆角、无厚重阴影。不要复制 Vercel Logo、品牌文案或页面结构。
- “紧凑”不等于拥挤。拉丁 display 标题默认行高 `1.02`；中文、日文、韩文标题必须经 `:lang()` 使用独立 token，默认行高 `1.12`、不得低于 `1.08`，不能直接继承英文常见的 `.98` 紧行高。桌面与移动截图都要检查多行标题是否碰撞。
- 默认报告必须保持稳定的左对齐轴：Hero、章节标签、章节标题、说明文字与下方主要内容共享容器左边线。章节编号放在标题上方；禁止使用 `180px 1fr`、`minmax(120px, 220px) 1fr` 等固定前导栏把章节标题整体推右。只有用户明确提供参考布局时才能覆盖，并必须在桌面与移动截图中验证。
- 未经用户明确覆盖，禁止回到奶油纸色、墨绿/砖红编辑配色、衬线巨型 Hero、18px+ 大圆角卡片墙、紫蓝渐变和玻璃效果。
- Vercel 黑白风格约束网页外壳，不限制数据图形。图表可使用多色分类、连续色阶和正负语义色；默认采用统一、克制、兼顾色盲的纯色色板，并保留直接标签、线型、形状、排序或文字说明等冗余编码。禁止把 ECharts `aria.decal.show` 作为全局默认；纹理只能在某张图确有无障碍或打印需求时显式开启。不要为了“高级感”把所有系列强制成灰色，也不要把高饱和颜色扩散到页面背景、卡片和正文层级。
- 默认是“滚动型编辑报告”，不是控制台式 dashboard。只有用户需要持续监控、筛选或运营操作时才采用仪表盘结构。
- 首屏先给一个明确结论、范围和阅读入口；KPI 只保留能推动判断的 2–4 个。
- 优先直接标注，少用图例；优先条形图、折线图、点图和小倍图。饼图仅用于少量、互斥且总和明确为 100% 的构成。
- “有趣”来自合适的视觉语法，不来自装饰。支持但严格约束：棒棒糖、哑铃、排名变化、瀑布、日历热力、蜂群、山脊、主题河流、矩形树、旭日、桑基、弦图和平行坐标。
- 同一页面默认最多一个高复杂度主图。若移动端无法保留同一结论，必须改用 small multiples、热力表、排序条形或结构化列表。
- **一个数字只有一个来源**：正文、图表、KPI、图注和截图里的数字都从同一份数据/指标文件生成，不手抄第二份；由审计的 `number_provenance` 清零证明。
- **标注落在实处**：注释紧贴它说明的数据点或系列，不用飘在空中的引线、气泡和箭头；文字放在图形周围，不压在密集图形上。
- **交互图的素养**：有动画或自动轮播时，滚出视口就停、`prefers-reduced-motion` 下保持静止但仍响应输入；可键盘聚焦，关键读数变化写进 `aria-live`；静态截图本身仍能读懂。
- 同一数字只设一个视觉所有者。标题讲结论时，图注补口径或原因，不复读整句话。
- 卡片不是默认容器。用网格、留白、字号、完整细轮廓和色面建立层级；禁用左侧彩色竖线式 callout。
- 长表与代码块可局部横向滚动，页面本身不得横向滚动。移动端应重排，不是按比例缩小桌面版。
- 若用户只要固定尺寸封面/社交卡片，路由到 `qiaomu-html-cover` 或 `qiaomu-info-card-designer`；若要完整网站/应用，使用网站开发流程；若只要现有网页截图，使用浏览器截图能力；若要讲“某个系统/算法怎么运作”的机制示意图（缓存淘汰、握手、锁、引擎），交给 `anatomy`，报告里需要时再嵌入它产出的图。

## Trust And Boundaries

- 默认离线，不上传用户数据，不复用用户浏览器 Profile，不读取 Cookie。
- 只读取用户提供或任务明确需要的输入，只写用户指定输出目录。
- 外部数据、远程字体或 CDN 必须得到任务授权，并在交付中声明依赖与失败降级。
- 脚本只启动临时 headless 浏览器并在结束后清理临时 Profile；不会修改现有 Chrome 配置。
- 自动审计可证明结构、资源边界和基础交付完整性；统计正确性与审美仍需数据复核和人工视觉检查。独立盲评、Windows/Linux 实机与跨浏览器比较为 `missing evidence`。

Copyright (c) 向阳乔木 · [X](https://x.com/vista8) · [GitHub](https://github.com/joeseesun/)
