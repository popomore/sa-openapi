# sa-openapi 实施计划

## 项目概述

基于神策分析、神策数界、神策业务门户的 OpenAPI 规范文件，实现完整的 Python SDK 和 CLI 工具。

**API 统计**:
- **Analytics (神策分析)**: 7 个服务，33 个端点
  - Dashboard (概览): 6 个端点
  - Channel (渠道追踪): 5 个端点
  - Dataset (业务集市): 1 个端点
  - EventMeta (事件元数据): 2 个端点
  - Model (分析模型): 5 个端点
  - PropertyMeta (属性元数据): 6 个端点
  - SmartAlarm (智能预警): 2 个端点
- **Horizon (神策数界)**: 6 个服务，19 个端点
  - Catalog (目录服务): 3 个端点
  - DataSubscription (订阅管理): 7 个端点
  - Schema (元数据管理): 3 个端点
  - Segment (分群管理): 2 个端点
  - Table (数据表服务): 3 个端点
  - Tag (标签管理): 2 个端点
- **Portal (神策业务门户)**: 3 个服务，12 个端点
  - Identity (身份服务): 3 个端点
  - Management (管理服务): 8 个端点
  - ResourceManagement (资源管理服务): 4 个端点
- **总计**: 16 个服务，64 个端点

## 实施阶段

### Phase 1: 基础框架 ✅ (已完成)

**目标**: 建立项目脚手架和核心基础设施

#### 任务清单

- [x] 创建项目结构
- [x] 配置 pyproject.toml
- [x] 编写 README.md
- [x] 编写 CONTRIBUTING.md
- [x] 配置 CI/CD (GitHub Actions)
- [x] 创建 .gitignore 和 LICENSE
- [ ] 实现核心基础设施
  - [ ] `_exceptions.py` - 异常体系
  - [ ] `_config.py` - 配置管理
  - [ ] `_auth.py` - 认证处理
  - [ ] `_transport.py` - HTTP 传输层
  - [ ] `_response.py` - 响应解包
- [ ] 实现通用数据模型
  - [ ] `models/common.py` - HttpApiResult, ErrorInfo, Pagination

**交付物**:
- ✅ 完整的项目结构
- ✅ 配置文件
- ✅ 文档
- ⏳ 核心基础设施代码
- ⏳ 通用数据模型

**预计时间**: 1 天

---

### Phase 2: Analytics 核心服务

**目标**: 实现 Analytics 的核心服务（Dashboard、Channel、EventMeta）

#### Dashboard 服务 (6 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| QueryDashboardNavigation | GET | /dashboard/navigation | 获取概览分组列表 |
| GetDashboardNavigation | GET | /dashboard/navigation/{id} | 获取指定概览分组 |
| QueryDashboardBookmark | GET | /dashboard/bookmark | 获取书签列表 |
| GetDashboardBookmark | GET | /dashboard/bookmark/{id} | 获取指定书签 |
| GetDashboardBookmarkData | POST | /dashboard/bookmark/{id}/data | 获取书签数据 |
| ExportDashboardBookmark | POST | /dashboard/bookmark/{id}/export | 导出书签 |

**数据模型**:
```python
# models/dashboard.py
class DashboardType(str, Enum):
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"

class Navigation(BaseModel):
    id: int
    name: str
    type: DashboardType
    owner_id: int = Field(alias="ownerId")
    created_at: datetime = Field(alias="createdAt")

class Bookmark(BaseModel):
    id: int
    name: str
    navigation_id: int = Field(alias="navigationId")
    # ... 其他字段

class BookmarkDataParams(BaseModel):
    start_date: str = Field(alias="startDate")
    end_date: str = Field(alias="endDate")
    # ... 其他参数

class BookmarkData(BaseModel):
    columns: list[str]
    rows: list[list[Any]]
    # ... 其他字段
```

#### Channel 服务 (5 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| QueryChannel | GET | /channel | 获取渠道列表 |
| QueryChannelLink | GET | /channel/link | 获取渠道链接列表 |
| GetChannelLink | GET | /channel/link/{id} | 获取指定链接 |
| GetChannelLinkData | POST | /channel/link/{id}/data | 获取链接数据 |
| ExportChannelLink | POST | /channel/link/{id}/export | 导出链接数据 |

