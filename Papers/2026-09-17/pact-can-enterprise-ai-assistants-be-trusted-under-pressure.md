# PACT: Can Enterprise AI Assistants Be Trusted Under Pressure?

> 类型：论文
> 大类：论文
> 小类：AI Infra / LLM / RL / Agent
> 推荐等级：可 skim
> 创建日期：2026-09-17
> 原文链接：https://arxiv.org/abs/2609.18605v1
> PDF：https://arxiv.org/pdf/2609.18605v1
> 返回日报：[[Daily/2026-09-17]]

## 一句话结论

这篇论文被今日 arXiv 扫描命中，主题与 LLM/RL/Agent/Serving 相关，适合作为低到中置信候选继续筛。

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文来源 | arXiv |
| 来源类型 | 预印本 / 论文索引 |
| 作者/机构 | Mika Okamoto, Ansel Kaplan Erol |
| 发布时间 | 2026-09-16 |
| arXiv | [abs](https://arxiv.org/abs/2609.18605v1) |
| PDF | [pdf](https://arxiv.org/pdf/2609.18605v1) |
| 代码 | 未发现 |
| Categories | cs.CL, cs.AI, cs.CY, cs.LG |

## 方法/系统图示

```mermaid
flowchart TB
  subgraph Q[研究问题]
    Q1[标题信号: PACT: Can Enterprise AI Assistants Be Trus]
    Q2[领域: cs.CL, cs.AI, cs.CY, cs.LG]
    Q3[待确认: benchmark/代码/实验规模]
  end
  subgraph M[可能方法]
    M1[模型/算法]
    M2[训练或推理流程]
    M3[评估协议]
  end
  subgraph D[阅读决策]
    D1[读摘要]
    D2[查代码]
    D3[若贴近 serving/RL/agent 再深读]
  end
  Q1 --> M1 --> D1
  Q2 --> M2 --> D2
  Q3 --> M3 --> D3
  classDef problem fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
  classDef method fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef decision fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  class Q1,Q2,Q3 problem; class M1,M2,M3 method; class D1,D2,D3 decision;
```

```mermaid
quadrantChart
  title 论文阅读决策：新意 × 可复现性
  x-axis 低可复现 --> 高可复现
  y-axis 低新意 --> 高新意
  quadrant-1 优先复现
  quadrant-2 读方法
  quadrant-3 暂存
  quadrant-4 工程可试
  当前论文: [0.45, 0.62]
```

## 摘要压缩

As corporate AI adoption continues to grow, enterprise-grade LLM agents are being deployed into sensitive contexts such as hiring, healthcare, and finance. In these contexts, compliance with rules specified in an agent's system context is a first-order legal concern. Currently, no evaluation framework systematically measures which LLM models tend to violate compliance rules, especially under pressure from a persistent user, a hurried manager, or circumstances where violation is convenient or attractive. We introduce PACT (Pressure-Applied Compliance Testing), a benchmark for rule-following under pressure in AI agents assisting employees in daily tasks across twelve regulated enterprise domains and forty-eight scenarios, each set in a realistic multi-turn conversation. Each benchmark item pairs a standing rule against a rule-violating shortcut, and applies a battery of pressures across different wordings and system-prompt modes. We construct PACT component by component under strict LLM-as-judge auditing to ensure samples are unambiguous, ungameable, and realistic enough to avoid eliciting evaluation-aware behavior. We use PACT to profile LLM compliance across six complementary metrics that create a holistic picture of an AI assistant's robustness under pressure and throughout multi-turn conversations, its transparency, and ability to correctly discern where a rule applies. We aggregate this profile into PACTScore, a reliability-weighted compliance rate over all items and modes. Our results across 22 common LLM models spanning multiple providers and sizes show substantial variability in compliance across models and metric dimensions. Even the strongest assistants mis-apply a rule on 6 to 10% of items, and ordinary user pressure raises the violation rate by 65% on average. PACT highlights compliance risks in LLM assistants, motivating guardrails and careful model selection.

## 对我的影响

| 维度 | 影响 | 建议动作 |
|---|---|---|
| AI Infra | 先确认是否有系统/Serving/训练效率贡献 | skim |
| LLM 工程 | 看是否涉及模型训练、推理或 eval | 读摘要 |
| RL / Game AI | 若涉及 RL/world model/imperfect information，可后续深挖 | 加入观察 |
| Agent / Eval | 若涉及 agent evaluation，可纳入 benchmark 列表 | 查实验 |

## 相关链接

- 原文：https://arxiv.org/abs/2609.18605v1
- PDF：https://arxiv.org/pdf/2609.18605v1

## 标签

#ai-radar #paper
