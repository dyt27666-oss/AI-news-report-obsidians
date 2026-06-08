# RLVR Reward Credit Assignment

> 类型：概念
> 分类：Post-training / RLHF
> 推荐等级：必读
> 创建日期：2026-06-08
> 原文链接：[RREDCoT](https://arxiv.org/abs/2606.06475v1)、[MDP-GRPO](https://arxiv.org/abs/2606.06058v1)、[MaxPO](https://arxiv.org/abs/2606.06080v1)

## 一句话结论

RLVR 的核心瓶颈正在从“有没有 verifier”转向“如何把稀疏、延迟、低方差奖励稳定地分配给中间推理步骤和采样组”。

## 专业解读

GRPO/RLVR 省掉 reward model、直接用可验证答案给奖励；代价是 reward 常常只在最终答案出现，导致 credit assignment 高方差。RREDCoT 关注 CoT 段级 reward redistribution，MDP-GRPO 关注低离散奖励下的 group normalization 病态，MaxPO/OrderGrad 把目标从期望奖励扩展到 pass@K、max@K、CVaR 等排序统计目标。这说明 RL 算法工程不能只替换 PPO 为 GRPO，而要联合设计采样、advantage、baseline、reward shaping 与 inference-time objective。

## 通俗解释

模型做题时，最后答对/答错只能告诉你“结果”，但不知道中间哪一步帮了忙。新的研究是在把“最后的分数”更聪明地分给推理过程，让模型学得更稳。

## 图示

```mermaid
flowchart TD
  A[最终答案 verifier] --> B[稀疏/延迟奖励]
  B --> C{奖励分配策略}
  C --> D[段级 CoT credit]
  C --> E[稳定 advantage / baseline]
  C --> F[pass@K / max@K 目标]
  D --> G[更低方差的 RLVR]
  E --> G
  F --> G
```

## 对我的影响

- AI Infra：训练系统需要记录 token/segment/trajectory 级元数据。
- LLM 工程：GRPO 实验要监控 group reward 方差、advantage 分布、pass@K 目标和长度偏置。
- RL / Game AI：稀疏奖励游戏任务可借鉴段级 credit assignment 与 order-statistic objectives。

## 相关链接

- [[Papers/RLHF/RREDCoT Segment-Level Reward Redistribution for Reasoning Models]]
- [[Papers/RLHF/MDP-GRPO Stabilized Group Relative Policy Optimization]]

#ai-radar #concept #rlvr #grpo #post-training
