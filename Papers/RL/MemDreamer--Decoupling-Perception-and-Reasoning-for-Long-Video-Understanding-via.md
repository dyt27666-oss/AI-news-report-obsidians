# MemDreamer: Decoupling Perception and Reasoning for Long Video Understanding via Hierarchical Graph Memory and Agentic Retrieval Mechanism

> 类型：论文
> 分类：RL for LLM / GRPO
> 推荐等级：必读
> 原文链接：https://arxiv.org/abs/2606.07512v1

## 论文信息
- 作者：Cong Chen, Guo Gan, Kaixiang Ji, ChaoYang Zhang, Zhen Yang
- 发布时间：2026-06-05
- PDF：https://arxiv.org/pdf/2606.07512v1
- 分类：cs.CV, cs.AI, cs.CL

## 专业解读
摘要要点：Current Vision-Language Models struggle with hours-long videos because processing full-length visual sequences induces prohibitive token explosion and attention dilution. To overcome this, we introduce MemDreamer to decouple perception and reasoning, shifting long-video understanding into an agentic exploration process. As a plug-and-play framework, it incrementally streams videos to construct a Hierarchical Graph Memory, a top-down three-tier architecture for semantic abstraction, anchored by a foundational graph capturing spatiotemporal and causal relations. During inference, the reasoning model employs agentic tool-augmented retrieval, navigating hierarchies, searching nodes, and traversing logical edges via an Observation-Reason-Action loop. Experiments show MemDreamer achieves SOTA results across four mainstream benchmarks, narrowing the gap with human experts to only 3.7 points. It

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
- 原文：https://arxiv.org/abs/2606.07512v1
- PDF：https://arxiv.org/pdf/2606.07512v1

#ai-radar #paper
