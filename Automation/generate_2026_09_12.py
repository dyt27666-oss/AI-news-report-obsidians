#!/usr/bin/env python3
from __future__ import annotations
import json, os, re, time, urllib.request, urllib.parse, xml.etree.ElementTree as ET, subprocess
from datetime import datetime
from pathlib import Path

DATE='2026-09-12'
VAULT=Path('/home/vscode-server/obsidian-ai-radar')
STATE=VAULT/'Automation/state'/f'github-stars-{DATE}.json'
BASE='https://github.com/dyt27666-oss/AI-news-report-obsidians/blob/main'
UA={'User-Agent':'ai-radar-cron/2026-09-12'}

DIRECT_REPOS=[
 'vllm-project/vllm','sgl-project/sglang','NVIDIA/TensorRT-LLM','huggingface/transformers','pytorch/pytorch','microsoft/DeepSpeed','NVIDIA/Megatron-LM','volcengine/verl','OpenRLHF/OpenRLHF','modelcontextprotocol/servers','langchain-ai/langgraph','microsoft/autogen','crewAIInc/crewAI','All-Hands-AI/OpenHands','Aider-AI/aider','openai/codex','google-gemini/gemini-cli','cline/cline','RooCodeInc/Roo-Code','continuedev/continue','QwenLM/qwen-code'
]
LOOP_REPOS=['All-Hands-AI/OpenHands','Aider-AI/aider','openai/codex','google-gemini/gemini-cli','cline/cline','RooCodeInc/Roo-Code','continuedev/continue','QwenLM/qwen-code','microsoft/autogen','crewAIInc/crewAI','langchain-ai/langgraph']
TOOL_REPOS={'OpenAI Codex':'openai/codex','Gemini Code Assist':'google-gemini/gemini-cli','Qwen Code':'QwenLM/qwen-code','Roo Code':'RooCodeInc/Roo-Code','Cline':'cline/cline','Continue':'continuedev/continue'}

def fetch_json(url):
    req=urllib.request.Request(url,headers=UA)
    with urllib.request.urlopen(req,timeout=25) as r:
        return json.loads(r.read().decode())

def get_repo(full):
    try:
        r=fetch_json(f'https://api.github.com/repos/{full}')
        return {'repo':r['full_name'],'stars':r.get('stargazers_count',0),'forks':r.get('forks_count',0),'language':r.get('language') or 'Unknown','updated_at':r.get('updated_at'),'pushed_at':r.get('pushed_at'),'topics':r.get('topics') or [],'html_url':r.get('html_url'),'description':r.get('description') or '', 'source':'direct /repos fallback'}
    except Exception as e:
        return {'repo':full,'stars':0,'forks':0,'language':'Unknown','updated_at':'访问失败','pushed_at':'访问失败','topics':[],'html_url':f'https://github.com/{full}','description':f'GitHub direct API failed: {e}','source':'direct failed'}

def last_release(full):
    try:
        rel=fetch_json(f'https://api.github.com/repos/{full}/releases/latest')
        return {'tag':rel.get('tag_name') or rel.get('name') or 'latest','name':rel.get('name') or rel.get('tag_name') or 'Release','published_at':rel.get('published_at') or rel.get('created_at') or 'unknown','url':rel.get('html_url') or f'https://github.com/{full}/releases','body':(rel.get('body') or '')[:220]}
    except Exception:
        return {'tag':'未获取','name':'未获取最新 release','published_at':'低置信/访问失败','url':f'https://github.com/{full}/releases','body':'GitHub release endpoint 访问失败或该项目未使用 GitHub Releases。'}

def arxiv_search(q, max_results=4):
    url='https://export.arxiv.org/api/query?'+urllib.parse.urlencode({'search_query':q,'sortBy':'submittedDate','sortOrder':'descending','max_results':max_results})
    try:
        req=urllib.request.Request(url,headers=UA)
        with urllib.request.urlopen(req,timeout=35) as r:
            root=ET.fromstring(r.read())
        ns={'a':'http://www.w3.org/2005/Atom'}
        out=[]
        for e in root.findall('a:entry',ns):
            aid=e.find('a:id',ns).text.split('/abs/')[-1]
            title=' '.join(e.find('a:title',ns).text.split())
            summ=' '.join(e.find('a:summary',ns).text.split())
            authors=', '.join(a.find('a:name',ns).text for a in e.findall('a:author',ns)[:4])
            pub=e.find('a:published',ns).text[:10]
            cats=', '.join(c.get('term') for c in e.findall('a:category',ns))
            out.append({'id':aid,'title':title,'summary':summ,'authors':authors,'published':pub,'cats':cats,'abs':f'https://arxiv.org/abs/{aid}','pdf':f'https://arxiv.org/pdf/{aid}'})
        return out
    except Exception as e:
        return [{'id':'low-confidence','title':f'arXiv 查询失败：{q}','summary':str(e),'authors':'未获取','published':'低置信','cats':'','abs':'https://arxiv.org','pdf':'https://arxiv.org'}]

def safe_slug(s):
    return re.sub(r'[^A-Za-z0-9._-]+','-',s).strip('-').lower()[:90]

