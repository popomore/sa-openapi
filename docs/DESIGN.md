# sa-openapi 设计方案

## 项目概述

基于神策分析 OpenAPI 3.0.1 规范构建 Python SDK 和 CLI 工具，提供类型安全、易用的接口来访问神策分析平台的 24 个 API 端点。

## 核心设计原则

### 1. 类型安全优先

- 使用 Pydantic v2 进行数据验证和序列化
- 所有公开 API 提供完整类型注解
- mypy strict 模式强制类型检查
- 运行时数据验证确保正确性

### 2. 用户友好

- 命名空间式 API 访问（`client.dashboard.list_navigation()`）
- 自动处理认证头注入
- 统一的错误处理机制
- 清晰的异常层次结构

### 3. 现代化架构

- 基于 httpx（原生支持异步）
- 同步/异步双客户端支持
- 自动分页迭代器
- 指数退避重试机制

### 4. CLI 优先体验

- 简洁的命令结构
- 多种输出格式（table/json/csv）
- 多环境配置支持
- 环境变量覆盖

## 技术架构

### 分层设计

```
┌─────────────────────────────────────────┐
│          User Application               │
├─────────────────────────────────────────┤
│   SensorsAnalyticsClient (Sync/Async)   │
├─────────────┬───────────────────────────┤
│  Dashboard  │  Channel  │ Dataset │Model│  ← Service Layer
├─────────────┴───────────────────────────┤
│         Pydantic Models (v2)            │  ← Model Layer
├─────────────────────────────────────────┤
│  Response Handler │ Auth │ Pagination   │  ← Core Layer
├─────────────────────────────────────────┤
│            httpx Transport              │  ← HTTP Layer
├─────────────────────────────────────────┤
│      神策分析 OpenAPI Endpoints          │
└─────────────────────────────────────────┘
```

### 核心组件

#### 1. Transport Layer (`_transport.py`)

**职责**: 封装 httpx，提供统一的 HTTP 请求接口

```python
class Transport:
    """HTTP 传输层."""

    def __init__(self, base_url: str, timeout: float, max_retries: int):
        self._client = httpx.Client(
            base_url=base_url,
            timeout=timeout,
        )

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> httpx.Response:
        """发送 HTTP 请求."""
```

**特性**:
- 自动重试（可配置次数）
- 请求/响应日志记录
- 超时控制
- 连接池管理

#### 2. Authentication (`_auth.py`)

**职责**: 自动注入认证头

```python
class AuthHandler:
    """认证处理器."""

    def __init__(self, api_key: str, project: str):
        self.api_key = api_key
        self.project = project

    def inject_headers(self, headers: dict[str, str]) -> dict[str, str]:
        """注入认证头."""
        return {
            **headers,
            "api-key": self.api_key,
            "sensorsdata-project": self.project,
        }
```

**认证头**:
- `api-key`: 全局唯一密钥
- `sensorsdata-project`: 项目名称

#### 3. Response Handler (`_response.py`)

**职责**: 解包 `HttpApiResult<T>` 响应结构

```python
@dataclass
class HttpApiResult[T]:
    """统一响应结构."""
    code: str
    message: str
    request_id: str
    data: T | None = None
    error_info: ErrorInfo | None = None
```

**处理流程**:
1. 解析 JSON 响应
2. 验证 `code` 字段
3. 成功 (SUCCESS) → 返回 `data`
4. 失败 → 根据 `code` 抛出对应异常

**异常映射**:
```python
CODE_TO_EXCEPTION = {
    "UNAUTHORIZED": AuthenticationError,
    "NOT_FOUND": NotFoundError,
    "INVALID_ARGUMENT": ValidationError,
    "PERMISSION_DENIED": PermissionError,
    "RATE_LIMIT_EXCEEDED": RateLimitError,
    # ... 其他错误码
}
```

#### 4. Exception Hierarchy (`_exceptions.py`)

```python
SensorsAnalyticsError (基类)
├── AuthenticationError        # 认证失败
├── AuthorizationError         # 权限不足
├── NotFoundError              # 资源不存在
├── ValidationError            # 参数验证失败
├── RateLimitError             # 频率限制
├── ServerError                # 服务器错误
└── NetworkError               # 网络错误
```

所有异常包含:
- `code`: 错误码
- `message`: 错误消息
- `request_id`: 请求 ID（便于追踪）
- `error_info`: 详细错误信息

#### 5. Configuration (`_config.py`)

```python
@dataclass
class ClientConfig:
    """客户端配置."""
    base_url: str
    api_key: str
    project: str
    timeout: float = 30.0
    max_retries: int = 3

    @classmethod
    def from_env(cls) -> ClientConfig:
        """从环境变量加载配置."""
        return cls(
            base_url=os.getenv("SA_BASE_URL", ""),
            api_key=os.getenv("SA_API_KEY", ""),
            project=os.getenv("SA_PROJECT", "default"),
        )
```

#### 6. Pagination (`_pagination.py`)

**职责**: 为支持分页的 API 提供迭代器

