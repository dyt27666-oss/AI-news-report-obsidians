# {{paper_title}}

> 类型：论文
> 大类：论文
> 小类：{{topic}}
> 推荐等级：{{priority}}
> 创建日期：{{date}}
> 原文链接：{{paper_url}}
> PDF：{{pdf_url}}
> 网页详情：{{github_blob_url}}
> 返回日报：[[Daily/{{date}}]]

## 一句话结论

{{one_line_takeaway}}

## TL;DR

- **研究问题**：{{problem_short}}
- **核心方法**：{{method_short}}
- **关键结果**：{{result_short}}
- **对我的价值**：{{user_value}}
- **建议动作**：{{recommended_action}}

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文来源 | {{paper_source}} |
| 来源类型 | {{source_type}} |
| 标题 | {{paper_title}} |
| 作者/机构 | {{authors}} |
| 发布时间 | {{published_at}} |
| arXiv | [abs]({{arxiv_url}}) |
| OpenReview / 会议页 | {{openreview_or_conference_url}} |
| Semantic Scholar | {{semantic_scholar_url}} |
| PDF | [pdf]({{pdf_url}}) |
| 代码 | {{code_url}} |
| 方向 | {{topic}} |

## 方法/系统图示

图示必须比文字更“信息密集”。不要只给单张单调流程图。每篇重要论文至少包含一个 Mermaid 主图和一个辅助视觉结构，例如时间线、象限图、机制表、mindmap 或实验矩阵。主图表达问题、方法模块、训练/推理流程、实验信号、局限性和我该不该读；如果论文原图非常关键，也可在 Mermaid 后附原图链接。

```mermaid
flowchart TB
  subgraph Q[1. 研究问题]
    Q1[目标: {{problem_short}}]
    Q2[难点: {{challenge_1}}]
    Q3[现有方法缺口: {{gap_1}}]
  end

  subgraph M[2. 方法结构]
    M1[模块 A: {{module_a}}]
    M2[模块 B: {{module_b}}]
    M3[模块 C: {{module_c}}]
  end

  subgraph Pipeline[3. 训练/推理流程]
    D[数据/任务] --> T[训练或优化]
    T --> I[推理/交互]
    I --> O[输出/行为]
  end

  subgraph Eval[4. 实验与证据]
    E1[Benchmark: {{benchmark_1}}]
    E2[指标: {{metric_1}}]
    E3[结论: {{result_short}}]
  end

  subgraph Read[5. 阅读决策]
    R1[适合深读: {{read_if}}]
    R2[可以跳过: {{skip_if}}]
  end

  Q1 --> M1
  Q2 --> M2
  Q3 --> M3
  M1 --> T
  M2 --> T
  M3 --> I
  O --> E1 --> E2 --> E3
  E3 --> R1
  E3 --> R2

  classDef problem fill:#fff2cc,stroke:#d6b656,stroke-width:2px,color:#111;
  classDef method fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#111;
  classDef eval fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#111;
  classDef decision fill:#f8cecc,stroke:#b85450,stroke-width:2px,color:#111;
  class Q1,Q2,Q3 problem;
  class M1,M2,M3,D,T,I,O method;
  class E1,E2,E3 eval;
  class R1,R2 decision;
```

### 辅助图：阅读/复现决策矩阵

```mermaid
quadrantChart
  title 论文阅读决策：新意 × 可复现性
  x-axis 低可复现 --> 高可复现
  y-axis 低新意 --> 高新意
  quadrant-1 优先复现
  quadrant-2 读方法
  quadrant-3 暂存
  quadrant-4 工程可试
  当前论文: [{{reproducibility_score}}, {{novelty_score}}]
```

## 专业解读

{{professional_explanation}}

必须覆盖：

- 论文到底解决什么问题。
- 方法核心是什么，不要只翻译摘要。
- 和已有工作相比差异在哪里。
- 实验设置是否可信，benchmark 是否贴近真实场景。
- 是否有代码，是否值得复现。
- 对 AI Infra / LLM / RL / Agent Eval 的影响。

## 通俗解释

{{plain_explanation}}

## 方法拆解

| 组件 | 作用 | 输入 | 输出 | 关键假设 |
|---|---|---|---|---|
| {{component_1}} | {{role_1}} | {{input_1}} | {{output_1}} | {{assumption_1}} |
| {{component_2}} | {{role_2}} | {{input_2}} | {{output_2}} | {{assumption_2}} |
| {{component_3}} | {{role_3}} | {{input_3}} | {{output_3}} | {{assumption_3}} |

## 实验与证据

| 实验 | 说明 | 我怎么看 |
|---|---|---|
| {{experiment_1}} | {{experiment_result_1}} | {{interpretation_1}} |
| {{experiment_2}} | {{experiment_result_2}} | {{interpretation_2}} |

## 局限性 / 风险

- {{limitation_1}}
- {{limitation_2}}
- {{risk_1}}

## 对我的影响

| 维度 | 影响 | 建议动作 |
|---|---|---|
| AI Infra | {{infra_impact}} | {{infra_action}} |
| LLM 工程 | {{llm_impact}} | {{llm_action}} |
| RL / Game AI | {{rl_impact}} | {{rl_action}} |
| Agent / Eval | {{agent_eval_impact}} | {{agent_eval_action}} |

## 相关链接

- 原文：{{paper_url}}
- PDF：{{pdf_url}}
- 网页详情：{{github_blob_url}}
- 代码：{{code_url}}
- 相关卡片：{{related_notes}}

## 标签

#ai-radar #paper {{tags}}