def note_link(path): return str(path.with_suffix('')).replace('\\','/')
def blob(path): return f'{BASE}/{urllib.parse.quote(str(path), safe="/")}'
def md_table_escape(s): return str(s).replace('|','/').replace('\n',' ')

def repo_row(i,r,detail):
    topics=', '.join((r.get('topics') or [])[:5]) or '无'
    return f"| {i} | {r['repo']} | {r.get('stars',0)} | {r.get('forks',0)} | {r.get('language','Unknown')} | {r.get('updated_at','')} | {md_table_escape(topics)} | {md_table_escape((r.get('description') or '无描述')[:90])} | {'值得试用' if r.get('stars',0)>1000 or r['repo'] in DIRECT_REPOS[:10] else '可观察'} | [[{detail}]] | [原文]({r.get('html_url')}) |"

def detail_repo(r, category):
    p=Path('GitHub')/category/DATE/(safe_slug(r['repo'])+'.md')
    full=VAULT/p; full.parent.mkdir(parents=True,exist_ok=True)
    content=f"""# {r['repo']}

> 一句话结论：{md_table_escape((r.get('description') or '该项目需要结合 README 进一步确认。')[:160])}

## TL;DR
- 来源：GitHub direct `/repos` fallback / snapshot。
- Stars/Forks：{r.get('stars')} / {r.get('forks')}；语言：{r.get('language')}。
- 更新时间：{r.get('updated_at')}；原文：{r.get('html_url')}。
- 对 AI Infra/Agent 的意义：用于观察 serving、训练、coding-agent loop 或工具链生态的工程成熟度。

## 元信息表
| 字段 | 值 |
|---|---|
| repo | {r['repo']} |
| stars | {r.get('stars')} |
| forks | {r.get('forks')} |
| language | {r.get('language')} |
| topics | {', '.join(r.get('topics') or []) or '无'} |
| source | {r.get('source','snapshot/direct')} |
| 原文 | {r.get('html_url')} |

## 信息压缩图示
```mermaid
flowchart TB
  subgraph Workload[Workload]
    W1[LLM/Agent 请求]
    W2[训练或推理任务]
    W3[工具调用/评测循环]
  end
  subgraph System[项目核心]
    S1[{r['repo']}]
    S2[Runtime / API / CLI]
    S3[Scheduler / State]
    S4[Docs / Examples / Releases]
  end
  subgraph Decision[决策]
    D1[快速试用]
    D2[对比现有栈]
    D3[观察风险]
  end
  W1 --> S1
  W2 --> S1
  W3 --> S2
  S1 --> S2 --> S3
  S1 --> S4
  S3 --> D1
  S4 --> D2
  S2 --> D3
  classDef workload fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
  classDef system fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef decision fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  class W1,W2,W3 workload;
  class S1,S2,S3,S4 system;
  class D1,D2,D3 decision;
```

## 机制 / 影响矩阵
| 维度 | 观察点 | 对我的影响 |
|---|---|---|
| 工程成熟度 | star、fork、更新频率、release | 判断是否进入试用队列 |
| Infra 相关性 | serving/training/agent/eval 组件 | 映射到现有 AI Infra 工作流 |
| 风险 | API 变化、维护频率、文档质量 | 试用前需要先跑 examples/benchmark |

## 专业解读
该项目今日作为 AI Radar 的候选进入榜单，主要价值在于为 LLM serving、训练后优化、agent loop 或 coding workflow 提供可观测的工程实现。若它属于基础设施类，应重点看调度、吞吐、延迟、KV/cache、分布式与硬件依赖；若属于 coding-agent 类，应重点看权限模式、上下文管理、工具调用、评测闭环和 IDE/CLI 集成。

## 通俗解释
把它当成一个“是否值得拿来做实验”的候选项目：先看活跃度和文档，再决定是否接入自己的小 benchmark。

## 可信度与局限性
- GitHub Search 今日部分 403，因此该页优先使用 direct `/repos` 或已保存 snapshot。
- 未自动阅读全文 README；结论偏工程雷达，不等于完整评测。

## 我应该如何跟进
1. 打开原 repo 阅读 README/Release。
2. 若与 serving/training/agent loop 强相关，拉取 examples 跑最小 demo。
3. 对比现有栈记录延迟、吞吐、上下文窗口、权限与评测能力。

#ai-radar #github #{category.lower()}
"""
    full.write_text(content,encoding='utf-8')
    return note_link(p), blob(p)