```python
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
```

使用示例:
```python
# 自动处理分页
for dataset in client.dataset.list_dataset_iter():
    print(dataset.name)
```

### 数据模型设计

#### 通用模型 (`models/common.py`)

```python
class HttpApiResult[T](BaseModel, Generic[T]):
    """API 统一响应结构."""
    code: str
    message: str
    request_id: str = Field(alias="requestId")
    data: T | None = None
    error_info: ErrorInfo | None = Field(None, alias="errorInfo")

class ErrorInfo(BaseModel):
    """错误详情."""
    code: str
    message: str
    details: dict[str, Any] | None = None

class Pagination(BaseModel):
    """分页信息."""
    page: int
    page_size: int = Field(alias="pageSize")
    total: int
    has_next: bool = Field(alias="hasNext")
```

#### 服务模型

每个服务有独立的模型文件:

- `models/dashboard.py`: Navigation, Bookmark, BookmarkData
- `models/channel.py`: Channel, Link, LinkData
- `models/dataset.py`: Dataset, QueryResult, Schema, SavedQuery
- `models/model.py`: FunnelReport, RetentionReport, AttributionReport

**模型特性**:
- 使用 Pydantic v2 BaseModel
- 自动 snake_case ↔ camelCase 转换
- 严格类型验证
- 可选字段使用 `Field(default=None)`
- 枚举类型使用 `Literal` 或 `Enum`

### 服务层设计

#### Base Service

```python
class BaseService:
    """服务基类."""

    def __init__(self, transport: Transport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth

    def _request(
        self,
        method: str,
        path: str,
        response_model: type[T],
        **kwargs: Any,
    ) -> T:
        """发送请求并解包响应."""
        headers = self._auth.inject_headers(kwargs.pop("headers", {}))
        response = self._transport.request(method, path, headers=headers, **kwargs)
        result = HttpApiResult[response_model].model_validate_json(response.content)

        if result.code != "SUCCESS":
            raise get_exception(result.code, result.message, result.request_id)

        return result.data
```

#### Dashboard Service (`services/dashboard.py`)

```python
class DashboardService(BaseService):
    """Dashboard 服务."""

    def list_navigation(
        self,
        type: Literal["PRIVATE", "PUBLIC"] | None = None,
    ) -> list[Navigation]:
        """获取概览分组列表."""
        return self._request(
            "GET",
            "/api/v3/analytics/v1/dashboard/navigation",
            response_model=list[Navigation],
            params={"type": type} if type else None,
        )

    def get_bookmark_data(
        self,
        bookmark_id: int,
        params: BookmarkDataParams,
    ) -> BookmarkData:
        """获取书签数据."""
        return self._request(
            "POST",
            f"/api/v3/analytics/v1/dashboard/bookmark/{bookmark_id}/data",
            response_model=BookmarkData,
            json=params.model_dump(exclude_none=True),
        )
```

### 客户端设计

#### 同步客户端 (`client.py`)

```python
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
        config = ClientConfig(
            base_url=base_url,
            api_key=api_key,
            project=project,
            timeout=timeout,
            max_retries=max_retries,
        )

        transport = Transport(config.base_url, config.timeout, config.max_retries)
        auth = AuthHandler(config.api_key, config.project)

        self.dashboard = DashboardService(transport, auth)
        self.channel = ChannelService(transport, auth)
        self.dataset = DatasetService(transport, auth)
        self.model = ModelService(transport, auth)

    def close(self) -> None:
        """关闭客户端."""
        self._transport.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *args: Any) -> None:
        self.close()
```

#### 异步客户端 (`async_client.py`)

```python
class AsyncSensorsAnalyticsClient:
    """神策分析异步客户端."""

    def __init__(self, ...):
        # 类似同步客户端，但使用 AsyncTransport
        self.dashboard = AsyncDashboardService(...)
        # ...

    async def aclose(self) -> None:
        """关闭客户端."""
        await self._transport.aclose()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *args: Any) -> None:
        await self.aclose()
```

### CLI 设计

#### 配置管理 (`cli/config.py`)

```python
class CLIConfig:
    """CLI 配置管理."""

    CONFIG_PATH = Path.home() / ".sa-openapi.toml"

    @classmethod
    def load(cls, profile: str = "default") -> ClientConfig:
        """加载配置."""
        if not cls.CONFIG_PATH.exists():
            raise ConfigError("配置文件不存在，请运行 'sa config init'")

        data = toml.load(cls.CONFIG_PATH)
        if profile not in data:
            raise ConfigError(f"Profile '{profile}' 不存在")

        return ClientConfig(**data[profile])

    @classmethod
    def init(cls) -> None:
        """交互式初始化配置."""
        base_url = click.prompt("Base URL")
        api_key = click.prompt("API Key", hide_input=True)
        project = click.prompt("Project", default="default")

        config = {
            "default": {
                "base_url": base_url,
                "api_key": api_key,
                "project": project,
            }
        }

        with open(cls.CONFIG_PATH, "w") as f:
            toml.dump(config, f)
```

