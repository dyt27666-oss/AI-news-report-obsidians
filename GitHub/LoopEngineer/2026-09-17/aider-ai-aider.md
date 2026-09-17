# aider-ai-aider

> 类型：Loop Engineer 详情页
> 创建日期：2026-09-17
> 原文链接：https://github.com/Aider-AI/aider
> 返回日报：[[Daily/2026-09-17]]

## 一句话结论

Aider 是 terminal pair programming agent，适合对比 patch 应用、git workflow 和交互式 loop。

## 信息压缩图示

```mermaid
flowchart TB
  A[任务描述] --> B[Aider 上下文]
  B --> C[模型生成修改]
  C --> D[diff]
  D --> E[git commit]
```

```mermaid
quadrantChart
  title Loop engineering 价值
  x-axis 低可落地性 --> 高可落地性
  y-axis 低价值 --> 高价值
  Aider: [0.78, 0.70]
```

## 相关链接

- 原文：https://github.com/Aider-AI/aider
