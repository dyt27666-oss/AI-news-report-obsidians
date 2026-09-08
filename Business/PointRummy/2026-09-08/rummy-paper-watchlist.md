# Point Rummy / Indian Rummy 论文资料 Watchlist - 2026-09-08

> 一句话结论：今日 Rummy 业务主题的强信号仍主要来自 GitHub 原型；论文侧保留 imperfect-information card game / ISMCTS / self-play 检索入口。

## TL;DR
- 今日未确认新的高置信 Point Rummy/Indian Rummy 论文。
- 可复用方向：belief/state abstraction、ISMCTS/MCTS、self-play evaluator、规则引擎 benchmark。
- 原文入口：https://arxiv.org/search/?query=rummy+imperfect+information+game+AI&searchtype=all

## 业务映射图
```mermaid
flowchart LR
  subgraph Research[论文关键词]
    R1[imperfect information]
    R2[ISMCTS/MCTS]
    R3[self-play RL]
    R4[belief state]
  end
  subgraph Business[Point Rummy 业务]
    B1[规则建模]
    B2[Bot 策略]
    B3[仿真评测]
    B4[作弊/视觉识别]
  end
  R1 --> B1
  R2 --> B2
  R3 --> B3
  R4 --> B2
  R4 --> B4
  classDef r fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef b fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  class R1,R2,R3,R4 r; class B1,B2,B3,B4 b;
```

## 下一步
- 建立 Point Rummy state/action/reward/evaluator checklist。
- 用 GitHub 原型先抽规则和测试集，再回头找论文补策略。

#ai-radar #point-rummy #paper
