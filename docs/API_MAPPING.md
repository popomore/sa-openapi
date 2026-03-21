# API 映射表

本文档记录 OpenAPI 规范端点到 Python SDK 方法和 CLI 命令的映射关系。

## 概览

### Analytics 服务（神策分析）

| 服务 | 版本 | Base Path | 端点数 | 描述 |
|------|------|-----------|--------|------|
| Dashboard | v1 | /api/v3/analytics/v1 | 6 | 概览书签开放接口 |
| Channel | v1 | /api/v3/analytics/v1 | 5 | 渠道追踪开放接口 |
| Dataset | v1 | /api/v3/analytics/v1 | 1 | 业务集市的数据查询开放接口 |
| EventMeta | v1 | /api/v3/analytics/v1 | 2 | 事件相关基础元数据 |
| Model | v1 | /api/v3/analytics/v1 | 5 | 分析模型开放接口 |
| PropertyMeta | v1 | /api/v3/analytics/v1 | 6 | 属性相关基础元数据 |
| SmartAlarm | v1 | /api/v3/analytics/v1 | 2 | 智能预警开放接口 |

**Analytics 小计**: 7 个服务，27 个端点

### Horizon 服务（神策数界）

| 服务 | 版本 | Base Path | 端点数 | 描述 |
|------|------|-----------|--------|------|
| Catalog | v1 | /api/v3/horizon/v1 | 3 | 目录服务 |
| DataSubscription | v1 | /api/v3/horizon/v1 | 7 | 订阅管理服务 |
| Schema | v1 | /api/v3/horizon/v1 | 3 | 元数据管理服务 |
| Segment | v1 | /api/v3/horizon/v1 | 2 | 分群管理服务 |
| Table | v1 | /api/v3/horizon/v1 | 3 | 数据表服务 |
| Tag | v1 | /api/v3/horizon/v1 | 2 | 标签管理服务 |

**Horizon 小计**: 6 个服务，20 个端点

### Portal 服务（神策业务门户）

| 服务 | 版本 | Base Path | 端点数 | 描述 |
|------|------|-----------|--------|------|
| Identity | v2 | /api/v3/portal/v2 | 3 | 身份服务主要负责管理账号权限相关的接口 |
| Management | v2 | /api/v3/portal/v2 | 8 | 管理服务主要负责管理 SBP 一些通用产品功能组件的 open api 接口 |
| ResourceManagement | v2 | /api/v3/portal/v2 | 4 | 资源管理服务主要负责资源管理相关模块的 open api 接口 |

**Portal 小计**: 3 个服务，15 个端点

**总计**: 16 个服务，62 个端点

---

## Analytics 服务详细映射

### Dashboard 服务 (6 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | QueryDashboardNavigation | GET | /dashboard/navigation | `client.dashboard.query_navigation()` | `sa analytics dashboard list-navigation` |
| 2 | QueryLegoDashboard | GET | /dashboard/lego | `client.dashboard.query_lego()` | `sa analytics dashboard list-lego` |
| 3 | QueryDashboard | GET | /dashboard/detail | `client.dashboard.query_dashboard()` | `sa analytics dashboard get` |
| 4 | AddDashboardNavigation | POST | /dashboard/navigation/create | `client.dashboard.add_navigation()` | `sa analytics dashboard create-navigation` |
| 5 | ShareDashboard | POST | /dashboard/share | `client.dashboard.share()` | `sa analytics dashboard share` |
| 6 | QueryAllBookmarks | GET | /dashboard/bookmarks | `client.dashboard.query_bookmarks()` | `sa analytics dashboard list-bookmarks` |

### Channel 服务 (5 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | CreateChannelUrl | POST | /channel/links/create | `client.channel.create_url()` | `sa analytics channel create` |
| 2 | UpdateChannelUrl | POST | /channel/links/update | `client.channel.update_url()` | `sa analytics channel update` |
| 3 | GetChannelUrl | POST | /channel/links/list | `client.channel.get_url()` | `sa analytics channel list` |
| 4 | DeleteChannleUrl | POST | /channel/links/delete | `client.channel.delete_url()` | `sa analytics channel delete` |
| 5 | GetCampaignList | POST | /channel/campaigns/list | `client.channel.get_campaigns()` | `sa analytics channel list-campaigns` |

