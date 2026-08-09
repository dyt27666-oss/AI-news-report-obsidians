# modelcontextprotocol/servers

> Type: GitHub detail
> Date: 2026-08-09
> Source: https://github.com/modelcontextprotocol/servers
> Back: [[Daily/2026-08-09]]

## One-line takeaway

MCP servers remain a key infrastructure layer for agent tool-use standardization.

## Mermaid overview

```mermaid
flowchart TB
  A[Coding agent] --> M[MCP client]
  M --> S[MCP servers]
  S --> F[File / shell / web tools]
  S --> D[Data systems]
  F --> O[Observable actions]
  D --> O
  O --> E[Eval and permission loop]
```

## Why it matters

For loop engineering, MCP is the boundary between agents and tools. Watch server coverage, permission models, and observability patterns.

#ai-radar #mcp #agent
