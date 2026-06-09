from pathlib import Path
from textwrap import dedent

VAULT = Path('/home/vscode-server/obsidian-ai-radar')
DATE = '2026-06-09'
GH = 'https://github.com/dyt27666-oss/AI-news-report-obsidians/blob/main/'

def web(path: str) -> str:
    return GH + path.replace(' ', '%20') + '.md'

def w(path: str, content: str):
    p = VAULT / (path + '.md')
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(dedent(content).strip() + '\n', encoding='utf-8')

paper_items = [
    {
        'path':'Papers/Serving/STAR-KV Low-Rank KV Cache Compression',
        'title':'STAR-KV: Low-Rank KV Cache Compression via Soft Thresholding for Adaptive Rank Control',
        'short':'STAR-KV 用自适应低秩和混合量化把 KV cache 压缩推进到 serving 可落地层，重点不只是压缩率，而是配套 Triton kernel 后的端到端吞吐。',
        'topic':'Serving / KV Cache', 'priority':'必读', 'id':'2606.08382v1',
        'authors':'Priyansh Bhatnagar, Ashkan Moradifirouzabadi, Se-Hyun Yang, SeungJae Lee, Jungwook Choi, Mingu Kang',
        'date':'2026-06-07', 'code':'https://github.com/PriyanshBhatnagar/STAR-KV',
        'problem':'长上下文 LLM serving 的 KV cache 成为显存和带宽瓶颈。',
        'method':'按 head/block 学习低秩阈值，K/V 使用不同分解策略，再叠加低秩感知 mixed-precision quantization。',
        'result':'报告最高 75% KV cache 压缩，结合量化最高 20x KV cache reduction，attention kernel 最高 6.9x speedup，端到端生成最高 3.1x throughput。',
        'value':'适合把 KV cache 压缩从论文指标转成 serving benchmark；可和 LMCache、vLLM/SGLang 的 cache 层做对照。',
        'tags':'#serving #kv-cache #triton #quantization'
    },
    {
        'path':'Papers/Serving/Vortex Programmable Sparse Attention Serving for AI Agents',
        'title':'Vortex: Efficient and Programmable Sparse Attention Serving for AI Agents',
        'short':'Vortex 把 sparse attention 变成可编程 serving 系统，让人和 Agent 都能快速搜索、部署、评估稀疏注意力策略。',
        'topic':'Serving / Sparse Attention', 'priority':'必读', 'id':'2606.06453v1',
        'authors':'Zhuoming Chen, Xinrui Zhong, Qilong Feng, Ranajoy Sadhukhan, Yang Zhou, Michael Qizhe Shieh, Zhihao Jia, Beidi Chen',
        'date':'2026-06-04', 'code':'未发现',
        'problem':'长生成场景下 full attention 成本高，但 sparse attention 从算法到 serving stack 的落地成本很高。',
        'method':'Python-embedded frontend + page-centric tensor abstraction + serving backend，把稀疏模式表达和高性能执行连接起来。',
        'result':'AI agents 可自动生成/迭代算法；报告最高 3.46x throughput，GLM-4.7-Flash 上最高 4.7x，MiniMax-M2.7 上 1.37x。',
        'value':'对长上下文 Agent rollout、deep research 和工具调用日志场景非常关键，因为这些 workload 的注意力结构可能比通用 chat 更稀疏。',
        'tags':'#serving #sparse-attention #agent #long-context'
    },
    {
        'path':'Papers/Serving/Tangram Non-Uniform KV Cache for Multi-turn LLM Serving',
        'title':'Tangram: Unlocking Non-Uniform KV Cache for Efficient Multi-turn LLM Serving',
        'short':'Tangram 关注 multi-turn serving 的非均匀 KV cache 管理，把压缩算法的“重要性不同”转成静态预算、head group page 和 AOT load balancing。',
        'topic':'Serving / Multi-turn KV Cache', 'priority':'必读', 'id':'2606.06302v1',
        'authors':'Hyungmin Kim, Minsoo Kim, Hongseok Kim, Jungwook Choi',
        'date':'2026-06-04', 'code':'https://github.com/aiha-lab/TANGRAM',
        'problem':'多轮对话 KV cache 线性增长；非均匀压缩能保留重要信息，但会带来碎片、调度复杂度和 kernel 利用率下降。',
        'method':'Deterministic Budget Allocation、Head Group Page、AOT Load Balancing 三件套，把非均匀 KV cache 变成系统可管理对象。',
        'result':'报告吞吐最高提升 2.6x，同时保持模型精度。',
        'value':'适合和 vLLM/SGLang 的 prefix cache、paged attention、session memory 做工程对照。',
        'tags':'#serving #kv-cache #multi-turn #scheduler'
    },
    {
        'path':'Papers/RLHF/CATPO Critique-Augmented Tree Policy Optimization',
        'title':'CATPO: Critique-Augmented Tree Policy Optimization',
        'short':'CATPO 把 RLVR 的 tree rollout 从“多采样”升级为“挑有信息的树 + 修复全失败分支 + 按信息量加权更新”。',
        'topic':'RLHF / RLVR / GRPO', 'priority':'必读', 'id':'2606.08346v1',
        'authors':'Ayush Singh, Umang Goyal, Ankur Dahiya',
        'date':'2026-06-06', 'code':'未发现',
        'problem':'TreeRPO/GRPO 类方法会浪费大量 rollout compute：全对、全错或 policy 已能预测 reward 的树对梯度帮助很小。',
        'method':'tree informativeness score + critique-guided healing + informativeness-weighted loss。',
        'result':'Qwen2.5-Math-1.5B + MATH 训练，在 AIME24/MATH-500/OlympiadBench/MinervaMath macro accuracy 37.5%，高于 TreeRPO 1.9%、GRPO 4.8%。',
        'value':'对 RL game agent 的稀疏奖励也有借鉴：不要只增加 rollout 数量，要提高每条轨迹对策略更新的信息密度。',
        'tags':'#rlhf #rlvr #grpo #post-training'
    },
    {
        'path':'Papers/Agents/ADWM Off-Policy Evaluation of LLM Agents',
        'title':'Autoregressive Diffusion World Models for Off-Policy Evaluation of LLM Agents',
        'short':'ADWM 用自回归 diffusion world model 做 LLM Agent 离线评估，目标是在不真实执行新 policy 的情况下估计多轮交互表现。',
        'topic':'Agent Eval / World Model', 'priority':'必读', 'id':'2606.05558v1',
        'authors':'Kaixuan Liu, Guojun Xiong, Weinan Zhang, Shengpu Tang',
        'date':'2026-06-04', 'code':'未发现',
        'problem':'在线评估多轮 LLM Agent 昂贵且有风险；传统 OPE 不适合离散文本 action 与环境响应交替出现的场景。',
        'method':'每一步用独立 denoising transition 模拟环境响应，并让被评估 policy 通过 score function 条件化 world model。',
        'result':'在多种 multi-turn agent tasks 上报告更准确的 value estimates 和 evaluation reliability。',
        'value':'对需要大量 rollout 的 Agent RL 和游戏环境评估很重要，可降低在线环境交互成本。',
        'tags':'#agent-eval #world-model #off-policy-evaluation #rl'
    },
    {
        'path':'Papers/Agents/Auditable Graph-Guided RCA for Kubernetes Incidents',
        'title':'Auditable Graph-Guided Root Cause Analysis for Kubernetes Incidents',
        'short':'这篇把 Kubernetes RCA Agent 放进 typed evidence graph + LangGraph traversal + 独立验证框架，重点是“可审计”，不是只追求 judge 分数。',
        'topic':'AgentOps / Kubernetes / Eval', 'priority':'可 skim', 'id':'2606.08590v1',
        'authors':'Anastasiia Kuvshinova, Seungmin Jin',
        'date':'2026-06-07', 'code':'未发现',
        'problem':'Kubernetes incident agent 的高分可能来自场景捷径，而非真实证据推理；生产 RCA 需要只读证据、边界、验证和无泄漏。',
        'method':'typed incident graph、deterministic graph/tool operations、LangGraph traversal state machine、separate validation stage。',
        'result':'在 ITBench common subset 上 root-cause-entity F1 从 0.6087 到 0.9130；去掉场景提示后 19-scenario subset 保留 0.6958 F1。',
        'value':'适合作为内部 AgentOps/RCA eval harness 的设计参考，尤其是 evidence graph 和 verdict validation。',
        'tags':'#agentops #kubernetes #eval #rca'
    },
]

