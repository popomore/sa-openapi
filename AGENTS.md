# AGENTS.md

## 常用命令

```bash
uv run pytest                        # 运行测试
uv run ruff check src/ --fix         # lint 修复
uv run ruff format src/              # 格式化（CI 会检查）
uv run mypy src/                     # 类型检查
uv run sa-openapi --help             # 运行 CLI
```

## 新增 API 端点

1. 查阅 `docs/openapi/` 中的 JSON spec 确认请求/响应结构
2. 在 `src/sa_openapi/models/<service>.py` 添加 Pydantic 模型
3. 在 `src/sa_openapi/services/<service>.py` 添加 async 方法
4. 在 `src/sa_openapi/cli/<service>.py` 添加 Click 命令

## 注意事项

- CLI help 字符串只用 ASCII 标点，不用全角 `，（）：`（ruff RUF001）
- 提交前必须跑 `ruff format`，否则 CI 会挂
- 模型字段用 `Field(alias="camelCase")` 并加 `model_config = {"populate_by_name": True}`
