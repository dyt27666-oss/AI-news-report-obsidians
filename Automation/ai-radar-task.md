# AI Radar 自动化任务说明

> 本文件是 AI Radar cron job 的主任务说明。以后优先改这里，而不是直接改 Hermes 的 `jobs.json`。

## 运行时间

- 北京时间每天 09:00。
- 服务器 UTC cron：`0 1 * * *`。

## 用户画像

用户是：

- AI Infra 工程师。
- 大模型工程师。
- RL 游戏模型训练算法工程师。

筛选和解读信息时，优先关注：

- LLM serving / inference / KV cache / speculative decoding / batching / scheduler。
- distributed training / post-training / RLHF / RLAIF / PPO / DPO / GRPO / reward design。
- agent systems / memory / tool use / evaluation / benchmark。
- RL game agents / world model / simulation / environment parallelism。
- 大厂工程化趋势、模型训练/推理基础设施、算法论文和工程博客。

## 输出原则

日报不是正文仓库，而是导航入口。真正用于理解的是详情页。

每天必须生成：

- `Daily/YYYY-MM-DD.md`：总览日报。
- `Papers/.../*.md`：论文详情页。
- `Industry/.../*.md`：大厂博客/工程文章详情页。
- `GitHub/.../*.md`：项目/资讯详情页。
- 必要时生成 `Concepts/.../*.md`：概念卡片。

### 强制覆盖范围

每天日报不能只靠“模型觉得重要”来裁剪来源，必须先完整扫一遍这些固定板块，再做筛选和解读：

1. 大厂资讯 / Research / Engineering Blog。
   - 必须覆盖 OpenAI、Anthropic、Google DeepMind、Meta AI、NVIDIA、Microsoft、Hugging Face、腾讯、字节、SpaceAI。
   - 每家公司必须在日报里出现：有高相关新内容则放入博客/大厂动态表；没有高相关新内容也要在“公司来源扫描矩阵”里写清楚“无高相关新项 / 低置信 / 访问失败”。
   - 每天至少保留 6-10 条大厂/工程博客/研究动态候选；其中至少 3 条生成 `Industry/...` 详情页。若当天不足 3 条，必须解释不足原因。
2. GitHub 高 star 项目。
   - 必须单独输出 “GitHub 高 star Top 10” 表，不得只挑 2-3 个项目混进总清单。
   - 每条必须包含 repo、stars、forks、language、updated_at、topics、原文链接、是否值得试用。
3. GitHub star 增长最快项目。
   - 必须单独输出 “GitHub star 增长最快 Top 10” 表。
   - 优先用本仓库保存的昨日/历史 star snapshot 计算 `stars_delta`。
   - 如果没有历史 snapshot，必须用 GitHub Trending、近期 created/updated + stars 排序作为冷启动代理，并明确标注“冷启动代理，非真实日增”。
   - 每次运行后必须保存当日 GitHub star snapshot，路径为 `Automation/state/github-stars-YYYY-MM-DD.json`，供次日计算真实增长。
4. 论文。
   - 继续保留高信号论文，但不能挤掉大厂和 GitHub 固定板块。

## 日报结构

日报必须是 Obsidian dashboard，不要只是单调长表。长表只能作为索引之一，必须搭配图、矩阵、卡片区和主题视图。

推荐结构：

1. 今日结论：3-5 条 bullet。
2. 今日态势图：用 Mermaid 展示今天信息流向，例如“大厂信号 -> 论文趋势 -> GitHub 工具 -> 对 AI Infra/RL 的行动”。
3. 必读卡片区：用 Markdown callout/card 风格列 3-5 条，不只放表格。
4. 优先级矩阵：用 Mermaid `quadrantChart` 或 Markdown 表格展示“影响力 × 可落地性”。
5. 大厂资讯 / 工程博客 / Research。
   - 按公司/实验室细分，例如：OpenAI、Anthropic、Google DeepMind、Meta AI、NVIDIA、Hugging Face、腾讯、字节、SpaceAI。
   - 必须包含“公司来源扫描矩阵”，即使某家公司今天没有高相关新项也要出现状态。
   - 可加公司信号图或 timeline。
