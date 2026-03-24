---
name: sa-openapi-dev
description: >
  sa-openapi 项目的开发辅助工具，用于神策分析（SensorsData Analytics）OpenAPI Python SDK。
  当用户在 sa-openapi 项目中需要添加新的 API 端点、新增服务方法、创建 Pydantic 数据模型、
  添加 CLI 命令、运行测试、执行代码质量检查时，应使用此 skill。
  适用场景：新增神策分析 API 支持、扩展任意服务（Dashboard/Channel/Dataset/EventMeta/PropertyMeta/Model/SmartAlarm）、
  调试 SDK、运行 pytest/ruff/mypy、查看 OpenAPI 规范（docs/openapi/）。
---

# sa-openapi 开发指南

## 项目概览

sa-openapi 是神策分析（SensorsData Analytics）的 Python SDK 和 CLI 工具。

**技术栈**：Python 3.10+、aiohttp、Pydantic v2、Click、Rich

**已实现的 7 个服务**（Analytics 全覆盖）：

| 服务 | 模块 | CLI group | 端点数 |
|------|------|-----------|--------|
| Dashboard | `services/dashboard.py` | `dashboard` | 6 |
| Channel | `services/channel.py` | `channel` | 5 |
| Dataset | `services/dataset.py` | `dataset` | 7 |
| EventMeta | `services/event_meta.py` | `event-meta` | 2 |
| PropertyMeta | `services/property_meta.py` | `property-meta` | 6 |
| Model | `services/model.py` | `model` | 10 |
| SmartAlarm | `services/smart_alarm.py` | `smart-alarm` | 2 |

**代码目录**：
```
src/sa_openapi/
├── models/        # Pydantic 数据模型
├── services/      # 异步 API 服务实现
├── cli/           # Click CLI 命令
├── _transport.py  # HTTP 传输层（aiohttp）
├── _auth.py       # 认证（api-key header）
├── _config.py     # 配置（~/.sa-openapi.toml + 环境变量）
├── async_client.py # 异步客户端
└── client.py       # 同步客户端（通过后台事件循环包装）
```

**OpenAPI 规范文件位置**：`docs/openapi/3.0.4-analytics-*-swagger.json`

---

## 添加新 API 端点：三步流程

始终按照 **模型 → 服务 → CLI** 的顺序实现。

### 第一步：定义 Pydantic 模型（`models/<service>.py`）

```python
from datetime import datetime
from pydantic import BaseModel, Field

class MyResource(BaseModel):
    """资源描述。"""
    id: int
    name: str
    # API 返回 camelCase，用 Field(alias=...) 映射为 snake_case
    owner_id: int = Field(alias="ownerId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime | None = Field(None, alias="updatedAt")

    model_config = {"populate_by_name": True}

class MyResourceParams(BaseModel):
    """请求参数模型（POST body）。"""
    start_date: str = Field(alias="startDate")
    end_date: str = Field(alias="endDate")

    model_config = {"populate_by_name": True}
```

**关键规则**：
- camelCase 字段用 `Field(alias="camelCase")` 映射
- 所有模型必须加 `model_config = {"populate_by_name": True}`
- **注意**：Dataset/EventMeta/PropertyMeta/SmartAlarm 的 API 字段名已经是 snake_case，无需 alias
- 序列化用 `model.model_dump(by_alias=True, exclude_none=True)`

### 第二步：实现服务方法（`services/<service>.py`）

```python
async def get_resource(self, resource_id: int) -> MyResource:
    """获取资源详情。"""
    response = await self._transport.get(
        f"{self._base_url}/resource/{resource_id}",
    )
    data = response.json()
    return MyResource(**data.get("data", {}))

async def list_resources(
    self,
    params: MyResourceParams | dict[str, Any] | None = None,
) -> list[MyResource]:
    """列出资源。"""
    if isinstance(params, dict):
        body = params
    elif params is None:
        body = {}
    else:
        body = params.model_dump(by_alias=True, exclude_none=True)

    response = await self._transport.post(
        f"{self._base_url}/resource/list",
        json=body,
    )
    data = response.json()
    return [MyResource(**item) for item in data.get("data", [])]
```

**关键规则**：
- 所有服务方法必须是 `async def`
- 响应固定结构 `{"data": ..., "code": 200}`，用 `data.get("data", {})` 或 `data.get("data", [])` 取数据
- 某些 API 返回嵌套结构，如 `{"data": {"events": [...]}}` — 需要再取一层
- **Base URL 选择**：Dashboard/Channel/Dataset/EventMeta/PropertyMeta/SmartAlarm 用 `transport.config.dashboard_v1_base_url`；Model 用 `transport.config.model_v1_base_url`（两者当前指向同一路径）

