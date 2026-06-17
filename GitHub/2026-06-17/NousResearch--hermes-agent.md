# NousResearch/hermes-agent

> 类型：GitHub 项目
> 大类：GitHub
> 小类：Agent Infra / Personal AI OS
> 推荐等级：必读
> 创建日期：2026-06-17
> 原文链接：https://github.com/NousResearch/hermes-agent
> 网页详情：https://github.com/dyt27666-oss/AI-news-report-obsidians/blob/main/GitHub/2026-06-17/NousResearch--hermes-agent.md
> 返回日报：[[Daily/2026-06-17]]

## 一句话结论

Hermes Agent 继续以真实 snapshot 日增 +903 增长，说明 skills、plugins、gateway、cron、Obsidian-first knowledge loop 这类 agent runtime 能力仍是高热方向。

## TL;DR

- **它是什么**：可扩展 agent runtime，强调技能、工具、网关、自动化任务和长期上下文。
- **为什么重要**：它把 agent 从一次性 CLI 变成可积累流程资产的系统。
- **和我相关的点**：当前 AI Radar 本身就是 Hermes cron + Obsidian + GitHub push 的组合，项目方向与用户工作流完全重合。
- **建议动作**：必读；持续跟踪权限、安全、skills 复用、MCP/gateway 设计。

## 元信息

| 字段 | 内容 |
|---|---|
| repo | NousResearch/hermes-agent |
| stars / forks | 195361 / 34307 |
| language | Python |
| updated_at | 2026-06-17T01:00:19Z |
| topics | ai, ai-agent, ai-agents, anthropic, chatgpt, claude |
| benchmark/docs/examples/release | docs/skills/plugins 明显；benchmark 需确认 |
| 是否值得试用 | 是 |
| 原文 | [GitHub](https://github.com/NousResearch/hermes-agent) |

## 信息压缩图示

```mermaid
flowchart TB
  subgraph Workload[Workload]
    W1[定时研究任务]
    W2[代码修改/审查]
    W3[Obsidian 知识库]
  end
  subgraph Runtime[Hermes Runtime]
    R1[Skills]
    R2[Plugins]
    R3[Gateway]
    R4[Cron Jobs]
    R5[Memory/Notes]
  end
  subgraph Control[控制面]
    C1[权限边界]
    C2[工具注册]
    C3[执行日志]
  end
  subgraph Outcome[结果]
    O1[流程复用]
    O2[知识沉淀]
    O3[自动交付]
    O4[安全风险]
  end
  W1 --> R4 --> R1
  W2 --> R2 --> C2
  W3 --> R5 --> O2
  R3 --> C1
  C3 --> O3
  R1 --> O1
  C1 --> O4
  classDef workload fill:#fff2cc,stroke:#d6b656,stroke-width:2px,color:#111;
  classDef runtime fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#111;
  classDef control fill:#e1d5e7,stroke:#9673a6,stroke-width:2px,color:#111;
  classDef outcome fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#111;
  classDef risk fill:#f8cecc,stroke:#b85450,stroke-width:2px,color:#111;
  class W1,W2,W3 workload;
  class R1,R2,R3,R4,R5 runtime;
  class C1,C2,C3 control;
  class O1,O2,O3 outcome;
  class O4 risk;
```

```mermaid
quadrantChart
  title Hermes Agent 试用优先级
  x-axis 低可落地性 --> 高可落地性
  y-axis 低影响力 --> 高影响力
  quadrant-1 立即试用
  quadrant-2 深读架构
  quadrant-3 暂存
  quadrant-4 工具化
  Skills/Cron/Obsidian: [0.90, 0.92]
  企业权限模型: [0.55, 0.82]
  通用聊天能力: [0.65, 0.45]
```

## 专业解读

Hermes 的价值在于把“提示词经验”提升为可版本化的技能，把“临时工具调用”提升为插件和网关，把“我每天要做的事”提升为 cron job。对于 AI Infra 工程师，这类系统提供了一个 agent control plane 的雏形：工具注册、权限、上下文、执行日志、结果交付和知识库存储。

增长 +903 也说明市场仍在寻找 Claude Code/Codex/OpenCode 之外的个人/团队 agent runtime。需要注意的是，增长不等于稳定性；真正可生产化还要看权限隔离、错误恢复和 eval。

## 通俗解释

它像一个会不断学会你工作流程的自动化同事：今天做日报，明天做代码审查，后天把这些流程沉淀成技能。

## 关键机制拆解

| 机制 | 解决的问题 | ���什么有效 | 可能的坑 |
|---|---|---|---|
| Skills | 经验难复用 | 把流程写成可调用程序记忆 | 技能过期会误导 |
| Cron | 人工触发成本高 | 自动执行周期任务 | 失败后需可观测 |
| Gateway/Plugins | 工具接入混乱 | 统一工具接口 | 权限风险 |

## 对我的影响

| 维度 | 影响 | 建议动作 |
|---|---|---|
| AI Infra | agent control plane 样例 | 深读架构 |
| LLM 工程 | 支持 coding/research loop | 跟踪技能复用 |
| RL / Game AI | 可沉淀环境操作技能 | 暂时观察 |
| Agent / Eval | 高度相关 | 设计 eval/trace |

## 可信度与局限性

- 证据强度：高热度 + 本地正在使用；但 star 增长不代表工程成熟。
- 局限性：需要持续验证稳定性、安全和插件生态。
- 潜在风险：自动化误操作、权限过宽、技能陈旧。
- 还需要确认：生产部署模式、权限模型、回滚机制。

## 我应该如何跟进

1. 继续用 AI Radar cron 作为 dogfood。
2. 把失败的采集/验证流程沉淀为更强的技能。
3. 关注 agent-vault / MCP gateway / trace eval 的整合机会。

## 相关链接

- 原文：https://github.com/NousResearch/hermes-agent
- 网页详情：https://github.com/dyt27666-oss/AI-news-report-obsidians/blob/main/GitHub/2026-06-17/NousResearch--hermes-agent.md
- 相关卡片：[[Daily/2026-06-17]]

## 标签

#ai-radar #github #agent #hermes #ai-infra
