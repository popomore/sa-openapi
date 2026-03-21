# CLI 使用指南

`sa-openapi` 提供了基于 Click 的命令行工具，覆盖 Dashboard、Channel、Dataset、Model 四类接口。

安装包后可以直接使用：

```bash
sa-openapi --help
```

在仓库开发环境中可以用：

```bash
uv run sa-openapi --help
```

## 配置

### 初始化配置

首次使用可以通过交互式命令写入默认配置：

```bash
sa-openapi config init
```

也可以直接通过选项传入：

```bash
sa-openapi config init \
  --base-url https://your-instance.sensorsdata.cn \
  --api-key sk-xxx \
  --project default
```

配置文件默认保存在 `~/.sa-openapi.toml`。

### 查看配置

```bash
sa-openapi config list
sa-openapi config show
sa-openapi config show production
```

### 多 profile

CLI 读取的配置文件格式如下：

```toml
[default]
base_url = "https://your-instance.sensorsdata.cn"
api_key = "sk-default-xxx"
project = "default"
timeout = 30.0
max_retries = 3

[production]
base_url = "https://prod.sensorsdata.cn"
api_key = "sk-prod-xxx"
project = "prod"
timeout = 30.0
max_retries = 3
```

使用指定 profile：

```bash
sa-openapi --profile production dashboard list
```

将某个 profile 设为默认：

```bash
sa-openapi config set-default production
```

注意：

- `config init` 当前只会写入 `[default]`。
- `config set-default PROFILE` 会把该 section 复制到 `[default]`，并删除原来的 `PROFILE` section。

### 环境变量和 `.env`

CLI 启动时会尝试加载 `.env`，并读取以下环境变量：

```bash
export SA_BASE_URL="https://your-instance.sensorsdata.cn"
export SA_API_KEY="sk-xxx"
export SA_PROJECT="default"
```

这些环境变量会覆盖配置文件里的 `[default]`。如果你在使用非默认 profile，且只想临时覆盖连接信息，优先使用全局选项：

```bash
sa-openapi \
  --profile production \
  --base-url https://override.example.com \
  --api-key sk-override \
  --project prod \
  dataset list
```

## 全局选项

所有业务命令都支持以下全局选项：

| 选项 | 说明 |
|------|------|
| `--debug` | 打开调试日志 |
| `--profile TEXT` | 选择配置 profile，默认是 `default` |
| `--base-url TEXT` | 临时覆盖实例地址 |
| `--api-key TEXT` | 临时覆盖 API Key |
| `--project TEXT` | 临时覆盖 project |

## 命令总览

| 命令组 | 子命令 |
|--------|--------|
| `dashboard` | `list`, `get`, `bookmarks`, `bookmark-data` |
| `channel` | `list`, `list-links`, `get-link`, `link-data` |
| `dataset` | `list`, `get`, `schema`, `sql-query`, `saved-queries`, `create-query`, `delete-query` |
| `model` | `funnel-report`, `retention-report`, `attribution-report`, `sql`, `explain-sql`, `validate-sql` |
| `config` | `init`, `list`, `show`, `set-default` |

## Dashboard

```bash
sa-openapi dashboard list --type PRIVATE
sa-openapi dashboard get 123
sa-openapi dashboard bookmarks --navigation-id 123
sa-openapi dashboard bookmark-data 456 --start-date 2026-03-01 --end-date 2026-03-07
```

| 子命令 | 说明 | 输出格式 |
|--------|------|----------|
| `dashboard list` | 列出概览分组 | `table`, `json` |
| `dashboard get NAVIGATION_ID` | 查看分组详情 | `table`, `json` |
| `dashboard bookmarks --navigation-id ID` | 列出分组下书签 | `table`, `json` |
| `dashboard bookmark-data BOOKMARK_ID --start-date ... --end-date ...` | 查询书签数据 | `table`, `json`, `csv` |

## Channel

```bash
sa-openapi channel list
sa-openapi channel list-links --channel-id 123
sa-openapi channel get-link 456
sa-openapi channel link-data 456 --start-date 2026-03-01 --end-date 2026-03-07 --format csv
```

| 子命令 | 说明 | 输出格式 |
|--------|------|----------|
| `channel list` | 列出渠道 | `table`, `json` |
| `channel list-links --channel-id ID` | 列出渠道下链接 | `table`, `json` |
| `channel get-link LINK_ID` | 查看链接详情 | `table`, `json` |
| `channel link-data LINK_ID --start-date ... --end-date ...` | 查询链接数据 | `table`, `json`, `csv` |

