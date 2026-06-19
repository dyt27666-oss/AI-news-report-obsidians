#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime

DATE='2026-06-19'
VAULT=Path('/home/vscode-server/obsidian-ai-radar')
GH_BASE='https://github.com/dyt27666-oss/AI-news-report-obsidians/blob/main'
state=json.loads((VAULT/f'Automation/state/github-stars-{DATE}.json').read_text())
high=state['high_star_top10']
growth=state['growth_top10']

def safe_repo(repo): return repo.replace('/','--')
def blob(path): return f'{GH_BASE}/{path}.md'
def md_link(path): return f'[[{path}]]'
def write(path, text):
    p=VAULT/path; p.parent.mkdir(parents=True, exist_ok=True); p.write_text(text, encoding='utf-8')

def repo_detail(r, rank, kind):
    repo=r['repo']; name=safe_repo(repo); path=Path(f'GitHub/{DATE}/{name}.md')
    topics=', '.join(r.get('topics') or []) or '未标注'
    delta=r.get('stars_delta')
    delta_txt='无历史基线' if delta is None else str(delta)
    desc=r.get('description') or '无描述'
    text=f'''---
source: GitHub
source_type: repository
repo: {repo}
original_url: {r['html_url']}
daily: Daily/{DATE}
---

# {repo}

## 一句话结论
{repo} 在今日 {kind} 榜单排名第 {rank}，核心信号是：{desc}

## TL;DR
- Stars / forks：{r['stars']} / {r['forks']}；今日 delta：{delta_txt}。
- 语言：{r.get('language') or 'Unknown'}；更新时间：{r.get('updated_at')}。
- 主题：{topics}。
- 对 AI Infra/LLM 工程的意义：可作为 agent runtime、serving、训练或评测生态的参考坐标。

## 元信息
| 字段 | 值 |
|---|---|
| Repo | [{repo}]({r['html_url']}) |
| Stars | {r['stars']} |
| Forks | {r['forks']} |
| Language | {r.get('language') or 'Unknown'} |
| Updated | {r.get('updated_at')} |
| Pushed | {r.get('pushed_at')} |
| Topics | {topics} |
| 描述 | {desc} |

## 信息压缩图示
```mermaid
flowchart TB
  subgraph Workload[Workload]
    W1[LLM / Agent 请求]
    W2[开发者集成]
    W3[生产环境约束]
  end
  subgraph System[项目能力]
    S1[{repo}]
    S2[API / SDK / CLI]
    S3[状态 / memory / runtime]
    S4[docs / examples / community]
  end
  subgraph Outcome[工程结果]
    O1[更快落地]
    O2[降低 glue code]
    O3[生态锁定风险]
    O4[值得试用判断]
  end
  W1 --> S1
  W2 --> S2 --> S1
  W3 --> S3 --> S1
  S1 --> S4
  S1 --> O1
  S2 --> O2
  S4 --> O4
  S3 --> O3 --> O4
  classDef workload fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
  classDef system fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef outcome fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  classDef risk fill:#f8cecc,stroke:#b85450,stroke-width:2px;
  class W1,W2,W3 workload;
  class S1,S2,S3,S4 system;
  class O1,O2,O4 outcome;
  class O3 risk;
```

## 专业解读
这个项目的价值不只来自 star 数，而是它在 agent、LLM serving/training 或 AI 工程链路中的位置。若它提供稳定 API、示例、benchmark 或活跃 issue/release，就可以缩短从 prototype 到 production 的路径；若主要是 prompt/列表型项目，则更适合作为观察信号而非直接依赖。

## 通俗解释
它像一个生态温度计：star 越高、增长越快，说明开发者正在把注意力投入到这类工具或工作流上。

## 关键机制拆解
| 模块 | 观察点 | 对我的用途 |
|---|---|---|
| 接口层 | SDK/API/CLI 是否清晰 | 判断接入成本 |
| 运行层 | 是否涉及调度、状态、缓存、工具调用 | 判断 infra 价值 |
| 评测层 | 是否有 benchmark/examples | 判断可信度 |
| 社区层 | stars/forks/update | 判断维护风险 |

## 对我的影响
可作为 AI Radar 后续试用池；若与 Hermes、Firecrawl、Dify、vLLM、verl 等链路相关，应优先评估能否改善自动研究、agent workflow、推理服务或 post-training 实验效率。

## 可信度与局限性
GitHub stars 有 hype 偏差；本页依据 GitHub API snapshot 自动生成，未进行源码级审计。

## 我应该如何跟进
1. 打开 README 和 examples，确认是否能在 30 分钟内跑通。
2. 查 release/issue 活跃度，避免引入维护风险。
3. 若与当前 AI Radar 或 RL/serving 工作流相关，加入 spike 清单。

## 相关链接
- 原文：[{repo}]({r['html_url']})
- 返回日报：[[Daily/{DATE}]]

#ai-radar #github #ai-infra #llm
'''
    write(path, text)
    return str(path.with_suffix(''))