**数据模型**:
```python
# models/channel.py
class Channel(BaseModel):
    id: int
    name: str
    created_at: datetime = Field(alias="createdAt")

class Link(BaseModel):
    id: int
    name: str
    channel_id: int = Field(alias="channelId")
    url: str
    # ... 其他字段

class LinkData(BaseModel):
    columns: list[str]
    rows: list[list[Any]]
```

#### EventMeta 服务 (2 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| ListEventsAll | GET | /event-meta/events/all | 获取事件列表 |
| ListEventTags | GET | /event-meta/events/tags | 获取事件标签列表 |

**数据模型**:
```python
# models/event_meta.py
class Event(BaseModel):
    id: int
    name: str
    cname: str
    is_virtual: bool
    tags: list[int]
    comment: str | None = None
    platforms: list[str]

class EventTag(BaseModel):
    id: int
    name: str
```

#### 任务清单

- [ ] 实现 Dashboard 数据模型
- [ ] 实现 Dashboard 服务类
- [ ] 实现 Channel 数据模型
- [ ] 实现 Channel 服务类
- [ ] 实现 EventMeta 数据模型
- [ ] 实现 EventMeta 服务类
- [ ] 编写 Dashboard 服务单元测试
- [ ] 编写 Channel 服务单元测试
- [ ] 编写 EventMeta 服务单元测试
- [ ] 实现 CLI dashboard 命令
- [ ] 实现 CLI channel 命令
- [ ] 实现 CLI event-meta 命令

**交付物**:
- Dashboard、Channel、EventMeta 完整实现
- 单元测试（80%+ 覆盖率）
- CLI 基础命令

**预计时间**: 3 天

---

### Phase 3: Analytics 数据服务

**目标**: 实现 Analytics 的数据相关服务（Dataset、PropertyMeta）

#### Dataset 服务 (1 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| DatasetDetail | GET | /dataset/detail | 查询业务模型详情信息 |

**数据模型**:
```python
# models/dataset.py
class Dataset(BaseModel):
    dataset_id: int
    name: str
    description: str | None = None
    # 业务模型详细配置和结构信息
```

#### PropertyMeta 服务 (6 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| ListAllEventProperties | GET | /property-meta/event-properties/all | 获取所有事件属性 |
| ListEventProperties | POST | /property-meta/event-properties | 获取指定的事件和相关属性 |
| ListAllUserProperties | GET | /property-meta/user-properties/all | 获取所有用户属性列表 |
| ListUserGroups | GET | /property-meta/user-groups/all | 获取所有用户分群列表 |
| ListUserTagsWithDir | GET | /property-meta/user-tags/dir | 获取带有目录结构的用户标签列表 |
| GetPropertyValues | POST | /property-meta/property/values | 获取属性候选值 |

**数据模型**:
```python
# models/property_meta.py
class EventProperty(BaseModel):
    id: int
    name: str
    cname: str
    data_type: str
    has_dict: bool

class UserProperty(BaseModel):
    id: int
    name: str
    cname: str
    data_type: str

class UserGroup(BaseModel):
    id: int
    name: str
    cname: str

class UserTag(BaseModel):
    id: int
    name: str
    parent_id: int | None = None
```

#### 任务清单

- [ ] 实现 Dataset 数据模型
- [ ] 实现 Dataset 服务类
- [ ] 实现 PropertyMeta 数据模型
- [ ] 实现 PropertyMeta 服务类
- [ ] 编写 Dataset 服务单元测试
- [ ] 编写 PropertyMeta 服务单元测试
- [ ] 实现 CLI dataset 命令
- [ ] 实现 CLI property-meta 命令

**交付物**:
- Dataset 和 PropertyMeta 服务完整实现
- 单元测试（80%+ 覆盖率）
- CLI 命令

**预计时间**: 2 天

---

### Phase 4: Analytics 分析模型和预警服务

**目标**: 实现 Analytics 的分析模型和智能预警服务（Model、SmartAlarm）

