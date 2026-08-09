# microsoft/autogen

> Type: GitHub detail
> Date: 2026-08-09
> Source: https://github.com/microsoft/autogen
> Back: [[Daily/2026-08-09]]

## One-line takeaway

AutoGen remains a high-signal multi-agent orchestration repo for loop engineering and agent evaluation.

## Mermaid overview

```mermaid
flowchart TB
  T[Task] --> A1[Agent 1]
  T --> A2[Agent 2]
  A1 --> C[Conversation / coordination]
  A2 --> C
  C --> Tool[Tool use]
  Tool --> Eval[Eval loop]
  Eval --> Result[Result / retry]
```

## Impact

Useful as a reference for multi-agent coding workflows, task decomposition, and conversation-based evaluation loops.

#ai-radar #agent #loop-engineering
