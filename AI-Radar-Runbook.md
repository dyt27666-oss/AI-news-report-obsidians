# AI Radar 自动化运行说明

## 目标

每天北京时间 09:00 生成一套完整 AI Radar 知识更新，而不是只生成一篇日报。

日报是总览入口；重要 GitHub 项目、论文、大厂博客会拆成独立 Obsidian 知识卡片，并从日报链接过去。

## Vault 路径

`/home/vscode-server/obsidian-ai-radar`

## 每日输出

- `Daily/YYYY-MM-DD.md`: 当日总览日报，只放可点击清单、Top 5、分类索引和短解读。
- `GitHub/...`: 重要 GitHub 项目详情页。
- `Papers/...`: 重要论文详情页。
- `Industry/...`: 大厂博客 / 工程文章详情页。
- `Concepts/...`: 可复用概念卡片。
- `Templates/detail-template.md`: 通用详情页模板。
- `Templates/paper-detail-template.md`: 论文详情页模板。

## 固定写作模式

日报不是正文仓库，而是总览导航页。每条重点资讯必须在日报中提供 `[[详情页]]` wikilink，用户可以从清单直接点击到该资讯的具体页面。

每个详情页必须包含：

- 原文链接。
- 分类。
- 推荐等级：`必读` / `可 skim` / `可收藏` / `暂不重要`。
- 专业解读：面向 AI Infra / LLM / RL 工程背景。
- 通俗解释：用简单语言讲清楚是什么和为什么重要。
- 图示：优先引用文章/论文原图；如果没有合适原图，用 Mermaid 画 LLM 整理出来的理解图。
- 对你的影响：是否值得读全文、试用、复现或暂时忽略。

## GitHub 同步

远端 repo：`git@github-tt:dyt27666-oss/AI-news-report-obsidians.git`

说明：这台机器默认 `git@github.com` 认证到 `hody2`；用于该 repo 的 SSH host 是 `github-tt`，对应 GitHub 用户 `dyt27666-oss`。

每日任务会检测是否存在 git remote；如果存在，会自动 commit 和 push。

## Telegram 推送

当前定时任务会把最终摘要投递回 Hermes 的 origin 会话。若你已经配置 Telegram gateway，可以之后把 cron job 的 delivery 改成具体 Telegram 目标，或配置 home channel 后改为投递到该 Telegram channel。

Hermes 相关入口：

```bash
hermes gateway setup
hermes gateway status
hermes cron list
hermes cron edit <JOB_ID>
```
