import json
import re
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

DATE = "2026-07-13"
VAULT = Path('/home/vscode-server/obsidian-ai-radar')
GITHUB_BASE = 'https://github.com/dyt27666-oss/AI-news-report-obsidians/blob/main'
SNAP = VAULT / f'Automation/state/github-stars-{DATE}.json'
PREV = VAULT / 'Automation/state/github-stars-2026-07-12.json'

WATCHED = [
    'huggingface/transformers','anthropics/claude-code','google-gemini/gemini-cli','pytorch/pytorch','openai/codex',
    'modelcontextprotocol/servers','vllm-project/vllm','OpenHands/OpenHands','cline/cline','microsoft/autogen',
    'langchain-ai/langgraph','continuedev/continue','QwenLM/qwen-code','RooCodeInc/Roo-Code','sgl-project/sglang',
    'verl-project/verl','OpenRLHF/OpenRLHF','NVIDIA/TensorRT-LLM','deepspeedai/DeepSpeed','microsoft/semantic-kernel'
]

TOOL_REPOS = {
    'Claude Code': 'anthropics/claude-code',
    'OpenAI Codex': 'openai/codex',
    'Gemini Code Assist': 'google-gemini/gemini-cli',
    'Qwen Code': 'QwenLM/qwen-code',
    'Roo Code': 'RooCodeInc/Roo-Code',
    'Cline': 'cline/cline',
    'Continue': 'continuedev/continue',
}

COMPANIES = [
    ('OpenAI', 'News / Research', '间接扫描', 1, 'Codex repo 延续增长；官网新闻未抓到新的高相关工程项', '以 GitHub/开发者文档为代理信号'),
    ('Anthropic', 'News / Research / Engineering', '间接扫描', 1, 'Claude Code repo 延续增长；官网未确认新增高相关研究项', '以 Claude Code release/docs 与 repo 活跃度为代理信号'),
    ('Google DeepMind', 'Blog / Research', '低置信', 0, '无高相关新项', '本轮未拿到新 research/blog 元数据'),
    ('Meta AI', 'Blog / Research', '低置信', 0, '无高相关新项', '本轮未拿到新 research/blog 元数据'),
    ('NVIDIA', 'Technical Blog / AI', '间接扫描', 1, 'TensorRT-LLM watched repo 仍是 serving 重点', '官网博客未确认新文，保留 repo 信号'),
    ('Microsoft', 'Research AI', '间接扫描', 1, 'AutoGen / Semantic Kernel 仍是 agent 编排观察项', 'Microsoft Research 页面未确认新文'),
    ('Hugging Face', 'Blog / Papers / Releases', '间接扫描', 1, 'Transformers repo 高 star 且持续活跃', '以 repo / model infra 生态代理'),
    ('腾讯', 'AI Lab / 技术博客', '低置信', 0, '无高相关新项', '本轮未发现可验证 AI Infra / RL / Agent 新项'),
    ('字节', 'Seed / 技术博客', '低置信', 0, '无高相关新项', '本轮未发现可验证 AI Infra / RL / Agent 新项'),
    ('SpaceAI', 'Blog / News', '访问失败/低置信', 0, '无高相关新项', '来源有效性低，本轮未获得可验证新项'),
]

PAPERS = [
    {
        'title':'Agentic RL / post-training 论文源扫描',
        'source':'arXiv / Semantic Scholar',
        'type':'预印本索引扫描',
        'authors':'多来源；本轮 API 超时，未确认新论文',
        'url':'https://export.arxiv.org/api/query?search_query=all:reinforcement+learning+language+models',
        'pdf':'未确认',
        'topic':'RLHF / Agent Eval',
        'summary':'arXiv live query 超时，本轮不硬塞弱相关论文；保留 RLHF、GRPO、agent eval 为后续跟踪方向。',
        'value':'避免把物理/泛 ML 噪声放入日报；对 post-training 工作流更重要的是保留失败 provenance 和后续查询入口。'
    },
    {
        'title':'LLM Serving / inference 论文源扫描',
        'source':'arXiv',
        'type':'预印本索引扫描',
        'authors':'多来源；本轮 API 超时，未确认新论文',
        'url':'https://export.arxiv.org/api/query?search_query=all:large+language+model+inference',
        'pdf':'未确认',
        'topic':'Serving / AI Infra',
        'summary':'围绕 KV cache、batching、speculative decoding 的论文扫描未完成；用 vLLM/SGLang/TensorRT-LLM repo 信号替代当天工程判断。',
        'value':'对 AI Infra 工程师来说，今天更可信的信号来自 serving repo 活跃度，而不是超时的论文 API。'
    },
    {
        'title':'Rummy imperfect-information game 论文源扫描',
        'source':'arXiv / Semantic Scholar',
        'type':'预印本索引扫描',
        'authors':'多来源；本轮 API 超时，未确认新论文',
        'url':'https://export.arxiv.org/api/query?search_query=all:rummy+imperfect+information+game+AI',
        'pdf':'未确认',
        'topic':'Point Rummy / Game AI',
        'summary':'未确认新增论文；以 GitHub 上 ISMCTS、RLCard、rule engine 候选作为今天可行动线索。',
        'value':'业务上先拆规则环境、仿真与 evaluator，比追逐低置信论文更可落地。'
    }
]

