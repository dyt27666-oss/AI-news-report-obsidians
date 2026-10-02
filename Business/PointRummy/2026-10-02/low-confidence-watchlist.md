# Point Rummy / Indian Rummy 低置信观察清单 - 2026-10-02

## 一句话结论
今日 Point Rummy 保留 snapshot 中候选；未发现可直接声明为今日高相关新项的论文。

```mermaid
flowchart LR
  R[规则/计分] --> E[环境并行]
  E --> B[Bot / RL Agent]
  B --> V[评测基准]
  V --> P[业务落地]
```

## 下一步
1. 抽取 rules/env 抽象。
2. 自建 meld/sequence/set 单元测试。
3. 继续搜索 imperfect-information card game、ISMCTS、Gin Rummy RL。