for x in paper_items:
    aid = x['id']
    path = x['path']
    w(path, f"""
# {x['title']}

> 类型：论文
> 大类：论文
> 小类：{x['topic']}
> 推荐等级：{x['priority']}
> 创建日期：{DATE}
> 原文链接：https://arxiv.org/abs/{aid}
> PDF：https://arxiv.org/pdf/{aid}
> 网页详情：{web(path)}
> 返回日报：[[Daily/{DATE}]]

## 一句话结论

{x['short']}

## TL;DR

- **研究问题**：{x['problem']}
- **核心方法**：{x['method']}
- **关键结果**：{x['result']}
- **对我的价值**：{x['value']}
- **建议动作**：{('深读并拉代码做 serving benchmark' if 'Serving' in x['topic'] else '纳入 RL/Agent eval 设计备忘并等代码或复现实验')}

## 论文信息

| 字段 | 内容 |
|---|---|
| 论文来源 | arXiv |
| 来源类型 | 预印本 |
| 标题 | {x['title']} |
| 作者/机构 | {x['authors']} |
| 发布时间 | {x['date']} |
| arXiv | [abs](https://arxiv.org/abs/{aid}) |
| OpenReview / 会议页 | 未发现 |
| Semantic Scholar | [arXiv:{aid}](https://www.semanticscholar.org/search?q={aid}) |
| PDF | [pdf](https://arxiv.org/pdf/{aid}) |
| 代码 | {x['code']} |
| 方向 | {x['topic']} |

## 方法/系统图示

```mermaid
flowchart TB
  subgraph Source[论文来源]
    A[arXiv 预印本]
    B[{aid}]
  end
  subgraph Q[研究问题]
    Q1[目标: {x['problem'][:34]}]
    Q2[瓶颈: 显存/奖励/环境交互/可审计性]
    Q3[缺口: 算法收益难直接落地为系统收益]
  end
  subgraph M[方法模块]
    M1[模块A: {x['method'][:34]}]
    M2[模块B: 结构化约束与选择]
    M3[模块C: 指标/验证闭环]
  end
  subgraph P[训练或推理流程]
    D[数据/请求/轨迹] --> R[rollout 或 serving execution]
    R --> S[scoring / compression / validation]
    S --> U[update / scheduling / cache decision]
  end
  subgraph E[证据与决策]
    E1[Benchmark 信号]
    E2[{x['result'][:34]}]
    E3[局限: 仍需独立复现]
    E4[动作: {x['priority']}]
  end
  A --> B --> Q1
  Q1 --> M1 --> R
  Q2 --> M2 --> S
  Q3 --> M3 --> U
  U --> E1 --> E2 --> E4
  S --> E3 --> E4
  classDef problem fill:#fff2cc,stroke:#d6b656,stroke-width:2px,color:#111;
  classDef method fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#111;
  classDef evidence fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#111;
  classDef risk fill:#f8cecc,stroke:#b85450,stroke-width:2px,color:#111;
  class A,B,Q1,Q2,Q3 problem;
  class M1,M2,M3,D,R,S,U method;
  class E1,E2,E4 evidence;
  class E3 risk;
```

### 辅助图：阅读/复现决策矩阵

```mermaid
quadrantChart
  title 论文阅读决策：新意 x 可复现性
  x-axis 低可复现 --> 高可复现
  y-axis 低新意 --> 高新意
  quadrant-1 优先复现
  quadrant-2 读方法
  quadrant-3 暂存
  quadrant-4 工程可试
  当前论文: [0.72, 0.82]
```

## 专业解读

{x['title']} 的价值在于把一个已经被大家意识到的瓶颈具体化：{x['problem']} 方法层面，作者没有只停留在抽象算法，而是提出了可操作的机制：{x['method']} 这类工作对用户最相关的点是，它可以直接改变 serving、RL rollout 或 Agent eval 的成本结构。需要注意的是，论文报告的数字来自作者设定的模型、硬件和 benchmark；真正进入内部平台前，必须用自己的模型长度分布、batching 策略、GPU/NPU 后端和评测任务复测。

## 通俗解释

可以把它理解为：原来系统在“记住上下文、探索策略或判断 Agent 是否真的会做事”时有很多浪费，这篇尝试把浪费的位置标出来，并给出更精细的压缩、选择、模拟或审计办法。

## 方法拆解

| 组件 | 作用 | 输入 | 输出 | 关键假设 |
|---|---|---|---|---|
| 问题建模 | 把瓶颈变成可测对象 | workload / rollout / benchmark | 可优化指标 | 指标能代表真实工程痛点 |
| 核心机制 | 执行 {x['method'][:28]} | 模型状态、轨迹或 cache | 更高效的路径 | 额外复杂度不会抵消收益 |
| 验证闭环 | 证明收益不只是局部 trick | baseline 与 ablation | 性能/准确性报告 | benchmark 没有被过拟合 |

## 实验与证据

| 实验 | 说明 | 我怎么看 |
|---|---|---|
| 论文主结果 | {x['result']} | 有方向价值，但需要按内部任务复现 |
| 消融/系统比较 | 关注是否比较了调度、kernel、baseline 或 judge 泄漏 | 决定它是算法点子还是平台能力 |

## 局限性 / 风险

- 结果依赖作者选择的模型、硬件、benchmark 和实现质量。
- 若没有公开代码或代码尚未成熟，短期只能读方法，不能直接纳入生产。
- 对 serving 论文要特别检查长尾延迟、mixed workload 和多租户调度；对 RL/Agent 论文要检查 reward hacking 与评测污染。

## 对我的影响

| 维度 | 影响 | 建议动作 |
|---|---|---|
| AI Infra | 可能影响 serving/cache/scheduler 或 AgentOps 平台设计 | 做同硬件同模型 microbenchmark |
| LLM 工程 | 影响长上下文、多轮对话、后训练或 eval 成本 | 加入实验 backlog |
| RL / Game AI | credit assignment、world model 或 rollout 效率可迁移 | 用小环境先验证假设 |
| Agent / Eval | 强调可审计、离线评估或环境真实性 | 更新 eval harness checklist |

## 相关链接

- 原文：https://arxiv.org/abs/{aid}
- PDF：https://arxiv.org/pdf/{aid}
- 网页详情：{web(path)}
- 代码：{x['code']}
- 相关卡片：[[Daily/{DATE}]]

## 标签

#ai-radar #paper {x['tags']}
""")

