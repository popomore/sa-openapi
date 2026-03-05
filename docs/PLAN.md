# sa-openapi 实施计划

## 项目概述

基于 4 个神策分析 OpenAPI 规范文件，实现完整的 Python SDK 和 CLI 工具。

**API 统计**:
- Dashboard (v1): 6 个端点
- Channel (v1): 5 个端点
- Dataset (v1): 7 个端点
- Model (v2): 6 个端点
- **总计**: 24 个端点

## 实施阶段

### Phase 1: 基础框架 ✅

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

### Phase 2: Dashboard & Channel 服务

**目标**: 实现前两个服务的完整功能

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

#### 任务清单

- [ ] 实现 Dashboard 数据模型
- [ ] 实现 Dashboard 服务类
- [ ] 实现 Channel 数据模型
- [ ] 实现 Channel 服务类
- [ ] 编写 Dashboard 服务单元测试
- [ ] 编写 Channel 服务单元测试
- [ ] 实现 CLI dashboard 命令
- [ ] 实现 CLI channel 命令

**交付物**:
- Dashboard 和 Channel 完整实现
- 单元测试（80%+ 覆盖率）
- CLI 基础命令

**预计时间**: 2 天

---

### Phase 3: Dataset 服务

**目标**: 实现最复杂的 Dataset 服务

#### Dataset 服务 (7 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| QueryDataset | GET | /dataset | 获取数据集列表 |
| GetDataset | GET | /dataset/{id} | 获取指定数据集 |
| QueryDatasetData | POST | /dataset/{id}/data | 执行 SQL 查询 |
| GetDatasetSchema | GET | /dataset/{id}/schema | 获取数据集 schema |
| QueryDatasetSavedQuery | GET | /dataset/{id}/saved_query | 获取保存的查询 |
| CreateDatasetSavedQuery | POST | /dataset/{id}/saved_query | 创建保存的查询 |
| DeleteDatasetSavedQuery | DELETE | /dataset/{id}/saved_query/{query_id} | 删除保存的查询 |

**数据模型**:
```python
# models/dataset.py
class Dataset(BaseModel):
    id: int
    name: str
    description: str | None = None
    type: str
    created_at: datetime = Field(alias="createdAt")

class QueryParams(BaseModel):
    sql: str
    limit: int | None = None
    offset: int | None = None

class QueryResult(BaseModel):
    columns: list[str]
    rows: list[list[Any]]
    total: int
    elapsed_ms: int = Field(alias="elapsedMs")

class SchemaField(BaseModel):
    name: str
    type: str
    nullable: bool
    comment: str | None = None

class Schema(BaseModel):
    fields: list[SchemaField]

class SavedQuery(BaseModel):
    id: int
    name: str
    sql: str
    dataset_id: int = Field(alias="datasetId")
    created_at: datetime = Field(alias="createdAt")
```

#### 任务清单

- [ ] 实现 Dataset 数据模型
- [ ] 实现 Dataset 服务类
- [ ] 实现 SQL 查询功能
- [ ] 实现 Schema 获取功能
- [ ] 实现保存查询管理
- [ ] 编写 Dataset 服务单元测试
- [ ] 实现 CLI dataset 命令
- [ ] 实现 SQL 查询 CLI 命令

**交付物**:
- Dataset 服务完整实现
- SQL 查询功能
- 单元测试（80%+ 覆盖率）
- CLI dataset 命令

**预计时间**: 2 天

---

### Phase 4: Model 服务

**目标**: 实现分析模型服务（漏斗、留存、归因）

#### Model 服务 (6 个端点)

| 端点 | 方法 | 路径 | 描述 |
|------|------|------|------|
| GetFunnelReport | POST | /model/funnel/report | 漏斗分析报告 |
| GetRetentionReport | POST | /model/retention/report | 留存分析报告 |
| GetAttributionReport | POST | /model/attribution/report | 归因分析报告 |
| QueryModelData | POST | /model/data | 自定义 SQL 查询 |
| ExplainModelSql | POST | /model/sql/explain | SQL 执行计划 |
| ValidateModelSql | POST | /model/sql/validate | SQL 语法验证 |