### Dataset 服务 (1 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | DatasetDetail | GET | /dataset/detail | `client.dataset.get_detail()` | `sa analytics dataset get` |

### EventMeta 服务 (2 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | ListEventsAll | GET | /event-meta/events/all | `client.event_meta.list_events()` | `sa analytics event-meta list-events` |
| 2 | ListEventTags | GET | /event-meta/events/tags | `client.event_meta.list_tags()` | `sa analytics event-meta list-tags` |

### Model 服务 (5 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | QuerySegmentationReport | POST | /model/segmentation/report | `client.model.query_segmentation()` | `sa analytics model segmentation` |
| 2 | QueryFunnelReport | POST | /model/funnel/report | `client.model.query_funnel()` | `sa analytics model funnel` |
| 3 | QueryRetentionReport | POST | /model/retention/report | `client.model.query_retention()` | `sa analytics model retention` |
| 4 | QueryIntervalReport | POST | /model/interval/report | `client.model.query_interval()` | `sa analytics model interval` |
| 5 | QueryAddictionReport | POST | /model/addiction/report | `client.model.query_addiction()` | `sa analytics model addiction` |

### PropertyMeta 服务 (6 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | ListAllEventProperties | GET | /property-meta/event-properties/all | `client.property_meta.list_event_properties()` | `sa analytics property-meta list-event-props` |
| 2 | ListEventProperties | POST | /property-meta/event-properties | `client.property_meta.get_event_properties()` | `sa analytics property-meta get-event-props` |
| 3 | ListAllUserProperties | GET | /property-meta/user-properties/all | `client.property_meta.list_user_properties()` | `sa analytics property-meta list-user-props` |
| 4 | ListUserGroups | GET | /property-meta/user-groups/all | `client.property_meta.list_user_groups()` | `sa analytics property-meta list-user-groups` |
| 5 | ListUserTagsWithDir | GET | /property-meta/user-tags/dir | `client.property_meta.list_user_tags()` | `sa analytics property-meta list-user-tags` |
| 6 | GetPropertyValues | POST | /property-meta/property/values | `client.property_meta.get_property_values()` | `sa analytics property-meta get-values` |

### SmartAlarm 服务 (2 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | QueryAlarmConfig | GET | /smart-alarm/detail | `client.smart_alarm.query_config()` | `sa analytics smart-alarm get` |
| 2 | QueryAllAlarms | POST | /smart-alarm/all | `client.smart_alarm.query_all()` | `sa analytics smart-alarm list` |

---

## Horizon 服务详细映射

### Catalog 服务 (3 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | ListCatalogTrees | POST | /catalog/tree/list | `client.catalog.list_trees()` | `sa horizon catalog list-trees` |
| 2 | BindCatalogResource | POST | /catalog/resource/bind | `client.catalog.bind_resource()` | `sa horizon catalog bind` |
| 3 | UnbindCatalogResource | POST | /catalog/resource/unbind | `client.catalog.unbind_resource()` | `sa horizon catalog unbind` |

### DataSubscription 服务 (7 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | AddSubscriptionApplication | POST | /data-subscription/application/add | `client.data_subscription.add_application()` | `sa horizon subscription add-app` |
| 2 | AppendSubscriptionApplicationConfig | POST | /data-subscription/application/config/append | `client.data_subscription.append_config()` | `sa horizon subscription append-config` |
| 3 | GetSubscriptionApplication | POST | /data-subscription/application/get | `client.data_subscription.get_application()` | `sa horizon subscription get-app` |
| 4 | DeleteSubscriptionApplication | POST | /data-subscription/application/delete | `client.data_subscription.delete_application()` | `sa horizon subscription delete-app` |
| 5 | CreateDataSubscription | POST | /data-subscription/create | `client.data_subscription.create()` | `sa horizon subscription create` |
| 6 | ListDataSubscriptions | GET | /data-subscription/list | `client.data_subscription.list()` | `sa horizon subscription list` |
| 7 | BatchDeleteDataSubscriptions | POST | /data-subscription/batch-delete | `client.data_subscription.batch_delete()` | `sa horizon subscription batch-delete` |

