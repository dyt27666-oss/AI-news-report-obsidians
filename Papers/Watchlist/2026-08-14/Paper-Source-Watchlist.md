# Paper Source Watchlist - 2026-08-14

> 一句话结论：今日论文 API 可访问性/相关性有限，只把可追踪 arXiv 条目作为 watchlist，不编造论文结论。

```mermaid
flowchart TB
  Q1[LLM serving / inference] --> A[arXiv query]
  Q2[RL language models / agent eval] --> A
  Q3[Rummy imperfect-information game] --> A
  A --> V[严格相关性过滤]
  V --> P[候选论文 watchlist]
  V --> R[低相关跳过]
  P --> N[下一轮深读/复现]
  classDef q fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
  classDef p fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef r fill:#f8cecc,stroke:#b85450,stroke-width:2px;
  class Q1,Q2,Q3 q; class A,V,P,N p; class R r;
```

## 候选


## 失败/低置信

- LLM serving inference scheduler: The read operation timed out
- reinforcement learning language models agent evaluation: The read operation timed out
- gin rummy imperfect information game AI: The read operation timed out

#ai-radar #papers #watchlist
