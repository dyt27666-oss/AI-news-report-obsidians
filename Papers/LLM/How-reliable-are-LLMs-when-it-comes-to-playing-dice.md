# How reliable are LLMs when it comes to playing dice?

> 类型：论文
> 分类：LLM Inference / Serving
> 推荐等级：必读
> 原文链接：https://arxiv.org/abs/2606.07515v1

## 论文信息
- 作者：Luca Avena, Gianmarco Bet, Bernardo Busoni
- 发布时间：2026-06-05
- PDF：https://arxiv.org/pdf/2606.07515v1
- 分类：cs.CL, cs.AI, cs.HC, math.PR

## 专业解读
摘要要点：We investigate the probabilistic reasoning capabilities of large language models through a controlled benchmarking study on discrete probability problems. We constructed two datasets, respectively a set of standard exercises and a set of counterintuitive exercises, designed to trigger heuristic reasoning, and evaluated 8 state-of-the-art models, each tested with and without Chain-of-Thought prompting. Models achieve an average accuracy of 0.96 on standard problems but only 0.59 on counterintuitive ones. We further provide empirical evidence of token bias: performance drops by over 20% when canonical formulations are replaced by disguised variants. Embedding misleading suggestions in the prompt reduces performance by up to 34%, with no model proving immune. Taken together, the reported findings suggest that current LLMs are not yet genuine probabilistic reasoners, despite their success in

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
- 原文：https://arxiv.org/abs/2606.07515v1
- PDF：https://arxiv.org/pdf/2606.07515v1

#ai-radar #paper
