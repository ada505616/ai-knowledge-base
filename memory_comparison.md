# Memory 对代码生成的影响对比

对比对象：`utils02/github_api_new.py`（无 Memory，即未提供 `AGENTS.md`）与 `utils/github_api.py`（有 Memory，即遵循项目 `AGENTS.md`）。

| 维度 | 无 Memory | 有 Memory | 差异说明 |
| --- | --- | --- | --- |
| 命名风格 | Python 标识符使用 `snake_case`，请求头中的 `User-Agent` 为通用的 `github-repository-info-client`。 | Python 标识符同样使用 `snake_case`，`User-Agent` 使用项目名 `ai-knowledge-base`。 | 两者均符合 Python 基本命名习惯；有 Memory 的版本更体现项目上下文与身份。 |
| docstring | 包含模块和函数 docstring，函数说明 `Args` 与 `Raises`，但未说明返回值。 | 包含模块和函数 docstring，函数说明 `Args`、`Returns` 与 `Raises`。 | 有 Memory 的版本更完整地满足 `AGENTS.md` 中公开模块和函数使用 Google 风格 docstring 的要求。 |
| 日志方式 | 未使用日志，也没有裸 `print()`。 | 未使用日志，也没有裸 `print()`。 | 两者都避免了裸 `print()`；但在请求失败等需要观测的场景，有 Memory 的版本也尚未使用项目统一日志设施，存在可改进空间。 |
| 错误处理 | 捕获 `HTTPError` 和 `URLError`，将 401、403、404 转为 `ValueError`，其余请求错误转为 `RuntimeError`，提供中文错误信息。 | 先校验 `owner` 和 `repository` 非空；未捕获网络异常，保留 `HTTPError` 与 `URLError` 供调用方处理。 | 无 Memory 的版本更强调面向调用方的异常包装；有 Memory 的版本补充了参数校验，并通过 docstring 明确异常契约，但网络错误信息较少。 |
| 文件位置 | 位于 `utils02/github_api_new.py`，使用了与项目职责不明确的临时目录和文件名。 | 位于 `utils/github_api.py`，目录和文件名表达了 GitHub API 工具模块的职责。 | 有 Memory 的版本更符合项目既有目录结构和模块命名语义。 |

## 结论

Memory（`AGENTS.md` 提供的项目上下文与规范）能让 AI 生成的代码更贴合项目：使用项目标识、放在语义明确的位置，并补齐输入校验、URL 编码和更完整的文档契约。它不会自动保证所有规范都被落实，例如本次两份代码均未使用统一日志设施；因此，Memory 能显著提升一致性，但仍需通过代码评审和测试确认细节质量。
