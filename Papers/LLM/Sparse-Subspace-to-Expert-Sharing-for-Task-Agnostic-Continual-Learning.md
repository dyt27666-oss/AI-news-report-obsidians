# Sparse Subspace-to-Expert Sharing for Task-Agnostic Continual Learning

> 类型：论文
> 分类：LLM Inference / Serving
> 推荐等级：必读
> 原文链接：https://arxiv.org/abs/2606.07500v1

## 论文信息
- 作者：Fatema Siddika, Md Anwar Hossen, Tanwi Mallick, Ali Jannesari
- 发布时间：2026-06-05
- PDF：https://arxiv.org/pdf/2606.07500v1
- 分类：cs.LG, cs.AI

## 专业解读
摘要要点：Continual learning in Large Language Models (LLMs) is hindered by the plasticity-stability dilemma, where acquiring new capabilities often leads to catastrophic forgetting of previous knowledge. Existing methods typically treat parameters uniformly, failing to distinguish between specific task knowledge and shared capabilities. We introduce Mixture of Sparse Experts for Task Agnostic Continual Learning (SETA), a framework that resolves the plasticity-stability conflict through adaptive sparse subspace decomposition into task-specific expert modules. Unlike standard updates, where tasks compete for the same parameters, SETA separates knowledge into unique experts, designed to isolate task-specific patterns, and shared experts, responsible for capturing common features. This structure is maintained through adaptive elastic anchoring and a routing-aware regularization that jointly protect s

工程上重点判断它是否能转化为训练、推理、评估或 agent 系统中的可复现改进。

## 通俗解释
这篇论文是在尝试改进 AI 系统的一项关键能力。先看图、实验表和限制，再决定是否深读。

## 方法图示
```mermaid
flowchart LR
  P[问题] --> M[方法]
  M --> E[实验]
  E --> I[对 LLM/RL/Infra 的影响]
```

## 相关链接
- 原文：https://arxiv.org/abs/2606.07500v1
- PDF：https://arxiv.org/pdf/2606.07500v1

#ai-radar #paper