# Industry detail
path='Industry/HuggingFace/OpenEnv Agentic RL Community Signal'
w(path, f"""
# The Open Source Community is backing OpenEnv for Agentic RL

> 类型：博客
> 大类：博客
> 小类：Agentic RL / Environments
> 推荐等级：必读
> 创建日期：{DATE}
> 原文链接：https://huggingface.co/blog/openenv-agentic-rl
> 网页详情：{web(path)}
> 返回日报：[[Daily/{DATE}]]

## 一句话结论

Hugging Face 上 OpenEnv 的社区信号说明 Agentic RL 的竞争焦点正在从单个模型/算法，转向可复用、可验证、可并行的环境基础设施。

## TL;DR

- **它是什么**：Hugging Face Blog 发布的 Agentic RL / OpenEnv 社区动态。
- **为什么重要**：后训练 Agent 需要大量可控环境、工具调用日志、reward 与重置机制，环境层会像 serving 层一样成为基础设施。
- **和我相关的点**：RL 游戏模型训练和 LLM Agent 训练都依赖环境并行、可验证 reward、任务分布和 replay 数据。
- **建议动作**：把 OpenEnv 与现有 Agent benchmark、verl/OpenRLHF rollout、内部游戏环境接口做对照。

## 元信息

| 字段 | 内容 |
|---|---|
| 发布方/来源 | Hugging Face Blog |
| 大厂/实验室 | Hugging Face / Open Source Community |
| 栏目/来源类型 | Blog / Community announcement |
| 作者/机构 | Hugging Face 社区文章 |
| 发布时间 | 2026-06-08 |
| 原文 | [原文](https://huggingface.co/blog/openenv-agentic-rl) |
| 代码 | 未在 RSS 元数据中确认 |
| PDF | 不适用 |
| 标签 | #agentic-rl #environment #huggingface |

## 信息压缩图示

```mermaid
flowchart LR
  subgraph Source[发布方]
    C[Hugging Face Blog]
    A[OpenEnv for Agentic RL]
  end
  subgraph Signal[释放的信号]
    S1[环境成为 Agent RL 核心资产]
    S2[社区希望统一接口]
    S3[训练需要可验证 feedback]
  end
  subgraph Infra[对工程的含义]
    I1[Environment registry]
    I2[Parallel rollout]
    I3[Reward/verifier API]
    I4[Replay/eval logs]
  end
  subgraph Action[我的动作]
    R1[深读生态设计]
    R2[对照 verl rollout]
    R3[观察是否形成标准]
  end
  C --> A --> S1
  A --> S2
  A --> S3
  S1 --> I1
  S2 --> I2
  S3 --> I3
  I2 --> I4
  I1 --> R1
  I3 --> R2
  I4 --> R3
  classDef company fill:#e1d5e7,stroke:#9673a6,stroke-width:2px,color:#111;
  classDef signal fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#111;
  classDef infra fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#111;
  classDef action fill:#ffe6cc,stroke:#d79b00,stroke-width:2px,color:#111;
  class C,A company;
  class S1,S2,S3 signal;
  class I1,I2,I3,I4 infra;
  class R1,R2,R3 action;
```

### 影响矩阵

| 方向 | 影响 | 需要验证 |
|---|---|---|
| Agent RL | 训练不再只是算法，环境接口和验证器同等重要 | OpenEnv 是否有稳定 API 与任务覆盖 |
| Game AI | 环境并行、reset、reward shaping 可直接迁移 | 是否支持复杂模拟器和长 episode |
| LLM Infra | rollout service 可能成为 post-training 平台核心组件 | 与 Ray/vLLM/SGLang/verl 的集成路径 |

## 专业解读

Agentic RL 的长期瓶颈不是“能不能跑一次 GRPO”，而是环境是否可扩展、可重置、可评分、可审计。OpenEnv 这类信号值得关注，是因为它把开源社区注意力导向环境层：任务定义、工具权限、reward/verifier、状态快照和并行 rollout。对用户来说，这比单个 leaderboard 更重要；如果环境接口被标准化，训练 Agent、游戏 RL 和评测 Agent 的数据生产成本会显著下降。

## 通俗解释

训练 Agent 不只是给模型题目，还要给它一个可以反复试错的世界。OpenEnv 类项目就是想把这些“世界”做成可复用的训练场。

## 关键机制拆解

| 机制 | 解决的问题 | 为什么有效 | 可能的坑 |
|---|---|---|---|
| 环境注册 | 任务和环境分散 | 统一发现与复用 | 标准过早可能限制复杂任务 |
| 可验证 reward | Agent 容易钻漏洞 | 让结果可自动判定 | verifier 设计本身会被 overfit |
| 并行 rollout | 训练吞吐不足 | 环境层横向扩展 | 状态隔离和资源成本高 |

## 对我的影响

| 维度 | 影响 | 建议动作 |
|---|---|---|
| AI Infra | 环境服务可能成为后训练平台新控制面 | 设计 env API / verifier API 草案 |
| LLM 工程 | Agent 训练数据从 prompt 扩展到交互轨迹 | 关注 trajectory schema |
| RL / Game AI | 与游戏模拟器、世界模型训练高度相关 | 试做小型环境适配 |
| Agent / Eval | 评测和训练可共享环境，但要防污染 | 做 train/eval split 与日志审计 |

## 可信度与局限性

- 证据强度：来自 Hugging Face 官方博客 RSS，可确认发布时间和标题；正文细节需后续深读。
- 局限性：社区倡议不等于事实标准，生态成熟度仍需验证。
- 潜在风险：环境标准化后可能出现 benchmark overfitting。

## 我应该如何跟进

1. 阅读 OpenEnv 具体接口和示例环境。
2. 对照 verl / OpenRLHF 的 rollout worker 需求，列出适配点。
3. 观察是否有高质量 game / browser / desktop / tool-use 环境加入。

## 相关链接

- 原文：https://huggingface.co/blog/openenv-agentic-rl
- 网页详情：{web(path)}
- 相关卡片：[[GitHub/RL/verl HybridFlow RL Post-Training Framework]]、[[Papers/Agents/ADWM Off-Policy Evaluation of LLM Agents]]

## 标签

#ai-radar #blog #huggingface #agentic-rl #environment
""")

