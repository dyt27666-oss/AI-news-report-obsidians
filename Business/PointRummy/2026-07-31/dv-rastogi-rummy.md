# dv-rastogi/Rummy - Point Rummy 候选

> 来源类型：GitHub theme search snapshot  
> 原文：https://github.com/dv-rastogi/Rummy  
> 可信度：低到中；小仓库候选，需人工审代码质量。

## 一句话结论
该仓库可作为 Point/Indian/Gin Rummy 规则、bot baseline、计分器或仿真参考，但不是成熟生产项目。

## TL;DR
- Stars/Forks：5 / 0；语言：Python。
- 描述：Variation of classical Indian Rummy made in Pygame
- 业务可用性：规则建模、动作空间、状态编码或 evaluator 样例。

## Rummy 业务映射图
```mermaid
flowchart TB
  subgraph Repo[候选仓库]
    R[dv-rastogi/Rummy]
    D[README / code]
  end
  subgraph Business[业务用途]
    B1[规则引擎]
    B2[计分 / evaluator]
    B3[bot baseline]
    B4[仿真环境]
  end
  subgraph Risk[风险]
    K1[stars 低]
    K2[规则可能不匹配 Indian Point Rummy]
    K3[需人工审查]
  end
  R --> D
  D --> B1
  D --> B2
  D --> B3
  B1 --> B4
  K1 --> K3
  K2 --> K3
  K3 --> B4
  classDef repo fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef business fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  classDef risk fill:#f8cecc,stroke:#b85450,stroke-width:2px;
  class R,D repo;
  class B1,B2,B3,B4 business;
  class K1,K2,K3 risk;
```

## 下一步
| 方向 | 动作 |
|---|---|
| 规则 | 对照 Indian Rummy / Point Rummy 规则检查 meld、sequence、joker、drop、points。 |
| Bot | 抽取 heuristic / MCTS / RL baseline。 |
| 仿真 | 改造成 deterministic simulator + evaluator。 |

#ai-radar #point-rummy #github
