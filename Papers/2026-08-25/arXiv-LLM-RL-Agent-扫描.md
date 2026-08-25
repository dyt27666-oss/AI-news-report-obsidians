# arXiv LLM/RL/Agent 扫描 - 2026-08-25

> 一句话结论：今日 arXiv 扫描仅作为候选入口；未阅读全文的论文不升级为必读。

## 候选表
| 论文来源 / 来源类型 | 标题 | 作者/机构 | 发布时间 | 摘要压缩 | PDF/原文 |
|---|---|---|---|---|---|
| arXiv / 预印本索引 | 低置信扫描 | arXiv API | 未确认 | LLM serving inference: HTTP Error 429: Too Many Requests；reinforcement learning language models: HTTP Error 429: Unknown Error | [原文](https://arxiv.org/search/advanced) |

## 论文扫描机制图
```mermaid
flowchart TB
  subgraph Query[查询]
    Q1[LLM serving]
    Q2[RLHF / post-training]
    Q3[Agent eval]
    Q4[World model / Game AI]
  end
  subgraph Filter[过滤]
    F1[AI Infra 强相关]
    F2[RL/Game AI 强相关]
    F3[弱相关降级]
  end
  subgraph Decision[决策]
    D1[必读: 需阅读全文]
    D2[可 skim: 摘要候选]
    D3[低置信: API/相关性不足]
  end
  Q1 --> F1 --> D2
  Q2 --> F1
  Q3 --> F1
  Q4 --> F2 --> D2
  F3 --> D3
  classDef query fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
  classDef filter fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef decision fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  class Q1,Q2,Q3,Q4 query; class F1,F2,F3 filter; class D1,D2,D3 decision;
```

## 可信度与局限性
- 错误/限制：LLM serving inference: HTTP Error 429: Too Many Requests; reinforcement learning language models: HTTP Error 429: Unknown Error
- 未阅读全文，不编造方法贡献或实验结果。

#ai-radar #papers #arxiv