# GitHub details
repos = [
('GitHub/Infra/OME Kubernetes LLM Serving Operator','Open Model Engine (OME) - Kubernetes operator for LLM serving','ome-projects/ome','464','81','Go','2026-06-08','Open Model Engine (OME) 是面向 Kubernetes 的 LLM serving operator，把 vLLM、SGLang、TensorRT-LLM、Triton、GPU scheduling 和 model lifecycle 管起来。','AI Infra / Serving Control Plane','必读','https://github.com/ome-projects/ome','deepseek, k8s, llm-inference, model-serving, multi-node-kubernetes, pd-disaggregation, sglang, vllm'),
('GitHub/Agents/trycua Computer-Use Agent Infrastructure','trycua/cua - Computer-Use Agent Infrastructure','trycua/cua','17761','1138','HTML','2026-06-09','cua 提供 Computer-Use Agents 的 sandbox、SDK 和 benchmark，覆盖 macOS/Linux/Windows 桌面控制，是 GUI/desktop Agent 训练评测基础设施信号。','Agent / Computer Use / Eval','必读','https://github.com/trycua/cua','agent, computer-use, desktop-automation, virtualization, macos, windows-sandbox'),
('GitHub/Infra/LLMGateway Unified LLM Request Gateway','theopenco/llmgateway - Unified LLM Request Gateway','theopenco/llmgateway','1278','143','TypeScript','2026-06-09','llmgateway 将多 provider LLM 请求的 routing、observability、rate limiting、guardrails 和 key management 收进统一 API，是在线 LLM 应用控制面的代表。','AI Infra / Gateway / Observability','可 skim','https://github.com/theopenco/llmgateway','ai-gateway, analytics, guardrails, inference, llm-proxy, observability, rate-limiting'),
]
for path,title,repo,stars,forks,lang,upd,short,topic,priority,url,topics in repos:
    w(path, f"""
# {title}

> 类型：GitHub
> 大类：GitHub
> 小类：{topic}
> 推荐等级：{priority}
> 创建日期：{DATE}
> 原文链接：{url}
> 网页详情：{web(path)}
> 返回日报：[[Daily/{DATE}]]

## 一句话结论

{short}

## TL;DR

- **它是什么**：{repo}，一个 {topic} 方向的开源项目。
- **为什么重要**：它把模型推理/Agent 执行/请求治理中的一层工程能力独立成可部署组件。
- **和我相关的点**：可用于比较内部 serving、Agent sandbox、eval harness 或 gateway/control-plane 设计。
- **建议动作**：先读 docs/examples，再用最小 workload 试部署，不要只看 stars。

## 元信息

| 字段 | 内容 |
|---|---|
| repo | {repo} |
| stars / forks | {stars} / {forks} |
| 语言 | {lang} |
| 最近更新时间 | {upd} |
| topics | {topics} |
| 原文 | [GitHub]({url}) |
| 是否有 docs/examples/release | GitHub 元数据可确认 issues/wiki；docs/examples/release 需进入仓库继续检查 |
| 是否值得试用 | {priority} |

## 信息压缩图示

```mermaid
flowchart TB
  subgraph Workload[Workload]
    W1[LLM request / Agent task]
    W2[Batch / stream / desktop session]
    W3[Tool calls / model lifecycle]
  end
  subgraph System[项目核心系统]
    S1[API / Control Plane]
    S2[Scheduler / Router]
    S3[Runtime / Sandbox / Backend]
    S4[Observability / Policy]
  end
  subgraph Hardware[硬件与依赖]
    H1[GPU / VM / Container]
    H2[Kubernetes / provider API]
    H3[Storage / logs / secrets]
  end
  subgraph Outcome[结果]
    O1[吞吐/并发提升]
    O2[延迟/成本可控]
    O3[可评测/可审计]
    O4[复杂度/锁定风险]
  end
  W1 --> S1
  W2 --> S2
  W3 --> S4
  S1 --> S2 --> S3
  S3 --> H1
  S2 --> H2
  S4 --> H3
  H1 --> O1
  H2 --> O2
  H3 --> O3
  S4 --> O4
  classDef workload fill:#fff2cc,stroke:#d6b656,stroke-width:2px,color:#111;
  classDef system fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#111;
  classDef hardware fill:#e1d5e7,stroke:#9673a6,stroke-width:2px,color:#111;
  classDef outcome fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#111;
  classDef risk fill:#f8cecc,stroke:#b85450,stroke-width:2px,color:#111;
  class W1,W2,W3 workload;
  class S1,S2,S3,S4 system;
  class H1,H2,H3 hardware;
  class O1,O2,O3 outcome;
  class O4 risk;
```

### 试用决策矩阵

| 维度 | 观察点 | 结论 |
|---|---|---|
| 成熟度 | stars {stars}、forks {forks}、近期更新 {upd} | 社区活跃度有信号 |
| 集成价值 | 是否能接入 vLLM/SGLang/Agent sandbox/observability | 与内部平台有关 |
| 风险 | API 稳定性、权限、安全、资源成本 | 先 sandbox 试用 |

## 专业解读

{repo} 的价值不在于替代所有平台能力，而在于暴露一个清晰趋势：AI Infra 正在拆成多层控制面。Serving 不只是模型 runtime，还包括调度、cache、gateway、生命周期、sandbox、审计与评测。对用户来说，这类项目适合用来做架构对照：哪些能力应该自己做，哪些可以接入开源组件，哪些只适合借鉴接口。

## 通俗解释

它相当于给大模型或 Agent 应用加了一层“操作系统/调度台”，让请求、环境、模型后端和日志不要散落在各处。

## 关键机制拆解

| 机制 | 解决的问题 | 为什么有效 | 可能的坑 |
|---|---|---|---|
| Control plane | 多后端/多任务难统一管理 | 集中路由、生命周期和策略 | 引入新单点和学习成本 |
| Runtime abstraction | 后端和环境差异大 | 用统一接口屏蔽差异 | 抽象可能牺牲性能或灵活性 |
| Observability | 线上问题难复盘 | 日志、指标、trace 可审计 | 采集成本和隐私风险 |

## 对我的影响

| 维度 | 影响 | 建议动作 |
|---|---|---|
| AI Infra | 可作为平台控制面/网关/调度层参考 | 读部署文档，画内部对照图 |
| LLM 工程 | 影响请求治理、provider 切换、serving 后端选择 | 做最小压测 |
| RL / Game AI | Agent sandbox/环境可用于 rollout/eval | 检查并行和 reset 能力 |
| Agent / Eval | 可能提供可审计执行环境 | 接入 eval harness 原型 |

## 可信度与局限性

- 证据强度：GitHub API 元数据可确认 stars、forks、语言、更新时间。
- 局限性：未完整审计代码质量、release cadence 和安全模型。
- 潜在风险：高 star 不等于生产可用；需要真实 workload 验证。

## 我应该如何跟进

1. 阅读 README、architecture、examples 和 release note。
2. 用一个小模型/小 Agent task 跑最小闭环。
3. 记录与内部平台能力的重叠和缺口。

## 相关链接

- 原文：{url}
- 网页详情：{web(path)}
- 相关卡片：[[Daily/{DATE}]]

## 标签

#ai-radar #github #ai-infra #agent
""")

