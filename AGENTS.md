# AI Knowledge Base Assistant

## 项目概述

本项目自动采集 GitHub Trending 和 Hacker News 中 AI、LLM、Agent 领域的技术动态，使用 AI 分析并结构化保存为 JSON 知识条目，再分发至 Telegram 和飞书等渠道。

## 技术栈

- Python 3.12
- OpenCode + 国产大模型
- LangGraph
- OpenClaw

## 编码规范

- 遵循 PEP 8；函数、变量和模块使用 `snake_case`。
- 为公开模块、类和函数编写 Google 风格 docstring。
- 禁止使用裸 `print()`；使用项目统一的日志设施。

## 项目结构

- `.opencode/agents/`：Agent 角色定义。
- `.opencode/skills/`：可复用的 Agent 技能。
- `knowledge/raw/`：采集到的原始数据。
- `knowledge/articles/`：分析整理后的知识条目。

## 知识条目格式

分析结果以 JSON 保存。每条记录至少包含以下字段：

```json
{
  "id": "string",
  "title": "string",
  "source_url": "string",
  "source": "github_trending | hacker_news",
  "summary": "string",
  "tags": ["AI", "LLM"],
  "status": "draft | published | archived",
  "published_at": "ISO 8601 datetime"
}
```

## Agent 角色

| 角色 | 职责 | 输入 | 输出 |
| --- | --- | --- | --- |
| 采集 Agent | 从 GitHub Trending 和 Hacker News 获取候选动态 | 外部数据源 | `knowledge/raw/` 原始数据 |
| 分析 Agent | 评估相关性、生成摘要和标签 | 原始数据 | 符合 JSON 契约的草稿条目 |
| 整理 Agent | 去重、校验条目并触发渠道分发 | 草稿条目 | `knowledge/articles/` 条目与分发结果 |

## 红线

- 绝对禁止提交 API 密钥、令牌、Webhook URL 或其他凭据。
- 绝对禁止未经确认删除 `knowledge/` 中已有知识条目或原始数据。
- 绝对禁止绕过 JSON 格式校验写入或分发知识条目。
- 绝对禁止将未审核的外部内容标记为 `published` 或直接分发。
