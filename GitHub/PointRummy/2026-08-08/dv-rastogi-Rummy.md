# dv-rastogi/Rummy

> 日期：2026-08-08  
> 来源：GitHub Point Rummy scan  
> 原文：https://github.com/dv-rastogi/Rummy

## 一句话结论
Pygame Indian Rummy 实现，可用于理解交互/规则边界，不适合直接作为生产环境。

```mermaid
flowchart LR
  A[Game UI] --> B[Rules]
  B --> C[State]
  C --> D[Action]
  D --> E[Scoring]
  E --> F[Test Ideas]
```

## 业务可用性
适合抽取规则测试、状态转移样例和 UI edge case；不建议直接用于 RL 环境。

#ai-radar #point-rummy