6. GitHub 高 star Top 10。
   - 单独表格，不得省略。
   - 重点看 AI Infra、LLM serving/training、agent、eval、RL、world model、MLOps。
7. GitHub star 增长最快 Top 10。
   - 单独表格，不得省略。
   - 真实增长优先；无历史 snapshot 时明确标注冷启动代理。
8. 论文。
   - 按主题细分，例如：Serving、RLHF、Agent Eval、World Model、Quantization。
   - 可加 `timeline` 展示近几天论文趋势。
9. 资讯 / 其他项目。
   - 按主题细分，例如：LLM Serving、AI Infra、RL Environment、Eval、Agent Framework。
   - 可加生态关系网或架构图。
10. 按主题索引。
11. 值得后续深挖。
12. 采集失败或低置信来源。

日报至少包含 2 种非表格可视化/结构化元素：

- Mermaid 态势图、象限图、时间线、mindmap、关系网中的至少一种。
- 必读卡片区、主题 radar 表、行动清单、影响力矩阵中的至少一种。

日报表格每条必须包含：

- 标签：必读 / 可 skim / 后续 / 低置信。
- 大类：论文 / 博客 / 资讯 / GitHub。
- 小类：主题、公司、实验室、人物或作者。
- 标题。
- 重点概括：中文，不能只是英文 description 截断。
- 为什么重要：从用户背景解释价值。
- Obsidian 详情：`[[path/to/note]]`。
- 网页详情：GitHub blob URL。
- 原文：原始来源链接。

## 来源标注要求

### 论文

论文必须明确标注：

- 论文来源：arXiv、OpenReview、Semantic Scholar、Papers with Code、NeurIPS/ICML/ICLR 会议页、公司 Research Blog 等。
- 来源类型：预印本、会议论文、公司论文页、代码榜单、论文索引等。
- 作者/机构。
- 发布时间。
- abs 链接。
- PDF 链接。
- 代码链接：未发现则写“未发现”。
- Semantic Scholar / OpenReview / 会议页：有则写。

论文过滤必须严格：只纳入 AI Infra、LLM、agent、RL、eval、serving、training、post-training、world model 强相关论文。弱相关论文放入低置信或跳过。

### 博客 / 大厂动态

大厂博客必须明确标注：

- 发布方/大厂，例如 OpenAI、Anthropic、Google DeepMind、Meta AI、NVIDIA、Microsoft、Hugging Face、腾讯、字节、SpaceAI。
- 栏目/来源类型，例如 News、Research、Engineering Blog、Technical Blog、Product Announcement。
- 作者/机构。
- 发布时间。
- 原文链接。

不要只写“博客”。

### GitHub / 资讯

GitHub 项目必须明确标注：

- repo。
- stars / forks。
- 语言。
- 最近更新时间。
- topics。
- 原文链接。
- 是否有 benchmark / docs / examples / release。
- 是否值得试用。

GitHub 必须分成两个固定榜单：

1. `GitHub 高 star Top 10`：按 stars 排序，重点关注 AI Infra、LLM serving/training、agent、eval、RL、world model、MLOps。不能只给 3 个项目。
2. `GitHub star 增长最快 Top 10`：按 `stars_delta` 排序；如果没有昨日 snapshot，则用冷启动代理，并写明“非真实日增”。

每次运行必须做 snapshot：

- 读取最近一个 `Automation/state/github-stars-*.json` 作为 baseline。
- 把今天扫描到的 repo 元数据保存到 `Automation/state/github-stars-YYYY-MM-DD.json`。
- snapshot 字段至少包含：`repo`, `stars`, `forks`, `language`, `updated_at`, `pushed_at`, `topics`, `html_url`, `description`, `collected_at`。

## 详情页要求

详情页必须比日报更深，不允许只有几句话。

每个重要详情页必须包含：

1. 一句话结论。
2. TL;DR。
3. 元信息表。
4. 信息压缩图示。
5. 专业解读。
6. 通俗解释。
7. 关键机制拆解。
8. 对我的影响。
9. 可信度与局限性。
10. 我应该如何跟进。
11. 相关链接。
12. 标签。

## 图示与结构要求

必须参考：

- `Templates/mermaid-patterns.md`

