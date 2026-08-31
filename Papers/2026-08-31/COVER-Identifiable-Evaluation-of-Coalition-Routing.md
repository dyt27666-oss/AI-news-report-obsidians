# COVER: Identifiable Evaluation of Coalition Routing

> 一句话结论：这是一篇来自 arXiv 的摘要级候选，和 LLM/Agent/RL/Serving 的关系需要后续 PDF 细读确认。

## TL;DR
- 来源：arXiv / 预印本
- 作者：Raghul Sugumar, Amrit Gopinath
- 发布时间：2026-08-28
- Abs：https://arxiv.org/abs/2608.28475v1
- PDF：https://arxiv.org/pdf/2608.28475v1
- 代码链接：未发现

## 元信息表
| 字段 | 值 |
|---|---|
| 论文来源 | arXiv |
| 来源类型 | 预印本 / API 摘要级检索 |
| 查询来源 | agent evaluation coding agents |
| 原文 | https://arxiv.org/abs/2608.28475v1 |

## 论文机制图
```mermaid
flowchart TB
  subgraph Q[研究问题]
    Q1[LLM/Agent/RL 任务]
    Q2[当前瓶颈: 数据/奖励/上下文/评估]
    Q3[摘要级待确认缺口]
  end
  subgraph M[方法线索]
    M1[模型/Agent 机制]
    M2[训练或推理流程]
    M3[评测/Benchmark]
  end
  subgraph E[证据与决策]
    E1[arXiv 摘要]
    E2[需要 PDF 细读]
    E3[复现/跳过决策]
  end
  Q1 --> M1 --> E1
  Q2 --> M2 --> E2
  Q3 --> M3 --> E3
  E1 --> E2 --> E3
  classDef problem fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
  classDef method fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef evidence fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  class Q1,Q2,Q3 problem; class M1,M2,M3 method; class E1,E2,E3 evidence;
```

## 摘要压缩
When a multi-agent system changes its team, it also changes the messages and final answer it produces, so an end-to-end accuracy gap does not by itself identify a routing effect. We introduce method, an evaluation contract that fixes a public information boundary, downstream stack G, and finite legal team family before outcomes are generated. Complete coverage identifies exact finite-benchmark oracle regret conditional on that stack. For any finite collection of frozen policies, executing the union of their distinct selected teams is the minimal assumption-free support for every pairwise policy contrast, though not for absolute oracle regret. Two controlled tables with source-ID-disjoint splits test the instrument. On MuSiQue-12, a pre-specified privileged positive control improves regret from 0.532 to 0.402; a later public-interface control reaches 0.424 versus 0.554 but is retrospective. On HotpotQA-4, a pre-specified public direct scorer improves regret from 0.313 to 0.110. In fixed-stack Llama execution, verified route regret improves by 0.190, while the raw-answer gain is 0.010 with an interval crossing zero. A five-family ToolSandbox variant-shift validation exhaustively eval

## 对我的影响
- 若论文涉及 agent experience、coding agent、RL/post-training 或 serving benchmark，可转化为评测/复现实验。
- 当前只完成摘要级筛选，不能把未读 PDF 的细节当成确定结论。

## 跟进
1. 阅读 PDF 的方法和实验章节。
2. 搜索是否有代码或 benchmark。
3. 判断是否进入复现队列。

#ai-radar #paper #arxiv