### 第三步：添加 CLI 命令（`cli/<service>.py`）

```python
@service_group.command("get")
@click.argument("resource_id", type=int)
@click.option("--format", "output_format",
              type=click.Choice(["table", "json"]), default="table")
@click.pass_context
def get_resource(ctx, resource_id, output_format):
    """获取资源详情。"""
    try:
        client = ctx.obj["client"]
        resource = client.service.get_resource(resource_id)
        if output_format == "json":
            print_json(resource.model_dump(by_alias=True))
        else:
            print_table([resource.model_dump(by_alias=True)], title=f"Resource {resource_id}")
    except Exception as e:
        print_error(str(e))
        raise click.Abort() from e
```

**关键规则**：
- 所有命令必须有 `try/except`，用 `print_error(str(e))` 输出错误
- 列表命令支持 `table` 和 `json`；数据导出额外支持 `csv`
- Model 分析报告命令用 `--json` 传递 JSON 参数（参考 `cli/model.py` 中的 `_display_v1_report`）

---

## 添加全新服务的完整流程

1. 创建 `src/sa_openapi/models/<service>.py`
2. 创建 `src/sa_openapi/services/<service>.py`
3. 创建 `src/sa_openapi/cli/<service>.py`
4. 在 `src/sa_openapi/services/__init__.py` 中注册（import + `__all__` + alias）
5. 在 `src/sa_openapi/async_client.py` 中实例化服务属性
6. 在 `src/sa_openapi/cli/main.py` 中 import 并 `cli.add_command()`
7. 在 `tests/test_models.py` 中为新模型添加测试

---

## 各服务端点一览

### Dataset（7 个端点）
```python
client.dataset.get_dataset_detail(dataset_id, model_type=None)  # GET /dataset/detail
client.dataset.list_datasets(params)                             # POST /dataset/detail_list
client.dataset.list_dataset_groups()                             # GET /dataset/group/list
client.dataset.sql_query(sql, query_parameters, description)     # POST /dataset/table/sql_query
client.dataset.model_query(params)                               # POST /dataset/model/query
client.dataset.refresh_dataset(dataset_id, ...)                  # POST /dataset/refresh
client.dataset.get_sync_task_detail(sync_task_id)                # GET /dataset/sync_task_detail
```

### EventMeta（2 个端点）
```python
client.event_meta.list_events_all()   # GET /event-meta/events/all
client.event_meta.list_event_tags()   # GET /event-meta/events/tags
```

### PropertyMeta（6 个端点）
```python
client.property_meta.list_all_event_properties()                        # GET /property-meta/event-properties/all
client.property_meta.list_event_properties(events=["click"])            # POST /property-meta/event-properties
client.property_meta.list_all_user_properties()                         # GET /property-meta/user-properties/all
client.property_meta.list_user_groups()                                  # GET /property-meta/user-groups/all
client.property_meta.list_user_tags_with_dir()                          # GET /property-meta/user-tags/dir
client.property_meta.get_property_values("event", "city", limit=50)     # POST /property-meta/property/values
```

### SmartAlarm（2 个端点）
```python
client.smart_alarm.get_alarm_config(config_id)  # GET /smart-alarm/detail
client.smart_alarm.list_alarms(params)           # POST /smart-alarm/all
```

### Model（10 个端点）
```python
client.model.segmentation_report(**params)   # POST /model/segmentation/report
client.model.funnel_report(**params)          # POST /model/funnel/report
client.model.retention_report(**params)       # POST /model/retention/report
client.model.interval_report(**params)        # POST /model/interval/report
client.model.addiction_report(**params)       # POST /model/addiction/report
client.model.user_property_report(**params)   # POST /model/user-analytics/report
client.model.attribution_report(**params)     # POST /model/attribution/report
client.model.ltv_report(**params)             # POST /model/ltv/report
client.model.session_report(**params)         # POST /model/session/report
client.model.sql_query(sql, limit)            # POST /model/sql/query
```

---

## 配置与环境变量

配置文件：`~/.sa-openapi.toml`（`config init` 初始化）

支持的环境变量（优先级高于配置文件）：
- `SA_BASE_URL` - 神策分析实例地址
- `SA_API_KEY` - API Key
- `SA_PROJECT` - 项目名称

---

## 开发常用命令

```bash
# 安装开发依赖
uv sync
# 或
pip install -e ".[dev]"

# 运行测试
pytest

# 代码质量（提交前运行）
ruff check src/ tests/ && ruff format --check src/ tests/ && mypy src/ tests/ && pytest
```

## 参考文件

- `docs/openapi/3.0.4-analytics-*-swagger.json` - OpenAPI 规范，添加端点时查阅
- `docs/DESIGN.md` - 架构设计
