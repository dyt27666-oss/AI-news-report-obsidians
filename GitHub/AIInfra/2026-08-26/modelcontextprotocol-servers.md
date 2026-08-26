# modelcontextprotocol/servers

> 类型：GitHub 项目
> 创建日期：2026-08-26
> 原文链接：https://github.com/modelcontextprotocol/servers
> 返回日报：[[Daily/2026-08-26]]

## 一句话结论

MCP servers 是 agent 工具生态的关键连接层，影响 coding-agent 与外部系统集成。

```mermaid
flowchart TB
  A[Agent] --> M[MCP Client]
  M --> S[MCP Servers]
  S --> T[Files / GitHub / DB / Browser]
  T --> E[Tool Execution]
```

```mermaid
quadrantChart
  title 影响力 × 可落地性
  x-axis 低可落地性 --> 高可落地性
  y-axis 低影响力 --> 高影响力
  MCP-Servers: [0.80, 0.86]
```

#ai-radar #mcp #agents