def detail_tool(tool, rel):
    p=Path('Industry/Tools')/DATE/(safe_slug(tool)+'.md')
    full=VAULT/p; full.parent.mkdir(parents=True,exist_ok=True)
    content=f"""# {tool} 工具更新观察

> 一句话结论：今日以 release/changelog 端点扫描 {tool}；最新信号为 `{rel['tag']}`，需要结合原文确认功能细节。

## TL;DR
- 工具/厂商：{tool}
- 来源类型：GitHub Release / Changelog / Docs
- 发布时间或 tag：{rel['published_at']} / {rel['tag']}
- 原文：{rel['url']}
- 对 AI coding workflow 的影响：重点看 agent mode、MCP、IDE/CLI、权限、上下文和远程执行是否变化。

## 元信息表
| 字段 | 值 |
|---|---|
| 工具 | {tool} |
| release/tag | {rel['tag']} |
| 发布时间 | {rel['published_at']} |
| 来源类型 | GitHub Release / Changelog |
| 原文 | {rel['url']} |

## 信息压缩图示
```mermaid
flowchart LR
  subgraph Source[来源]
    C[{tool}]
    R[{rel['tag']}]
  end
  subgraph Signal[可能功能变化]
    S1[Agent mode]
    S2[MCP / Tool use]
    S3[IDE/CLI/TUI]
    S4[权限/Rate limit]
  end
  subgraph Workflow[我的 coding 工作流]
    W1[多 agent 并行]
    W2[代码审查]
    W3[远程执行]
    W4[上下文工程]
  end
  C --> R
  R --> S1
  R --> S2
  R --> S3
  R --> S4
  S1 --> W1
  S2 --> W3
  S3 --> W2
  S4 --> W4
  classDef source fill:#e1d5e7,stroke:#9673a6,stroke-width:2px;
  classDef signal fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef workflow fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  class C,R source; class S1,S2,S3,S4 signal; class W1,W2,W3,W4 workflow;
```

## 功能变化摘要
{md_table_escape(rel.get('body') or '未从 release body 获取到明确摘要；建议打开原文确认。')}

## 对我的影响
若本次更新涉及 agent mode、上下文窗口、MCP 或权限模式，优先评估它是否能降低多 agent 编排和代码审查成本；若只是小修复，则作为低优先级观察。

## 可信度与局限性
自动扫描 release/changelog 只能确认“有无发布信号”，不能替代人工完整阅读文档。

#ai-radar #coding-tools
"""
    full.write_text(content,encoding='utf-8')
    return note_link(p), blob(p)

def detail_paper(paper):
    p=Path('Papers/arXiv')/DATE/(safe_slug(paper['id']+'-'+paper['title'])+'.md')
    full=VAULT/p; full.parent.mkdir(parents=True,exist_ok=True)
    content=f"""# {paper['title']}

> 一句话结论：这是一篇来自 arXiv 的候选论文，主题与 LLM/Agent/RL/AI Infra 相关，建议按摘要先做二次筛选。

## TL;DR
- 论文来源：arXiv
- 来源类型：预印本
- 作者/机构：{paper['authors']}
- 发布时间：{paper['published']}
- abs：{paper['abs']}
- PDF：{paper['pdf']}
- 代码链接：未发现

## 元信息表
| 字段 | 值 |
|---|---|
| arXiv ID | {paper['id']} |
| Categories | {paper['cats']} |
| Authors | {paper['authors']} |
| Published | {paper['published']} |
| Abs | {paper['abs']} |
| PDF | {paper['pdf']} |

## 信息压缩图示
```mermaid
flowchart TB
  subgraph Q[研究问题]
    Q1[LLM/Agent/RL 工程瓶颈]
    Q2[训练/推理/评测成本]
    Q3[现有方法缺口]
  end
  subgraph M[论文信号]
    M1[{paper['id']}]
    M2[方法/系统设计]
    M3[实验与评测]
  end
  subgraph D[阅读决策]
    D1[读 abstract]
    D2[查代码/benchmark]
    D3[决定是否复现]
  end
  Q1 --> M1
  Q2 --> M2
  Q3 --> M3
  M1 --> D1 --> D2 --> D3
  M2 --> D3
  M3 --> D3
  classDef problem fill:#fff2cc,stroke:#d6b656,stroke-width:2px;
  classDef method fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef decision fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  class Q1,Q2,Q3 problem; class M1,M2,M3 method; class D1,D2,D3 decision;
```

## 摘要压缩
{paper['summary'][:900]}

## 专业解读
本条进入雷达是因为查询词限定在 LLM serving、agent evaluation、post-training、RL/world model 等方向。后续应验证论文是否提供可复现实验、代码或足够清晰的 benchmark。若只是泛 AI 应用而缺少系统/训练/评测贡献，应降级为 skim。

## 对我的影响
- AI Infra：关注是否提供吞吐、延迟、调度或分布式训练信号。
- LLM/Agent：关注是否改善工具调用、评测闭环、上下文管理。
- RL/Game AI：关注是否能迁移到 self-play、环境并行或奖励设计。

## 可信度与局限性
仅基于 arXiv API 摘要；未阅读全文 PDF。

#ai-radar #paper #arxiv
"""
    full.write_text(content,encoding='utf-8')
    return note_link(p), blob(p)

# Load snapshots and direct fallback
snap=json.loads(STATE.read_text())
prev_files=sorted((VAULT/'Automation/state').glob('github-stars-*.json'))
prev={}
for pf in reversed(prev_files):
    if DATE in pf.name: continue
    try:
        d=json.loads(pf.read_text())
        for r in d.get('repos',[]):
            prev.setdefault(r.get('repo'), r)
    except Exception: pass
    if len(prev)>100: break

direct=[]
for full in DIRECT_REPOS:
    r=get_repo(full); old=prev.get(r['repo']); r['stars_delta']=None if not old else r.get('stars',0)-int(old.get('stars',0)); r['growth_basis']='direct watched repo fallback，非完整全网日增' if old else 'direct watched repo fallback，缺少历史基线'; direct.append(r); time.sleep(0.15)