**数据模型**:
```python
# models/model.py
class Measure(BaseModel):
    """指标定义."""
    event: str
    aggregator: str  # COUNT, SUM, AVG, etc.
    property: str | None = None

class Filter(BaseModel):
    """筛选条件."""
    property: str
    operator: str  # =, !=, >, <, IN, etc.
    value: Any

class ByField(BaseModel):
    """分组字段."""
    property: str
    type: str | None = None

class FunnelParams(BaseModel):
    """漏斗分析参数."""
    measures: list[Measure]
    filter: Filter | None = None
    by_fields: list[ByField] | None = Field(None, alias="byFields")
    window: int | None = None  # 转化窗口期（天）

class FunnelStep(BaseModel):
    """漏斗步骤结果."""
    step: int
    event: str
    total: int
    conversion_rate: float = Field(alias="conversionRate")
    avg_duration: float | None = Field(None, alias="avgDuration")

class FunnelReport(BaseModel):
    """漏斗分析报告."""
    steps: list[FunnelStep]
    total: int
    overall_conversion: float = Field(alias="overallConversion")

class RetentionParams(BaseModel):
    """留存分析参数."""
    initial_event: str = Field(alias="initialEvent")
    return_event: str = Field(alias="returnEvent")
    filter: Filter | None = None
    by_fields: list[ByField] | None = Field(None, alias="byFields")
    periods: list[int]  # 留存周期，如 [1, 3, 7, 14, 30]

class RetentionData(BaseModel):
    """留存数据."""
    period: int
    retention_rate: float = Field(alias="retentionRate")
    returned_users: int = Field(alias="returnedUsers")
    total_users: int = Field(alias="totalUsers")

class RetentionReport(BaseModel):
    """留存分析报告."""
    data: list[RetentionData]
    cohort_size: int = Field(alias="cohortSize")

class AttributionParams(BaseModel):
    """归因分析参数."""
    conversion_event: str = Field(alias="conversionEvent")
    touch_points: list[str] = Field(alias="touchPoints")
    model: str  # FIRST_TOUCH, LAST_TOUCH, LINEAR, etc.
    window: int | None = None

class AttributionData(BaseModel):
    """归因数据."""
    touch_point: str = Field(alias="touchPoint")
    credit: float
    conversions: int

class AttributionReport(BaseModel):
    """归因分析报告."""
    data: list[AttributionData]
    total_conversions: int = Field(alias="totalConversions")

class SqlQueryParams(BaseModel):
    """SQL 查询参数."""
    sql: str
    limit: int | None = None

class SqlExplainResult(BaseModel):
    """SQL 执行计划."""
    plan: str
    estimated_cost: float = Field(alias="estimatedCost")
    estimated_rows: int = Field(alias="estimatedRows")

class SqlValidateResult(BaseModel):
    """SQL 验证结果."""
    valid: bool
    error: str | None = None
```

#### 任务清单

- [ ] 实现 Model 数据模型（漏斗）
- [ ] 实现 Model 数据模型（留存）
- [ ] 实现 Model 数据模型（归因）
- [ ] 实现 Model 服务类
- [ ] 实现漏斗分析功能
- [ ] 实现留存分析功能
- [ ] 实现归因分析功能
- [ ] 实现 SQL 查询/验证功能
- [ ] 编写 Model 服务单元测试
- [ ] 实现 CLI model 命令

**交付物**:
- Model 服务完整实现（含 3 种分析类型）
- SQL 查询和验证功能
- 单元测试（80%+ 覆盖率）
- CLI model 命令

**预计时间**: 3 天

---

### Phase 5: 客户端集成

**目标**: 整合所有服务到统一客户端

#### 同步客户端

```python
# client.py
class SensorsAnalyticsClient:
    """神策分析同步客户端."""

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

        # 初始化服务
        self.dashboard = DashboardService(transport, auth)
        self.channel = ChannelService(transport, auth)
        self.dataset = DatasetService(transport, auth)
        self.model = ModelService(transport, auth)

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

**预计时间**: 1 天

---

### Phase 6: CLI 完善

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

**预计时间**: 2 天

---

### Phase 7: 高级特性

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

### Phase 8: 测试和文档

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

**预计时间**: 2 天

---

### Phase 9: 发布准备

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
| Phase 2 | Dashboard & Channel | 2 天 | 3 天 |
| Phase 3 | Dataset 服务 | 2 天 | 5 天 |
| Phase 4 | Model 服务 | 3 天 | 8 天 |
| Phase 5 | 客户端集成 | 1 天 | 9 天 |
| Phase 6 | CLI 完善 | 2 天 | 11 天 |
| Phase 7 | 高级特性 | 2 天 | 13 天 |
| Phase 8 | 测试和文档 | 2 天 | 15 天 |
| Phase 9 | 发布准备 | 1 天 | 16 天 |

**总计**: 约 16 个工作日（3-4 周）

## 优先级

### P0 (必须)
- Phase 1-5: 基础框架到客户端集成
- Phase 6: 基础 CLI 命令
- Phase 8: 基础测试（≥70% 覆盖率）

### P1 (重要)
- Phase 6: 完整 CLI 功能
- Phase 7: 异步客户端
- Phase 8: 完整测试（≥90% 覆盖率）

### P2 (可选)
- Phase 7: 分页迭代器、重试逻辑
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
- ✅ 24 个 API 端点全部实现
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
