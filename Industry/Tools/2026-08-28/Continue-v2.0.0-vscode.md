# Continue 工具更新扫描

> 类型：Coding 工具 / AI 工具功能更新
> 工具/厂商：Continue / Continue
> 来源类型：GitHub Releases
> 发布时间/release tag：2026-06-19T00:24:01Z
> 原文链接：https://github.com/continuedev/continue/releases/tag/v2.0.0-vscode
> 返回日报：[[Daily/2026-08-28]]

## 一句话结论
Continue 今日保留固定扫描；重点观察 agent mode、MCP、IDE/CLI 集成、权限模式、上下文窗口、pricing/rate limit 对 AI coding 工作流的影响。

## TL;DR
- **代表更新**：v2.0.0-vscode
- **功能变化**：未解析到 release body
- **对我的影响**：若涉及 CLI/TUI、MCP、权限和远程执行，会直接影响多 agent 编排、tmux 监控和代码审查闭环。

## 信息压缩图示
```mermaid
flowchart TB
  subgraph Source[来源]
    A[Continue]
    B[Continue]
    C[GitHub Releases]
  end
  subgraph Signals[重点信号]
    S1[agent mode]
    S2[MCP / tool use]
    S3[IDE/CLI/TUI]
    S4[权限 / rate limit]
  end
  subgraph Workflow[AI coding 工作流]
    W1[多 agent 编排]
    W2[代码审查]
    W3[上下文工程]
    W4[远程执行风险]
  end
  A --> B --> C
  C --> S1 --> W1
  C --> S2 --> W3
  C --> S3 --> W2
  C --> S4 --> W4
  classDef source fill:#e1d5e7,stroke:#9673a6,stroke-width:2px;
  classDef signal fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef workflow fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  class A,B,C source; class S1,S2,S3,S4 signal; class W1,W2,W3,W4 workflow;
```

## 关键机制拆解
| 观察点 | 为什么重要 | 今日状态 |
|---|---|---|
| release/changelog | 捕捉破坏性和效率变化 | v2.0.0-vscode |
| MCP/tool use | 决定可扩展工具生态 | 需人工深读 |
| 权限/远程执行 | 决定安全边界 | 需人工深读 |

## 相关链接
- 原文：https://github.com/continuedev/continue/releases/tag/v2.0.0-vscode
- 网页详情：https://github.com/dyt27666-oss/AI-news-report-obsidians/blob/main/Industry/Tools/2026-08-28/Continue-v2.0.0-vscode.md

#ai-radar #coding-tools #agent