# patch snapshot with direct fallback state
existing={r.get('repo'):r for r in snap.get('repos',[])}
for r in direct: existing[r['repo']]=dict(r, themes=(['loop_engineer'] if r['repo'] in LOOP_REPOS else []))
snap['repos']=list(existing.values())
snap['direct_fallback_2026_09_12']=True
snap['direct_fallback_note']='GitHub Search after niche queries was rate-limited; broad AI Infra and Loop tables use fixed direct /repos watched set, labelled non-complete all-GitHub growth.'
snap['high_star_top10']=sorted(direct,key=lambda x:x.get('stars',0),reverse=True)[:10]
snap['growth_top10']=sorted(direct,key=lambda x:(x.get('stars_delta') if x.get('stars_delta') is not None else -1, x.get('stars',0)),reverse=True)[:10]
loop=[r for r in direct if r['repo'] in LOOP_REPOS]
snap.setdefault('theme_sections',{})['loop_engineer']={'repos':loop,'high_star_top10':sorted(loop,key=lambda x:x.get('stars',0),reverse=True)[:10],'growth_top10':sorted(loop,key=lambda x:(x.get('stars_delta') if x.get('stars_delta') is not None else -1, x.get('stars',0)),reverse=True)[:10]}
STATE.write_text(json.dumps(snap,ensure_ascii=False,indent=2),encoding='utf-8')

# detail pages
repo_notes={}
for r in snap['high_star_top10']+snap['growth_top10']+loop[:10]:
    if r['repo'] not in repo_notes: repo_notes[r['repo']]=detail_repo(r, 'AIInfra' if r['repo'] not in LOOP_REPOS else 'LoopEngineer')
# point rummy from snapshot
point=snap.get('theme_sections',{}).get('point_rummy',{}).get('high_star_top10',[])[:5]
for r in point:
    if r['repo'] not in repo_notes: repo_notes[r['repo']]=detail_repo(r,'PointRummy')

# tools
tool_rows=[]; tool_notes={}
static_tools=[('Claude Code','Anthropic','Changelog / Release Notes','低置信：扫描 docs/changelog URL，未使用专用 API','需人工打开 changelog 确认 Claude Tag/权限/上下文变化','https://docs.anthropic.com/en/release-notes/claude-code'),('Cursor','Cursor','Changelog','低置信：扫描 changelog URL，未使用专用 API','关注 agent mode、MCP、IDE 内联体验','https://cursor.com/changelog'),('Windsurf','Windsurf','Changelog','低置信：扫描 changelog URL，未使用专用 API','关注远程执行、agent 模式和 pricing/rate limit','https://windsurf.com/changelog'),('GitHub Copilot','GitHub','Changelog / Blog','低置信：扫描 Copilot changelog/blog','关注 agent mode、代码审查与企业权限','https://github.blog/changelog/label/copilot/')]
for name,vendor,stype,status,impact,url in static_tools:
    rel={'tag':'docs/changelog','published_at':'网页扫描低置信','url':url,'body':status}
    tool_notes[name]=detail_tool(name,rel)
    tool_rows.append((name,vendor,stype,status,'未确认高相关新项',impact,url))
for name,full in TOOL_REPOS.items():
    rel=last_release(full); tool_notes[name]=detail_tool(name,rel)
    status='已获取 latest release' if rel['tag']!='未获取' else '低置信/访问失败'
    vendor={'OpenAI Codex':'OpenAI','Gemini Code Assist':'Google','Qwen Code':'Alibaba/Qwen','Roo Code':'Roo Code','Cline':'Cline','Continue':'Continue'}[name]
    update=f"{rel['tag']} / {rel['name']} / {rel['published_at']}"
    impact='若涉及 CLI/TUI、agent loop、MCP 或上下文管理，影响多 agent 编排和代码审查效率。'
    tool_rows.append((name,vendor,'GitHub Releases',status,update,impact,rel['url']))

# papers
papers=[]
for q in ['cat:cs.AI AND all:agent evaluation','cat:cs.LG AND all:LLM serving','cat:cs.LG AND all:reinforcement learning language models','cat:cs.AI AND all:world model reinforcement learning']:
    papers.extend(arxiv_search(q,2)); time.sleep(3)
# de-dup and select
seen=set(); paper_notes=[]
for p in papers:
    if p['id'] in seen: continue
    seen.add(p['id']); n=detail_paper(p); paper_notes.append((p,n))
    if len(paper_notes)>=5: break