#### 输出格式化 (`cli/output.py`)

```python
class OutputFormatter:
    """输出格式化器."""

    @staticmethod
    def format_table(data: list[dict[str, Any]]) -> None:
        """表格格式."""
        table = Table()
        if data:
            for key in data[0].keys():
                table.add_column(key)
            for row in data:
                table.add_row(*[str(v) for v in row.values()])
        console.print(table)

    @staticmethod
    def format_json(data: Any) -> None:
        """JSON 格式."""
        console.print_json(data=data)

    @staticmethod
    def format_csv(data: list[dict[str, Any]]) -> None:
        """CSV 格式."""
        if data:
            writer = csv.DictWriter(sys.stdout, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
```

#### 命令结构 (`cli/main.py`)

```python
@click.group()
@click.option("--profile", default="default", help="配置 profile")
@click.option("--format", type=click.Choice(["table", "json", "csv"]), default="table")
@click.pass_context
def cli(ctx: click.Context, profile: str, format: str) -> None:
    """神策分析 OpenAPI CLI 工具."""
    ctx.ensure_object(dict)
    ctx.obj["config"] = CLIConfig.load(profile)
    ctx.obj["format"] = format

@cli.group()
def config() -> None:
    """配置管理."""

@config.command()
def init() -> None:
    """初始化配置."""
    CLIConfig.init()

@cli.group()
def dashboard() -> None:
    """Dashboard 服务."""

@dashboard.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    """列出概览分组."""
    client = SensorsAnalyticsClient(**ctx.obj["config"])
    data = client.dashboard.list_navigation()
    OutputFormatter.format(data, ctx.obj["format"])
```

## API Base Path 策略

神策分析 API 使用两个不同的 base path:

1. **Dashboard/Channel/Dataset**: `/api/v3/analytics/v1`
2. **Model**: `/api/v3/analytics/v2`

**解决方案**: 在 Transport 层处理

```python
class Transport:
    BASE_PATHS = {
        "v1": "/api/v3/analytics/v1",
        "v2": "/api/v3/analytics/v2",
    }

    def request(self, method: str, path: str, **kwargs: Any) -> httpx.Response:
        # path 已包含完整路径，如 "/api/v3/analytics/v1/dashboard/navigation"
        full_url = self._client.base_url.join(path)
        return self._client.request(method, full_url, **kwargs)
```

## 错误处理策略

### 1. HTTP 层错误

- `httpx.TimeoutError` → `NetworkError`
- `httpx.ConnectError` → `NetworkError`
- `httpx.HTTPStatusError` → 根据状态码转换

### 2. API 层错误

- 解析响应 `code` 字段
- 映射到对应异常类型
- 包含 `request_id` 便于追踪

### 3. 用户友好的错误消息

```python
try:
    result = client.dataset.sql_query(dataset_id=999, sql="SELECT *")
except NotFoundError as e:
    print(f"数据集不存在: {e.message}")
    print(f"请求 ID: {e.request_id}")
```

## 性能优化

### 1. 连接复用

- httpx.Client 使用连接池
- 避免每次请求创建新连接

### 2. 响应流式处理

- 大数据导出使用流式响应
- 避免内存占用过大

### 3. 并发控制

- 异步客户端支持并发请求
- 使用 `asyncio.gather()` 批量操作

## 安全考虑

### 1. 凭证管理

- 配置文件权限检查（仅用户可读）
- 支持环境变量（容器化部署）
- 不在日志中输出敏感信息

### 2. 输入验证

- Pydantic 自动验证输入
- SQL 参数化（防止注入）
- URL 参数编码

### 3. HTTPS Only

- 强制使用 HTTPS
- 拒绝不安全的连接

## 测试策略

### 1. 单元测试

- 使用 `pytest-httpx` mock HTTP 请求
- 覆盖所有服务方法
- 测试错误处理路径

### 2. 集成测试（可选）

- 对真实实例执行只读操作
- 使用测试环境

### 3. 类型测试

- mypy strict 模式
- 确保类型安全

## 文档策略

### 1. 代码文档

- 所有公开 API 有 docstring
- 使用 Google 风格
- 包含使用示例

### 2. README

- 快速开始指南
- API 参考表格
- 常见用例

### 3. 类型提示

- 完整的类型注解
- IDE 自动补全支持

## 发布流程

1. **版本管理**: 语义化版本 (SemVer)
2. **变更日志**: 记录每个版本的变更
3. **CI/CD**: GitHub Actions 自动测试和发布
4. **PyPI**: 自动发布到 PyPI

## 未来扩展

### 1. 批量操作 API

```python
client.dataset.batch_query([
    {"dataset_id": 1, "sql": "..."},
    {"dataset_id": 2, "sql": "..."},
])
```

### 2. 缓存层

```python
@cached(ttl=300)
def get_dataset(dataset_id: int) -> Dataset:
    ...
```

### 3. Webhook 支持

处理神策分析的异步回调。

### 4. 插件系统

允许用户扩展功能。
