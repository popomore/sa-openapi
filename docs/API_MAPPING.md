# API 映射表

本文档记录 OpenAPI 规范端点到 Python SDK 方法的映射关系。

## 概览

| 服务 | 版本 | Base Path | 端点数 | 规范文件 |
|------|------|-----------|--------|----------|
| Dashboard | v1 | /api/v3/analytics/v1 | 6 | 3.0.4-analytics-Dashboard-v1-swagger.json |
| Channel | v1 | /api/v3/analytics/v1 | 5 | 3.0.4-analytics-Channel-v1-swagger.json |
| Dataset | v1 | /api/v3/analytics/v1 | 7 | 3.0.4-analytics-Dataset-v1-swagger.json |
| Model | v2 | /api/v3/analytics/v2 | 6 | 3.0.4-analytics-Model-v2-swagger.json |

---

## Dashboard 服务 (6 个端点)

### 1. QueryDashboardNavigation

**OpenAPI**:
- operationId: `QueryDashboardNavigation`
- 方法: `GET`
- 路径: `/dashboard/navigation`
- 描述: 获取所有的概览分组信息

**SDK 映射**:
```python
client.dashboard.list_navigation(
    type: Literal["PRIVATE", "PUBLIC"] | None = None
) -> list[Navigation]
```

**请求参数**:
| 参数 | 位置 | 类型 | 必填 | 描述 |
|------|------|------|------|------|
| api-key | header | string | ✅ | API 密钥 |
| sensorsdata-project | header | string | ✅ | 项目名 |
| type | query | enum | ❌ | 概览类型 (PRIVATE/PUBLIC) |

**响应模型**: `HttpApiResult<list[Navigation]>`

---

### 2. GetDashboardNavigation

**OpenAPI**:
- operationId: `GetDashboardNavigation`
- 方法: `GET`
- 路径: `/dashboard/navigation/{id}`
- 描述: 获取指定的概览分组信息

**SDK 映射**:
```python
client.dashboard.get_navigation(
    navigation_id: int
) -> Navigation
```

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | integer | ✅ | 概览分组 ID |

**响应模型**: `HttpApiResult<Navigation>`

---

### 3. QueryDashboardBookmark

**OpenAPI**:
- operationId: `QueryDashboardBookmark`
- 方法: `GET`
- 路径: `/dashboard/bookmark`
- 描述: 获取概览书签列表

**SDK 映射**:
```python
client.dashboard.list_bookmark(
    navigation_id: int | None = None
) -> list[Bookmark]
```

**请求参数**:
| 参数 | 位置 | 类型 | 必填 | 描述 |
|------|------|------|------|------|
| navigation_id | query | integer | ❌ | 概览分组 ID |

**响应模型**: `HttpApiResult<list[Bookmark]>`

---

### 4. GetDashboardBookmark

**OpenAPI**:
- operationId: `GetDashboardBookmark`
- 方法: `GET`
- 路径: `/dashboard/bookmark/{id}`
- 描述: 获取指定的概览书签

**SDK 映射**:
```python
client.dashboard.get_bookmark(
    bookmark_id: int
) -> Bookmark
```

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | integer | ✅ | 书签 ID |

**响应模型**: `HttpApiResult<Bookmark>`

---

### 5. GetDashboardBookmarkData

**OpenAPI**:
- operationId: `GetDashboardBookmarkData`
- 方法: `POST`
- 路径: `/dashboard/bookmark/{id}/data`
- 描述: 获取概览书签数据

**SDK 映射**:
```python
client.dashboard.get_bookmark_data(
    bookmark_id: int,
    params: BookmarkDataParams
) -> BookmarkData
```

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | integer | ✅ | 书签 ID |

**请求体**: `BookmarkDataParams`

**响应模型**: `HttpApiResult<BookmarkData>`

---

### 6. ExportDashboardBookmark

**OpenAPI**:
- operationId: `ExportDashboardBookmark`
- 方法: `POST`
- 路径: `/dashboard/bookmark/{id}/export`
- 描述: 导出概览书签数据

**SDK 映射**:
```python
client.dashboard.export_bookmark(
    bookmark_id: int,
    format: Literal["CSV", "EXCEL"] = "CSV"
) -> bytes
```

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | integer | ✅ | 书签 ID |

**请求体**:
```json
{
  "format": "CSV"
}
```