# industry detail pages for source matrix notable/low-confidence pages
def industry_detail(company, title, url, status):
    p=Path('Industry/CompanyScan')/DATE/(safe_slug(company)+'-'+safe_slug(title)+'.md')
    full=VAULT/p; full.parent.mkdir(parents=True,exist_ok=True)
    content=f"""# {company} - {title}

> 一句话结论：今日公司来源扫描项；状态：{status}。

## TL;DR
- 发布方/大厂：{company}
- 栏目/来源类型：News / Research / Engineering Blog / Product Announcement
- 发布时间：未从自动 API 确认，低置信
- 原文链接：{url}

## 信息压缩图示
```mermaid
flowchart LR
  subgraph Source[发布方]
    C[{company}]
    A[{title}]
  end
  subgraph Signal[信号]
    S1[产品方向]
    S2[研究方向]
    S3[工程瓶颈]
  end
  subgraph Impact[对我的影响]
    I1[AI Infra]
    I2[LLM/Agent]
    I3[RL/Game AI]
    I4[继续观察]
  end
  C --> A --> S1
  A --> S2
  A --> S3
  S1 --> I2
  S2 --> I3
  S3 --> I1
  S3 --> I4
  classDef company fill:#e1d5e7,stroke:#9673a6,stroke-width:2px;
  classDef signal fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;
  classDef impact fill:#d5e8d4,stroke:#82b366,stroke-width:2px;
  class C,A company; class S1,S2,S3 signal; class I1,I2,I3,I4 impact;
```

## 专业解读
该页用于保证大厂来源矩阵的可点击追踪。今日自动扫描未对该来源确认高相关新项；后续若出现模型发布、训练/推理基础设施、agent/eval、coding workflow 或 RL/world model 相关更新，应升级为必读并补全发布时间、作者和技术细节。

## 可信度与局限性
低置信：仅记录来源入口或扫描状态，不代表完整抓取成功。

#ai-radar #industry
"""
    full.write_text(content,encoding='utf-8')
    return note_link(p), blob(p)
companies=[('OpenAI','News / Research','https://openai.com/news/'),('Anthropic','News / Research / Engineering','https://www.anthropic.com/news'),('Google DeepMind','Blog / Research','https://deepmind.google/discover/blog/'),('Meta AI','Blog / Research','https://ai.meta.com/blog/'),('NVIDIA','Technical Blog / AI','https://developer.nvidia.com/blog/category/artificial-intelligence/'),('Microsoft','Research AI','https://www.microsoft.com/en-us/research/research-area/artificial-intelligence/'),('Hugging Face','Blog / Papers / Releases','https://huggingface.co/blog'),('腾讯','AI Lab / 技术博客','https://ai.tencent.com/ailab/en/index'),('字节','Seed / 技术博客','https://seed.bytedance.com/en/'),('SpaceAI','Blog / News','https://spaceai.com/')]
industry_notes={}
for c,src,url in companies[:4]: industry_notes[c]=industry_detail(c,'来源扫描入口',url,'无高相关新项 / 低置信')

# rummy paper low conf
rummy_papers=arxiv_search('all:"gin rummy" OR all:"indian rummy"',2)

# Daily content
def gh_url(path): return blob(Path(path+'.md'))

top=snap['high_star_top10']; growth=snap['growth_top10']; loop_hi=snap['theme_sections']['loop_engineer']['high_star_top10']; loop_gr=snap['theme_sections']['loop_engineer']['growth_top10']
lines=[]
lines.append(f"# AI Radar Daily - {DATE}\n\n> 生成时间：2026-09-12 09:00 CST\n> 范围：AI Infra / LLM / RL / Game AI / 大厂博客 / 论文 / GitHub / Coding 工具\n> 说明：日报是总览导航页；详情页负责深度理解。GitHub Search 今日在 niche 查询后出现 403，因此 broad/Loop 榜单使用 direct watched repo fallback，并显式标注非完整全网日增。\n")
lines.append('## 0. 今日结论\n\n- 今日最值得关注：GitHub Search 部分 403，但已保存当日 snapshot，并用 direct `/repos` watched set 补齐 AI Infra、Loop Engineer 与 coding 工具榜单。\n- AI Infra 侧重点：vLLM、Transformers、PyTorch、TensorRT-LLM、SGLang、verl/OpenRLHF 仍是 serving/training/post-training 观察主线。\n- Coding workflow 侧重点：Codex、Gemini CLI、Cline、Roo、Continue、Qwen Code 等 release 端点已扫描，需继续关注 agent mode、MCP、权限和上下文窗口变化。\n- Point Rummy：今日 niche snapshot 捕获多个 Rummy/AI/规则候选，但整体 star 低，适合作为规则建模和 bot baseline 参考，不应直接视为成熟业务组件。\n- 建议今天深读：先看 vLLM/TensorRT-LLM/SGLang 生态，再看 Codex/Gemini CLI/Cline/Roo release，最后 skim arXiv agent/eval/serving 候选。\n')
lines.append('## 1. 今日态势图\n\n```mermaid\nflowchart LR\n  subgraph Sources[今日来源]\n    C[公司/Research 矩阵]\n    P[arXiv 论文]\n    G[GitHub snapshot + direct repos]\n    T[Coding 工具 releases]\n  end\n  subgraph Themes[主题聚类]\n    I[Serving / Training Infra]\n    A[Agent / Eval / Coding Loop]\n    R[RL / Post-training]\n    B[Point Rummy 业务]\n  end\n  subgraph Actions[动作]\n    D1[必读: vLLM/Transformers/PyTorch]\n    D2[试用: Codex/Gemini/Cline/Roo]\n    D3[观察: Rummy baseline]\n    D4[标注低置信: 403/页面扫描]\n  end\n  C --> I\n  P --> A\n  P --> R\n  G --> I\n  G --> B\n  T --> A\n  I --> D1\n  A --> D2\n  B --> D3\n  C --> D4\n  classDef source fill:#e1d5e7,stroke:#9673a6,stroke-width:2px;\n  classDef theme fill:#dae8fc,stroke:#6c8ebf,stroke-width:2px;\n  classDef action fill:#d5e8d4,stroke:#82b366,stroke-width:2px;\n  class C,P,G,T source; class I,A,R,B theme; class D1,D2,D3,D4 action;\n```\n')
# cards
card_items=[top[0], top[1], loop_hi[0], growth[0]]
lines.append('## 2. 必读卡片区\n')
for idx,r in enumerate(card_items,1):
    detail,web=repo_notes[r['repo']]
    lines.append(f"> [!important] {r['repo']}\n> - 大类：GitHub\n> - 小类：{'Loop Engineer' if r['repo'] in LOOP_REPOS else 'AI Infra'}\n> - 重点：{md_table_escape((r.get('description') or '')[:140])}\n> - 为什么重要：这是今日 fallback broad/Loop 榜单的关键工程项目，可用于判断 serving、training、agent loop 或 coding workflow 的生态方向。\n> - 详情：[[{detail}]] / [网页详情]({web}) / [原文]({r.get('html_url')})\n")
