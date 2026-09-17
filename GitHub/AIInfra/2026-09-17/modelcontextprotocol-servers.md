# modelcontextprotocol-servers

> 类型：GitHub 详情页
> 创建日期：2026-09-17
> 原文链接：https://github.com/modelcontextprotocol/servers
> 返回日报：[[Daily/2026-09-17]]

## 一句话结论

MCP servers 是 agent 工具生态的关键基础设施，适合观察工具调用协议、权限边界和 enterprise integration。

## 信息压缩图示

```mermaid
flowchart TB
  A[Agent] --> B[MCP Client]
  B --> C[MCP Server]
  C --> D[外部工具 / 数据源]
  D --> E[可审计工具调用]
```

```mermaid
quadrantChart
  title 工具生态价值
  x-axis 低可落地性 --> 高可落地性
  y-axis 低价值 --> 高价值
  MCP: [0.80, 0.82]
```

## 对我的影响

- AI coding workflow：影响 Claude Code / Codex / IDE agent 的工具扩展方式。
- Eval：需要为工具调用建立 mock server 和回放评测。

## 相关链接

- 原文：https://github.com/modelcontextprotocol/servers
