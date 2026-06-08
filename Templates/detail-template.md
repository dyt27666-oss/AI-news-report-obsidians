# {{title}}

> 类型：{{type}}
> 大类：{{major_category}}
> 小类：{{minor_category}}
> 推荐等级：{{priority}}
> 创建日期：{{date}}
> 原文链接：{{source_url}}
> 网页详情：{{github_blob_url}}
> 返回日报：[[Daily/{{date}}]]

## 一句话结论

{{one_line_takeaway}}

## TL;DR

- **它是什么**：{{what_it_is}}
- **为什么重要**：{{why_it_matters}}
- **和我相关的点**：{{why_relevant_to_user}}
- **建议动作**：{{recommended_action}}

## 元信息

| 字段 | 内容 |
|---|---|
| 发布方/来源 | {{source_name}} |
| 大厂/实验室 | {{company_or_lab}} |
| 栏目/来源类型 | {{source_type}} |
| 作者/机构 | {{authors_or_org}} |
| 发布时间 | {{published_at}} |
| 原文 | [原文]({{source_url}}) |
| 代码 | {{code_url}} |
| PDF | {{pdf_url}} |
| 标签 | {{tags}} |

## 信息压缩图示

图示是详情页的核心。不要只给单张单调流程图。每个重要详情页至少包含一个 Mermaid 主图和一个辅助视觉结构，例如影响矩阵、时间线、象限图、关系网、mindmap 或机制表。

### 主图：机制 / 系统逻辑

优先使用 Mermaid，把系统逻辑、因果关系、数据流、决策点、收益/风险压缩到一张图里。允许更丰富、更“花”的结构，但必须帮助理解，不要装饰。

```mermaid
flowchart TB
  %% 用 8-15 个节点表达逻辑关系；节点名要具体，不能只写 A/B/C。
  subgraph Problem[问题背景]
    P1[现有痛点: {{pain_point_1}}]
    P2[工程约束: {{constraint_1}}]
  end

  subgraph Idea[核心想法]
    I1[关键机制 1: {{mechanism_1}}]
    I2[关键机制 2: {{mechanism_2}}]
    I3[关键机制 3: {{mechanism_3}}]
  end

  subgraph System[系统/方法流程]
    S1[输入/请求]
    S2[处理路径]
    S3[调度/训练/检索]
    S4[输出/反馈]
  end

  subgraph Impact[影响]
    E1[收益: {{benefit_1}}]
    E2[代价/风险: {{risk_1}}]
    E3[我该怎么用: {{action_short}}]
  end

  P1 --> I1
  P2 --> I2
  I1 --> S1 --> S2 --> S3 --> S4
  I2 --> S3
  I3 --> S4
  S4 --> E1
  S3 --> E2
  E1 --> E3

  classDef hot fill:#ffe4d6,stroke:#d35400,stroke-width:2px,color:#111;
  classDef core fill:#d6ecff,stroke:#1f77b4,stroke-width:2px,color:#111;
  classDef risk fill:#ffe1e1,stroke:#c0392b,stroke-width:2px,color:#111;
  class P1,I1,I2,S3,E1 hot;
  class I3,S1,S2,S4,E3 core;
  class E2 risk;
```

### 辅助图：影响力 × 可落地性

```mermaid
quadrantChart
  title 影响力 × 可落地性
  x-axis 低可落地性 --> 高可落地性
  y-axis 低影响力 --> 高影响力
  quadrant-1 立即试用/深读
  quadrant-2 关注趋势
  quadrant-3 暂存
  quadrant-4 可工具化
  当前条目: [{{implementation_score}}, {{impact_score}}]
```

## 专业解读

{{professional_explanation}}

要求覆盖：

- 技术/系统问题的本质。
- 核心机制如何工作。
- 和已有方案相比的新意。
- 工程落地条件：依赖、规模、硬件、数据、评估。
- 对 AI Infra / LLM / RL 的潜在影响。

## 通俗解释

{{plain_explanation}}

## 关键机制拆解

| 机制 | 解决的问题 | 为什么有效 | 可能的坑 |
|---|---|---|---|
| {{mechanism_1}} | {{problem_1}} | {{why_works_1}} | {{pitfall_1}} |
| {{mechanism_2}} | {{problem_2}} | {{why_works_2}} | {{pitfall_2}} |
| {{mechanism_3}} | {{problem_3}} | {{why_works_3}} | {{pitfall_3}} |

## 对我的影响

| 维度 | 影响 | 建议动作 |
|---|---|---|
| AI Infra | {{infra_impact}} | {{infra_action}} |
| LLM 工程 | {{llm_impact}} | {{llm_action}} |
| RL / Game AI | {{rl_impact}} | {{rl_action}} |
| Agent / Eval | {{agent_eval_impact}} | {{agent_eval_action}} |

## 可信度与局限性

- 证据强度：{{evidence_strength}}
- 局限性：{{limitation_1}}
- 潜在风险：{{risk_1}}
- 还需要确认：{{open_question_1}}

## 我应该如何跟进

1. {{next_step_1}}
2. {{next_step_2}}
3. {{next_step_3}}

## 相关链接

- 原文：{{source_url}}
- 网页详情：{{github_blob_url}}
- 代码：{{code_url}}
- PDF：{{pdf_url}}
- 相关卡片：{{related_notes}}

## 标签

#ai-radar {{tags}}