lines.append('## 3. 优先级矩阵\n\n```mermaid\nquadrantChart\n  title 今日内容优先级：影响力 × 可落地性\n  x-axis 低可落地性 --> 高可落地性\n  y-axis 低影响力 --> 高影响力\n  quadrant-1 立即读/试\n  quadrant-2 看趋势\n  quadrant-3 暂存\n  quadrant-4 可工具化\n  vLLM: [0.86, 0.92]\n  TensorRT-LLM: [0.78, 0.88]\n  Codex/Gemini CLI: [0.80, 0.76]\n  Point Rummy baseline: [0.45, 0.48]\n  arXiv agent/eval: [0.58, 0.70]\n```\n')
# classification
lines.append('## 4. 分类清单\n\n| 标签 | 大类 | 小类 | 标题 | 重点概括 | 为什么重要 | Obsidian 详情 | 网页详情 | 原文 |\n|---|---|---|---|---|---|---|---|---|')
for r in top[:5]:
    detail,web=repo_notes[r['repo']]
    lines.append(f"| 必读 | GitHub | AI Infra/Agent | {r['repo']} | {md_table_escape((r.get('description') or '')[:80])} | direct fallback 榜单核心项目，适合进入试用/benchmark 队列。 | [[{detail}]] | [网页详情]({web}) | [原文]({r.get('html_url')}) |")
for p,n in paper_notes[:3]:
    lines.append(f"| 可 skim | 论文 | arXiv | {md_table_escape(p['title'][:70])} | {md_table_escape(p['summary'][:90])} | 作为 LLM/Agent/RL/Infra 论文候选，需要二次过滤和读 PDF。 | [[{n[0]}]] | [网页详情]({n[1]}) | [原文]({p['abs']}) |")
lines.append('')
# company matrix
lines.append('## 5. 大厂资讯 / 工程博客 / Research\n\n### 5.1 公司来源扫描矩阵\n\n| 公司/实验室 | 来源/栏目 | 今日状态 | 高相关条数 | 代表条目 | 备注 |\n|---|---|---|---:|---|---|')
for c,src,url in companies:
    status='无高相关新项 / 低置信'
    count=0
    rep='来源入口扫描'
    note='未确认当天强相关更新；保留矩阵防漏扫。'
    if c in ['OpenAI','Anthropic','Google DeepMind','Meta AI']:
        detail,web=industry_notes[c]
        rep=f'[[{detail}]] / [网页详情]({web}) / [原文]({url})'
    else:
        rep=f'[原文]({url})'
    lines.append(f"| {c} | {src} | {status} | {count} | {rep} | {note} |")
lines.append('\n### 5.2 高相关大厂条目\n\n| 标签 | 发布方/大厂 | 栏目/来源 | 标题 | 重点概括 | 工程/算法影响 | Obsidian 详情 | 网页详情 | 原文 |\n|---|---|---|---|---|---|---|---|---|')
for c in list(industry_notes):
    detail,web=industry_notes[c]
    lines.append(f"| 低置信 | {c} | News / Research / Engineering | 来源扫描入口 | 今日未确认高相关新项，保留入口用于后续追踪。 | 若出现模型/infra/agent/eval 更新需升级为必读。 | [[{detail}]] | [网页详情]({web}) | [原文]({[x[2] for x in companies if x[0]==c][0]}) |")
# github tables
lines.append('\n## 6. GitHub 高 star Top 10\n\n| 排名 | repo | stars | forks | language | updated_at | topics | 重点概括 | 是否值得试用 | Obsidian 详情 | 原文 |\n|---:|---|---:|---:|---|---|---|---|---|---|---|')
for i,r in enumerate(top,1): lines.append(repo_row(i,r,repo_notes[r['repo']][0]))
lines.append('\n## 7. GitHub star 增长最快 Top 10\n\n> 增长依据：direct watched repo fallback，非完整全网日增；若 `stars_delta` 为 null/缺失，表示当前 watched repo 在历史 snapshot 中缺少可靠 baseline。\n\n| 排名 | repo | stars_delta | stars | forks | language | updated_at | 增长依据 | 重点概括 | Obsidian 详情 | 原文 |\n|---:|---|---:|---:|---:|---|---|---|---|---|---|')
for i,r in enumerate(growth,1):
    detail=repo_notes[r['repo']][0]
    lines.append(f"| {i} | {r['repo']} | {r.get('stars_delta')} | {r.get('stars')} | {r.get('forks')} | {r.get('language')} | {r.get('updated_at')} | {r.get('growth_basis')} | {md_table_escape((r.get('description') or '')[:90])} | [[{detail}]] | [原文]({r.get('html_url')}) |")
