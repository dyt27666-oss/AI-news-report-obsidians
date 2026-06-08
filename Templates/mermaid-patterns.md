# Mermaid 图示模式库

Mermaid 是一种基于文本的图表语言，可在 Obsidian 中原生使用，无需额外插件即可生成流程图、时序图、思维导图、时间线等多种图表。它特别适合将知识和研究内容以可视化形式**压缩**呈现。例如，在 AI Radar 详情页中，常用 **子图 (subgraph)**、**类别样式 (classDef)**、**内部链接** 等功能来分组关键节点、统一配色，并保持文本与结构简洁。以下归纳了一些常见的信息结构模式，每种模式附带示例代码和配色建议，可直接复制粘贴到 Obsidian 的 ```mermaid``` 代码块中使用。

## 1. 论文机制图 (Research Paper Overview)
- **用途**：总结科研论文的结构脉络，包括研究目标、瓶颈/缺口、方法模块、训练/推理流程以及结果证据等。通过多层次子图展示从“研究问题 → 方法模块 → 执行流程 → 证据/决策”的逻辑流程，帮助快速了解论文核心。
- **结构**：示例中将“研究问题 (Q)”、“方法模块 (M)”、“流程 (P)”、“证据 (E)”分别用 `subgraph` 包含相关节点。箭头表示因果或数据流向。节点简短明了，以突出关键信息。
- **样式**：使用 `classDef` 定义类别背景色，再通过 `class` 将节点归类。例如，可为“问题/瓶颈”设淡橙填充，为“方法/模块”设淡蓝色，为“证据/评估”设淡绿色，为“风险/局限”设淡红色。示例代码如下：

```mermaid
flowchart TB
  subgraph Q[研究问题]
    Q1[目标: 提升推理/训练/评估]
    Q2[瓶颈: 数据、奖励、上下文、吞吐]
    Q3[缺口: 现有方法无法同时满足 X/Y/Z]
  end

  subgraph M[方法模块]
    M1[模块 A: 表征/检索/策略]
    M2[模块 B: 优化/奖励/调度]
    M3[模块 C: 约束/校验/过滤]
  end

  subgraph P[训练或推理流程]
    D[数据/任务] --> R[rollout / inference]
    R --> S[scoring / reward / eval]
    S --> U[update / selection / cache]
  end

  subgraph E[证据与决策]
    E1[Benchmark]
    E2[指标变化]
    E3[局限性]
    E4[是否值得复现]
  end

  Q1 --> M1 --> R
  Q2 --> M2 --> S
  Q3 --> M3 --> U
  U --> E1 --> E2 --> E4
  S --> E3 --> E4

  classDef problem  fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
  classDef method   fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef evidence fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  classDef risk     fill:#f8cecc,stroke:#b85450,stroke-width:2px;
  class Q1,Q2,Q3 problem;
  class M1,M2,M3,D,R,S,U method;
  class E1,E2,E4 evidence;
  class E3 risk;
```

复制上述代码到 Obsidian，即可生成与示例一致的层次流程图。节点归类后，色块背景对比明显，帮助快速区分不同模块。在示例中，`classDef` 的使用方式参考官方文档，通过统一 CSS 样式实现一致的配色和边框。

## 2. 大厂博客信号图 (Corporate Announcement Signals)
- **用途**：剖析大公司/实验室的公告、博客或论文如何传递产品、研究或技术瓶颈等信号，并指引我们相应的行动（如阅读、试用等）。  
- **结构**：可用 `flowchart LR`（或 `TB`）按横向分列，将流程分为“发布方 (公司/实验室) → 信号 (产品方向/研究方向/工程瓶颈) → 工程影响 (如数据、推理、安全等) → 我们的动作（必读、复现、观察等）”四段。箭头表示信息流向和逻辑关系。  
- **配色**：为不同分组定义颜色。如示例中给“公司/文章”使用紫色系、给“信号”使用浅蓝色、“基础设施意义”使用浅绿色、“行动”使用浅橙色，借助 `classDef` 区分视觉区域。  
- **示例**：