repo_paths={}
for i,r in enumerate(high,1): repo_paths[r['repo']]=repo_detail(r,i,'高 star')
for i,r in enumerate(growth,1):
    if r['repo'] not in repo_paths: repo_paths[r['repo']]=repo_detail(r,i,'增长最快')

industry_items=[
('OpenAI','News / Enterprise AI','New usage analytics and updated spend controls for enterprises','OpenAI 将企业版成本治理与使用分析做成产品能力，说明大模型平台开始进入 FinOps / governance 阶段。','https://openai.com/index/chatgpt-enterprise-spend-controls','Industry/2026-06-19/OpenAI-Enterprise-Usage-Analytics-Spend-Controls'),
('Google DeepMind','Blog / Agent Safety','Securing the future of AI agents','DeepMind 将 AI agent 安全显式落到 control roadmap、实时监控和内部系统防护，适合作为 agent runtime 安全架构参考。','https://deepmind.google/blog/securing-the-future-of-ai-agents/','Industry/2026-06-19/DeepMind-Securing-Future-AI-Agents'),
('Hugging Face','Blog / Agent Eval','Is it agentic enough? Benchmarking open models on your own tooling','HF 把 agentic 能力评测从封闭榜单推向用户自有工具链，对 agent eval 和生产验收更有参考价值。','https://huggingface.co/blog/is-it-agentic-enough','Industry/2026-06-19/HuggingFace-Agentic-Enough-Benchmarking'),
('Hugging Face','Blog / Fine-tuning','Beyond LoRA: Can you beat the most popular fine-tuning technique?','PEFT/微调路线继续演进，适合关注 post-training 性价比和 adapter 方法替代。','https://huggingface.co/blog/peft-beyond-lora','Industry/2026-06-19/HuggingFace-Beyond-LoRA'),
('Microsoft Research','Research Blog / Agent Systems','MagenticLite, MagenticBrain, Fara1.5: an agentic experience optimized for small models','Microsoft 的 Magentic 系列把小模型 agent 体验作为优化目标，提示 agent infra 不能只围绕最大模型设计。','https://www.microsoft.com/en-us/research/','Industry/2026-06-19/Microsoft-MagenticLite-MagenticBrain-Fara15'),
]
for company,typ,title,summary,url,path in industry_items:
    text=f'''---
source: {company}
source_type: {typ}
original_url: {url}
daily: Daily/{DATE}
---

# {title}

## 一句话结论
{summary}

## TL;DR
- 发布方/大厂：{company}
- 栏目/来源类型：{typ}
- 原文：{url}
- 对用户画像的价值：把公司信号映射到 AI Infra、LLM 工程、Agent Eval 或 Post-training 的实际动作。

## 元信息
| 字段 | 值 |
|---|---|
| 发布方/大厂 | {company} |
| 栏目/来源类型 | {typ} |
| 发布时间 | 2026-06-18/近期 RSS |
| 原文链接 | [原文]({url}) |
| 返回日报 | [[Daily/{DATE}]] |

## 信息压缩图示
```mermaid
flowchart LR
  subgraph Source[发布方]
    C[{company}]
    A[文章/公告]
  end
  subgraph Signal[释放的信号]
    S1[产品/研究方向]
    S2[工程瓶颈]
    S3[评测/治理要求]
  end
  subgraph Infra[对工程的含义]
    I1[Agent runtime]
    I2[LLM platform / FinOps]
    I3[Eval / Safety]
    I4[Post-training]
  end
  subgraph Action[我的动作]
    R1[深读原文]
    R2[抽取 checklist]
    R3[加入观察列表]
  end
  C --> A --> S1
  A --> S2
  A --> S3
  S1 --> I1
  S1 --> I2
  S2 --> I4
  S3 --> I3
  I1 --> R2
  I2 --> R2
  I3 --> R1
  I4 --> R3
  classDef company fill:#e1d5e7,stroke:#9673a6,stroke-width:2px;
  classDef signal fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef infra fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  classDef action fill:#ffe6cc,stroke:#d79b00,stroke-width:2px;
  class C,A company;
  class S1,S2,S3 signal;
  class I1,I2,I3,I4 infra;
  class R1,R2,R3 action;
```

## 专业解读
{summary} 对 AI Infra 工程师的重点不在新闻本身，而在它暴露出的平台能力边界：成本治理、agent 安全、评测可迁移性、小模型 agent 体验或微调方法迭代，都会影响后续系统设计。

## 通俗解释
这条信息说明大厂正在把“能 demo 的 AI”推进到“能被企业、研究团队或工程团队稳定使用和评估的 AI”。

## 关键机制拆解
| 层级 | 关注点 | 可转化动作 |
|---|---|---|
| 产品/研究信号 | 发布方强调的能力 | 判断方向是否进入主流路线 |
| 工程约束 | 成本、安全、评测、延迟 | 转化为内部 checklist |
| 生态影响 | 是否改变工具链 | 决定是否试用/跟踪 |

## 对我的影响
如果后续要做 agent workflow、research automation、LLM 平台治理或 post-training 实验，应把这条作为需求输入，而不是只作为资讯阅读。

## 可信度与局限性
来自官方/公司渠道，可信度较高但有产品叙事偏差；本次 cron 主要基于 RSS/公开页面元数据，未完整抓取全文。

## 我应该如何跟进
1. 深读原文并抽取可执行 checklist。
2. 对照现有 AI Radar / Hermes / serving / post-training 工作流寻找可落地点。
3. 若涉及 benchmark 或开源工具，后续补一次源码/实验复现。

## 相关链接
- 原文：[{title}]({url})
- 返回日报：[[Daily/{DATE}]]

#ai-radar #industry #ai-infra #llm #agent
'''
    write(Path(path+'.md'), text)