# tools
lines.append('\n## 8. Coding 工具 / AI 工具功能更新\n\n### 8.1 Coding 工具扫描矩阵\n\n| 工具 | 厂商 | 来源类型 | 今日状态 | 代表更新 | 对我的影响 | 原文 |\n|---|---|---|---|---|---|---|')
for name,vendor,stype,status,update,impact,url in tool_rows:
    lines.append(f"| {name} | {vendor} | {stype} | {status} | {md_table_escape(update)} | {md_table_escape(impact)} | [原文]({url}) |")
lines.append('\n### 8.2 高相关工具更新\n\n| 标签 | 工具/厂商 | 来源类型 | 标题/功能 | 重点概括 | 对 AI coding 工作流的影响 | Obsidian 详情 | 网页详情 | 原文 |\n|---|---|---|---|---|---|---|---|---|')
for name,vendor,stype,status,update,impact,url in tool_rows:
    detail,web=tool_notes[name]
    lines.append(f"| 后续 | {name} / {vendor} | {stype} | {md_table_escape(update)} | {md_table_escape(status)} | {md_table_escape(impact)} | [[{detail}]] | [网页详情]({web}) | [原文]({url}) |")
# point rummy
lines.append('\n## 9. Point Rummy / Indian Rummy 业务主题\n\n### 9.1 GitHub 候选\n\n| 标签 | repo | stars | forks | language | updated_at | 重点概括 | 业务可用性 | Obsidian 详情 | 原文 |\n|---|---|---:|---:|---|---|---|---|---|---|')
for r in point[:10]:
    detail=repo_notes[r['repo']][0]
    lines.append(f"| 后续 | {r['repo']} | {r.get('stars')} | {r.get('forks')} | {r.get('language')} | {r.get('updated_at')} | {md_table_escape((r.get('description') or '')[:90])} | 可作为规则/AI opponent/计分 baseline，成熟度偏低需重构。 | [[{detail}]] | [原文]({r.get('html_url')}) |")
lines.append('\n### 9.2 论文 / 资料候选\n\n| 标签 | 来源 | 标题 | 作者/机构 | 重点概括 | 对 Point Rummy 业务有什么用 | Obsidian 详情 | 原文 |\n|---|---|---|---|---|---|---|---|')
for rp in rummy_papers[:2]:
    lines.append(f"| 低置信 | arXiv | {md_table_escape(rp['title'])} | {md_table_escape(rp['authors'])} | {md_table_escape(rp['summary'][:100])} | 可参考 imperfect-information card game / MCTS / self-play 思路；需确认是否真与 Rummy 相关。 | 未生成 | [原文]({rp['abs']}) |")
lines.append('\n### 9.3 业务可用性判断\n\n| 方向 | 今日信号 | 可用性 | 下一步 |\n|---|---|---|---|\n| 规则引擎 / 计分 | 多个低 star Rummy repo | 中：可借鉴规则和计分，不宜直接复用 | 抽取规则测试用例，建立统一 evaluator |\n| Bot / RL Agent | rummy-ai / Gin Rummy Java 等候选 | 中低：可作为 ISMCTS/MCTS baseline | 先复现单机 bot，再接入 self-play |\n| 仿真 / 评测 | 未发现成熟高 star 环境 | 低：需要自建环境并行与评测 | 设计 Gymnasium-style env + benchmark |\n')
# loop
lines.append('## 10. Loop Engineer / Loop Engineering 主题\n\n### 10.1 Loop Engineer GitHub 高 star Top 10\n\n| 排名 | repo | stars | forks | language | updated_at | topics | 重点概括 | 是否值得试用 | Obsidian 详情 | 原文 |\n|---:|---|---:|---:|---|---|---|---|---|---|---|')
for i,r in enumerate(loop_hi,1): lines.append(repo_row(i,r,repo_notes[r['repo']][0]))
lines.append('\n### 10.2 Loop Engineer GitHub star 增长最快 Top 10\n\n| 排名 | repo | stars_delta | stars | forks | language | updated_at | 增长依据 | 重点概括 | Obsidian 详情 | 原文 |\n|---:|---|---:|---:|---:|---|---|---|---|---|---|')
for i,r in enumerate(loop_gr,1):
    detail=repo_notes[r['repo']][0]
    lines.append(f"| {i} | {r['repo']} | {r.get('stars_delta')} | {r.get('stars')} | {r.get('forks')} | {r.get('language')} | {r.get('updated_at')} | {r.get('growth_basis')} | {md_table_escape((r.get('description') or '')[:90])} | [[{detail}]] | [原文]({r.get('html_url')}) |")