# Daily
rows = [
('必读','论文','Serving / KV Cache','STAR-KV','自适应低秩 + mixed precision 量化压缩 KV cache，报告端到端生成吞吐 3.1x。','KV cache 是长上下文 serving 的核心成本；这篇有公开代码和 Triton kernel，适合做内部 serving 压测。','Papers/Serving/STAR-KV Low-Rank KV Cache Compression','https://arxiv.org/abs/2606.08382v1'),
('必读','论文','Serving / Sparse Attention','Vortex','可编程 sparse attention serving 系统，让 Agent 自动搜索长上下文注意力模式。','长 Agent rollout 和 deep research 任务会放大 attention 成本；Vortex 把算法探索连接到 serving stack。','Papers/Serving/Vortex Programmable Sparse Attention Serving for AI Agents','https://arxiv.org/abs/2606.06453v1'),
('必读','论文','Serving / Multi-turn KV','Tangram','面向多轮对话的非均匀 KV cache 系统，解决碎片、调度和 kernel 利用率问题。','多轮 memory/chat session 是生产 LLM 的真实 workload，比单轮 benchmark 更接近平台痛点。','Papers/Serving/Tangram Non-Uniform KV Cache for Multi-turn LLM Serving','https://arxiv.org/abs/2606.06302v1'),
('必读','论文','RLHF / RLVR','CATPO','按 tree informativeness 选择和修复 rollout，减少 GRPO/TreeRPO 的无效采样。','后训练成本越来越由 rollout 质量决定；这对推理模型和游戏 RL 稀疏奖励都有迁移价值。','Papers/RLHF/CATPO Critique-Augmented Tree Policy Optimization','https://arxiv.org/abs/2606.08346v1'),
('必读','论文','Agent Eval / World Model','ADWM','用 diffusion world model 做 LLM Agent 离线评估，避免昂贵/危险的在线交互。','如果 Agent/RL 训练依赖大量环境交互，离线 OPE 能显著降低成本并提升安全性。','Papers/Agents/ADWM Off-Policy Evaluation of LLM Agents','https://arxiv.org/abs/2606.05558v1'),
('可 skim','论文','AgentOps / Kubernetes','Auditable Graph-Guided RCA','Typed evidence graph + LangGraph traversal + 独立验证，用于 Kubernetes incident RCA Agent。','RCA Agent 的关键不是单次回答，而是证据链和可审计性；适合内部 AgentOps eval 参考。','Papers/Agents/Auditable Graph-Guided RCA for Kubernetes Incidents','https://arxiv.org/abs/2606.08590v1'),
('必读','博客','Hugging Face / Agentic RL','OpenEnv Agentic RL','Hugging Face 社区推动 OpenEnv，环境层成为 Agentic RL 基础设施。','训练 Agent 和游戏模型都需要可复用、可验证、可并行环境；这是后训练平台的下一层。','Industry/HuggingFace/OpenEnv Agentic RL Community Signal','https://huggingface.co/blog/openenv-agentic-rl'),
('必读','GitHub','Serving Control Plane','OME Kubernetes LLM Serving Operator','K8s operator 管 vLLM/SGLang/TensorRT-LLM/Triton、GPU scheduling 和模型生命周期。','Serving 工程正在从单 runtime 走向 Kubernetes 控制面，适合对照内部平台。','GitHub/Infra/OME Kubernetes LLM Serving Operator','https://github.com/ome-projects/ome'),
('必读','GitHub','Computer-Use Agent','trycua/cua','Computer-use Agent sandbox、SDK、benchmark，覆盖 macOS/Linux/Windows。','GUI/desktop Agent 训练评测需要真实 sandbox；这和 MacArena、CLI-Anything 趋势呼应。','GitHub/Agents/trycua Computer-Use Agent Infrastructure','https://github.com/trycua/cua'),
('可 skim','GitHub','LLM Gateway','LLMGateway','统一多 provider LLM 请求路由、观测、限流和 guardrails。','在线 LLM 应用的控制面会影响成本、可靠性和 eval 数据采集。','GitHub/Infra/LLMGateway Unified LLM Request Gateway','https://github.com/theopenco/llmgateway'),
]
row_md='\n'.join([f"| {a} | {b} | {c} | {d} | {e} | {f} | [[{g}]] | [网页详情]({web(g)}) | [原文]({h}) |" for a,b,c,d,e,f,g,h in rows])
paper_rows='\n'.join([f"| {a} | arXiv / 预印本 | {d} | {c} | {e} | {f} | [[{g}]] | [网页详情]({web(g)}) | [PDF/原文]({h}) |" for a,b,c,d,e,f,g,h in rows if b=='论文'])
blog_rows='\n'.join([f"| {a} | Hugging Face | Blog / Community announcement | {d} | {e} | {f} | [[{g}]] | [网页详情]({web(g)}) | [原文]({h}) |" for a,b,c,d,e,f,g,h in rows if b=='博客'])
gh_rows='\n'.join([f"| {a} | GitHub repo | {d} | {e} | {f} | [[{g}]] | [网页详情]({web(g)}) | [原文]({h}) |" for a,b,c,d,e,f,g,h in rows if b=='GitHub'])

