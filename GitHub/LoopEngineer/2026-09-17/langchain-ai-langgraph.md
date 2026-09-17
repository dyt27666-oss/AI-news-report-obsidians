# langchain-ai-langgraph

> 类型：Loop Engineer 详情页
> 创建日期：2026-09-17
> 原文链接：https://github.com/langchain-ai/langgraph
> 返回日报：[[Daily/2026-09-17]]

## 一句话结论

LangGraph 是 agent state graph 和 loop orchestration 的重要参考，可用于 coding-agent harness 和 eval loop 设计。

## 信息压缩图示

```mermaid
flowchart TB
  A[State] --> B[Node]
  B --> C[Tool Call]
  C --> D[State Update]
  D --> B
  D --> E[Eval / Done]
```

```mermaid
quadrantChart
  title Agent loop 价值
  x-axis 低可落地性 --> 高可落地性
  y-axis 低价值 --> 高价值
  LangGraph: [0.75, 0.78]
```

## 相关链接

- 原文：https://github.com/langchain-ai/langgraph