### Schema 服务 (3 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | ListEventSchemas | POST | /schema/event/list | `client.schema.list_events()` | `sa horizon schema list-events` |
| 2 | GetEvent | POST | /schema/event/get | `client.schema.get_event()` | `sa horizon schema get-event` |
| 3 | CreateEvent | POST | /schema/event/create | `client.schema.create_event()` | `sa horizon schema create-event` |

### Segment 服务 (2 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | ListSegmentDefinitions | POST | /segment/definition/list | `client.segment.list_definitions()` | `sa horizon segment list` |
| 2 | GetSegmentDefinition | POST | /segment/definition/get | `client.segment.get_definition()` | `sa horizon segment get` |

### Table 服务 (3 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | ListTables | POST | /table/list | `client.table.list()` | `sa horizon table list` |
| 2 | GetTable | POST | /table/get | `client.table.get()` | `sa horizon table get` |
| 3 | CreateTable | POST | /table/create | `client.table.create()` | `sa horizon table create` |

### Tag 服务 (2 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | ListTagDefinitions | POST | /tag/definition/list | `client.tag.list_definitions()` | `sa horizon tag list` |
| 2 | GetTagDefinition | POST | /tag/definition/get | `client.tag.get_definition()` | `sa horizon tag get` |

---

## Portal 服务详细映射

### Identity 服务 (3 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | ListAccounts | GET | /identity/account/list | `client.identity.list_accounts()` | `sa portal identity list-accounts` |
| 2 | GetAccount | GET | /identity/account/get | `client.identity.get_account()` | `sa portal identity get-account` |
| 3 | GetAccountByName | GET | /identity/account/get-by-name | `client.identity.get_account_by_name()` | `sa portal identity get-by-name` |

### Management 服务 (8 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | ListBehaviorDefines | GET | /management/behavior/define/list | `client.management.list_behavior_defines()` | `sa portal management list-behavior-defines` |
| 2 | ListBehaviors | GET | /management/behavior/list | `client.management.list_behaviors()` | `sa portal management list-behaviors` |
| 3 | GetLicenseProduct | GET | /management/license/product | `client.management.get_license()` | `sa portal management get-license` |
| 4 | SendNoticeMessage | POST | /management/notice/send | `client.management.send_notice()` | `sa portal management send-notice` |
| 5 | GetAllProductVersion | GET | /management/product/versions | `client.management.get_versions()` | `sa portal management get-versions` |
| 6 | GetProjectByIdOrName | GET | /management/project/get | `client.management.get_project()` | `sa portal management get-project` |
| 7 | GetProjectsByAccountId | GET | /management/project/get-by-account-id | `client.management.get_projects_by_account()` | `sa portal management get-by-account` |
| 8 | ListProjects | GET | /management/project/list | `client.management.list_projects()` | `sa portal management list-projects` |

### ResourceManagement 服务 (4 个端点)

| # | OperationId | Method | Path | SDK 方法 | CLI 命令 |
|---|-------------|--------|------|----------|----------|
| 1 | ListAssets | POST | /resource-management/assets/list | `client.resource_management.list_assets()` | `sa portal resource list-assets` |
| 2 | ListAssetQuery | POST | /resource-management/assets/query/list | `client.resource_management.list_asset_query()` | `sa portal resource list-asset-query` |
| 3 | ListCompletedQueryTaskTable | GET | /resource-management/query/task/completed | `client.resource_management.list_completed_tasks()` | `sa portal resource list-completed` |
| 4 | ListExecutingQueryTaskTable | GET | /resource-management/query/task/executing | `client.resource_management.list_executing_tasks()` | `sa portal resource list-executing` |

---

## 旧版本映射（已废弃，仅供参考）

### 1. QueryChannel


---

## 数据模型说明

### 通用响应结构

所有 API 都使用 `HttpApiResult<T>` 包装响应：

