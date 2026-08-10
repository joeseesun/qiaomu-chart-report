# 开源图表系统

## 1. Runtime 选择

默认从数据关系出发，再选择运行时。不要为了“有趣”而选择难读图表。

| Runtime | 固定版本 | 角色 | 优势 | 代价 / 边界 | License |
|---|---:|---|---|---|---|
| Apache ECharts | 6.1.0 | 默认图表引擎 | 20+ 内置类型、声明式配置、SVG/Canvas、ARIA、响应式、复杂关系图 | 完整包约 1.1MB；自定义语法仍需测试 | Apache-2.0 |
| D3 | 7.9.0 | 特殊图形适配器 | 图形语法和布局自由度高，适合弦图、蜂群、山脊等 | 更容易产生脆弱布局；必须使用已验证 recipe | ISC |
| Observable Plot | 0.6.17 | 轻量探索候选，不内置 | marks/transforms 简洁，适合统计探索 | 与 D3 能力重叠；完整依赖链增加包体 | ISC |
| Vega-Lite | 6.4.3 | JSON 语法候选，不内置 | 声明式、可复现、适合自动生成规范 | runtime 较重；复杂定制与页面融合成本更高 | BSD-3-Clause |
| AntV G2 | 5.4.8 | 图形语法候选，不内置 | 语法清晰，官方 chart skill 生态丰富 | 与 ECharts 重叠，避免双默认引擎 | MIT |

内置文件位于 `assets/vendor/`，许可证与 NOTICE 随包保留。默认只嵌入实际使用的 runtime：普通和多数高级图使用 ECharts；只有弦图、蜂群或山脊等 recipe 才同时嵌入 D3。

## 2. 图表选择矩阵

### 比较与变化

| 图表 | 回答的问题 | 数据条件 | 不要使用时 | 移动端降级 |
|---|---|---|---|---|
| Lollipop 棒棒糖 | 类别谁高谁低 | 一个数值 + 一个类别，建议 ≤15 类 | 数值需从共同零点精确比较时优先条形图 | 横向、按值排序 |
| Dumbbell 哑铃 | 同一对象前后差多少 | 每类两个可比数值 | 超过两个时间点 | 改差值条或分组表 |
| Bump 排名变化 | 名次如何换位 | 3–8 个时期、≤8 条系列 | 实际数值比名次更重要 | 只保留重点 3–5 条或 small multiples |
| Slope 斜率图 | 两个时点如何变化 | 正好两个时点 | 系列太多或标签重叠 | 改哑铃图 |
| Waterfall 瀑布 | 哪些贡献形成最终增减 | 可加总的正负贡献 | 项目不守恒或顺序随意 | 横向瀑布或贡献表 |
| Marimekko | 两个构成维度如何共同变化 | 宽度和高度都有明确分母 | 需要精确查值 | 矩阵热力图 |

### 分布与不确定性

| 图表 | 回答的问题 | 数据条件 | 不要使用时 | 移动端降级 |
|---|---|---|---|---|
| Beeswarm 蜂群 | 每个观测值在哪里、是否聚集 | 单个定量变量，建议 ≤400 点 | 点数太多或精确密度更重要 | 抽样 + 直方图摘要 |
| Ridgeline 山脊 | 多组分布形状如何变化 | 3–10 组同尺度密度 | 需要精确比较高度或样本量很小 | 小倍直方图 |
| Violin 小提琴 | 分布形状与中位位置 | 每组足够样本 | 样本很少、受众不熟悉密度 | 箱线 + 抖动点 |
| Raincloud | 分布、箱线和原始点同时看 | 有原始样本且版面足够 | 一屏很多分组 | 箱线 + 关键点 |
| Horizon | 多条时间序列的密集异常 | 同尺度且周期长 | 普通读者第一次阅读 | 小倍折线图 |
| Fan / uncertainty band | 预测范围如何扩散 | 有置信区间或分位数 | 只有单点预测 | 区间表 + 折线 |

### 时间与节奏

| 图表 | 回答的问题 | 数据条件 | 不要使用时 | 移动端降级 |
|---|---|---|---|---|
| Calendar heatmap | 日级连续性、周期与异常 | 连续日期 + 数值 | 日期稀疏或比较多个指标 | 月度 small multiples |
| Streamgraph / ThemeRiver | 多主题相对盛衰 | 多类别、密集时间序列 | 需要精确读数或总量不稳定未说明 | 堆叠面积或重点小倍图 |
| Cycle plot | 季节内和跨季节模式 | 重复周期数据 | 时间序列太短 | 普通折线 + 周期标记 |
| Spiral timeline | 周期性与长时跨度 | 周期含义强 | 线性趋势更重要 | 线性时间轴 |

