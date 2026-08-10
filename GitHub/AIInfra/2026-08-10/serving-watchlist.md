# Serving Watchlist - 2026-08-10

## 一句话结论
vLLM / SGLang / TensorRT-LLM / Transformers / PyTorch 构成今日 AI Infra serving/training 的高置信 watched set；GitHub Search 403 后仍可用 direct repo metadata 保持连续观察。

## 主图
```mermaid
flowchart TB
  subgraph Request[请求与模型]
    R1[Prompt/Batch]
    R2[Streaming]
    R3[Tool/Agent traffic]
  end
  subgraph Runtime[Serving Runtime]
    V[vLLM]
    S[SGLang]
    T[TensorRT-LLM]
    H[Transformers]
    P[PyTorch]
  end
  subgraph Bottleneck[瓶颈]
    B1[KV Cache]
    B2[Scheduler]
    B3[Spec Decode]
    B4[GPU Kernel]
    B5[MoE/Long Context]
  end
  subgraph Action[动作]
    A1[读 release/benchmark]
    A2[小流量 PoC]
    A3[记录风险]
  end
  R1 --> V --> B1 --> A1
  R2 --> S --> B2 --> A2
  R3 --> T --> B4 --> A2
  H --> B5 --> A1
  P --> B3 --> A3
```

## 今日判断
| 项目 | 作用 | 跟进动作 |
|---|---|---|
| vLLM | 高吞吐 serving | 看 scheduler/KV cache/release |
| SGLang | structured generation 与 serving runtime | 看 runtime / VLM / RL serving |
| TensorRT-LLM | NVIDIA GPU inference | 看硬件适配与 benchmark |
| Transformers | 模型生态入口 | 看新模型与量化接入 |
| PyTorch | 训练/推理底层 | 看 compile/distributed/GPU runtime |

#ai-radar #serving #ai-infra
