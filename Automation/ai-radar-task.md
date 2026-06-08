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

## 日报结构

日报必须按大类组织，不要混成一个长表。

推荐结构：

1. 今日结论。
2. 必读 / 高优先级。
3. 论文。
   - 按主题细分，例如：Serving、RLHF、Agent Eval、World Model、Quantization。
4. 博客。
   - 按公司/实验室细分，例如：OpenAI、Anthropic、Google DeepMind、Meta AI、NVIDIA、Hugging Face、腾讯、字节、SpaceAI。
5. 资讯 / GitHub 项目。
   - 按主题细分，例如：LLM Serving、AI Infra、RL Environment、Eval、Agent Framework。
6. 按主题索引。
7. 值得后续深挖。
8. 采集失败或低置信来源。

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

## Mermaid 图示要求

必须参考：

- `Templates/mermaid-patterns.md`

Obsidian 支持 Mermaid，所以图示可以丰富一些。图示是压缩信息的核心，不是装饰。

每个重要论文、博客、资讯详情页至少一张 Mermaid 图。图示应该包含 8-15 个节点，并使用：

- `subgraph` 分组。
- `classDef` 配色。
- 具体节点名。
- 多路径逻辑，而不是简单 A -> B -> C。
- 必要时使用 `flowchart TB/LR`、`mindmap`、`sequenceDiagram`、`timeline`、`quadrantChart`、`gantt`。

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

## GitHub / Telegram

- Obsidian vault：`/home/vscode-server/obsidian-ai-radar`
- Git remote：`git@github-tt:dyt27666-oss/AI-news-report-obsidians.git`
- 网页详情链接格式：`https://github.com/dyt27666-oss/AI-news-report-obsidians/blob/main/<note_path>.md`
- Telegram 推送必须包含可直接点击的 GitHub 日报网页链接。

## 安全要求

- 不要删除 vault 中已有内容。
- 不要覆盖非当天日报，除非是在更新当天文件。
- git 操作只允许在 `/home/vscode-server/obsidian-ai-radar` 内执行。
