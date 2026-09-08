# arXiv LLM Serving / Agent Eval / RLHF Watchlist - 2026-09-08

> 一句话结论：论文侧今日以可验证 arXiv 入口和低置信 watchlist 为主；只保留 AI Infra、LLM、Agent、RL 强相关候选，不编造摘要外结论。

## TL;DR
- [RefactorPlatform: An Open-Source Harness for Controlled Evaluation of Repository-Scale Refactoring Agents](https://arxiv.org/abs/2609.04898v1) — Aziz Ben Amor, Drish Mali, Mann Acharya, Vijayasri Iyer，2026-09-04
- [Harbor Adapters and Harbor-Index: Infrastructure and a Curated Meta-Dataset for Large-Scale Agentic Evaluation](https://arxiv.org/abs/2609.04298v1) — Lin Shi, Haowei Lin, Zixuan Zhu, Xiaoyue Zhou，2026-09-03

## 论文来源与来源类型
| 字段 | 内容 |
|---|---|
| 论文来源 | arXiv |
| 来源类型 | 预印本 / API 查询 |
| 查询主题 | LLM serving、agent evaluation、reinforcement learning language models |
| 低置信/失败 | cat:cs.LG AND all:"LLM serving": The read operation timed out; cat:cs.LG AND all:"reinforcement learning language models": HTTP Error 429: Unknown Error |

## 研究信号图
```mermaid
flowchart TB
  subgraph Q[研究问题]
    Q1[LLM serving 吞吐/延迟]
    Q2[Agent evaluation 可靠性]
    Q3[RL/post-training 奖励与 rollout]
  end
  subgraph M[方法观察]
    M1[调度/KV/cache]
    M2[benchmark/eval harness]
    M3[PPO/DPO/GRPO/self-play]
  end
  subgraph D[决策]
    D1[先读摘要]
    D2[找代码/benchmark]
    D3[低置信不进入深读]
  end
  Q1 --> M1 --> D2
  Q2 --> M2 --> D1
  Q3 --> M3 --> D2
  D1 --> D3
  classDef problem fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
  classDef method fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef decision fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  class Q1,Q2,Q3 problem; class M1,M2,M3 method; class D1,D2,D3 decision;
```

## 跟进
- 逐条验证 PDF、代码链接和 benchmark，再决定是否生成单篇深度详情。

#ai-radar #paper #arxiv
