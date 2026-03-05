# sa-openapi

> 神策分析（SensorsData Analytics）OpenAPI Python SDK 和 CLI 工具

[![Python Version](https://img.shields.io/pypi/pyversions/sa-openapi)](https://pypi.org/project/sa-openapi/)
[![License](https://img.shields.io/github/license/popomore/sa-openapi)](https://github.com/popomore/sa-openapi/blob/main/LICENSE)

## 特性

- 🚀 **完整的 API 覆盖**：支持 Dashboard、Channel、Dataset、Model 四大服务，共 24 个 API 端点
- 🔒 **类型安全**：基于 Pydantic v2 的完整类型提示和运行时验证
- ⚡ **同步/异步支持**：同时提供同步和异步客户端
- 🛠️ **强大的 CLI**：命令行工具支持表格、JSON、CSV 多种输出格式
- 📦 **现代化设计**：基于 httpx 和 Pydantic v2 构建
- 🧪 **高测试覆盖率**：90%+ 的测试覆盖率

## 安装

```bash
pip install sa-openapi
```

支持异步功能（可选）：

```bash
pip install sa-openapi[async]
```

开发环境安装：

```bash
pip install sa-openapi[dev]
```

## 快速开始

### Python SDK

#### 基础用法

```python
from sa_openapi import SensorsAnalyticsClient

# 初始化客户端
client = SensorsAnalyticsClient(
    base_url="https://your-instance.sensorsdata.cn",
    api_key="sk-xxx",
    project="default",
)

# Dashboard 服务
navigations = client.dashboard.list_navigation(type="PRIVATE")
bookmarks = client.dashboard.list_bookmark(navigation_id=123)

# Channel 服务
links = client.channel.list_link(channel_id=456)

# Dataset 服务
result = client.dataset.sql_query(
    dataset_id=1,
    sql="SELECT * FROM events LIMIT 10"
)

# Model 服务 - 漏斗分析
funnel_result = client.model.funnel_report(
    measures=[...],
    filter={...},
    by_fields=[...]
)
```

#### 异步客户端

```python
from sa_openapi import AsyncSensorsAnalyticsClient

async def main():
    async with AsyncSensorsAnalyticsClient(
        base_url="https://your-instance.sensorsdata.cn",
        api_key="sk-xxx",
        project="default",
    ) as client:
        navigations = await client.dashboard.list_navigation(type="PRIVATE")
        print(navigations)

import asyncio
asyncio.run(main())
```

#### 错误处理

```python
from sa_openapi.exceptions import (
    SensorsAnalyticsError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
)

try:
    result = client.dataset.sql_query(dataset_id=999, sql="SELECT *")
except NotFoundError as e:
    print(f"资源未找到: {e.message}")
except ValidationError as e:
    print(f"参数验证失败: {e.message}")
except AuthenticationError as e:
    print(f"认证失败: {e.message}")
except SensorsAnalyticsError as e:
    print(f"API 错误: {e.code} - {e.message}")
```

### CLI 工具

#### 配置

首次使用需要配置认证信息：

```bash
sa-openapi config init
```

交互式配置会提示输入：
- Base URL（神策实例地址）
- API Key
- Project Name

配置文件保存在 `~/.sa-openapi.toml`

#### 基础命令

```bash
# 查看帮助
sa-openapi --help

# Dashboard 相关
sa-openapi dashboard list                              # 列出所有概览分组
sa-openapi dashboard bookmarks --navigation-id 123     # 列出指定分组的书签

# Channel 相关
sa-openapi channel list-links --channel-id 456         # 列出渠道链接
sa-openapi channel get-link --link-id 789              # 获取链接详情

# Dataset 相关
sa-openapi dataset list                                # 列出所有数据集
sa-openapi dataset sql-query --dataset-id 1 --sql "SELECT * FROM events LIMIT 10"

# Model 相关
sa-openapi model funnel-report --json '{...}'          # 漏斗分析报告
sa-openapi model retention-report --json '{...}'       # 留存分析报告
sa-openapi model sql --sql "SELECT ..."                # 自定义 SQL 查询
```

#### 输出格式

支持三种输出格式：

```bash
# 表格格式（默认）
sa-openapi dashboard list

# JSON 格式
sa-openapi dashboard list --format json

# CSV 格式
sa-openapi dashboard list --format csv
```

#### 多环境配置

支持配置多个环境（profile）：

```bash
# 使用指定 profile
sa-openapi --profile production dashboard list

# 设置默认 profile
sa-openapi config set-default production
```

配置文件示例 (`~/.sa-openapi.toml`)：

```toml
[default]
base_url = "https://your-instance.sensorsdata.cn"
api_key = "sk-xxx"
project = "default"

[production]
base_url = "https://prod.sensorsdata.cn"
api_key = "sk-prod-xxx"
project = "prod"

[staging]
base_url = "https://staging.sensorsdata.cn"
api_key = "sk-staging-xxx"
project = "staging"
```

#### 环境变量

可以使用环境变量覆盖配置：

```bash
export SA_BASE_URL="https://your-instance.sensorsdata.cn"
export SA_API_KEY="sk-xxx"
export SA_PROJECT="default"

sa-openapi dashboard list
```

## API 参考

### Dashboard 服务

| 方法 | 描述 |
|------|------|
| `list_navigation(type)` | 获取概览分组列表 |
| `get_navigation(navigation_id)` | 获取指定概览分组 |
| `list_bookmark(navigation_id)` | 获取概览书签列表 |
| `get_bookmark(bookmark_id)` | 获取指定概览书签 |
| `get_bookmark_data(bookmark_id, params)` | 获取概览书签数据 |
| `export_bookmark(bookmark_id, format)` | 导出概览书签 |

### Channel 服务

| 方法 | 描述 |
|------|------|
| `list_channel()` | 获取渠道列表 |
| `list_link(channel_id)` | 获取渠道链接列表 |
| `get_link(link_id)` | 获取指定渠道链接 |
| `get_link_data(link_id, params)` | 获取渠道链接数据 |
| `export_link(link_id, format)` | 导出渠道链接数据 |

### Dataset 服务

| 方法 | 描述 |
|------|------|
| `list_dataset()` | 获取数据集列表 |
| `get_dataset(dataset_id)` | 获取指定数据集 |
| `sql_query(dataset_id, sql, limit)` | 执行 SQL 查询 |
| `get_schema(dataset_id)` | 获取数据集 schema |
| `list_saved_query(dataset_id)` | 获取保存的查询列表 |
| `create_saved_query(...)` | 创建保存的查询 |
| `delete_saved_query(query_id)` | 删除保存的查询 |

### Model 服务

| 方法 | 描述 |
|------|------|
| `funnel_report(measures, filter, by_fields)` | 漏斗分析报告 |
| `retention_report(measures, filter, by_fields)` | 留存分析报告 |
| `attribution_report(measures, filter, by_fields)` | 归因分析报告 |
| `sql_query(sql, limit)` | 自定义 SQL 查询 |
| `explain_sql(sql)` | SQL 执行计划 |
| `validate_sql(sql)` | SQL 语法验证 |

## 架构设计

### 认证机制

所有 API 请求需要两个 HTTP 头：
- `api-key`: 全局唯一的访问密钥
- `sensorsdata-project`: 项目名称

这些在客户端初始化时配置，通过 httpx event hook 自动注入到每个请求中。

### 响应处理

所有 API 响应都包装在 `HttpApiResult<T>` 结构中：

```json
{
  "code": "SUCCESS",
  "message": "操作成功",
  "request_id": "abc123",
  "data": { ... },
  "error_info": null
}
```

SDK 会自动解包 `data` 字段，当 `code` 不是 `SUCCESS` 时抛出相应异常。

### 双 Base Path

- Dashboard/Channel/Dataset → `/api/v3/analytics/v1`
- Model → `/api/v3/analytics/v2`

### 分页处理

对于支持分页的 API，SDK 提供迭代器自动处理翻页：

```python
# 自动处理分页
for item in client.dataset.list_dataset_iter():
    print(item)
```

## 开发指南

### 环境设置

```bash
# 克隆仓库
git clone https://github.com/popomore/sa-openapi.git
cd sa-openapi

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装开发依赖
pip install -e ".[dev]"
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行带覆盖率报告
pytest --cov=sa_openapi --cov-report=html

# 运行特定测试
pytest tests/test_dashboard.py
```

### 代码质量检查

```bash
# 格式检查和自动修复
ruff check src/ --fix
ruff format src/

# 类型检查
mypy src/

# 全部检查
ruff check src/ && mypy src/ && pytest
```

### 项目结构

```
sa-openapi/
├── docs/                          # OpenAPI 规范文件
├── src/sa_openapi/
│   ├── __init__.py                # 公开 API
│   ├── py.typed                   # PEP 561 类型标记
│   ├── client.py                  # 同步客户端
│   ├── async_client.py            # 异步客户端
│   ├── _base_client.py            # 共享基础逻辑
│   ├── _auth.py                   # 认证处理
│   ├── _config.py                 # 配置管理
│   ├── _transport.py              # HTTP 传输层
│   ├── _response.py               # 响应解包
│   ├── _pagination.py             # 分页处理
│   ├── _exceptions.py             # 异常定义
│   ├── models/                    # 数据模型
│   │   ├── common.py
│   │   ├── dashboard.py
│   │   ├── channel.py
│   │   ├── dataset.py
│   │   └── model.py
│   ├── services/                  # API 服务实现
│   │   ├── dashboard.py
│   │   ├── channel.py
│   │   ├── dataset.py
│   │   └── model.py
│   └── cli/                       # CLI 工具
│       ├── main.py
│       ├── config.py
│       ├── output.py
│       ├── dashboard.py
│       ├── channel.py
│       ├── dataset.py
│       └── model.py
├── tests/                         # 测试文件
├── pyproject.toml                 # 项目配置
└── README.md
```

## 贡献指南

欢迎贡献！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add some amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 开启 Pull Request

### 代码规范

- 使用 ruff 进行代码格式化和 linting
- 使用 mypy 进行严格类型检查
- 所有公开 API 必须有类型注解和文档字符串
- 测试覆盖率不低于 90%

## 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

## 致谢

基于神策分析 OpenAPI 3.0.1 规范构建。

## 变更日志

### 0.1.0 (2024-03-02)

- 🎉 初始版本发布
- ✅ 支持 Dashboard、Channel、Dataset、Model 四大服务
- ✅ 提供同步和异步客户端
- ✅ 完整的 CLI 工具
- ✅ 完整的类型提示支持