lines.append('\n### 10.3 Loop Engineering 方法信号\n\n| 标签 | 来源 | 标题 | 重点概括 | 对 AI coding 工作流的影响 | Obsidian 详情 | 原文 |\n|---|---|---|---|---|---|---|')
for r in loop_hi[:5]:
    detail=repo_notes[r['repo']][0]
    lines.append(f"| 后续 | GitHub | {r['repo']} | {md_table_escape((r.get('description') or '')[:100])} | 观察 agent loop、任务分解、上下文工程、eval loop 和权限边界。 | [[{detail}]] | [原文]({r.get('html_url')}) |")
# papers
lines.append('\n## 11. 论文\n\n### 11.1 Agent / Serving / RL / World Model 候选\n\n| 标签 | 论文来源 | 论文 | 作者/机构 | 重点概括 | 工程/研究价值 | Obsidian 详情 | 网页详情 | PDF/原文 |\n|---|---|---|---|---|---|---|---|---|')
for p,n in paper_notes:
    lines.append(f"| 可 skim | arXiv / 预印本 | {md_table_escape(p['title'])} | {md_table_escape(p['authors'])} | {md_table_escape(p['summary'][:100])} | 作为 LLM/Agent/RL/Infra 候选，需读 PDF 验证是否有系统或实验价值。 | [[{n[0]}]] | [网页详情]({n[1]}) | [PDF]({p['pdf']}) / [abs]({p['abs']}) |")
lines.append('\n## 12. 资讯 / 其他 GitHub 项目\n\n### 12.1 AI Infra direct watched repo fallback\n\n| 标签 | 来源 | 标题 | 重点概括 | 对我有什么用 | Obsidian 详情 | 网页详情 | 原文 |\n|---|---|---|---|---|---|---|---|')
for r in direct[10:15]:
    if r['repo'] not in repo_notes: repo_notes[r['repo']]=detail_repo(r,'AIInfra')
    detail,web=repo_notes[r['repo']]
    lines.append(f"| 后续 | GitHub | {r['repo']} | {md_table_escape((r.get('description') or '')[:100])} | 扩展 watched repo 池，辅助判断生态活跃度。 | [[{detail}]] | [网页详情]({web}) | [原文]({r.get('html_url')}) |")
lines.append('\n## 13. 按主题索引\n\n### AI Infra / Serving / Training\n')
for r in top[:5]: lines.append(f"- [[{repo_notes[r['repo']][0]}]] - {r['repo']} direct fallback 重点项目")
lines.append('\n### LLM / Agent / RAG / Evaluation\n')
for r in loop_hi[:5]: lines.append(f"- [[{repo_notes[r['repo']][0]}]] - Loop/coding agent 观察")
lines.append('\n### RL / Game AI / World Model\n')
for p,n in paper_notes[:2]: lines.append(f"- [[{n[0]}]] - arXiv 候选论文")
lines.append('\n### Point Rummy / Indian Rummy\n')
for r in point[:3]: lines.append(f"- [[{repo_notes[r['repo']][0]}]] - Rummy 规则/bot baseline")
lines.append('\n### Loop Engineer / Coding Agent Loop\n')
for r in loop_hi[:5]: lines.append(f"- [[{repo_notes[r['repo']][0]}]] - coding agent loop 工具/框架")
lines.append('\n### 公司 / 实验室\n')
for c in industry_notes: lines.append(f"- {c}: [[{industry_notes[c][0]}]]")
lines.append('\n## 14. 值得后续深挖\n\n| 标签 | 大类 | 小类 | 标题 | 后续动作 | Obsidian 详情 | 原文 |\n|---|---|---|---|---|---|---|')
for r in top[:3]: lines.append(f"| 必读 | GitHub | AI Infra | {r['repo']} | 拉 README + examples，跑最小 benchmark。 | [[{repo_notes[r['repo']][0]}]] | [原文]({r.get('html_url')}) |")
for name in ['OpenAI Codex','Cline','Roo Code']:
    lines.append(f"| 后续 | Coding 工具 | Agent workflow | {name} | 打开 release/changelog 核对 agent mode/MCP/权限变化。 | [[{tool_notes[name][0]}]] | [原文]({[x[6] for x in tool_rows if x[0]==name][0]}) |")
lines.append(f"\n## 15. 采集失败或低置信来源\n\n- GitHub Search snapshot 已保存：`Automation/state/github-stars-{DATE}.json`；但 Search 在部分 Rummy/Loop/broad 查询后返回 403 rate limit，因此 broad AI Infra 和 Loop Engineer 榜单使用 direct `/repos` watched repo fallback，并标注非完整全网日增。\n- 公司来源扫描矩阵今日以来源入口和低置信状态为主；未声称已完整抓取所有动态。\n- arXiv API 若返回低相关候选，已标注可 skim/低置信，需要人工读 PDF 二次确认。\n\n## 16. 归档标签\n\n#ai-radar #daily #ai-infra #llm #rl #point-rummy #loop-engineering\n")

daily=VAULT/'Daily'/f'{DATE}.md'; daily.parent.mkdir(exist_ok=True); daily.write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'daily':str(daily),'files_created':len(list((VAULT/'GitHub').glob(f'**/{DATE}/*.md')))+len(list((VAULT/'Industry').glob(f'**/{DATE}/*.md')))+len(list((VAULT/'Papers').glob(f'**/{DATE}/*.md')))+1,'snapshot':str(STATE)},ensure_ascii=False))
