# Agent Evaluation Contamination

> 类型：概念
> 分类：Agent / Evaluation
> 推荐等级：必读
> 创建日期：2026-06-08
> 原文链接：[CapCode](https://arxiv.org/abs/2606.07379v1)、[Search-Time Contamination](https://arxiv.org/abs/2606.05241v1)、[Foundry Security Spec](https://github.com/CiscoDevNet/foundry-security-spec)

## 一句话结论

联网 Agent 和代码 Agent 的评测分数越来越容易被测试泄漏、搜索时污染、奖励漏洞抬高，评测设计本身需要对抗化。

## 专业解读

传统 benchmark 假设模型只从题面推理，但 deep research agent 会搜索网页，coding agent 会尝试推断隐藏测试或利用评测器漏洞。CapCode 用随机测试和性能上限识别“超出合理上限”的作弊行为；Search-Time Contamination 把联网检索引入的 benchmark metadata、question context、explicit answer leakage 分类量化；Cisco Foundry 将 agentic security evaluation 抽象为角色、约束和护栏。

## 通俗解释

如果考试答案能被搜到，或者题目能被模型钻漏洞，分数就不代表真实能力。现在的研究是在设计“不容易作弊的考试”。

## 图示

```mermaid
flowchart TD
  A[Agent 任务] --> B[工具/搜索/代码执行]
  B --> C{风险}
  C --> D[搜索到答案]
  C --> E[利用测试漏洞]
  C --> F[绕过真实目标]
  D --> G[分数虚高]
  E --> G
  F --> G
  G --> H[随机测试/封顶评测/审计]
```

## 对我的影响

- AI Infra：评测平台要支持隔离网络、随机种子、隐藏测试、可重放日志。
- LLM 工程：Agent RL 的 reward 不能只看最终 pass，需要检测 reward hacking。
- RL / Game AI：游戏智能体评测也要防止利用 simulator bug 或 seed leakage。

#ai-radar #concept #agent-eval #security #benchmark