BLOG_ITEMS = [
    ('OpenAI Codex watched repo growth', 'OpenAI', 'GitHub / Developer Tool', 'Codex watched repo 增长仍强，说明 CLI/TUI coding agent 仍是开发者工具主战场。', '对多 agent 编码、权限模式、远程执行和 repo 内上下文管理有直接影响。', 'GitHub/Tools/2026-07-13/openai-codex'),
    ('Claude Code watched repo growth', 'Anthropic', 'GitHub / Developer Tool', 'Claude Code 继续高 star 增长；即使官网 changelog 未确认新功能，生态热度仍值得跟踪。', '影响 tmux 多 agent 监控、代码审查、CLI 权限边界和 agent loop 设计。', 'GitHub/Tools/2026-07-13/claude-code'),
    ('TensorRT-LLM / vLLM / SGLang serving watchlist', 'NVIDIA / vLLM / SGLang', 'GitHub / AI Infra', 'GitHub Search 被限流后，使用 watched repo 直连回退观察 serving 三件套。', '可直接映射到推理吞吐、KV cache、scheduler、GPU runtime 的工程选型。', 'GitHub/AIInfra/2026-07-13/serving-watchlist'),
]

DESCS = {
 'huggingface/transformers':'模型定义与推理/训练生态底座，仍是新模型接入和 eval pipeline 的首要观察源。',
 'anthropics/claude-code':'终端内 agentic coding 工具，高增长说明 CLI agent workflow 仍在扩张。',
 'google-gemini/gemini-cli':'Gemini 终端 agent，topics 显式覆盖 MCP client/server，适合观察开放 agent 工具链。',
 'pytorch/pytorch':'训练/推理框架底层，任何 GPU/runtime 变化都会影响大模型工程。',
 'openai/codex':'Rust 终端 coding agent，高增长且与权限/远程执行/上下文策略直接相关。',
 'modelcontextprotocol/servers':'MCP server 生态入口，影响 coding agent 的工具接入标准化。',
 'vllm-project/vllm':'LLM serving 高吞吐引擎，关注 batching、KV cache、并发与硬件适配。',
 'OpenHands/OpenHands':'开源 AI coding agent 工作台，可作为 loop engineer/harness 参考。',
 'cline/cline':'IDE/CLI 自主 coding agent，适合观察 agent SDK 与 extension 工作流。',
 'microsoft/autogen':'多 agent 编程框架，适合作为 agent orchestration 和 eval loop 参考。',
 'langchain-ai/langgraph':'构建 resilient agents 的图式编排框架，适合生产 agent state machine。',
 'continuedev/continue':'开源 coding agent，适合观察 IDE/CLI 结合与模型路由。',
 'QwenLM/qwen-code':'Qwen 终端 coding agent，适合国产模型 coding workflow 观察。',
 'RooCodeInc/Roo-Code':'编辑器内 AI agent 团队式协作，适合观察多角色 coding agent。',
 'sgl-project/sglang':'高性能 LLM/VLM serving 框架，关注 attention、CUDA、MoE、RL serving。',
 'verl-project/verl':'HybridFlow RL post-training 框架，适合 GRPO/PPO/agentic RL 训练管线。',
 'OpenRLHF/OpenRLHF':'Ray + vLLM 的 RLHF/agentic RL 框架，适合可扩展 post-training。',
 'NVIDIA/TensorRT-LLM':'NVIDIA GPU 上 LLM inference runtime 和 kernel 优化核心。',
 'deepspeedai/DeepSpeed':'分布式训练/推理优化库，关注 ZeRO、pipeline/model parallel。',
 'microsoft/semantic-kernel':'LLM app/agent SDK，适合企业 agent 编排和插件化。',
}


def gh_get(repo):
    req = urllib.request.Request('https://api.github.com/repos/' + repo, headers={'User-Agent':'ai-radar-cron'})
    with urllib.request.urlopen(req, timeout=20) as resp:
        d = json.load(resp)
    return {
        'repo': repo,
        'stars': d.get('stargazers_count', 0),
        'forks': d.get('forks_count', 0),
        'language': d.get('language') or 'Unknown',
        'updated_at': d.get('updated_at'),
        'pushed_at': d.get('pushed_at'),
        'topics': d.get('topics') or [],
        'html_url': d.get('html_url'),
        'description': d.get('description') or DESCS.get(repo, ''),
        'collected_at': datetime.now(timezone.utc).isoformat(),
        'themes': ['loop_engineer'] if repo in ['OpenHands/OpenHands','anthropics/claude-code','openai/codex','cline/cline','continuedev/continue','QwenLM/qwen-code','RooCodeInc/Roo-Code','google-gemini/gemini-cli','langchain-ai/langgraph','modelcontextprotocol/servers'] else [],
    }

prev_data = json.loads(PREV.read_text())
prev_by_repo = {r['repo']: r for r in prev_data.get('repos', [])}
current = []
errors = []
for repo in WATCHED:
    try:
        item = gh_get(repo)
        prev = prev_by_repo.get(repo, {})
        item['stars_delta'] = item['stars'] - prev.get('stars', item['stars']) if prev else None
        item['growth_basis'] = 'direct watched repo fallback vs 2026-07-12 daily value; 非完整全网日增' if prev else 'direct watched repo fallback; no baseline for this repo'
        current.append(item)
    except Exception as e:
        errors.append({'repo': repo, 'error': str(e)})
        if repo in prev_by_repo:
            item = dict(prev_by_repo[repo])
            item['fallback_from'] = 'github-stars-2026-07-12.json'
            item['growth_basis'] = 'rate-limit fallback from previous snapshot; not fresh'
            current.append(item)

