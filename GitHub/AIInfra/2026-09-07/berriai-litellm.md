# BerriAI/litellm

> Alias/detail page for AI Infra table. Canonical Loop Engineer note: [[GitHub/LoopEngineer/2026-09-07/berriai-litellm]]

## TL;DR

LiteLLM 是多模型/多厂商调用网关，对 AI Infra 的价值在于统一 API、路由、成本/限流治理；对 Loop Engineer 的价值在于让多 agent 系统在 OpenAI-compatible 接口下切换模型与供应商。

## 信息压缩图示

```mermaid
flowchart TB
  subgraph Workload[LLM workload]
    W1[Chat/Completion]
    W2[Agent tool calls]
    W3[Eval batch]
  end
  subgraph Gateway[LiteLLM gateway]
    G1[Provider routing]
    G2[OpenAI-compatible API]
    G3[Budget / rate limit]
    G4[Logging / observability]
  end
  subgraph Impact[工程影响]
    I1[供应商切换]
    I2[成本治理]
    I3[Agent loop 稳定性]
    I4[需压测延迟/错误恢复]
  end
  W1 --> G2 --> I1
  W2 --> G1 --> I3
  W3 --> G3 --> I2
  G4 --> I4
  classDef w fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
  classDef g fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef i fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  classDef risk fill:#f8cecc,stroke:#b85450,stroke-width:2px;
  class W1,W2,W3 w; class G1,G2,G3,G4 g; class I1,I2,I3 i; class I4 risk;
```

## 元信息

| 字段 | 内容 |
|---|---|
| repo | BerriAI/litellm |
| 原文 | https://github.com/BerriAI/litellm |
| 日期 | 2026-09-07 |
| 类型 | GitHub / AI Gateway / LLM Infra |

## 后续动作

- 查看 gateway 部署模式、fallback/routing 策略、observability 与限流能力。
- 对多 agent / 多模型 coding workflow 做小流量压测。

#ai-radar #github #ai-infra #llm-gateway