#### Model 服务 (5 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| QuerySegmentationReport | POST | /model/segmentation/report | 查询事件分析报告 |
| QueryFunnelReport | POST | /model/funnel/report | 查询漏斗分析报告 |
| QueryRetentionReport | POST | /model/retention/report | 查询留存分析报告 |
| QueryIntervalReport | POST | /model/interval/report | 查询间隔分析报告 |
| QueryAddictionReport | POST | /model/addiction/report | 查询分布分析报告 |

**数据模型**:
```python
# models/model.py
class SegmentationReportRequest(BaseModel):
    """事件分析请求参数."""
    # 事件分析参数

class SegmentationReportResponse(BaseModel):
    """事件分析报告响应."""
    metadata_columns: dict[str, str]
    truncated: bool
    detail_rows: list[list[Any]]

class FunnelReportRequest(BaseModel):
    """漏斗分析请求参数."""
    # 漏斗分析参数

class FunnelReportResponse(BaseModel):
    """漏斗分析报告响应."""
    # 漏斗分析结果

class RetentionReportRequest(BaseModel):
    """留存分析请求参数."""
    # 留存分析参数

class RetentionReportResponse(BaseModel):
    """留存分析报告响应."""
    # 留存分析结果

class IntervalReportRequest(BaseModel):
    """间隔分析请求参数."""
    # 间隔分析参数

class IntervalReportResponse(BaseModel):
    """间隔分析报告响应."""
    # 间隔分析结果

class AddictionReportRequest(BaseModel):
    """分布分析请求参数."""
    # 分布分析参数

class AddictionReportResponse(BaseModel):
    """分布分析报告响应."""
    # 分布分析结果
```

#### SmartAlarm 服务 (2 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| QueryAlarmConfig | GET | /smart-alarm/detail | 获取一个预警配置的详细信息 |
| QueryAllAlarms | POST | /smart-alarm/all | 获取所有的预警列表 |

**数据模型**:
```python
# models/smart_alarm.py
class SmartAlarmConfig(BaseModel):
    id: int
    title: str
    emails: list[str]
    unit: str  # HOUR, DAY, WEEK, MONTH, YEAR
    send_alarm: bool
    history: dict | None = None
```

#### 任务清单

- [ ] 实现 Model 数据模型（事件分析）
- [ ] 实现 Model 数据模型（漏斗分析）
- [ ] 实现 Model 数据模型（留存分析）
- [ ] 实现 Model 数据模型（间隔分析）
- [ ] 实现 Model 数据模型（分布分析）
- [ ] 实现 Model 服务类
- [ ] 实现 SmartAlarm 数据模型
- [ ] 实现 SmartAlarm 服务类
- [ ] 编写 Model 服务单元测试
- [ ] 编写 SmartAlarm 服务单元测试
- [ ] 实现 CLI model 命令
- [ ] 实现 CLI smart-alarm 命令

**交付物**:
- Model 服务完整实现（含 5 种分析类型）
- SmartAlarm 服务完整实现
- 单元测试（80%+ 覆盖率）
- CLI 命令

**预计时间**: 3 天

---

### Phase 5: Horizon 服务（神策数界）

**目标**: 实现 Horizon 的所有服务（Catalog、DataSubscription、Schema、Segment、Table、Tag）

#### Catalog 服务 (3 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| ListCatalogTrees | POST | /catalog/tree/list | 查询目录树 |
| BindCatalogResource | POST | /catalog/resource/bind | 挂载资源节点 |
| UnbindCatalogResource | POST | /catalog/resource/unbind | 解绑资源节点 |

#### DataSubscription 服务 (7 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| AddSubscriptionApplication | POST | /data-subscription/application/add | 创建订阅方 |
| AppendSubscriptionApplicationConfig | POST | /data-subscription/application/config/append | 补充订阅方配置信息 |
| GetSubscriptionApplication | POST | /data-subscription/application/get | 查询订阅方信息 |
| DeleteSubscriptionApplication | POST | /data-subscription/application/delete | 删除订阅方 |
| CreateDataSubscription | POST | /data-subscription/create | 创建数据订阅 |
| ListDataSubscriptions | GET | /data-subscription/list | 批量查询订阅记录列表 |
| BatchDeleteDataSubscriptions | POST | /data-subscription/batch-delete | 批量取消订阅 |