Obsidian 支持丰富 Mermaid，所以不要只用单调流程图。图示是压缩信息的核心，不是装饰。

### 日报图示

日报必须至少包含 2 种不同类型的结构化呈现，优先组合：

- `flowchart` 今日态势图：表达大厂信号、论文趋势、GitHub 项目和行动建议之间的关系。
- `quadrantChart` 优先级矩阵：影响力 × 可落地性。
- `timeline` 时间线：新发布/更新的时间序列。
- `mindmap` 主题树：AI Infra、LLM、RL、Agent、Eval 的今日分布。
- Markdown 卡片区 / callout：展示 Top 3-5 必读内容。
- Markdown 矩阵表：主题 × 来源 × 推荐动作。

日报不能只有一个长表。

### 详情页图示

每个重要论文、博客、资讯详情页至少包含 2 个视觉/结构模块：

1. 一张 Mermaid 主图，8-15 个节点，使用 `subgraph`、`classDef`、具体节点名、多路径逻辑。
2. 一个辅助结构：机制表、影响矩阵、timeline、quadrantChart、mindmap、sequenceDiagram、gantt 或关系网。

不要只画简单 A -> B -> C。必要时使用：

- `flowchart TB/LR`
- `mindmap`
- `sequenceDiagram`
- `timeline`
- `quadrantChart`
- `gantt`
- `pie`
- 关系网 graph
- Markdown 表格/矩阵/callout

### 论文图示

论文图示必须表达：

- 论文来源。
- 研究问题。
- 方法模块。
- 训练/推理流程。
- 实验信号。
- 局限性。
- 阅读/复现决策。

### 大厂博客图示

大厂博客图示必须表达：

- 发布方/大厂。
- 文章/公告信号。
- 产品方向。
- 研究方向。
- 工程瓶颈。
- 对 AI Infra / LLM / RL 的影响。
- 我的行动建议。

### AI Infra 项目图示

AI Infra 项目图示必须表达：

- workload。
- 系统核心组件。
- runtime / scheduler / cache / control plane。
- 硬件和依赖。
- 成本、吞吐、延迟、风险。
- 是否值得试用。

## 写作风格

- 中文输出。
- 专业讲解先行，再给通俗解释。
- 不要泛泛地说“值得关注”。必须说明为什么值得关注。
- 不要堆砌信息。日报 10-20 条，详情页展开。
- 每条必须保留原文链接。
- 低置信内容要明确标注低置信，不要混入必读。

## 运行前后验收检查

生成日报前必须读取本文件和 `Sources/sources.yaml`。生成日报后必须检查当天 `Daily/YYYY-MM-DD.md` 是否满足以下硬性条件，不满足就继续补齐，不要直接推送：

- 存在 `## 5. 大厂资讯 / 工程博客 / Research`。
- 存在 `### 5.1 公司来源扫描矩阵`，且矩阵包含 OpenAI、Anthropic、Google DeepMind、Meta AI、NVIDIA、Microsoft、Hugging Face、腾讯、字节、SpaceAI。
- 存在 `## 6. GitHub 高 star Top 10`，表内尽量 10 条；不足 10 条必须写明原因。
- 存在 `## 7. GitHub star 增长最快 Top 10`，表内尽量 10 条；若无历史 snapshot 必须写“冷启动代理，非真实日增”。
- 存在 `Automation/state/github-stars-YYYY-MM-DD.json`。
- Telegram 摘要必须提到大厂扫描、GitHub 高 star Top 10、GitHub 增长 Top 10 是否已生成。

## GitHub / Telegram

- Obsidian vault：`/home/vscode-server/obsidian-ai-radar`
- Git remote：`git@github-tt:dyt27666-oss/AI-news-report-obsidians.git`
- 网页详情链接格式：`https://github.com/dyt27666-oss/AI-news-report-obsidians/blob/main/<note_path>.md`
- Telegram 推送必须包含可直接点击的 GitHub 日报网页链接。

## 安全要求

- 不要删除 vault 中已有内容。
- 不要覆盖非当天日报，除非是在更新当天文件。
- git 操作只允许在 `/home/vscode-server/obsidian-ai-radar` 内执行。
