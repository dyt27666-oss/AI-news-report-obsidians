# sgl-project/sglang

> 类型：GitHub 项目
> 创建日期：2026-08-26
> 原文链接：https://github.com/sgl-project/sglang
> 返回日报：[[Daily/2026-08-26]]

## 一句话结论

SGLang 是高性能 LLM/multimodal serving 框架，适合与 vLLM / TensorRT-LLM 对比。

```mermaid
flowchart TB
  Q[Requests] --> S[SGLang Runtime]
  S --> B[Batching]
  S --> K[KV Cache]
  B --> O[Throughput]
  K --> L[Latency]
```

```mermaid
quadrantChart
  title 影响力 × 可落地性
  x-axis 低可落地性 --> 高可落地性
  y-axis 低影响力 --> 高影响力
  SGLang: [0.78, 0.82]
```

#ai-radar #serving #sglang