#### Schema 服务 (3 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| ListEventSchemas | POST | /schema/event/list | 获取事件定义列表 |
| GetEvent | POST | /schema/event/get | 获取事件定义 |
| CreateEvent | POST | /schema/event/create | 创建事件定义 |

#### Segment 服务 (2 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| ListSegmentDefinitions | POST | /segment/definition/list | 获取分群列表 |
| GetSegmentDefinition | POST | /segment/definition/get | 获取分群信息 |

#### Table 服务 (3 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| ListTables | POST | /table/list | 批量查询数据表信息 |
| GetTable | POST | /table/get | 查询数据表信息 |
| CreateTable | POST | /table/create | 创建数据表 |

#### Tag 服务 (2 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| ListTagDefinitions | POST | /tag/definition/list | 查询标签列表 |
| GetTagDefinition | POST | /tag/definition/get | 查询单个标签信息 |

#### 任务清单

- [ ] 实现 Catalog 数据模型和服务类
- [ ] 实现 DataSubscription 数据模型和服务类
- [ ] 实现 Schema 数据模型和服务类
- [ ] 实现 Segment 数据模型和服务类
- [ ] 实现 Table 数据模型和服务类
- [ ] 实现 Tag 数据模型和服务类
- [ ] 编写 Horizon 所有服务的单元测试
- [ ] 实现 CLI horizon 命令

**交付物**:
- Horizon 6 个服务完整实现
- 单元测试（80%+ 覆盖率）
- CLI 命令

**预计时间**: 4 天

---

### Phase 6: Portal 服务（神策业务门户）

**目标**: 实现 Portal 的所有服务（Identity、Management、ResourceManagement）

#### Identity 服务 (3 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| ListAccounts | GET | /identity/account/list | 获取账号列表 |
| GetAccount | GET | /identity/account/get | 获取单个账号 |
| GetAccountByName | GET | /identity/account/get-by-name | 通过名称获取单个账号 |

#### Management 服务 (8 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| ListBehaviorDefines | GET | /management/behavior/define/list | 获取操作日志定义列表 |
| ListBehaviors | GET | /management/behavior/list | 获取操作日志列表 |
| GetLicenseProduct | GET | /management/license/product | 查询许可证组件 |
| SendNoticeMessage | POST | /management/notice/send | 发送站内消息 |
| GetAllProductVersion | GET | /management/product/versions | 查询产品版本信息 |
| GetProjectByIdOrName | GET | /management/project/get | 获取项目详情 |
| GetProjectsByAccountId | GET | /management/project/get-by-account-id | 按账号 ID 查询项目 |
| ListProjects | GET | /management/project/list | 获取项目列表 |

#### ResourceManagement 服务 (4 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| ListAssets | POST | /resource-management/assets/list | 获取资源信息和使用量 |
| ListAssetQuery | POST | /resource-management/assets/query/list | 获取资源相关查询任务 |
| ListCompletedQueryTaskTable | GET | /resource-management/query/task/completed | 获取已完成查询任务 |
| ListExecutingQueryTaskTable | GET | /resource-management/query/task/executing | 获取执行中查询任务 |

#### 任务清单

- [ ] 实现 Identity 数据模型和服务类
- [ ] 实现 Management 数据模型和服务类
- [ ] 实现 ResourceManagement 数据模型和服务类
- [ ] 编写 Portal 所有服务的单元测试
- [ ] 实现 CLI portal 命令

**交付物**:
- Portal 3 个服务完整实现
- 单元测试（80%+ 覆盖率）
- CLI 命令

**预计时间**: 3 天

---

### Phase 7: 客户端集成

**目标**: 整合所有 16 个服务到统一客户端

#### 同步客户端

