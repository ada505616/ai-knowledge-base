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
- 对外部请求、文件读写和 JSON 解析等可预期失败场景，捕获具体异常；禁止使用裸 `except` 或静默吞掉异常。
- 异常转换时使用 `raise ... from error` 保留原始异常链；日志应包含必要上下文且不得记录密钥、令牌、Webhook URL 等敏感信息。

## 项目结构

- `.opencode/agents/`：Agent 角色定义。
- `.opencode/skills/`：可复用的 Agent 技能。
- `knowledge/raw/`：采集到的原始数据。
- `knowledge/articles/`：分析整理后的知识条目。

## 知识条目格式

最终知识条目以 JSON 保存。每条记录至少包含以下字段：

```json
{
  "id": "string",
  "title": "string",
  "source_url": "string",
  "source": "github_trending | hacker_news",
  "summary": "string",
  "tags": ["AI", "LLM"],
  "status": "draft | published | archived",
  "published_at": "null | ISO 8601 datetime"
}
```

`published_at` 仅在 `status` 为 `published` 时填写 ISO 8601 时间；`draft` 与 `archived` 条目使用 `null`。

## Agent 角色

| 角色 | 职责 | 输入 | 输出 |
| --- | --- | --- | --- |
| 采集 Agent | 从 GitHub Trending 和 Hacker News 获取候选动态 | 外部数据源 | `knowledge/raw/` 原始数据 |
| 分析 Agent | 评估相关性、生成摘要、亮点、评分和标签建议 | 原始数据 | 结构化分析结果 |
| 整理 Agent | 去重、校验分析结果并格式化为标准 JSON 草稿 | 结构化分析结果 | `knowledge/articles/` 中状态为 `draft` 的条目 |
| 审核 Agent | 核验草稿的来源、事实、相关性与内容风险，并给出审核建议 | `knowledge/articles/` 草稿条目及公开来源 | `approved`、`needs_revision` 或 `rejected` 审核结果 |

处理链路为：采集 Agent → 分析 Agent → 整理 Agent → 审核 Agent → 人工确认 → 发布与分发。审核 Agent 的 `approved` 仅表示建议，不得自行修改条目状态、发布或分发内容。

## 红线

- 绝对禁止提交 API 密钥、令牌、Webhook URL 或其他凭据。
- 绝对禁止未经确认删除 `knowledge/` 中已有知识条目或原始数据。
- 绝对禁止绕过 JSON 格式校验写入或分发知识条目。
- 绝对禁止将未审核的外部内容标记为 `published` 或直接分发。
- 审核 Agent 仅输出审核建议；即使结论为 `approved`，也必须经人工确认后才能将条目发布或分发。
