# kserve/kserve

> 日期：2026-09-04
> 来源类型：GitHub direct /repos fallback
> 原文：https://github.com/kserve/kserve

## 一句话结论
KServe 是 K8s 上的 inference control plane，对 GenAI serving 的流量治理、SLO、部署形态有参考意义。

## TL;DR
- 关注 control plane、autoscaling、model routing 和观测。
- 与 vLLM/SGLang/TensorRT-LLM 等 runtime 形成上下层关系。
- 今日为 fixed watched repo fallback。

## 信息压缩图示
```mermaid
flowchart TB
  subgraph Runtime[Runtime]
    R1[vLLM]
    R2[SGLang]
    R3[TensorRT-LLM]
  end
  subgraph Control[KServe]
    C1[InferenceService]
    C2[Autoscaling]
    C3[Routing]
    C4[Observability]
  end
  subgraph Outcome[结果]
    O1[SLO]
    O2[成本]
    O3[可靠性]
  end
  R1 --> C1
  R2 --> C1
  R3 --> C1
  C1 --> C2 --> O2
  C1 --> C3 --> O1
  C4 --> O3
```

## 专业解读
对 AI Infra 工程师，KServe 的价值在于把 runtime 能力挂到统一 control plane，而不是替代底层推理引擎。

## 相关链接
- 日报：[[Daily/2026-09-04]]
- 原文：https://github.com/kserve/kserve

#ai-radar #serving #kubernetes