**响应**: 文件流 (application/octet-stream)

---

## Channel 服务 (5 个端点)

### 1. QueryChannel

**OpenAPI**:
- operationId: `QueryChannel`
- 方法: `GET`
- 路径: `/channel`
- 描述: 获取渠道列表

**SDK 映射**:
```python
client.channel.list_channel() -> list[Channel]
```

**响应模型**: `HttpApiResult<list[Channel]>`

---

### 2. QueryChannelLink

**OpenAPI**:
- operationId: `QueryChannelLink`
- 方法: `GET`
- 路径: `/channel/link`
- 描述: 获取渠道链接列表

**SDK 映射**:
```python
client.channel.list_link(
    channel_id: int | None = None
) -> list[Link]
```

**请求参数**:
| 参数 | 位置 | 类型 | 必填 | 描述 |
|------|------|------|------|------|
| channel_id | query | integer | ❌ | 渠道 ID |

**响应模型**: `HttpApiResult<list[Link]>`

---

### 3. GetChannelLink

**OpenAPI**:
- operationId: `GetChannelLink`
- 方法: `GET`
- 路径: `/channel/link/{id}`
- 描述: 获取指定的渠道链接

**SDK 映射**:
```python
client.channel.get_link(
    link_id: int
) -> Link
```

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | integer | ✅ | 链接 ID |

**响应模型**: `HttpApiResult<Link>`

---

### 4. GetChannelLinkData

**OpenAPI**:
- operationId: `GetChannelLinkData`
- 方法: `POST`
- 路径: `/channel/link/{id}/data`
- 描述: 获取渠道链接数据

**SDK 映射**:
```python
client.channel.get_link_data(
    link_id: int,
    params: LinkDataParams
) -> LinkData
```

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | integer | ✅ | 链接 ID |

**请求体**: `LinkDataParams`

**响应模型**: `HttpApiResult<LinkData>`

---

### 5. ExportChannelLink

**OpenAPI**:
- operationId: `ExportChannelLink`
- 方法: `POST`
- 路径: `/channel/link/{id}/export`
- 描述: 导出渠道链接数据

**SDK 映射**:
```python
client.channel.export_link(
    link_id: int,
    format: Literal["CSV", "EXCEL"] = "CSV"
) -> bytes
```

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | integer | ✅ | 链接 ID |

**请求体**:
```json
{
  "format": "CSV"
}
```

**响应**: 文件流 (application/octet-stream)

---

## Dataset 服务 (7 个端点)

### 1. QueryDataset

**OpenAPI**:
- operationId: `QueryDataset`
- 方法: `GET`
- 路径: `/dataset`
- 描述: 获取数据集列表

**SDK 映射**:
```python
client.dataset.list_dataset() -> list[Dataset]
```

**响应模型**: `HttpApiResult<list[Dataset]>`

---

### 2. GetDataset

**OpenAPI**:
- operationId: `GetDataset`
- 方法: `GET`
- 路径: `/dataset/{id}`
- 描述: 获取指定的数据集

**SDK 映射**:
```python
client.dataset.get_dataset(
    dataset_id: int
) -> Dataset
```

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | integer | ✅ | 数据集 ID |

**响应模型**: `HttpApiResult<Dataset>`

---

### 3. QueryDatasetData

**OpenAPI**:
- operationId: `QueryDatasetData`
- 方法: `POST`
- 路径: `/dataset/{id}/data`
- 描述: 执行 SQL 查询数据集

**SDK 映射**:
```python
client.dataset.sql_query(
    dataset_id: int,
    sql: str,
    limit: int | None = None,
    offset: int | None = None
) -> QueryResult
```

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | integer | ✅ | 数据集 ID |

**请求体**:
```json
{
  "sql": "SELECT * FROM events LIMIT 10",
  "limit": 100,
  "offset": 0
}
```

**响应模型**: `HttpApiResult<QueryResult>`

---

### 4. GetDatasetSchema

**OpenAPI**:
- operationId: `GetDatasetSchema`
- 方法: `GET`
- 路径: `/dataset/{id}/schema`
- 描述: 获取数据集 schema

**SDK 映射**:
```python
client.dataset.get_schema(
    dataset_id: int
) -> Schema
```

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | integer | ✅ | 数据集 ID |

**响应模型**: `HttpApiResult<Schema>`

---