```mermaid
flowchart LR
  subgraph Source[发布方]
    C[公司/实验室]
    A[文章/公告]
  end

  subgraph Signal[释放的信号]
    S1[产品方向]
    S2[研究方向]
    S3[工程瓶颈]
  end

  subgraph Infra[对工程的含义]
    I1[数据/训练]
    I2[推理/Serving]
    I3[Agent/Memory/Eval]
    I4[安全/治理]
  end

  subgraph Action[我的动作]
    R1[必读]
    R2[试用/复现]
    R3[加入观察列表]
  end

  C --> A --> S1
  A --> S2
  A --> S3
  S1 --> I2
  S2 --> I1
  S3 --> I3
  S3 --> I4
  I1 --> R1
  I2 --> R2
  I3 --> R3
  I4 --> R3

  classDef company fill:#e1d5e7,stroke:#9673a6,stroke-width:2px;
  classDef signal  fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef infra   fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  classDef action  fill:#ffe6cc,stroke:#d79b00,stroke-width:2px;
  class C,A company;
  class S1,S2,S3 signal;
  class I1,I2,I3,I4 infra;
  class R1,R2,R3 action;
```

这一模式常用于**信息过滤**：将外部发布的信号映射到自身关注点上。使用分组（subgraph）可以清晰标示各层级内容，并用 `classDef` 区分不同主题颜色。

## 3. AI 基础设施项目架构图
- **用途**：描述 AI 平台或项目从工作负载到系统组件再到硬件依赖的完整架构，以及最终的性能、成本等结果。  
- **结构**：通常采用 `flowchart TB`，从顶部工作负载 (Workload) 开始，经过系统核心组件 (System)，然后到硬件 (Hardware)，最终到效果 (Outcome)。箭头展现调度和依赖关系。  
- **配色**：为每个层级设定不同颜色，例如示例中工作负载用浅橙、系统核心用浅蓝、硬件用浅紫、结果用浅绿，突出不同内容块。  
- **示例**：

```mermaid
flowchart TB
  subgraph Workload[Workload]
    W1[Prompt / Request]
    W2[Batch / Stream]
    W3[Agent Tool Calls]
  end

  subgraph System[项目核心系统]
    S1[Scheduler]
    S2[KV Cache / State]
    S3[Runtime / Kernel]
    S4[API / Control Plane]
  end

  subgraph Hardware[硬件与依赖]
    H1[GPU / NPU]
    H2[Network / RDMA]
    H3[Storage / DB]
  end

  subgraph Outcome[结果]
    O1[吞吐提升]
    O2[延迟下降]
    O3[成本下降]
    O4[复杂度/风险]
  end

  W1 --> S1
  W2 --> S1
  W3 --> S4
  S1 --> S2 --> S3
  S3 --> H1
  S2 --> H2
  S4 --> H3
  H1 --> O1
  H2 --> O2
  H3 --> O3
  S4 --> O4

  classDef workload fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
  classDef system   fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef hardware fill:#e1d5e7,stroke:#9673a6,stroke-width:2px;
  classDef outcome  fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  classDef risk     fill:#f8cecc,stroke:#b85450,stroke-width:2px;
  class W1,W2,W3 workload;
  class S1,S2,S3,S4 system;
  class H1,H2,H3 hardware;
  class O1,O2,O3 outcome;
  class O4 risk;
```

该模式适合展示**系统架构和数据/控制流**：上层为输入负载，中间为核心调度和状态管理，下层为硬件，最后用结果节点表示优化目标或存在风险。通过 `classDef` 统一风格，使图表更具层次感和美观。

## 4. 时间线 (Timeline)
- **用途**：展示技术、产品或研究的关键事件时序。例如记录模型发行、框架发布等里程碑。  
- **方法**：可以用纯 Markdown 的标题加无序列表（如示例），也可用 Mermaid 的时间线或甘特图功能。Mermaid 原生支持 `timeline` 图（需要新版支持）。  
- **示例**：Markdown 列表或 Mermaid 语法均可。

Markdown 形式示例：
```markdown
## Timeline

2023  
- Arbitrum 发币  
2024  
- Blast 上线  
2025  
- Hyperliquid 爆发  
```

Mermaid 时间线示例：
```mermaid
timeline
    2023 : Arbitrum 发币
    2024 : Blast 上线
    2025 : Hyperliquid 爆发
```

这两种效果类似。使用 Mermaid 时间线可以生成可视化横轴图，但部分旧版 Obsidian 可能暂不支持（可使用插件或更新到支持 v10+ 的 Mermaid）。无论哪种方式，都能帮助梳理发展脉络。