## Dataset

```bash
sa-openapi dataset list
sa-openapi dataset get 1
sa-openapi dataset schema 1
sa-openapi dataset sql-query --dataset-id 1 --sql "SELECT * FROM events LIMIT 10"
sa-openapi dataset saved-queries 1
sa-openapi dataset create-query 1 --name "recent_events" --sql "SELECT * FROM events LIMIT 10"
sa-openapi dataset delete-query 1 1001
```

| 子命令 | 说明 | 输出格式 |
|--------|------|----------|
| `dataset list` | 列出数据集 | `table`, `json` |
| `dataset get DATASET_ID` | 查看数据集详情 | `table`, `json` |
| `dataset schema DATASET_ID` | 查看 schema | `table`, `json` |
| `dataset sql-query --dataset-id ID --sql ...` | 执行 SQL | `table`, `json`, `csv` |
| `dataset saved-queries DATASET_ID` | 列出保存的查询 | `table`, `json` |
| `dataset create-query DATASET_ID --name ... --sql ...` | 创建保存的查询 | 固定输出 JSON |
| `dataset delete-query DATASET_ID QUERY_ID` | 删除保存的查询 | 固定输出成功消息 |

## Model

### 分析命令

`funnel-report`、`retention-report`、`attribution-report` 通过 `--json` 接收请求参数字符串。

漏斗分析示例：

```bash
sa-openapi model funnel-report --json '{
  "measures": [
    {"event": "view_product", "aggregator": "COUNT"},
    {"event": "add_to_cart", "aggregator": "COUNT"}
  ],
  "window": 7,
  "start_date": "2026-03-01",
  "end_date": "2026-03-07"
}'
```

留存分析示例：

```bash
sa-openapi model retention-report --json '{
  "initial_event": "sign_up",
  "return_event": "login",
  "periods": [1, 3, 7, 14, 30],
  "start_date": "2026-03-01",
  "end_date": "2026-03-07"
}'
```

归因分析示例：

```bash
sa-openapi model attribution-report --json '{
  "conversion_event": "purchase",
  "touch_points": ["ad_click", "email_open", "visit"],
  "model": "LAST_TOUCH",
  "window": 7,
  "start_date": "2026-03-01",
  "end_date": "2026-03-07"
}'
```

说明：

- 顶层 JSON 键支持 `snake_case` 和 `camelCase`，例如 `start_date` 与 `startDate` 都可以。
- 建议在 shell 中用单引号包住整个 JSON 字符串。

### SQL 相关

```bash
sa-openapi model sql --sql "SELECT * FROM events LIMIT 10" --format json
sa-openapi model explain-sql "SELECT * FROM events LIMIT 10"
sa-openapi model validate-sql "SELECT * FROM events LIMIT 10"
```

| 子命令 | 说明 | 输出格式 |
|--------|------|----------|
| `model funnel-report --json ...` | 漏斗分析 | `table`, `json` |
| `model retention-report --json ...` | 留存分析 | `table`, `json` |
| `model attribution-report --json ...` | 归因分析 | `table`, `json` |
| `model sql --sql ...` | 自定义 SQL 查询 | `table`, `json`, `csv` |
| `model explain-sql SQL` | SQL 执行计划 | 固定输出 JSON |
| `model validate-sql SQL` | SQL 语法校验 | 固定输出文本结果 |

注意：

- `explain-sql` 和 `validate-sql` 的命令帮助里都标注了 “Not available in Model v1 API”。如果实例端未开放对应接口，这两个命令可能失败。

## 输出格式

CLI 目前没有全局 `--format`，输出格式是按子命令定义的。

常见规律如下：

- 资源列表和详情命令通常支持 `table`、`json`
- 数据查询命令通常支持 `table`、`json`、`csv`
- 配置命令和部分写操作命令使用固定输出

示例：

```bash
sa-openapi dashboard list --format json
sa-openapi dataset sql-query --dataset-id 1 --sql "SELECT * FROM events LIMIT 10" --format csv
sa-openapi model sql --sql "SELECT * FROM events LIMIT 10" --format table
```

## 快速排错

- `Profile 'xxx' not found`：先执行 `sa-openapi config list` 或 `sa-openapi config init`
- 认证失败：检查 `api_key`、`project` 是否和目标实例匹配
- 返回空数据：优先确认 `--start-date`、`--end-date`、ID 参数和 project 是否正确
- 调试请求：加上 `--debug`