### 5. QueryDatasetSavedQuery

**OpenAPI**:
- operationId: `QueryDatasetSavedQuery`
- 方法: `GET`
- 路径: `/dataset/{id}/saved_query`
- 描述: 获取保存的查询列表

**SDK 映射**:
```python
client.dataset.list_saved_query(
    dataset_id: int
) -> list[SavedQuery]
```

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | integer | ✅ | 数据集 ID |

**响应模型**: `HttpApiResult<list[SavedQuery]>`

---

### 6. CreateDatasetSavedQuery

**OpenAPI**:
- operationId: `CreateDatasetSavedQuery`
- 方法: `POST`
- 路径: `/dataset/{id}/saved_query`
- 描述: 创建保存的查询

**SDK 映射**:
```python
client.dataset.create_saved_query(
    dataset_id: int,
    name: str,
    sql: str
) -> SavedQuery
```

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | integer | ✅ | 数据集 ID |

**请求体**:
```json
{
  "name": "查询名称",
  "sql": "SELECT * FROM events WHERE ..."
}
```

**响应模型**: `HttpApiResult<SavedQuery>`

---

### 7. DeleteDatasetSavedQuery

**OpenAPI**:
- operationId: `DeleteDatasetSavedQuery`
- 方法: `DELETE`
- 路径: `/dataset/{id}/saved_query/{query_id}`
- 描述: 删除保存的查询

**SDK 映射**:
```python
client.dataset.delete_saved_query(
    dataset_id: int,
    query_id: int
) -> None
```

**路径参数**:
| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| id | integer | ✅ | 数据集 ID |
| query_id | integer | ✅ | 查询 ID |

**响应**: 空响应（204 No Content）

---

## Model 服务 (6 个端点)

> **注意**: Model 服务使用 `/api/v3/analytics/v2` base path

### 1. GetFunnelReport

**OpenAPI**:
- operationId: `GetFunnelReport`
- 方法: `POST`
- 路径: `/model/funnel/report`
- 描述: 获取漏斗分析报告

**SDK 映射**:
```python
client.model.funnel_report(
    measures: list[Measure],
    filter: Filter | None = None,
    by_fields: list[ByField] | None = None,
    window: int | None = None
) -> FunnelReport
```

**请求体**: `FunnelParams`
```json
{
  "measures": [
    {
      "event": "PageView",
      "aggregator": "COUNT"
    },
    {
      "event": "AddToCart",
      "aggregator": "COUNT"
    }
  ],
  "filter": {
    "property": "platform",
    "operator": "=",
    "value": "iOS"
  },
  "byFields": [
    {
      "property": "city"
    }
  ],
  "window": 7
}
```

**响应模型**: `HttpApiResult<FunnelReport>`

---

### 2. GetRetentionReport

**OpenAPI**:
- operationId: `GetRetentionReport`
- 方法: `POST`
- 路径: `/model/retention/report`
- 描述: 获取留存分析报告

**SDK 映射**:
```python
client.model.retention_report(
    initial_event: str,
    return_event: str,
    filter: Filter | None = None,
    by_fields: list[ByField] | None = None,
    periods: list[int] = [1, 3, 7, 14, 30]
) -> RetentionReport
```

**请求体**: `RetentionParams`
```json
{
  "initialEvent": "AppInstall",
  "returnEvent": "AppLaunch",
  "filter": {
    "property": "channel",
    "operator": "IN",
    "value": ["organic", "paid"]
  },
  "periods": [1, 3, 7, 14, 30]
}
```

**响应模型**: `HttpApiResult<RetentionReport>`

---

### 3. GetAttributionReport

**OpenAPI**:
- operationId: `GetAttributionReport`
- 方法: `POST`
- 路径: `/model/attribution/report`
- 描述: 获取归因分析报告

**SDK 映射**:
```python
client.model.attribution_report(
    conversion_event: str,
    touch_points: list[str],
    model: Literal["FIRST_TOUCH", "LAST_TOUCH", "LINEAR"],
    window: int | None = None
) -> AttributionReport
```

**请求体**: `AttributionParams`
```json
{
  "conversionEvent": "Purchase",
  "touchPoints": ["Ad Click", "Email Open", "Website Visit"],
  "model": "LINEAR",
  "window": 30
}
```

**响应模型**: `HttpApiResult<AttributionReport>`

---