## 5. 关系网（Graph / Network）
- **用途**：可视化实体（如项目方、团队成员、合作伙伴、链上地址、KOL 等）之间的**关联关系**。有助于了解生态结构或社群网络。  
- **结构**：使用 `graph LR`（或 TB/BT/RL）画无中心树或网络状图。节点可分组（`subgraph`）或单独高亮，并用箭头或双向线表示联系。  
- **配色/样式**：可为不同实体类别定义颜色（如团队 vs 社区 vs 代币），并使用 `class` 给重要节点加标记。借助 `internal-link` 类让节点文本变成 Obsidian 笔记链接。  
- **示例**：
```mermaid
graph LR
  subgraph A[项目团队]
    A1[核心团队]
    A2[代币/产品]
  end
  subgraph B[社区/KOL]
    B1[KOL x]
    B2[Meme 社区]
  end
  A1 --> A2
  B1 --> A2
  B1 --> B2

  classDef core       fill:#dae8fc,stroke:#6c8ebf;
  classDef community  fill:#d5e8d4,stroke:#82b366;
  class A1 core;
  class B1,B2 community;
```

在这个例子中，我们用 `subgraph` 简要分组，用 `classDef` 使“核心团队”节点呈现蓝色背景、“社区/KOL”节点呈现绿背景。通过 `A1 --> A2` 等箭头表示关系链。若需要可加 `class A1 internal-link;` 使节点链接到笔记（前提是存在同名文档）。

## 6. 其它常用图表
- **甘特图 (Gantt)**：展示计划/进度或任务时间序列，可用来规划研究路线。Mermaid 支持 `gantt` 语法。  
- **饼图 (Pie)**：用来表示占比，如市场份额、功能分布等。Mermaid 有 `pie` 语法。  
- **象限图 (Quadrant)**：常用于风险收益、影响力-投入等二维评估。Mermaid 支持 `quadrantChart`。  
- **石川图 (Ishikawa / 鱼骨图)**：分析问题原因，例如在识别瓶颈或风险时使用。Mermaid 提供 `flowchart` 结合特定布局或独立的 `fish` 语法。  
- **看板图 (Kanban)**：如果需要展示任务状态，可用 Mermaid 的 `kanban` 语法，支持拖动列。  
- **Wardley 地图**：战略级图，可借助 Mermaid 的 `wardley` 语法绘制。

以上这些图表类型均在 Mermaid 官方文档中有示例。在 Obsidian 中使用时，只需在代码块头写 `mermaid`，即可渲染。例如：
```mermaid
gantt
    title 项目计划
    dateFormat  YYYY-MM-DD
    section 训练
    数据收集        :done,    a1, 2024-01-01, 30d
    模型训练        :active,  a2, 2024-02-01, 60d
    section 测试
    验证集评估      :         b1, after a2, 20d
```

## 7. 样式与配色建议
- **统一主题**：使用 `classDef` 可以轻松统一节点样式。按照功能或层次给不同类别节点设置统一填充色和边框。可采用柔和色调（如示例中的浅橙、浅蓝、浅绿），提高可读性。切忌使用过多强烈颜色，防止信息过载。  
- **内部链接**：在 Obsidian 中，可以给节点加上 `class 某类 internal-link;`（或直接在文本中用 `[[]]`）让节点可点击跳转到笔记。这使图示与知识库双向联动，方便导航。  
- **文本格式**：Mermaid 支持“Markdown 字符串”，可用 `**粗体**`、`*斜体*` 等。对于较长标题可以自动换行，避免节点过宽。  
- **布局方向**：根据内容选择合适方向（TB、LR、BT、RL）。例如流程通常用 TB（自上而下）；关系网可用 LR 扩展；子图内也可指定方向。  
- **外部样式**：尽量用内置的 `classDef` 样式，不推荐在外部 CSS 强行覆盖，因 Mermaid 内部样式较高优先级。

## 8. 测试与示例
以上示例代码可直接复制到 Obsidian 的 ```mermaid``` 代码块中查看效果（Obsidian 支持原生渲染）。若想调整或尝试其他模式，可使用官方[Mermaid Live Editor](https://mermaid-js.github.io/mermaid-live-editor)进行在线编辑和预览。结合社区经验和官方文档，我们可以根据实际需求灵活组合子图、类、样式与交互。

**参考资料：** Obsidian 官方文档和社区教程介绍了 Mermaid 的用法，Mermaid 官方文档提供了各种图表语法示例。可根据这些资源扩展更多模板与风格。