paper_items=[
('OpenAI LifeSciBench','OpenAI Research Blog','benchmark / company report','OpenAI expert-authored life science benchmark，强调真实研究任务和专家审核，可作为 agent/LLM eval 设计参考。','https://openai.com/index/introducing-life-sci-bench','Papers/2026-06-19/OpenAI-LifeSciBench'),
('AdaSR Adaptive Streaming Reasoning','arXiv watchlist','preprint / low-confidence metadata','自适应 streaming reasoning 方向与推理预算、延迟控制和 serving 策略相关；arXiv 今日访问失败，沿用 watchlist。','https://arxiv.org/','Papers/2026-06-19/AdaSR-Adaptive-Streaming-Reasoning-Watchlist'),
]
for title,source,stype,summary,url,path in paper_items:
    text=f'''---
source: {source}
source_type: {stype}
original_url: {url}
daily: Daily/{DATE}
---

# {title}

## 一句话结论
{summary}

## TL;DR
- 论文来源：{source}
- 来源类型：{stype}
- 原文/索引：{url}
- 采集说明：今日 arXiv/Semantic Scholar 出现 429/timeout，论文项以高相关 watchlist 和公司研究 benchmark 为主，已标注低置信来源。

## 元信息
| 字段 | 值 |
|---|---|
| 论文来源 | {source} |
| 来源类型 | {stype} |
| 作者/机构 | 见原文 |
| 发布时间 | 近期/待核验 |
| abs 链接 | {url} |
| PDF 链接 | 待核验 |
| 代码链接 | 未发现 |

## 信息压缩图示
```mermaid
flowchart TB
  subgraph Q[研究问题]
    Q1[真实任务评测 / 推理预算]
    Q2[Agent / LLM 行为是否可靠]
    Q3[线上 serving 成本与质量权衡]
  end
  subgraph M[方法模块]
    M1[任务/benchmark 设计]
    M2[reasoning / streaming 控制]
    M3[专家或自动评测]
  end
  subgraph P[训练或推理流程]
    D[任务输入] --> R[模型推理 / rollout]
    R --> S[scoring / eval]
    S --> U[策略或系统决策]
  end
  subgraph E[证据与决策]
    E1[Benchmark 信号]
    E2[工程可落地性]
    E3[元数据低置信]
    E4[后续是否深读]
  end
  Q1 --> M1 --> D
  Q2 --> M3 --> S
  Q3 --> M2 --> R
  U --> E1 --> E2 --> E4
  E3 --> E4
  classDef problem fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
  classDef method fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef evidence fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  classDef risk fill:#f8cecc,stroke:#b85450,stroke-width:2px;
  class Q1,Q2,Q3 problem;
  class M1,M2,M3,D,R,S,U method;
  class E1,E2,E4 evidence;
  class E3 risk;
```

## 专业解读
{summary} 对用户最有价值的是把研究问题转成系统问题：如何定义任务、如何控制 reasoning budget、如何把评测结果变成 serving 或 post-training 的调参依据。

## 通俗解释
它回答的是“模型看起来会做题，是否真的能在复杂任务中稳定完成目标”。

## 关键机制拆解
| 机制 | 需要核验的问题 | 对工程的影响 |
|---|---|---|
| Benchmark 设计 | 任务是否真实、可复现 | 决定评测可信度 |
| 推理流程 | 是否控制 latency/cost | 决定 serving 价值 |
| 结果证据 | 是否有 ablation / baseline | 决定是否复现 |

## 对我的影响
适合纳入 agent eval / serving quality / post-training reward design 的阅读池，但需要在源站恢复后补齐元数据。

## 可信度与局限性
本页受 arXiv/Semantic Scholar 429/timeout 影响，部分字段待核验；已避免把低置信论文包装成确定结论。

## 我应该如何跟进
1. 明天或源站恢复后补抓 PDF/作者/实验结果。
2. 若有代码，检查是否能复现实验。
3. 抽取可迁移到内部 agent eval 的指标。

## 相关链接
- 原文/索引：[{title}]({url})
- 返回日报：[[Daily/{DATE}]]

#ai-radar #paper #eval #llm
'''
    write(Path(path+'.md'), text)

