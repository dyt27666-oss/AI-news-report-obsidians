# arXiv LLM Serving / Agent Eval / RLHF Watchlist - 2026-09-10

> 论文来源：arXiv / Semantic Scholar 预印本索引  
> 来源类型：API 低置信 watchlist  
> 原文：https://arxiv.org/search/?query=LLM+serving+agent+evaluation+reinforcement+learning+language+models&searchtype=all

## 一句话结论
今日论文侧保持低置信 watchlist：优先等待 arXiv / Semantic Scholar 稳定后再纳入具体论文，避免把 API 失败时的未验证条目写成结论。

## TL;DR
- 关注主题：LLM serving、agent evaluation、RLHF/GRPO、world model、game RL、distributed training。
- 今日动作：保留入口，不编造标题/摘要/作者。
- 下一步：重试后为强相关论文生成独立 `Papers/...` 详情页。

## 信息压缩图示
```mermaid
flowchart TB
  subgraph Query[查询方向]
    Q1[LLM serving]
    Q2[Agent evaluation]
    Q3[RLHF / GRPO]
    Q4[World model / Game RL]
  end
  subgraph Verify[验证要求]
    V1[arXiv abs/pdf]
    V2[作者/机构]
    V3[代码/benchmark]
    V4[Semantic Scholar 引用]
  end
  subgraph Decision[阅读决策]
    D1[强相关才入日报]
    D2[低置信保留 watchlist]
    D3[不编造论文结论]
  end
  Q1 --> V1 --> D1
  Q2 --> V2 --> D1
  Q3 --> V3 --> D1
  Q4 --> V4 --> D2
  V1 --> D3
  classDef query fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
  classDef verify fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef decision fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  class Q1,Q2,Q3,Q4 query; class V1,V2,V3,V4 verify; class D1,D2,D3 decision;
```

## 跟进清单
| 主题 | 复核目标 | 入选标准 |
|---|---|---|
| Serving | KV cache / scheduler / speculative decoding | 有工程指标或可复现代码 |
| RLHF/GRPO | reward design / rollout infra | 与 post-training pipeline 强相关 |
| Agent Eval | benchmark / harness / replay | 能改善 coding-agent loop |
| Game AI | imperfect information / self-play | 可映射到 Rummy state/action/reward |

#ai-radar #papers #arxiv #low-confidence
