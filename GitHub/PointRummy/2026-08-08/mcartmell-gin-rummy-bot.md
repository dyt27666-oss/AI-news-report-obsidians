# mcartmell/gin-rummy-bot

> 日期：2026-08-08  
> 来源：GitHub Point Rummy scan  
> 原文：https://github.com/mcartmell/gin-rummy-bot

## 一句话结论
Web-based Gin Rummy game and AI，适合作为旧式 bot / web game 参考。

```mermaid
flowchart LR
  A[Web Game] --> B[Game State]
  B --> C[Bot Logic]
  C --> D[Move]
  D --> E[Score]
  E --> F[Baseline Review]
```

## 业务可用性
可低成本参考 bot 决策接口，但不应直接复用到 Indian/Point Rummy 生产规则。

#ai-radar #point-rummy