```python
# client.py
class SensorsDataClient:
    """神策数据同步客户端."""

    def __init__(
        self,
        base_url: str,
        api_key: str,
        project: str,
        *,
        timeout: float = 30.0,
        max_retries: int = 3,
    ):
        config = ClientConfig(...)
        transport = Transport(...)
        auth = AuthHandler(...)

        # Analytics 服务 (7 个)
        self.dashboard = DashboardService(transport, auth)
        self.channel = ChannelService(transport, auth)
        self.dataset = DatasetService(transport, auth)
        self.event_meta = EventMetaService(transport, auth)
        self.model = ModelService(transport, auth)
        self.property_meta = PropertyMetaService(transport, auth)
        self.smart_alarm = SmartAlarmService(transport, auth)

        # Horizon 服务 (6 个)
        self.catalog = CatalogService(transport, auth)
        self.data_subscription = DataSubscriptionService(transport, auth)
        self.schema = SchemaService(transport, auth)
        self.segment = SegmentService(transport, auth)
        self.table = TableService(transport, auth)
        self.tag = TagService(transport, auth)

        # Portal 服务 (3 个)
        self.identity = IdentityService(transport, auth)
        self.management = ManagementService(transport, auth)
        self.resource_management = ResourceManagementService(transport, auth)

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()

    def close(self) -> None:
        """关闭客户端."""
```

#### 任务清单

- [ ] 实现 _base_client.py（共享逻辑）
- [ ] 实现同步客户端 client.py
- [ ] 集成所有服务
- [ ] 添加上下文管理器支持
- [ ] 编写客户端集成测试
- [ ] 更新 __init__.py 导出

**交付物**:
- 完整的同步客户端
- 集成测试
- 使用示例

**预计时间**: 2 天

---

### Phase 8: CLI 完善

**目标**: 完善 CLI 工具的所有功能

#### CLI 功能清单

**配置管理**:
- [ ] `sa-openapi config init` - 交互式初始化
- [ ] `sa-openapi config list` - 列出所有 profile
- [ ] `sa-openapi config set-default` - 设置默认 profile
- [ ] `sa-openapi config show` - 显示当前配置

**Dashboard 命令**:
- [ ] `sa-openapi dashboard list` - 列出概览分组
- [ ] `sa-openapi dashboard get` - 获取指定分组
- [ ] `sa-openapi dashboard bookmarks` - 列出书签
- [ ] `sa-openapi dashboard bookmark-data` - 获取书签数据
- [ ] `sa-openapi dashboard export` - 导出书签

**Channel 命令**:
- [ ] `sa-openapi channel list` - 列出渠道
- [ ] `sa-openapi channel list-links` - 列出链接
- [ ] `sa-openapi channel get-link` - 获取链接详情
- [ ] `sa-openapi channel link-data` - 获取链接数据
- [ ] `sa-openapi channel export` - 导出链接数据

**Dataset 命令**:
- [ ] `sa-openapi dataset list` - 列出数据集
- [ ] `sa-openapi dataset get` - 获取数据集详情
- [ ] `sa-openapi dataset sql-query` - 执行 SQL 查询
- [ ] `sa-openapi dataset schema` - 获取 schema
- [ ] `sa-openapi dataset saved-queries` - 列出保存的查询
- [ ] `sa-openapi dataset create-query` - 创建保存的查询
- [ ] `sa-openapi dataset delete-query` - 删除保存的查询

**Model 命令**:
- [ ] `sa-openapi model funnel-report` - 漏斗分析
- [ ] `sa-openapi model retention-report` - 留存分析
- [ ] `sa-openapi model attribution-report` - 归因分析
- [ ] `sa-openapi model sql` - 自定义 SQL 查询
- [ ] `sa-openapi model explain-sql` - SQL 执行计划
- [ ] `sa-openapi model validate-sql` - SQL 语法验证

**输出格式**:
- [ ] 表格格式（rich Table）
- [ ] JSON 格式（rich JSON）
- [ ] CSV 格式

#### 任务清单

- [ ] 实现 cli/config.py（配置管理）
- [ ] 实现 cli/output.py（输出格式化）
- [ ] 实现 cli/dashboard.py
- [ ] 实现 cli/channel.py
- [ ] 实现 cli/dataset.py
- [ ] 实现 cli/model.py
- [ ] 实现 cli/main.py（主入口）
- [ ] 添加命令自动补全
- [ ] 编写 CLI 集成测试