# Merge current direct fallback into today's snapshot while preserving point-rummy search results.
snap = json.loads(SNAP.read_text())
point = [r for r in snap.get('repos', []) if 'point_rummy' in r.get('themes', [])]
merged_by_repo = {r['repo']: r for r in current}
for r in point:
    merged_by_repo.setdefault(r['repo'], r)
merged = list(merged_by_repo.values())
high = sorted(current, key=lambda r: r.get('stars') or 0, reverse=True)[:10]
growth = sorted(current, key=lambda r: (r.get('stars_delta') is not None, r.get('stars_delta') or -1), reverse=True)[:10]
loop_high = sorted([r for r in current if 'loop_engineer' in r.get('themes', [])], key=lambda r: r.get('stars') or 0, reverse=True)[:10]
loop_growth = sorted([r for r in current if 'loop_engineer' in r.get('themes', [])], key=lambda r: (r.get('stars_delta') is not None, r.get('stars_delta') or -1), reverse=True)[:10]
point_high = sorted(point, key=lambda r: r.get('stars') or 0, reverse=True)[:10]
point_growth = sorted(point, key=lambda r: r.get('updated_at') or '', reverse=True)[:10]

snap['repos'] = merged
snap['high_star_top10'] = high
snap['growth_top10'] = growth
snap['loop_engineer_high_star_top10'] = loop_high
snap['loop_engineer_growth_top10'] = loop_growth
snap['fallback_note'] = 'GitHub Search partially rate-limited after Point Rummy results; broad AI/Loop tables use direct watched repo fallback, not complete all-GitHub ranking.'
snap['direct_fallback_errors'] = errors
SNAP.write_text(json.dumps(snap, ensure_ascii=False, indent=2) + '\n')


def safe_name(repo):
    return repo.replace('/', '__').replace('-', '-').replace('.', '_')

def wiki(path_no_ext):
    return f'[[{path_no_ext}]]'

def blob(path_no_ext):
    return f'{GITHUB_BASE}/{path_no_ext}.md'

def md_link(text, url):
    return f'[{text}]({url})'

def topics_str(r):
    return ', '.join(r.get('topics') or [])[:100] or '无'

def detail_page(path_no_ext, title, kind, source_name, source_type, source_url, summary, impact, mechanisms=None):
    mechanisms = mechanisms or ['源信号', '工程机制', '落地动作']
    content = f"""# {title}

> 类型：{kind}
> 大类：AI Radar 详情
> 小类：{source_type}
> 推荐等级：可 skim
> 创建日期：{DATE}
> 原文链接：{source_url}
> 网页详情：{blob(path_no_ext)}
> 返回日报：[[Daily/{DATE}]]

## 一句话结论

{summary}

## TL;DR

- **它是什么**：{source_name} 的今日雷达条目。
- **为什么重要**：{impact}
- **和我相关的点**：用于 AI Infra / LLM serving / agent loop / RL 训练判断。
- **建议动作**：先读摘要和原文，再按表格里的机制决定是否试用或复现。

## 元信息

| 字段 | 内容 |
|---|---|
| 发布方/来源 | {source_name} |
| 栏目/来源类型 | {source_type} |
| 发布时间 | {DATE} |
| 原文 | [原文]({source_url}) |
| 代码 | {source_url if 'github.com' in source_url else '未发现'} |
| PDF | 未发现 |
| 标签 | #ai-radar |

## 信息压缩图示

```mermaid
flowchart TB
  subgraph Source[来源信号]
    S1[{source_name}]
    S2[{source_type}]
    S3[原文/仓库元数据]
  end
  subgraph Mechanism[机制拆解]
    M1[{mechanisms[0]}]
    M2[{mechanisms[1]}]
    M3[{mechanisms[2]}]
  end
  subgraph Impact[工程影响]
    I1[AI Infra/Serving]
    I2[Agent/Coding Loop]
    I3[RL/Post-training]
    I4[风险: 低置信或需验证]
  end
  subgraph Action[我的动作]
    A1[阅读原文]
    A2[加入 watchlist]
    A3[小规模试用/复现]
  end
  S1 --> S2 --> S3
  S3 --> M1 --> I1
  S3 --> M2 --> I2
  S3 --> M3 --> I3
  I1 --> A1
  I2 --> A2
  I3 --> A3
  S3 --> I4 --> A2
  classDef source fill:#e1d5e7,stroke:#9673a6,stroke-width:2px,color:#111;
  classDef mech fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px,color:#111;
  classDef impact fill:#d5e8d4,stroke:#82b366,stroke-width:2px,color:#111;
  classDef risk fill:#f8cecc,stroke:#b85450,stroke-width:2px,color:#111;
  class S1,S2,S3 source;
  class M1,M2,M3 mech;
  class I1,I2,I3,A1,A2,A3 impact;
  class I4 risk;
```

### 辅助图：影响力 x 可落地性

```mermaid
quadrantChart
  title 今日条目优先级
  x-axis 低可落地性 --> 高可落地性
  y-axis 低影响力 --> 高影响力
  当前条目: [0.72, 0.78]
```

## 专业解读

{summary} {impact} 需要注意：本条目来自自动化雷达采集，若标注为 fallback 或间接扫描，则不能当作完整全网排名，只能当作 watched-source 信号。

## 通俗解释

可以把它理解成今天雷达里的一个“灯塔”：它不一定代表全网唯一最热，但对用户关注的 AI Infra、LLM 工程、Agent/Coding Workflow 或 RL/Game AI 有明确可行动价值。

## 关键机制拆解

| 机制 | 解决的问题 | 为什么有效 | 可能的坑 |
|---|---|---|---|
| {mechanisms[0]} | 找到高信号来源 | 保留原文与元数据 | 可能受 API 限流影响 |
| {mechanisms[1]} | 映射到工程问题 | 对齐 serving/agent/RL 关注点 | 需要二次验证 |
| {mechanisms[2]} | 形成行动建议 | 可进入试用/复现/watchlist | 不等于生产就绪 |

## 对我的影响

| 维度 | 影响 | 建议动作 |
|---|---|---|
| AI Infra | 影响 serving、runtime、训练或工具链判断 | 看原文和 repo 活跃度 |
| LLM 工程 | 影响模型接入、上下文、推理或 agent loop | 加入 watchlist |
| RL / Game AI | 若相关，映射到环境、reward、evaluator | 只保留强相关候选 |
| Agent / Eval | 关注工具调用、MCP、评测闭环 | 小规模试用 |

## 可信度与局限性

- 证据强度：中；来自公开来源或 fallback snapshot。
- 局限性：今日 GitHub Search 有 403 限流，部分榜单使用 watched repo direct fallback。
- 还需要确认：是否有正式 release note、benchmark 或论文细节。

## 我应该如何跟进

1. 打开原文确认 release / README / paper 是否有实质更新。
2. 若和当前工作栈相关，记录最小复现实验。
3. 对低置信来源只加入观察，不进入生产决策。

## 相关链接

- 原文：{source_url}
- 网页详情：{blob(path_no_ext)}
- 返回日报：[[Daily/{DATE}]]

## 标签

#ai-radar #{kind.replace(' ', '-')}
"""
    out = VAULT / f'{path_no_ext}.md'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(content)