### 层级、流向与网络

| 图表 | 回答的问题 | 数据条件 | 不要使用时 | 移动端降级 |
|---|---|---|---|---|
| Treemap | 层级中谁占得多 | 正值、2–3 层层级 | 需要精确比较相近值 | 排序条形 + 面包屑 |
| Sunburst | 层级路径与构成 | 有明确根节点、≤3 层 | 标签长、层级多 | Icicle 或树表 |
| Icicle | 从根到叶的路径 | 层级树且路径重要 | 宽度不足 | 缩进树表 |
| Circle packing | 群组与聚类结构 | 面积近似即可 | 精确比较是主任务 | Treemap / 列表 |
| Sankey / Alluvial | 流量如何从来源到去向 | 非负、可守恒流量 | 有环、缺失流量、节点太多 | 分阶段表或分组条形 |
| Chord | 群体之间双向关系密度 | 小规模方阵，建议 ≤8 节点 | 方向或精确值是核心、节点多 | 邻接热力图 |
| Force graph | 关系簇、桥接与孤立 | 节点/边有真实语义 | 只想表达线性流程 | 邻接表或 Sankey |
| Edge bundling | 大层级网络的关系模式 | 网络同时具有层级 | 需要逐边追踪 | 聚合矩阵 |

### 多维与空间

| 图表 | 回答的问题 | 数据条件 | 不要使用时 | 移动端降级 |
|---|---|---|---|---|
| Parallel coordinates | 多维轮廓与异常 | 4–10 个可标准化维度 | 精确值或系列太多 | 重点对象雷达 + 表 |
| Scatter matrix | 多变量两两关系 | 3–8 个数值变量 | 受众只需一个结论 | 选出最关键散点 |
| Hexbin / density contour | 大量散点在哪里聚集 | 点数大、重叠明显 | 样本很少 | 普通散点 |
| Radar | 少量对象的标准化轮廓 | 3–8 同方向维度、≤3 对象 | 各轴尺度含义不同或需精确比较 | 分组点图 |
| Arc map | 地理流向 | 起终点位置有分析意义 | 地理只是标签 | Sankey / 排序条形 |
| Cartogram | 地理面积按数值变形 | 受众熟悉地图轮廓 | 精确位置重要 | 分级设色图 + 排名 |

## 3. 使用 recipes

模板中保留占位符：

```html
<!-- QIAOMU_VENDOR:ECHARTS -->
<!-- QIAOMU_VENDOR:D3 -->
<!-- QIAOMU_CHART_RECIPES -->
```

生成单文件 HTML：

```bash
python3 "$SKILL_DIR/scripts/embed_chart_lib.py" report.template.html report.html --libraries echarts
python3 "$SKILL_DIR/scripts/embed_chart_lib.py" report.template.html report.html --libraries echarts,d3
```

每个容器必须有可访问名称并位于带图注的 figure 中：

```html
<figure data-qiaomu-chart-figure>
  <div id="chart-a" data-qiaomu-chart="lollipop" role="img" aria-label="六个渠道的转化率比较"></div>
  <figcaption>来源、口径、单位与一句话结论。</figcaption>
</figure>
<script>
  QiaomuCharts.mountECharts("#chart-a", QiaomuCharts.echarts.lollipop(data, {title: "自然搜索领先"}));
  QiaomuCharts.ready();
</script>
```

## 4. “有趣”门禁

复杂图表必须同时满足：

1. 比普通条/线图多表达一个真实关系，如流向、分布、层级、排名、周期或多维轮廓。
2. 数据结构满足该图的守恒、层级、尺度或样本量条件。
3. 10 秒内能说明图形语法，重要值不只藏在 tooltip。
4. 静态截图仍能读懂；交互是增强，不是证据唯一入口。
5. 移动端有明确降级；不能简单缩小到标签不可读。
6. 标签和注释与图形共用阅读轴。语义长标签放在封闭图形外，节点内只放短标记。
7. 同一页面最多一个高复杂度主图，其余图形从属于主问题。

不通过时回退到排序条形、点图、小倍图、热力表或证据表。

## 5. 验收

- 调用 `QiaomuCharts.ready()`，截图器会等待 `window.__QIAOMU_CHARTS_READY__`。
- ECharts 默认 SVG renderer；大规模点数据可改 Canvas，但必须保留文本替代。
- 所有 `data-qiaomu-chart` 容器必须有 `role`/ARIA、figure 和 figcaption；静态审计会阻断缺失。
- 截图后检查标签碰撞、tooltip 依赖、颜色编码、空数据、极端值、长中文标签和移动端降级。
- 图表库版本、SHA-256 与许可证见 `assets/vendor/NOTICE.md`。