**交付物**:
- 完整的 CLI 工具
- 所有命令实现
- 多种输出格式支持
- 多环境配置支持

**预计时间**: 3 天

---

### Phase 9: 高级特性

**目标**: 实现高级功能和优化

#### 异步客户端

```python
# async_client.py
class AsyncSensorsAnalyticsClient:
    """神策分析异步客户端."""

    def __init__(self, ...):
        self.dashboard = AsyncDashboardService(...)
        # ...

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()
```

#### 分页迭代器

```python
# _pagination.py
class PageIterator[T]:
    """分页迭代器."""

    def __iter__(self) -> Iterator[T]:
        page = 1
        while True:
            response = self._fetch_page(page)
            yield from response.items
            if not response.has_next:
                break
            page += 1

# 使用示例
for dataset in client.dataset.list_dataset_iter():
    print(dataset.name)
```

#### 重试逻辑

```python
# _transport.py
class Transport:
    def request_with_retry(self, ...):
        for attempt in range(self.max_retries):
            try:
                return self._client.request(...)
            except httpx.TimeoutError:
                if attempt == self.max_retries - 1:
                    raise
                wait_time = 2 ** attempt  # 指数退避
                time.sleep(wait_time)
```

#### 任务清单

- [ ] 实现 AsyncTransport
- [ ] 实现异步服务类
- [ ] 实现异步客户端
- [ ] 实现分页迭代器
- [ ] 实现重试逻辑（指数退避）
- [ ] 实现请求日志记录
- [ ] 编写异步功能测试
- [ ] 性能基准测试

**交付物**:
- 异步客户端
- 分页迭代器
- 重试机制
- 性能优化

**预计时间**: 2 天

---

### Phase 10: 测试和文档

**目标**: 达到发布标准

#### 测试要求

**单元测试**:
- [ ] 所有服务方法 100% 覆盖
- [ ] 错误处理路径测试
- [ ] 边界条件测试
- [ ] Mock 所有 HTTP 请求

**集成测试**:
- [ ] 客户端端到端测试
- [ ] CLI 端到端测试
- [ ] 多环境配置测试

**类型测试**:
- [ ] mypy --strict 通过
- [ ] 所有公开 API 有类型注解
- [ ] 无类型忽略

**代码质量**:
- [ ] ruff check 通过
- [ ] ruff format 通过
- [ ] 测试覆盖率 ≥ 90%

#### 文档要求

**代码文档**:
- [ ] 所有公开函数有 docstring
- [ ] 使用 Google 风格
- [ ] 包含使用示例

**用户文档**:
- [ ] README.md 完善
- [ ] API 参考完整
- [ ] 使用示例丰富
- [ ] 故障排除指南

**开发文档**:
- [ ] CONTRIBUTING.md
- [ ] 架构设计文档
- [ ] API 映射表

#### 任务清单

- [ ] 编写完整单元测试（覆盖率 ≥ 90%）
- [ ] 编写集成测试
- [ ] mypy 类型检查通过
- [ ] ruff 代码质量检查通过
- [ ] 完善 README.md
- [ ] 编写 API 参考文档
- [ ] 添加更多使用示例
- [ ] 编写故障排除指南

**交付物**:
- 90%+ 测试覆盖率
- 完整文档
- 类型检查通过
- 代码质量检查通过

**预计时间**: 3 天

---

### Phase 11: 发布准备

**目标**: 准备 v0.1.0 发布

#### 发布清单

**版本管理**:
- [ ] 更新版本号（pyproject.toml）
- [ ] 更新版本号（__init__.py）
- [ ] 编写变更日志（CHANGELOG.md）
- [ ] 创建 Git tag

**包构建**:
- [ ] 验证包可以正确构建
- [ ] 验证包可以正确安装
- [ ] 验证 CLI 可以正常运行

**CI/CD**:
- [ ] 所有 CI 检查通过
- [ ] 配置 PyPI trusted publishing
- [ ] 测试发布流程