# tables
high_rows=[]
for i,r in enumerate(high,1):
    p=repo_paths[r['repo']]
    topics=', '.join((r.get('topics') or [])[:5]) or '未标注'
    high_rows.append(f"| {i} | {r['repo']} | {r['stars']} | {r['forks']} | {r.get('language') or 'Unknown'} | {r.get('updated_at')} | {topics} | {(r.get('description') or '').replace('|','/')[:80]} | {'值得试用/观察' if i<=6 else '可观察'} | [[{p}]] | [GitHub]({r['html_url']}) |")
growth_rows=[]
for i,r in enumerate(growth,1):
    p=repo_paths[r['repo']]
    delta=r.get('stars_delta')
    basis='historical_snapshot' if delta is not None else '新增/无基线'
    growth_rows.append(f"| {i} | {r['repo']} | {delta if delta is not None else 'N/A'} | {r['stars']} | {r['forks']} | {r.get('language') or 'Unknown'} | {r.get('updated_at')} | {basis} | {(r.get('description') or '').replace('|','/')[:80]} | [[{p}]] | [GitHub]({r['html_url']}) |")

matrix=[
('OpenAI','News / Research','有高相关新项',2,'Enterprise usage analytics; LifeSciBench','RSS 可访问；官网浏览器 Cloudflare'),
('Anthropic','News / Research / Engineering','访问失败/低置信',0,'无高相关新项','RSS 404；未强行补弱相关'),
('Google DeepMind','Blog / Research','有高相关新项',1,'Securing the future of AI agents','RSS 可访问'),
('Meta AI','Blog / Research','访问失败/低置信',0,'无高相关新项','RSS 404；保留矩阵'),
('NVIDIA','Technical Blog / AI','低置信',0,'无高相关新项','Feed 只返回站点标题，未取到条目'),
('Microsoft','Research AI','有高相关新项/低置信',1,'MagenticLite/MagenticBrain/Fara1.5','Feed 访问超时，基于已知 Research feed 标题'),
('Hugging Face','Blog / Papers / Releases','有高相关新项',3,'MosaicLeaks; Beyond LoRA; Agentic enough','RSS 可访问'),
('腾讯','AI Lab / 技术博客','低置信',0,'无高相关新项','公开源未取到新 AI infra 强相关条目'),
('字节','Seed / 技术博客','低置信',0,'无高相关新项','公开源未取到新 AI infra 强相关条目'),
('SpaceAI','Blog / News','低置信',0,'无高相关新项','公开源未取到可核验条目'),
]
matrix_rows='\n'.join(f'| {a} | {b} | {c} | {d} | {e} | {f} |' for a,b,c,d,e,f in matrix)
industry_rows='\n'.join(f"| {'必读' if i<3 else '可 skim'} | {c} | {t} | {title} | {s} | {'抽取为 agent/infra/eval checklist'} | [[{p}]] | [网页详情]({blob(p)}) | [原文]({u}) |" for i,(c,t,title,s,u,p) in enumerate(industry_items))
paper_rows='\n'.join(f"| {'可 skim' if 'watchlist' not in st else '低置信'} | {src} / {st} | {title} | 见原文 | {s} | {'Agent/Eval/Serving 方向参考'} | [[{p}]] | [网页详情]({blob(p)}) | [原文]({u}) |" for title,src,st,s,u,p in paper_items)
class_rows='\n'.join([
f"| 必读 | GitHub | Agent Infra | Hermes Agent / Firecrawl / Dify 增长 | Agent 外层 infra、web data 和 workflow control plane 持续升温 | 直接影响自动研究、agent memory、tool use 和生产 workflow | [[{repo_paths['NousResearch/hermes-agent']}]] | [网页详情]({blob(repo_paths['NousResearch/hermes-agent'])}) | [原文](https://github.com/NousResearch/hermes-agent) |",
f"| 必读 | 博客 | Agent Safety | DeepMind: Securing the future of AI agents | Agent 安全从 policy 进入 control roadmap 与实时监控 | 可转化为 agent runtime 安全设计 checklist | [[Industry/2026-06-19/DeepMind-Securing-Future-AI-Agents]] | [网页详情]({blob('Industry/2026-06-19/DeepMind-Securing-Future-AI-Agents')}) | [原文](https://deepmind.google/blog/securing-the-future-of-ai-agents/) |",
f"| 可 skim | 博客 | Agent Eval | HF: Is it agentic enough? | 在用户自有 tooling 上评测开放模型 agentic 能力 | 比封闭榜单更贴近真实工具链验收 | [[Industry/2026-06-19/HuggingFace-Agentic-Enough-Benchmarking]] | [网页详情]({blob('Industry/2026-06-19/HuggingFace-Agentic-Enough-Benchmarking')}) | [原文](https://huggingface.co/blog/is-it-agentic-enough) |",
f"| 低置信 | 论文 | Eval / Serving | LifeSciBench / AdaSR watchlist | 论文源 429，保留高相关 watchlist 并标注低置信 | 避免用弱相关论文填充，同时保留后续深挖入口 | [[Papers/2026-06-19/OpenAI-LifeSciBench]] | [网页详情]({blob('Papers/2026-06-19/OpenAI-LifeSciBench')}) | [原文](https://openai.com/index/introducing-life-sci-bench) |",
])