# Detail pages for broad repos, loop, tools, point-rummy, papers/company items.
for r in high + growth + loop_high + point_high[:8]:
    path = 'GitHub/AIInfra/2026-07-13/' + safe_name(r['repo'])
    if 'point_rummy' in r.get('themes', []):
        path = 'GitHub/PointRummy/2026-07-13/' + safe_name(r['repo'])
    elif 'loop_engineer' in r.get('themes', []):
        path = 'GitHub/LoopEngineer/2026-07-13/' + safe_name(r['repo'])
    detail_page(path, r['repo'], 'GitHub', r['repo'], 'GitHub repo / watched fallback', r['html_url'], DESCS.get(r['repo'], r.get('description') or ''), '该 repo 对今日 AI Infra / coding agent / RL radar 有可行动观察价值。', ['repo 元数据', 'stars / update 信号', '试用决策'])

for title, company, stype, summary, impact, path in BLOG_ITEMS:
    detail_page(path, title, 'Industry', company, stype, 'https://github.com/' + ('openai/codex' if 'Codex' in title else 'anthropics/claude-code' if 'Claude' in title else 'vllm-project/vllm'), summary, impact, ['公告/仓库信号', '工程趋势', '行动建议'])

for p in PAPERS:
    path = 'Papers/Watchlist/2026-07-13/' + re.sub(r'[^a-zA-Z0-9]+', '-', p['title']).strip('-').lower()
    detail_page(path, p['title'], 'Paper', p['source'], p['type'], p['url'], p['summary'], p['value'], ['论文源扫描', '相关性过滤', '后续查询'])
    p['path'] = path

# Build tables.
def repo_row(i, r, path_prefix='GitHub/AIInfra/2026-07-13'):
    path = f'{path_prefix}/{safe_name(r["repo"])}'
    return f"| {i} | `{r['repo']}` | {r.get('stars',0)} | {r.get('forks',0)} | {r.get('language','Unknown')} | {r.get('updated_at','')} | {topics_str(r)} | {DESCS.get(r['repo'], (r.get('description') or '')[:80])} | 值得 skim/按需试用 | {wiki(path)} | {md_link('GitHub', r['html_url'])} |"

def growth_row(i, r, path_prefix='GitHub/AIInfra/2026-07-13'):
    path = f'{path_prefix}/{safe_name(r["repo"])}'
    delta = r.get('stars_delta')
    delta_s = '未知' if delta is None else str(delta)
    return f"| {i} | `{r['repo']}` | {delta_s} | {r.get('stars',0)} | {r.get('forks',0)} | {r.get('language','Unknown')} | {r.get('updated_at','')} | {r.get('growth_basis','direct fallback')} | {DESCS.get(r['repo'], (r.get('description') or '')[:80])} | {wiki(path)} | {md_link('GitHub', r['html_url'])} |"

