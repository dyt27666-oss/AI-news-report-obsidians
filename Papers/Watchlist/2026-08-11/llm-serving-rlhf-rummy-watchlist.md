# 论文源 watchlist - 2026-08-11

> 一句话结论：arXiv 今日返回 429/timeout，因此论文区只保留低置信 watchlist，不把无法验证的论文包装成必读。

## TL;DR
- 来源：arXiv API / Semantic Scholar 计划重试。
- 来源类型：预印本索引 / 论文元数据源。
- 今日状态：访问失败或超时；保守降级为 watchlist。
- 原文查询：https://export.arxiv.org/api/query?search_query=all:large+language+model+inference

## 信息压缩图示
```mermaid
flowchart TB
  subgraph Sources[论文来源]
    A[arXiv API]
    S[Semantic Scholar]
    O[OpenReview/会议页]
  end
  subgraph Queries[主题查询]
    Q1[LLM serving]
    Q2[RLHF/GRPO]
    Q3[Agent evaluation]
    Q4[Rummy/Game AI]
  end
  subgraph Decision[今日决策]
    D1[429/timeout]
    D2[低置信 watchlist]
    D3[不伪造摘要]
    D4[明日重试]
  end
  A --> Q1 --> D1 --> D2
  A --> Q2 --> D1
  S --> Q3 --> D2
  O --> Q4 --> D4
  D2 --> D3
  classDef source fill:#e1d5e7,stroke:#9673a6; classDef query fill:#dae8fc,stroke:#6c8ebf; classDef decision fill:#f8cecc,stroke:#b85450;
  class A,S,O source; class Q1,Q2,Q3,Q4 query; class D1,D2,D3,D4 decision;
```

## 论文筛选矩阵
| 主题 | 今日状态 | 处理 |
|---|---|---|
| LLM serving / inference | arXiv 429/timeout | 低置信，明日重试 |
| RLHF / GRPO / post-training | arXiv 429/timeout | 低置信，明日重试 |
| Agent eval | arXiv 429/timeout | 低置信，明日重试 |
| Rummy / imperfect information game | arXiv 429/timeout | 先用 GitHub 规则/AI opponent 候选推进业务 |

## 可信度与局限性
今日论文源不可稳定访问，因此只记录 provenance 和查询入口。未验证作者、摘要、PDF 的条目不会进入必读。

## 我应该如何跟进
1. 明日重试 arXiv/Semantic Scholar。
2. 若 Rummy 论文仍稀疏，优先搭规则状态机和 evaluator。
3. 对 LLM serving/RLHF 论文只纳入强相关、可验证 metadata 的条目。

#ai-radar #papers #low-confidence