daily='''
# AI Radar Daily - 2026-06-09

> 生成时间：2026-06-09 09:00 CST
> 范围：AI Infra / LLM / RL / Game AI / 大厂博客 / 论文 / GitHub / 行业资讯
> 说明：日报是总览导航页，不是全部正文。Obsidian 中点 `[[详情页]]`，Telegram/GitHub 中点“网页详情”。

## 0. 今日结论

- 今日最值得关注：Serving 方向连续出现 STAR-KV、Tangram、Vortex，说明长上下文/多轮 Agent 的瓶颈正在从“模型能否支持”转为“KV cache、sparse attention 和调度如何系统化落地”。
- 对 AI Infra 的直接影响：OME、LLMGateway、LMCache/vLLM/SGLang 生态共同指向一个趋势：LLM serving 需要 control plane、cache plane、gateway plane 分层治理。
- 对 LLM 训练 / 推理 / Agent 的影响：CATPO 和 ADWM 都在减少无效 rollout：前者提高 RLVR 树采样的信息密度，后者用 world model 降低 Agent 在线评估成本。
- 对 RL / 游戏模型训练的影响：OpenEnv 与 ADWM 显示“环境层 + 离线世界模型评估”会成为 Agentic RL 的基础设施重点。
- 建议今天深读：[[Papers/Serving/STAR-KV Low-Rank KV Cache Compression]]、[[Papers/Serving/Vortex Programmable Sparse Attention Serving for AI Agents]]、[[Papers/RLHF/CATPO Critique-Augmented Tree Policy Optimization]]、[[Industry/HuggingFace/OpenEnv Agentic RL Community Signal]]、[[GitHub/Infra/OME Kubernetes LLM Serving Operator]]。

## 1. 今日态势图

```mermaid
flowchart LR
  subgraph Sources[今日来源]
    C[Hugging Face / OpenAI RSS]
    P[arXiv: Serving / RLVR / Agent Eval]
    G[GitHub: OME / cua / LLMGateway]
    N[低置信: 部分大厂 feed 404/空]
  end
  subgraph Themes[主题聚类]
    T1[KV Cache / Sparse Attention]
    T2[Serving Control Plane]
    T3[RLVR Rollout Efficiency]
    T4[Agentic RL Environments]
    T5[Agent Eval / RCA]
  end
  subgraph Actions[我的动作]
    A1[立即深读/复现]
    A2[做平台架构对照]
    A3[加入 RL 环境观察]
    A4[低置信暂存]
  end
  P --> T1
  G --> T2
  P --> T3
  C --> T4
  P --> T5
  T1 --> A1
  T2 --> A2
  T3 --> A1
  T4 --> A3
  N --> A4
  classDef source fill:#e1d5e7,stroke:#9673a6,stroke-width:2px,color:#111;
  classDef theme fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#111;
  classDef action fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#111;
  class C,P,G,N source;
  class T1,T2,T3,T4,T5 theme;
  class A1,A2,A3,A4 action;
```

## 2. 必读卡片区

> [!important] STAR-KV / Tangram / Vortex：Serving 进入 KV cache + sparse attention 系统战
> - 大类：论文
> - 小类：Serving / KV Cache / Sparse Attention
> - 重点：三篇都不只是“压缩一点显存”，而是在处理长上下文、多轮和 Agent workload 下 cache 表示、调度、kernel、吞吐之间的系统耦合。
> - 为什么重要：你的 serving/eval/RL rollout 成本都会被 KV cache 和 attention backend 决定；STAR-KV 有公开代码，优先拉下来做同硬件 benchmark。
> - 详情：[[Papers/Serving/STAR-KV Low-Rank KV Cache Compression]] / [网页详情](''' + web('Papers/Serving/STAR-KV Low-Rank KV Cache Compression') + ''') / [原文](https://arxiv.org/abs/2606.08382v1)

> [!tip] CATPO：RLVR 训练要优化 rollout 信息密度
> - 大类：论文
> - 小类：RLHF / RLVR / GRPO
> - 重点：用 tree informativeness score 过滤无效树，并用 critique healing 修复全失败分支。
> - 为什么重要：对推理模型 post-training 和稀疏奖励游戏 Agent 都说明一个事实：更多 rollout 不一定更好，关键是哪些 rollout 给梯度。
> - 详情：[[Papers/RLHF/CATPO Critique-Augmented Tree Policy Optimization]] / [网页详情](''' + web('Papers/RLHF/CATPO Critique-Augmented Tree Policy Optimization') + ''') / [原文](https://arxiv.org/abs/2606.08346v1)

> [!tip] OpenEnv + ADWM：Agentic RL 的核心资产是环境和离线评估
> - 大类：博客 / 论文
> - 小类：Agentic RL / World Model
> - 重点：OpenEnv 指向可复用环境层，ADWM 指向不用在线执行也能评估新 Agent policy。
> - 为什么重要：这正是 RL 游戏模型训练关心的环境并行、reward/verifier、offline evaluation 和安全试错。
> - 详情：[[Industry/HuggingFace/OpenEnv Agentic RL Community Signal]]、[[Papers/Agents/ADWM Off-Policy Evaluation of LLM Agents]]

> [!important] OME：LLM serving control plane 上 K8s
> - 大类：GitHub
> - 小类：AI Infra / Serving Control Plane
> - 重点：OME 管 vLLM、SGLang、TensorRT-LLM、Triton、GPU scheduling 和模型生命周期。
> - 为什么重要：如果内部要做多后端推理平台，operator/control-plane 是绕不开的设计层。
> - 详情：[[GitHub/Infra/OME Kubernetes LLM Serving Operator]] / [网页详情](''' + web('GitHub/Infra/OME Kubernetes LLM Serving Operator') + ''') / [原文](https://github.com/ome-projects/ome)

## 3. 优先级矩阵

```mermaid
quadrantChart
  title 今日内容优先级：影响力 x 可落地性
  x-axis 低可落地性 --> 高可落地性
  y-axis 低影响力 --> 高影响力
  quadrant-1 立即读/试
  quadrant-2 读论文/看趋势
  quadrant-3 暂存
  quadrant-4 可工具化
  STAR-KV: [0.86, 0.90]
  Vortex: [0.68, 0.88]
  Tangram: [0.75, 0.84]
  CATPO: [0.62, 0.82]
  OpenEnv: [0.58, 0.78]
  OME: [0.82, 0.80]
  cua: [0.72, 0.76]
```

## 4. 分类总清单

| 标签 | 大类 | 小类 | 标题 | 重点概括 | 为什么重要 | Obsidian 详情 | 网页详情 | 原文 |
|---|---|---|---|---|---|---|---|---|
''' + row_md + '''

## 5. 论文

### 5.1 Serving / KV Cache / Sparse Attention

| 标签 | 论文来源 | 论文 | 作者/机构 | 重点概括 | 工程/研究价值 | Obsidian 详情 | 网页详情 | PDF/原文 |
|---|---|---|---|---|---|---|---|---|
''' + paper_rows + '''

## 6. 博客

### 6.1 Hugging Face

| 标签 | 发布方/大厂 | 栏目/来源 | 标题 | 重点概括 | 工程/算法影响 | Obsidian 详情 | 网页详情 | 原文 |
|---|---|---|---|---|---|---|---|---|
''' + blog_rows + '''

## 7. 资讯 / GitHub 项目

### 7.1 AI Infra / Agent Infrastructure

| 标签 | 来源 | 标题 | 重点概括 | 对我有什么用 | Obsidian 详情 | 网页详情 | 原文 |
|---|---|---|---|---|---|---|---|
''' + gh_rows + '''

## 8. 按主题索引

### AI Infra / Serving / Training

- [[Papers/Serving/STAR-KV Low-Rank KV Cache Compression]] - KV cache 压缩 + Triton kernel，最适合今天复现。
- [[Papers/Serving/Vortex Programmable Sparse Attention Serving for AI Agents]] - sparse attention serving 的可编程系统。
- [[Papers/Serving/Tangram Non-Uniform KV Cache for Multi-turn LLM Serving]] - multi-turn serving 的非均匀 cache 管理。
- [[GitHub/Infra/OME Kubernetes LLM Serving Operator]] - Kubernetes 控制面管理多 serving backend。
- [[GitHub/Infra/LLMGateway Unified LLM Request Gateway]] - LLM 请求网关和 observability。

### LLM / Agent / RAG / Evaluation

- [[Papers/Agents/ADWM Off-Policy Evaluation of LLM Agents]] - LLM Agent 离线评估世界模型。
- [[Papers/Agents/Auditable Graph-Guided RCA for Kubernetes Incidents]] - AgentOps/RCA 的 evidence graph 和可审计评测。
- [[GitHub/Agents/trycua Computer-Use Agent Infrastructure]] - Computer-use Agent sandbox 和 benchmark。

### RL / Game AI / World Model

- [[Papers/RLHF/CATPO Critique-Augmented Tree Policy Optimization]] - 提高 RLVR tree rollout 的信息密度。
- [[Industry/HuggingFace/OpenEnv Agentic RL Community Signal]] - Agentic RL 环境层社区信号。
- [[Papers/Agents/ADWM Off-Policy Evaluation of LLM Agents]] - 离线世界模型评估可迁移到游戏 Agent。

### 公司 / 实验室

- Hugging Face: [[Industry/HuggingFace/OpenEnv Agentic RL Community Signal]]
- OpenAI: 今日 RSS 新增 S-1、benefit everyone plan、Economic Research Exchange，和核心 AI Infra/RL 相关性弱，未纳入详情。
- Google DeepMind: RSS 无今日新核心技术项。

## 9. 值得后续深挖

| 标签 | 大类 | 小类 | 标题 | 后续动作 | Obsidian 详情 | 原文 |
|---|---|---|---|---|---|---|
| 后续 | 论文 | Computer-Use Agent | MacArena | 和 trycua/cua、OSWorld、mobilegym 做 GUI Agent benchmark 横向表 | 暂未生成 | [arXiv](https://arxiv.org/abs/2606.06560v1) |
| 后续 | 论文 | Agent-native Interface | CLI-Anything | 和 Hugging Face hf CLI for agents 形成 agent-native interface checklist | 暂未生成 | [arXiv](https://arxiv.org/abs/2606.03854v1) |
| 后续 | GitHub | KV Cache | LMCache | 继续跟踪 dev branch 和 vLLM 集成；今日已有旧卡片可复用 | [[GitHub/Agents/LMCache-LMCache]] | [GitHub](https://github.com/LMCache/LMCache) |
| 低置信 | 博客 | OpenAI | Economic Research Exchange / S-1 / benefit plan | 偏政策/公司动态，和 AI Infra/RL 相关性弱，跳过详情 | 暂未生成 | [OpenAI News](https://openai.com/news/) |

## 10. 采集失败或低置信来源

- `blogwatcher-cli` 未安装；本次直接解析 RSS/Atom feed。
- Anthropic feed URL 返回 404，Meta AI RSS 返回 404；今日未纳入新重点。
- NVIDIA AI category feed 可访问但未返回可解析新条目。
- GitHub Search API 对后续 query 出现 rate limit，已用已获取 repo API 元数据完成筛选。
- arXiv 宽泛 query 噪声很高，已改用 title/abstract 精确 query 严格过滤。

## 11. 归档标签

#ai-radar #daily #ai-infra #llm #rl #serving #kv-cache #agentic-rl
'''
w('Daily/2026-06-09', daily)
print('generated', len(paper_items)+1+len(repos)+1, 'files')