high_rows = '\n'.join(repo_row(i,r) for i,r in enumerate(high,1))
growth_rows = '\n'.join(growth_row(i,r) for i,r in enumerate(growth,1))
loop_high_rows = '\n'.join(repo_row(i,r,'GitHub/LoopEngineer/2026-07-13') for i,r in enumerate(loop_high,1))
loop_growth_rows = '\n'.join(growth_row(i,r,'GitHub/LoopEngineer/2026-07-13') for i,r in enumerate(loop_growth,1))
point_rows = '\n'.join(repo_row(i,r,'GitHub/PointRummy/2026-07-13') for i,r in enumerate(point_high[:10],1))
point_paper_rows = '\n'.join(f"| 低置信 | {p['source']} / {p['type']} | {p['title']} | {p['authors']} | {p['summary']} | {p['value']} | {wiki(p['path'])} | {md_link('原文', p['url'])} |" for p in PAPERS if 'Rummy' in p['title']) or '| 低置信 | arXiv / Semantic Scholar | Rummy 论文 API 超时 | 多来源 | 未确认新增论文 | 今日以 GitHub 规则/仿真候选为主 | - | [查询](https://export.arxiv.org/) |'
company_rows = '\n'.join(f"| {c} | {src} | {status} | {cnt} | {item} | {note} |" for c,src,status,cnt,item,note in COMPANIES)
blog_rows = '\n'.join(f"| 可 skim | {company} | {stype} | {title} | {summary} | {impact} | {wiki(path)} | {md_link('网页详情', blob(path))} | {md_link('原文', 'https://github.com/' + ('openai/codex' if 'Codex' in title else 'anthropics/claude-code' if 'Claude' in title else 'vllm-project/vllm'))} |" for title,company,stype,summary,impact,path in BLOG_ITEMS)

coding_rows = []
for tool in ['Claude Code','OpenAI Codex','Cursor','Windsurf','GitHub Copilot','Gemini Code Assist','Qwen Code','Roo Code','Cline','Continue']:
    repo = TOOL_REPOS.get(tool)
    if repo and repo in {r['repo'] for r in current}:
        r = next(x for x in current if x['repo']==repo)
        update = f"watched repo stars_delta={r.get('stars_delta')}；非完整全网日增"
        impact = '影响 CLI/TUI、agent loop、MCP 或 IDE coding workflow，建议持续观察。'
        url = r['html_url']
        status = '间接扫描/有 repo 信号'
    else:
        update = '无高相关新项或官网未确认新增 release'
        impact = '暂不调整工作流；保留扫描矩阵避免漏扫。'
        url = {'Cursor':'https://cursor.com/changelog','Windsurf':'https://windsurf.com/changelog','GitHub Copilot':'https://github.blog/changelog/label/copilot/'}.get(tool, 'https://github.com/')
        status = '低置信/无高相关新项'
    vendor = {'Claude Code':'Anthropic','OpenAI Codex':'OpenAI','Cursor':'Cursor','Windsurf':'Windsurf','GitHub Copilot':'GitHub','Gemini Code Assist':'Google','Qwen Code':'Alibaba/Qwen','Roo Code':'Roo Code','Cline':'Cline','Continue':'Continue'}[tool]
    stype = 'GitHub Releases / Changelog / Docs'
    coding_rows.append(f"| {tool} | {vendor} | {stype} | {status} | {update} | {impact} | {md_link('原文', url)} |")
coding_rows = '\n'.join(coding_rows)

tool_update_rows = '\n'.join([
    f"| 必读 | OpenAI Codex | GitHub / Docs | Codex watched repo 增长 | stars_delta={next(r for r in current if r['repo']=='openai/codex').get('stars_delta')}，说明终端 coding agent 继续强势 | 适合跟踪权限模式、远程执行和上下文窗口策略 | {wiki('GitHub/Tools/2026-07-13/openai-codex')} | {md_link('网页详情', blob('GitHub/Tools/2026-07-13/openai-codex'))} | {md_link('原文','https://github.com/openai/codex')} |",
    f"| 必读 | Claude Code | GitHub / Docs | Claude Code watched repo 增长 | stars_delta={next(r for r in current if r['repo']=='anthropics/claude-code').get('stars_delta')}，继续验证 CLI agent workflow 热度 | 适合多 agent 监控、代码审查与工具权限设计 | {wiki('GitHub/Tools/2026-07-13/claude-code')} | {md_link('网页详情', blob('GitHub/Tools/2026-07-13/claude-code'))} | {md_link('原文','https://github.com/anthropics/claude-code')} |",
])

paper_rows = '\n'.join(f"| 低置信 | {p['source']} / {p['type']} | {p['title']} | {p['authors']} | {p['summary']} | {p['value']} | {wiki(p['path'])} | {md_link('网页详情', blob(p['path']))} | {md_link('原文', p['url'])} |" for p in PAPERS)

classification_rows = '\n'.join([
    f"| 必读 | GitHub | Coding Agent | OpenAI Codex | Direct watched repo stars_delta={next(r for r in current if r['repo']=='openai/codex').get('stars_delta')}，不是完整全网增长 | Codex 与 CLI 权限/远程执行/上下文策略直接相关 | {wiki('GitHub/Tools/2026-07-13/openai-codex')} | {md_link('网页详情', blob('GitHub/Tools/2026-07-13/openai-codex'))} | {md_link('原文','https://github.com/openai/codex')} |",
    f"| 必读 | GitHub | Coding Agent | Claude Code | Direct watched repo stars_delta={next(r for r in current if r['repo']=='anthropics/claude-code').get('stars_delta')}，生态热度继续 | 影响多 agent 编码、代码审查、TUI/CLI agent loop | {wiki('GitHub/Tools/2026-07-13/claude-code')} | {md_link('网页详情', blob('GitHub/Tools/2026-07-13/claude-code'))} | {md_link('原文','https://github.com/anthropics/claude-code')} |",
    f"| 必读 | GitHub | Serving | vLLM / SGLang / TensorRT-LLM | GitHub Search 限流后使用 watched repo 回退 | 对 LLM serving 选型仍是当天最高可信工程信号 | {wiki('GitHub/AIInfra/2026-07-13/serving-watchlist')} | {md_link('网页详情', blob('GitHub/AIInfra/2026-07-13/serving-watchlist'))} | {md_link('原文','https://github.com/vllm-project/vllm')} |",
    f"| 可 skim | GitHub | Point Rummy | rummy-ai / gin-rummy-ai | 小型 repo 但主题强相关，适合规则/ISMCTS/RL 环境借鉴 | 对 Point Rummy 业务的规则引擎、bot 策略和 evaluator 有用 | {wiki('GitHub/PointRummy/2026-07-13/nakkekakke__rummy-ai')} | {md_link('网页详情', blob('GitHub/PointRummy/2026-07-13/nakkekakke__rummy-ai'))} | {md_link('原文','https://github.com/nakkekakke/rummy-ai')} |",
])