### 4. QueryModelData

**OpenAPI**:
- operationId: `QueryModelData`
- 方法: `POST`
- 路径: `/model/data`
- 描述: 执行自定义 SQL 查询

**SDK 映射**:
```python
client.model.sql_query(
    sql: str,
    limit: int | None = None
) -> QueryResult
```

**请求体**:
```json
{
  "sql": "SELECT event, COUNT(*) FROM events GROUP BY event",
  "limit": 1000
}
```

**响应模型**: `HttpApiResult<QueryResult>`

---

### 5. ExplainModelSql

**OpenAPI**:
- operationId: `ExplainModelSql`
- 方法: `POST`
- 路径: `/model/sql/explain`
- 描述: 获取 SQL 执行计划

**SDK 映射**:
```python
client.model.explain_sql(
    sql: str
) -> SqlExplainResult
```

**请求体**:
```json
{
  "sql": "SELECT * FROM events WHERE event_date > '2024-01-01'"
}
```

**响应模型**: `HttpApiResult<SqlExplainResult>`

---

### 6. ValidateModelSql

**OpenAPI**:
- operationId: `ValidateModelSql`
- 方法: `POST`
- 路径: `/model/sql/validate`
- 描述: 验证 SQL 语法

**SDK 映射**:
```python
client.model.validate_sql(
    sql: str
) -> SqlValidateResult
```

**请求体**:
```json
{
  "sql": "SELECT * FROM events"
}
```

**响应模型**: `HttpApiResult<SqlValidateResult>`

---

## 通用响应结构

所有 API 都使用 `HttpApiResult<T>` 包装响应：

```python
class HttpApiResult[T](BaseModel, Generic[T]):
    """API 统一响应结构."""
    code: str                           # 状态码 (SUCCESS, ERROR, etc.)
    message: str                        # 消息
    request_id: str                     # 请求 ID
    data: T | None = None               # 数据（成功时）
    error_info: ErrorInfo | None = None # 错误详情（失败时）
```

SDK 会自动解包 `data` 字段，错误时抛出异常。

## 错误码映射

| API Code | SDK Exception | HTTP Status | 描述 |
|----------|---------------|-------------|------|
| SUCCESS | - | 200 | 成功 |
| UNAUTHORIZED | AuthenticationError | 401 | 认证失败 |
| PERMISSION_DENIED | AuthorizationError | 403 | 权限不足 |
| NOT_FOUND | NotFoundError | 404 | 资源不存在 |
| INVALID_ARGUMENT | ValidationError | 400 | 参数验证失败 |
| RATE_LIMIT_EXCEEDED | RateLimitError | 429 | 频率限制 |
| INTERNAL_ERROR | ServerError | 500 | 服务器错误 |
| UNAVAILABLE | NetworkError | 503 | 服务不可用 |

## CLI 命令映射

每个 SDK 方法都对应一个 CLI 命令：

```bash
# Dashboard
sa dashboard list              → client.dashboard.list_navigation()
sa dashboard get 123           → client.dashboard.get_navigation(123)
sa dashboard bookmarks         → client.dashboard.list_bookmark()

# Channel
sa channel list                → client.channel.list_channel()
sa channel list-links          → client.channel.list_link()

# Dataset
sa dataset list                → client.dataset.list_dataset()
sa dataset sql-query --sql "..." → client.dataset.sql_query(...)

# Model
sa model funnel-report --json {...} → client.model.funnel_report(...)
sa model sql --sql "..."       → client.model.sql_query(...)
```

## 命名规范

### SDK 方法命名
- 列表操作: `list_*` (如 `list_navigation`)
- 获取单个: `get_*` (如 `get_bookmark`)
- 创建: `create_*`
- 删除: `delete_*`
- 导出: `export_*`
- 查询: `*_query` (如 `sql_query`)
- 报告: `*_report` (如 `funnel_report`)

### 参数命名
- OpenAPI camelCase → Python snake_case
  - `navigationId` → `navigation_id`
  - `startDate` → `start_date`
  - `byFields` → `by_fields`

### 模型命名
- 实体: 大驼峰 (如 `Navigation`, `Bookmark`)
- 参数: 大驼峰 + Params 后缀 (如 `BookmarkDataParams`)
- 结果: 大驼峰 + Result/Report/Data 后缀 (如 `QueryResult`, `FunnelReport`)