daily=f'''# AI Radar Daily - {DATE}

> 生成时间：2026-06-19 09:00 BJT  
> 范围：AI Infra / LLM / RL / Agent / Eval / Serving / Training / Post-training / World Model  
> 说明：日报是总览导航页；详情页负责深度理解。GitHub snapshot: `Automation/state/github-stars-{DATE}.json`。

## 0. 今日结论

- 今日最强信号：Agent 外层基础设施继续高热，Hermes Agent、Firecrawl、ECC、Dify、browser-use 同时出现在高 star/增长榜。
- 对 AI Infra 的直接影响：GitHub snapshot 可用但 API 局部 403；arXiv/Semantic Scholar 多次 429/timeout，说明 research agent 必须依赖 snapshot、缓存和失败矩阵。
- 对 LLM 训练 / 推理 / Agent 的影响：OpenAI 企业 usage analytics、DeepMind agent safety、HF agentic benchmark 都指向“可治理、可评测、可落地”的 agent 平台。
- 对 RL / 游戏模型训练的影响：今日没有强新 RL/game paper；保留 post-training、reasoning budget 和 eval watchlist，避免弱相关填充。
- 建议今天深读：[[Industry/2026-06-19/DeepMind-Securing-Future-AI-Agents]]、[[Industry/2026-06-19/HuggingFace-Agentic-Enough-Benchmarking]]、[[GitHub/2026-06-19/NousResearch--hermes-agent]]、[[GitHub/2026-06-19/firecrawl--firecrawl]]。

## 1. 今日态势图

```mermaid
flowchart LR
  subgraph Sources[今日来源]
    C[大厂博客 / RSS]
    P[论文源 / arXiv 429]
    G[GitHub snapshot 132 repos]
    F[失败/低置信来源]
  end
  subgraph Themes[主题聚类]
    T1[Agent runtime / harness]
    T2[Web data / research agent]
    T3[Enterprise AI governance]
    T4[Agent safety / eval]
  end
  subgraph Actions[我的动作]
    A1[必读: Hermes / Firecrawl]
    A2[深读: DeepMind agent safety]
    A3[试用: HF agent eval]
    A4[补抓: arXiv / S2]
  end
  C --> T3
  C --> T4
  G --> T1
  G --> T2
  P --> F
  F --> A4
  T1 --> A1
  T2 --> A1
  T3 --> A2
  T4 --> A3
  classDef source fill:#e1d5e7,stroke:#9673a6,stroke-width:2px,color:#111;
  classDef theme fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#111;
  classDef action fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#111;
  class C,P,G,F source;
  class T1,T2,T3,T4 theme;
  class A1,A2,A3,A4 action;
```

## 2. 必读卡片区

> [!important] Agent runtime / harness 与 web data 继续增长
> - 大类：GitHub
> - 小类：Agent Infra / Web Data
> - 重点：Hermes Agent +806、Firecrawl +625、ECC +476，说明 skills/memory、web extraction、agent harness 正在成为模型外关键资产。
> - 为什么重要：自动研究、tool use、agent workflow 的质量越来越依赖模型外 runtime 和可控数据入口。
> - 详情：[[GitHub/2026-06-19/NousResearch--hermes-agent]] / [网页详情]({blob('GitHub/2026-06-19/NousResearch--hermes-agent')}) / [原文](https://github.com/NousResearch/hermes-agent)

> [!important] DeepMind: Securing the future of AI agents
> - 大类：博客 / Research
> - 小类：Agent Safety
> - 重点：DeepMind 把 agent 安全落到 control roadmap、实时监控和内部系统防护。
> - 为什么重要：agent 越接近生产工具链，越需要 runtime 级安全控制，而不是只靠模型对齐口号。
> - 详情：[[Industry/2026-06-19/DeepMind-Securing-Future-AI-Agents]] / [网页详情]({blob('Industry/2026-06-19/DeepMind-Securing-Future-AI-Agents')}) / [原文](https://deepmind.google/blog/securing-the-future-of-ai-agents/)

> [!tip] HF: Benchmarking open models on your own tooling
> - 大类：博客
> - 小类：Agent Eval
> - 重点：把 agentic 能力评测放到用户自己的工具链中，而不是只看封闭 leaderboard。
> - 为什么重要：这更接近真实 agent 上线验收：工具调用、上下文、失败恢复和安全边界都必须在本地环境测。
> - 详情：[[Industry/2026-06-19/HuggingFace-Agentic-Enough-Benchmarking]] / [网页详情]({blob('Industry/2026-06-19/HuggingFace-Agentic-Enough-Benchmarking')}) / [原文](https://huggingface.co/blog/is-it-agentic-enough)

## 3. 优先级矩阵

```mermaid
quadrantChart
  title 今日内容优先级：影响力 × 可落地性
  x-axis 低可落地性 --> 高可落地性
  y-axis 低影响力 --> 高影响力
  quadrant-1 立即读/试
  quadrant-2 读趋势
  quadrant-3 暂存
  quadrant-4 可工具化
  Hermes Agent: [0.90, 0.92]
  Firecrawl: [0.88, 0.86]
  DeepMind Agent Safety: [0.62, 0.88]
  HF Agent Eval: [0.78, 0.80]
  OpenAI Enterprise Analytics: [0.70, 0.74]
```

## 4. 分类清单

| 标签 | 大类 | 小类 | 标题 | 重点概括 | 为什么重要 | Obsidian 详情 | 网页详情 | 原文 |
|---|---|---|---|---|---|---|---|---|
{class_rows}

## 5. 大厂资讯 / 工程博客 / Research

### 5.1 公司来源扫描矩阵

| 公司/实验室 | 来源/栏目 | 今日状态 | 高相关条数 | 代表条目 | 备注 |
|---|---|---|---:|---|---|
{matrix_rows}

### 5.2 高相关大厂条目

| 标签 | 发布方/大厂 | 栏目/来源 | 标题 | 重点概括 | 工程/算法影响 | Obsidian 详情 | 网页详情 | 原文 |
|---|---|---|---|---|---|---|---|---|
{industry_rows}

## 6. GitHub 高 star Top 10

| 排名 | repo | stars | forks | language | updated_at | topics | 重点概括 | 是否值得试用 | Obsidian 详情 | 原文 |
|---:|---|---:|---:|---|---|---|---|---|---|---|
{chr(10).join(high_rows)}

## 7. GitHub star 增长最快 Top 10

> 使用 `Automation/state/github-stars-2026-06-18.json` 作为历史 baseline，非冷启动；GitHub API 部分 query 403，增长榜基于成功采集到的 132 个 repo。

| 排名 | repo | stars_delta | stars | forks | language | updated_at | 增长依据 | 重点概括 | Obsidian 详情 | 原文 |
|---:|---|---:|---:|---:|---|---|---|---|---|---|
{chr(10).join(growth_rows)}

## 8. 论文

### 8.1 Eval / Reasoning / Serving Watchlist

| 标签 | 论文来源 | 论文 | 作者/机构 | 重点概括 | 工程/研究价值 | Obsidian 详情 | 网页详情 | PDF/原文 |
|---|---|---|---|---|---|---|---|---|
{paper_rows}

## 9. 资讯 / 其他 GitHub 项目

### 9.1 Agent / Web Data / Workflow Infra

| 标签 | 来源 | 标题 | 重点概括 | 对我有什么用 | Obsidian 详情 | 网页详情 | 原文 |
|---|---|---|---|---|---|---|---|
| 必读 | GitHub | Firecrawl | Web search/scrape/extract API 增长 +625，直接对应 research agent 数据入口 | 可作为 crawler fallback 和网页转 markdown 方案观察 | [[GitHub/2026-06-19/firecrawl--firecrawl]] | [网页详情]({blob('GitHub/2026-06-19/firecrawl--firecrawl')}) | [原文](https://github.com/firecrawl/firecrawl) |
| 可 skim | GitHub | Dify | agentic workflow development 平台仍在高 star 榜 | 对比 workflow control plane 和企业落地模式 | [[GitHub/2026-06-19/langgenius--dify]] | [网页详情]({blob('GitHub/2026-06-19/langgenius--dify')}) | [原文](https://github.com/langgenius/dify) |

## 10. 按主题索引

### AI Infra / Serving / Training
- [[GitHub/2026-06-19/vllm-project--vllm]] - 高吞吐 LLM serving 基线项目。
- [[GitHub/2026-06-19/huggingface--transformers]] - 模型定义、训练与推理生态核心依赖。
- [[Industry/2026-06-19/OpenAI-Enterprise-Usage-Analytics-Spend-Controls]] - 企业 AI 平台成本治理信号。

### LLM / Agent / RAG / Evaluation
- [[GitHub/2026-06-19/NousResearch--hermes-agent]] - agent skills/memory/runtime 高增长。
- [[Industry/2026-06-19/DeepMind-Securing-Future-AI-Agents]] - agent runtime 安全 roadmap。
- [[Industry/2026-06-19/HuggingFace-Agentic-Enough-Benchmarking]] - 自有工具链上的 agent eval。

### RL / Game AI / World Model
- [[Papers/2026-06-19/AdaSR-Adaptive-Streaming-Reasoning-Watchlist]] - reasoning budget / streaming watchlist；今日低置信。

### 公司 / 实验室
- OpenAI: [[Industry/2026-06-19/OpenAI-Enterprise-Usage-Analytics-Spend-Controls]]
- DeepMind: [[Industry/2026-06-19/DeepMind-Securing-Future-AI-Agents]]
- Hugging Face: [[Industry/2026-06-19/HuggingFace-Agentic-Enough-Benchmarking]]
- Microsoft: [[Industry/2026-06-19/Microsoft-MagenticLite-MagenticBrain-Fara15]]

## 11. 值得后续深挖

| 标签 | 大类 | 小类 | 标题 | 后续动作 | Obsidian 详情 | 原文 |
|---|---|---|---|---|---|---|
| 后续 | 论文 | arXiv / S2 | 今日 arXiv 与 Semantic Scholar 429/timeout | 明日补抓论文元数据，避免弱相关填充 | [[Papers/2026-06-19/AdaSR-Adaptive-Streaming-Reasoning-Watchlist]] | [arXiv](https://arxiv.org/) |
| 后续 | 工程 | GitHub API | collect_github_stars.py 部分 query 403 | 可加 token/缓存/退避策略 | [[GitHub/2026-06-19/NousResearch--hermes-agent]] | [Snapshot](../Automation/state/github-stars-2026-06-19.json) |

## 12. 采集失败或低置信来源

- arXiv API：多个 query timeout / 429；未用弱相关论文补齐。
- Semantic Scholar：HTTP 429；论文 citation/related work 暂未补齐。
- GitHub Search：snapshot 已保存 132 repo，但 `topic:agents`、`topic:inference` 等后续 query 触发 403 rate limit。
- Anthropic RSS 404、Meta AI RSS 404、NVIDIA feed 未返回可用条目、Microsoft Research feed timeout；矩阵中已标注。
- 腾讯、字节、SpaceAI：本次未取到可核验 AI Infra/LLM/RL 强相关新项，标注低置信而非省略。

## 13. 归档标签

#ai-radar #daily #ai-infra #llm #rl #agent #eval
'''
write(Path(f'Daily/{DATE}.md'), daily)
print('generated daily and detail pages')
