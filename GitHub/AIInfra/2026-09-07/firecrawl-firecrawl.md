# firecrawl/firecrawl

> Alias/detail page for AI Infra table. Canonical Loop Engineer note: [[GitHub/LoopEngineer/2026-09-07/firecrawl-firecrawl]]

## TL;DR

Firecrawl 是面向 agent/context pipeline 的 web search/scrape/context API。今日同时出现在 AI Infra 与 Loop Engineer 视角：在 AI Infra 侧，它提供数据采集与上下文构建入口；在 Loop Engineer 侧，它影响 coding agent 的 web context 获取。

## 信息压缩图示

```mermaid
flowchart TB
  subgraph Workload[Agent / RAG workload]
    W1[Search]
    W2[Scrape]
    W3[Context API]
  end
  subgraph System[系统价值]
    S1[网页解析]
    S2[结构化上下文]
    S3[多 agent 可复用输入]
  end
  subgraph Impact[对我的影响]
    I1[减少手写 crawler]
    I2[提升 coding/research agent grounding]
    I3[需评估成本和可靠性]
  end
  W1 --> S1 --> I1
  W2 --> S2 --> I2
  W3 --> S3 --> I3
  classDef w fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
  classDef s fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef i fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  class W1,W2,W3 w; class S1,S2,S3 s; class I1,I2,I3 i;
```

## 元信息

| 字段 | 内容 |
|---|---|
| repo | firecrawl/firecrawl |
| 原文 | https://github.com/firecrawl/firecrawl |
| 日期 | 2026-09-07 |
| 类型 | GitHub / AI Infra / Agent context |

## 后续动作

- 打开 README / pricing / deployment docs，确认是否适合内部 research/coding agent。
- 和本地 crawler、browser 工具链对比吞吐、失败率、成本。

#ai-radar #github #ai-infra #agent