**文档**:
- [ ] 确认 README 准确
- [ ] 确认示例代码可运行
- [ ] 添加徽章（版本、CI、覆盖率）

#### 任务清单

- [ ] 完成所有功能开发
- [ ] 所有测试通过
- [ ] 文档完整
- [ ] 更新版本号
- [ ] 编写 CHANGELOG.md
- [ ] 创建 Git tag (v0.1.0)
- [ ] 测试 PyPI 发布（TestPyPI）
- [ ] 正式发布到 PyPI

**交付物**:
- v0.1.0 版本发布
- PyPI 包可安装
- 完整文档

**预计时间**: 1 天

---

## 时间线总览

| 阶段 | 内容 | 预计时间 | 累计时间 |
|------|------|----------|----------|
| Phase 1 | 基础框架 | 1 天 | 1 天 |
| Phase 2 | Analytics 核心服务 (Dashboard, Channel, EventMeta) | 3 天 | 4 天 |
| Phase 3 | Analytics 数据服务 (Dataset, PropertyMeta) | 2 天 | 6 天 |
| Phase 4 | Analytics 分析模型和预警 (Model, SmartAlarm) | 3 天 | 9 天 |
| Phase 5 | Horizon 服务 (6 个服务) | 4 天 | 13 天 |
| Phase 6 | Portal 服务 (3 个服务) | 3 天 | 16 天 |
| Phase 7 | 客户端集成 | 2 天 | 18 天 |
| Phase 8 | CLI 完善 | 3 天 | 21 天 |
| Phase 9 | 高级特性 | 2 天 | 23 天 |
| Phase 10 | 测试和文档 | 3 天 | 26 天 |
| Phase 11 | 发布准备 | 1 天 | 27 天 |

**总计**: 约 27 个工作日（5-6 周）

## 优先级

### P0 (必须)
- Phase 1: 基础框架
- Phase 2-4: Analytics 所有服务（7 个服务）
- Phase 7: 客户端集成
- Phase 8: 基础 CLI 命令
- Phase 10: 基础测试（≥70% 覆盖率）

### P1 (重要)
- Phase 5-6: Horizon 和 Portal 服务（9 个服务）
- Phase 8: 完整 CLI 功能
- Phase 9: 异步客户端
- Phase 10: 完整测试（≥90% 覆盖率）

### P2 (可选)
- Phase 9: 分页迭代器、重试逻辑
- 性能优化
- 批量操作 API

## 风险和缓解

### 风险 1: OpenAPI 规范不完整或有误

**缓解措施**:
- 仔细阅读规范文件
- 与实际 API 对比验证
- 预留时间调整模型

### 风险 2: 依赖库版本冲突

**缓解措施**:
- 使用宽松的版本约束
- 测试多个 Python 版本
- 持续集成验证

### 风险 3: 测试覆盖不足

**缓解措施**:
- 每个 Phase 完成后立即编写测试
- 使用 pytest-cov 监控覆盖率
- CI 强制覆盖率检查

### 风险 4: 性能问题

**缓解措施**:
- 使用连接池
- 异步客户端支持并发
- 性能基准测试

## 成功标准

### 功能完整性
- ✅ 64 个 API 端点全部实现
- ✅ 16 个服务全部可用
- ✅ SDK 和 CLI 都可用
- ✅ 同步和异步客户端

### 质量标准
- ✅ 测试覆盖率 ≥ 90%
- ✅ mypy --strict 通过
- ✅ ruff check 通过
- ✅ 所有 CI 检查通过

### 文档标准
- ✅ README 完整
- ✅ API 参考完整
- ✅ 使用示例丰富
- ✅ 代码有文档字符串

### 发布标准
- ✅ 可从 PyPI 安装
- ✅ CLI 可正常运行
- ✅ 示例代码可运行

## 下一步

从 **Phase 1: 基础框架** 开始实施：

1. 实现 `_exceptions.py`
2. 实现 `_config.py`
3. 实现 `_auth.py`
4. 实现 `_transport.py`
5. 实现 `_response.py`
6. 实现 `models/common.py`

每完成一个组件，立即编写单元测试。
