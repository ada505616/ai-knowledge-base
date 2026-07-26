---
name: github-trending
description: 当需要采集 GitHub 热门开源项目时使用此技能
allowed-tools: Read, Grep, Glob, WebFetch
---

# GitHub Trending 采集

## 使用场景

当需要从 GitHub 采集热门开源项目，并筛选 AI、LLM、Agent 相关候选条目写入知识库原始数据时，使用此技能。

## 执行步骤

1. 使用 GitHub API 搜索近期热门仓库，优先按 `stars`、`pushed` 或创建时间组合查询，并记录查询条件与返回时间。
2. 从每个仓库提取名称、仓库 URL、描述、star 数、主要编程语言和 topics。
3. 仅纳入与 AI、LLM、Agent 明确相关的仓库；排除 Awesome 列表、纯资源导航、无实际项目内容及无法确认相关性的仓库。
4. 按仓库 URL 和规范化后的项目名称去重；同一项目仅保留信息最完整且 star 数最高的记录。
5. 为每个保留项目撰写中文摘要，使用“项目名 + 做什么 + 为什么值得关注”的公式，避免编造功能、性能或热度数据。
6. 以 star 数为主、项目活跃度与主题相关性为辅排序，取 Top 15。
7. 按下方 JSON 格式生成输出内容；由调用方将该内容写入 `knowledge/raw/github-trending-YYYY-MM-DD.json`。

## 注意事项

- 仅使用公开可访问的 GitHub API 或仓库页面，并以实际响应中的数据为准。
- 不得在输出中包含 GitHub Token、请求头、Cookie 或其他凭据。
- `stars` 必须为 API 返回的数值；无法获取时不猜测，排除该条目。
- `topics` 使用 GitHub 返回的主题标签；没有主题时使用空数组。
- `collected_at` 使用采集完成时的 ISO 8601 UTC 时间。
- 输出前确认 JSON 合法、项目数量不超过 15 条，且每个项目均符合 AI、LLM 或 Agent 相关性要求。

## 输出格式

```json
{
  "source": "github_trending",
  "skill": "github-trending",
  "collected_at": "2026-07-26T00:00:00Z",
  "items": [
    {
      "name": "example-ai-project",
      "url": "https://github.com/example/example-ai-project",
      "summary": "example-ai-project 是一个用于构建 AI 应用的开源工具，因其清晰的开发者集成方式而值得关注。",
      "stars": 12345,
      "language": "Python",
      "topics": ["ai", "llm"]
    }
  ]
}
```
