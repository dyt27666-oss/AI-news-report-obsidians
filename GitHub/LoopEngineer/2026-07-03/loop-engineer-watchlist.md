# Loop Engineer / Loop Engineering watchlist - 2026-07-03

> 类型：Loop Engineering watchlist  
> 返回日报：[[Daily/2026-07-03]]  
> 来源：2026-06-30 broad snapshot fallback；今日 loop GitHub API rate-limited。

## 一句话结论

今日 loop 查询受限，只能使用 fallback；但 context engineering、AGENTS.md、skills、eval loop、multi-agent orchestration 仍是 coding-agent 工作流的核心观察维度。

## High-star fallback

| repo | stars | 重点 | 原文 |
|---|---:|---|---|
| dair-ai/Prompt-Engineering-Guide | 76088 | Prompt/context engineering 资料库 | https://github.com/dair-ai/Prompt-Engineering-Guide |
| cobusgreyling/loop-engineering | 4244 | Practical patterns / starters / CLI tools for loop engineering | https://github.com/cobusgreyling/loop-engineering |
| thesongzhu/Friday | 918 | Private control plane for AI agents | https://github.com/thesongzhu/Friday |

## Growth fallback

| repo | stars_delta | 重点 | 原文 |
|---|---:|---|---|
| dair-ai/Prompt-Engineering-Guide | 135 | context/prompt learning resource | https://github.com/dair-ai/Prompt-Engineering-Guide |
| thesongzhu/Friday | 1 | agent control plane | https://github.com/thesongzhu/Friday |
| cobusgreyling/loop-engineering | None | loop engineering patterns | https://github.com/cobusgreyling/loop-engineering |

## Loop 结构图

```mermaid
flowchart TB
  subgraph Task[任务]
    T1[需求/issue]
    T2[上下文收集]
  end
  subgraph Harness[Harness]
    H1[AGENTS.md / instructions]
    H2[skills / tools]
    H3[planner / executor]
    H4[reviewer / verifier]
  end
  subgraph Eval[评测闭环]
    E1[tests]
    E2[lint/build]
    E3[human review]
    E4[postmortem]
  end
  subgraph Memory[沉淀]
    M1[checklist]
    M2[skill]
    M3[template]
  end
  T1 --> T2 --> H1 --> H2 --> H3 --> H4
  H4 --> E1 --> E2 --> E3 --> E4
  E4 --> M1 --> M2 --> M3 --> H1
```

## 今日建议

1. 不把 fallback 当作真实今日增长。
2. 用 Qwen Code / Cline 今日 release 做同题 eval，补齐 loop engineering 实证数据。
3. 明日 GitHub API 恢复后优先跑 `loop engineering`、`AGENTS.md harness`、`coding agent loop`。

## 标签

#ai-radar #loop-engineering #coding-agent #fallback