```python
class HttpApiResult[T](BaseModel, Generic[T]):
    """API 统一响应结构."""
    code: str                           # 状态码 (SUCCESS, ERROR, etc.)
    message: str | None = None          # 消息
    request_id: str | None = None       # 请求 ID
    data: T | None = None               # 数据（成功时）
    error_info: ErrorInfo | None = None # 错误详情（失败时）
```

SDK 会自动解包 `data` 字段，错误时抛出异常。

### 错误信息结构

```python
class ErrorInfo(BaseModel):
    """错误信息结构."""
    code: str                                    # 具体的错误码
    description: str | None = None               # 错误描述
    system_response: str | None = None           # 系统响应信息
    error_causes: list[ErrorCause] | None = None # 致错原因列表
    context: dict | None = None                  # 错误上下文信息

class ErrorCause(BaseModel):
    """致错原因."""
    error_cause: str                             # 错误原因
    action_suggestion: str | None = None         # 行动建议
```

### 分页信息结构

```python
class Page(BaseModel):
    """分页信息."""
    total: int                    # 总记录数
    current_page: int             # 当前页号
    page_count: int               # 总页数
```

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

## CLI 命令结构

CLI 命令按照三层结构组织：

```
sa <product> <service> <action> [options]
```

例如：
```bash
# Analytics 服务
sa analytics dashboard list-navigation
sa analytics channel create --json {...}
sa analytics model funnel --json {...}

# Horizon 服务
sa horizon catalog list-trees
sa horizon subscription create --json {...}
sa horizon table list --project-id 1

# Portal 服务
sa portal identity list-accounts
sa portal management get-project --project-id 1
sa portal resource list-assets --json {...}
```

## 命名规范

### SDK 方法命名
- 列表操作: `list_*` (如 `list_navigation`)
- 查询操作: `query_*` (如 `query_dashboard`)
- 获取单个: `get_*` (如 `get_account`)
- 创建: `create_*` (如 `create_event`)
- 更新: `update_*` (如 `update_url`)
- 删除: `delete_*` (如 `delete_url`)
- 批量操作: `batch_*` (如 `batch_delete`)
- 绑定/解绑: `bind_*` / `unbind_*` (如 `bind_resource`)

### 参数命名
- OpenAPI camelCase → Python snake_case
  - `projectId` → `project_id`
  - `entityName` → `entity_name`
  - `pageSize` → `page_size`

### 模型命名
- 实体: 大驼峰 (如 `Account`, `Project`, `Table`)
- 请求参数: 大驼峰 + Request 后缀 (如 `CreateTableRequest`)
- 响应结果: 大驼峰 + Response 后缀 (如 `ListAccountsResponse`)
- 定义: 大驼峰 + Definition 后缀 (如 `SegmentDefinition`)

## 公共请求头

所有 API 接口都需要以下请求头：

| Header 名称 | 类型 | 必填 | 描述 |
|-------------|------|------|------|
| api-key | string | 是 | 全局唯一的密钥，用于验证和授权访问 API 接口 |
| sensorsdata-project | string | 是 | 项目名, 指定请求所属项目 |

## 使用示例

### SDK 使用

```python
from sensorsdata import SensorsDataClient

# 初始化客户端
client = SensorsDataClient(
    base_url="https://api.sensorsdata.cn",
    api_key="your-api-key",
    project="your-project-name"
)

# Analytics - 获取概览导航
navigations = client.dashboard.query_navigation(type="PRIVATE")

# Horizon - 列出数据表
tables = client.table.list(project_id=1, db_name="horizon_default_db")

# Portal - 获取账号列表
accounts = client.identity.list_accounts(page_index=1, page_size=20)
```

### CLI 使用

```bash
# 配置初始化
sa config init

# Analytics 服务
sa analytics dashboard list-navigation --type PRIVATE
sa analytics model funnel --json '{"measures": [...]}'

# Horizon 服务
sa horizon table list --project-id 1 --db-name horizon_default_db

# Portal 服务
sa portal identity list-accounts --page-size 20

# 输出格式
sa analytics dashboard list-navigation --output json
sa analytics dashboard list-navigation --output table
sa analytics dashboard list-navigation --output csv
```