daily = f"""# AI Radar Daily - {DATE}

> 生成时间：2026-07-13 09:00 北京时间
> 范围：AI Infra / LLM / RL / Game AI / 大厂博客 / 论文 / GitHub / 行业资讯
> 说明：日报是总览导航页，不是全部正文。Obsidian 中点 `[[详情页]]`，Telegram/GitHub 中点“网页详情”。

## 0. 今日结论

- 今日最值得关注：GitHub Search 在 Point Rummy 后被 403 限流，因此通用 AI Infra / Loop Engineer 榜单采用 direct watched repo fallback；不要把它当完整全网排名。
- 对 AI Infra 的直接影响：vLLM、SGLang、TensorRT-LLM、Transformers、PyTorch 仍是 today watchlist，适合继续围绕 serving/runtime/KV cache 做选型观察。
- 对 LLM 训练 / 推理 / Agent 的影响：Codex、Claude Code、Gemini CLI、Cline、Continue、Qwen Code 的 repo 信号说明 CLI/TUI + IDE agent workflow 仍是高热区。
- 对 RL / 游戏模型训练的影响：Point Rummy 搜到 86 个主题 repo，质量偏小但包含 ISMCTS、RLCard、规则引擎、AI opponent，可用于业务拆解。
- 建议今天深读：Codex / Claude Code 增长信号、serving watched repo、nakkekakke/rummy-ai 的 ISMCTS 思路。

## 1. 今日态势图

```mermaid
flowchart LR
  subgraph Sources[今日来源]
    GH[GitHub Search: Point Rummy 成功]
    FB[Direct watched repo fallback]
    AX[arXiv: timeout/低置信]
    CO[公司/工具源: 间接扫描]
  end
  subgraph Themes[主题聚类]
    T1[Serving / Infra]
    T2[Coding Agent Loop]
    T3[Point Rummy / Game AI]
    T4[Research Watchlist]
  end
  subgraph Actions[我的动作]
    A1[读 Codex / Claude Code]
    A2[观察 vLLM/SGLang/TRT-LLM]
    A3[提炼 Rummy 环境/规则/eval]
    A4[记录 API 失败 provenance]
  end
  GH --> T3 --> A3
  FB --> T1 --> A2
  FB --> T2 --> A1
  AX --> T4 --> A4
  CO --> T2
  classDef source fill:#e1d5e7,stroke:#9673a6,stroke-width:2px;
  classDef theme fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef action fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  class GH,FB,AX,CO source;
  class T1,T2,T3,T4 theme;
  class A1,A2,A3,A4 action;
```

## 2. 必读卡片区

> [!important] OpenAI Codex watched repo 继续增长
> - 大类：GitHub / Coding 工具
> - 小类：Coding Agent / CLI
> - 重点：direct fallback 显示 Codex stars_delta={next(r for r in current if r['repo']=='openai/codex').get('stars_delta')}，注意这是 watched repo 非完整全网日增。
> - 为什么重要：Codex 代表终端 coding agent 的权限、远程执行、上下文窗口、CLI/TUI 工作流方向。
> - 详情：[[GitHub/Tools/2026-07-13/openai-codex]] / [网页详情]({blob('GitHub/Tools/2026-07-13/openai-codex')}) / [原文](https://github.com/openai/codex)

> [!tip] Claude Code watched repo 继续增长
> - 大类：GitHub / Coding 工具
> - 小类：Agentic coding
> - 重点：direct fallback 显示 Claude Code stars_delta={next(r for r in current if r['repo']=='anthropics/claude-code').get('stars_delta')}。
> - 为什么重要：对 tmux 多 agent、代码审查、工具权限边界和 agent loop 监控有直接参考价值。
> - 详情：[[GitHub/Tools/2026-07-13/claude-code]] / [网页详情]({blob('GitHub/Tools/2026-07-13/claude-code')}) / [原文](https://github.com/anthropics/claude-code)

> [!note] Point Rummy 小型 repo 候选可用于业务拆解
> - 大类：GitHub / 业务主题
> - 小类：Rummy AI / ISMCTS / RL
> - 重点：nakkekakke/rummy-ai、rickgorman/gin-rummy-ai 等不大，但主题强相关。
> - 为什么重要：可抽取规则环境、MCTS/ISMCTS、bot 策略和 evaluator 设计。
> - 详情：[[GitHub/PointRummy/2026-07-13/nakkekakke__rummy-ai]] / [网页详情]({blob('GitHub/PointRummy/2026-07-13/nakkekakke__rummy-ai')}) / [原文](https://github.com/nakkekakke/rummy-ai)

## 3. 优先级矩阵

```mermaid
quadrantChart
  title 今日内容优先级：影响力 x 可落地性
  x-axis 低可落地性 --> 高可落地性
  y-axis 低影响力 --> 高影响力
  Codex/Claude Code: [0.88, 0.86]
  Serving watchlist: [0.80, 0.82]
  Rummy ISMCTS/RL repos: [0.68, 0.70]
  arXiv timeout watchlist: [0.25, 0.45]
```

## 4. 分类清单

| 标签 | 大类 | 小类 | 标题 | 重点概括 | 为什么重要 | Obsidian 详情 | 网页详情 | 原文 |
|---|---|---|---|---|---|---|---|---|
{classification_rows}

## 5. 大厂资讯 / 工程博客 / Research

### 5.1 公司来源扫描矩阵

| 公司/实验室 | 来源/栏目 | 今日状态 | 高相关条数 | 代表条目 | 备注 |
|---|---|---|---:|---|---|
{company_rows}

### 5.2 高相关大厂条目

| 标签 | 发布方/大厂 | 栏目/来源 | 标题 | 重点概括 | 工程/算法影响 | Obsidian 详情 | 网页详情 | 原文 |
|---|---|---|---|---|---|---|---|---|
{blog_rows}

## 6. GitHub 高 star Top 10

> 说明：今日 GitHub Search 部分 403；此表使用 direct watched repo fallback，不是完整全网 Top 10，但每项都与 AI Infra / LLM / Agent / RL 强相关。

| 排名 | repo | stars | forks | language | updated_at | topics | 重点概括 | 是否值得试用 | Obsidian 详情 | 原文 |
|---:|---|---:|---:|---|---|---|---|---|---|---|
{high_rows}

## 7. GitHub star 增长最快 Top 10

> 说明：使用 2026-07-12 snapshot baseline 计算 watched repo stars_delta；这是“非完整全网日增”，不是冷启动代理。

| 排名 | repo | stars_delta | stars | forks | language | updated_at | 增长依据 | 重点概括 | Obsidian 详情 | 原文 |
|---:|---|---:|---:|---:|---|---|---|---|---|---|
{growth_rows}

## 8. Coding 工具 / AI 工具功能更新

### 8.1 Coding 工具扫描矩阵

| 工具 | 厂商 | 来源类型 | 今日状态 | 代表更新 | 对我的影响 | 原文 |
|---|---|---|---|---|---|---|
{coding_rows}

### 8.2 高相关工具更新

| 标签 | 工具/厂商 | 来源类型 | 标题/功能 | 重点概括 | 对 AI coding 工作流的影响 | Obsidian 详情 | 网页详情 | 原文 |
|---|---|---|---|---|---|---|---|---|
{tool_update_rows}

## 9. Point Rummy / Indian Rummy 业务主题

### 9.1 GitHub 候选

| 排名 | repo | stars | forks | language | updated_at | topics | 重点概括 | 是否值得试用 | Obsidian 详情 | 原文 |
|---:|---|---:|---:|---|---|---|---|---|---|---|
{point_rows}

### 9.2 论文 / 资料候选

| 标签 | 来源 | 标题 | 作者/机构 | 重点概括 | 对 Point Rummy 业务有什么用 | Obsidian 详情 | 原文 |
|---|---|---|---|---|---|---|---|
{point_paper_rows}

### 9.3 业务可用性判断

| 方向 | 今日信号 | 可用性 | 下一步 |
|---|---|---|---|
| 规则引擎 / 计分 | mudont/indian-rummy、RummyServer、若干 scoreboard repo | 中：可抽规则对象、计分和房间模型 | 提取 13-card Indian Rummy 状态机和积分规则 |
| Bot / RL Agent | rummy-ai、gin-rummy-ai、IndianRummyRLCard、RummyGym | 中低：repo 小但主题强相关 | 先复现 ISMCTS / DQN 环境接口，不直接用生产代码 |
| 仿真 / 评测 | gym/RL lab/AI opponent repo | 中：适合搭 evaluator 和 rollout harness | 定义 observation/action/reward，接入并行 self-play |

## 10. Loop Engineer / Loop Engineering 主题

### 10.1 Loop Engineer GitHub 高 star Top 10

| 排名 | repo | stars | forks | language | updated_at | topics | 重点概括 | 是否值得试用 | Obsidian 详情 | 原文 |
|---:|---|---:|---:|---|---|---|---|---|---|---|
{loop_high_rows}

### 10.2 Loop Engineer GitHub star 增长最快 Top 10

| 排名 | repo | stars_delta | stars | forks | language | updated_at | 增长依据 | 重点概括 | Obsidian 详情 | 原文 |
|---:|---|---:|---:|---:|---|---|---|---|---|---|
{loop_growth_rows}

### 10.3 Loop Engineering 方法信号

| 标签 | 来源 | 标题 | 重点概括 | 对 AI coding 工作流的影响 | Obsidian 详情 | 原文 |
|---|---|---|---|---|---|---|
| 必读 | GitHub watched fallback | Codex / Claude Code / Gemini CLI / Cline | 今天 Loop Engineer 榜单不依赖 GitHub Search，而使用固定 watched repo，避免被 Point Rummy 主题偏置 | 适合设计 AGENTS.md、权限模式、eval loop、multi-agent orchestration | [[GitHub/LoopEngineer/2026-07-13/openai__codex]] | [原文](https://github.com/openai/codex) |

## 11. 论文

### 11.1 Research watchlist / API timeout

| 标签 | 论文来源 | 论文 | 作者/机构 | 重点概括 | 工程/研究价值 | Obsidian 详情 | 网页详情 | PDF/原文 |
|---|---|---|---|---|---|---|---|---|
{paper_rows}

## 12. 资讯 / 其他 GitHub 项目

### 12.1 Serving / Agent / MCP 观察

| 标签 | 来源 | 标题 | 重点概括 | 对我有什么用 | Obsidian 详情 | 网页详情 | 原文 |
|---|---|---|---|---|---|---|---|
| 可 skim | GitHub | Model Context Protocol servers | MCP server 生态是 agent tool-use 标准化入口 | 对 coding agent 接工具、权限边界、可观测性有长期价值 | [[GitHub/AIInfra/2026-07-13/modelcontextprotocol__servers]] | [网页详情]({blob('GitHub/AIInfra/2026-07-13/modelcontextprotocol__servers')}) | [原文](https://github.com/modelcontextprotocol/servers) |
| 可 skim | GitHub | LangGraph | 图式 agent state machine 仍是生产 agent 的重要抽象 | 可用于 coding-agent loop、eval loop 和工具调用恢复 | [[GitHub/LoopEngineer/2026-07-13/langchain-ai__langgraph]] | [网页详情]({blob('GitHub/LoopEngineer/2026-07-13/langchain-ai__langgraph')}) | [原文](https://github.com/langchain-ai/langgraph) |

## 13. 按主题索引

### AI Infra / Serving / Training

- [[GitHub/AIInfra/2026-07-13/vllm-project__vllm]] - LLM serving 引擎观察。
- [[GitHub/AIInfra/2026-07-13/sgl-project__sglang]] - 高性能 serving / VLM / RL serving 观察。
- [[GitHub/AIInfra/2026-07-13/NVIDIA__TensorRT-LLM]] - NVIDIA GPU inference runtime 观察。

### LLM / Agent / RAG / Evaluation

- [[GitHub/LoopEngineer/2026-07-13/openai__codex]] - CLI coding agent 增长信号。
- [[GitHub/LoopEngineer/2026-07-13/anthropics__claude-code]] - Claude Code agent workflow 观察。
- [[GitHub/AIInfra/2026-07-13/modelcontextprotocol__servers]] - MCP tool-use 生态入口。

### RL / Game AI / World Model

- [[GitHub/AIInfra/2026-07-13/verl-project__verl]] - RL post-training 框架观察。
- [[GitHub/AIInfra/2026-07-13/OpenRLHF__OpenRLHF]] - Ray/vLLM RLHF 框架观察。

### Point Rummy / Indian Rummy

- [[GitHub/PointRummy/2026-07-13/nakkekakke__rummy-ai]] - ISMCTS Rummy AI，可拆 bot 策略。
- [[GitHub/PointRummy/2026-07-13/rickgorman__gin-rummy-ai]] - neuroevolution Gin Rummy AI 参考。

### Loop Engineer / Coding Agent Loop

- [[GitHub/LoopEngineer/2026-07-13/OpenHands__OpenHands]] - agent workspace / harness 参考。
- [[GitHub/LoopEngineer/2026-07-13/cline__cline]] - IDE/CLI autonomous coding agent 参考。
- [[GitHub/LoopEngineer/2026-07-13/continuedev__continue]] - open-source coding agent 参考。

### 公司 / 实验室

- OpenAI: [[GitHub/Tools/2026-07-13/openai-codex]]
- Anthropic: [[GitHub/Tools/2026-07-13/claude-code]]
- NVIDIA: [[GitHub/AIInfra/2026-07-13/NVIDIA__TensorRT-LLM]]
- Hugging Face: [[GitHub/AIInfra/2026-07-13/huggingface__transformers]]
- Microsoft: [[GitHub/AIInfra/2026-07-13/microsoft__autogen]]

## 14. 值得后续深挖

| 标签 | 大类 | 小类 | 标题 | 后续动作 | Obsidian 详情 | 原文 |
|---|---|---|---|---|---|---|
| 后续 | GitHub | Point Rummy | rummy-ai / RummyGym / IndianRummyRLCard | 建一个最小 gym-like environment + evaluator 复现计划 | [[GitHub/PointRummy/2026-07-13/nakkekakke__rummy-ai]] | [原文](https://github.com/nakkekakke/rummy-ai) |
| 后续 | Tool | Coding Agent | Codex / Claude Code 权限模式 | 后续专门扫 release notes / docs，确认是否有权限、远程执行、上下文窗口变化 | [[GitHub/Tools/2026-07-13/openai-codex]] | [原文](https://github.com/openai/codex) |

## 15. 采集失败或低置信来源

- GitHub Search：Point Rummy 前半成功，随后大量 403 rate limit；通用 GitHub / Loop Engineer 表已标注 direct watched repo fallback。
- arXiv：live query timeout；论文区只保留 watchlist 和 provenance，不硬塞弱相关论文。
- 公司官网/博客：本轮多为间接扫描或低置信，矩阵中逐项保留状态。
- 今日 snapshot：`Automation/state/github-stars-{DATE}.json` 已保存，包含 Point Rummy search 结果和 broad watched fallback。

## 16. 归档标签

#ai-radar #daily #ai-infra #llm #rl #point-rummy #loop-engineering
"""

out = VAULT / f'Daily/{DATE}.md'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(daily)
print(json.dumps({'daily': str(out), 'files_written': 'daily + detail pages + snapshot', 'high': len(high), 'growth': len(growth), 'point': len(point_high), 'loop': len(loop_high)}, ensure_ascii=False))
