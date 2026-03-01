# 贡献指南

感谢你对 sa-openapi 项目的兴趣！

## 开发环境设置

1. **Fork 并克隆仓库**

```bash
git clone https://github.com/your-username/sa-openapi.git
cd sa-openapi
```

2. **创建虚拟环境**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
```

3. **安装开发依赖**

```bash
pip install -e ".[dev]"
```

## 开发流程

1. **创建功能分支**

```bash
git checkout -b feature/your-feature-name
```

2. **编写代码**

- 遵循项目的代码风格（使用 ruff）
- 为新功能添加类型注解
- 编写文档字符串

3. **添加测试**

```bash
# 运行测试
pytest

# 查看覆盖率
pytest --cov=sa_openapi --cov-report=html
```

4. **代码质量检查**

```bash
# 格式化代码
ruff format src/ tests/

# 检查代码质量
ruff check src/ tests/ --fix

# 类型检查
mypy src/
```

5. **提交更改**

```bash
git add .
git commit -m "feat: 添加新功能的简短描述"
```

提交信息格式：
- `feat:` 新功能
- `fix:` 修复 bug
- `docs:` 文档更新
- `test:` 测试相关
- `refactor:` 重构
- `style:` 代码格式调整
- `chore:` 构建/工具链更新

6. **推送并创建 PR**

```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request。

## 代码规范

### Python 代码风格

- 使用 **ruff** 进行代码格式化和 linting
- 遵循 **PEP 8** 规范
- 行长度限制为 100 字符
- 使用 Python 3.10+ 的类型语法（`X | Y` 而不是 `Union[X, Y]`）

### 类型注解

- 所有公开函数必须有完整的类型注解
- 使用 **mypy strict** 模式进行类型检查
- 私有函数也应该有类型注解

```python
def process_data(data: dict[str, Any]) -> list[str]:
    """处理数据并返回结果列表。

    Args:
        data: 输入数据字典

    Returns:
        处理后的字符串列表
    """
    ...
```

### 文档字符串

使用 Google 风格的文档字符串：

```python
def example_function(param1: str, param2: int) -> bool:
    """函数的简短描述。

    更详细的描述（如果需要）。

    Args:
        param1: 第一个参数的描述
        param2: 第二个参数的描述

    Returns:
        返回值的描述

    Raises:
        ValueError: 什么情况下抛出此异常
    """
    ...
```

### 测试

- 使用 **pytest** 编写测试
- 测试覆盖率应达到 90% 以上
- 使用 **pytest-httpx** mock HTTP 请求
- 测试文件命名格式：`test_<module>.py`
- 测试函数命名格式：`test_<function>_<scenario>`

```python
def test_client_authentication_success():
    """测试客户端认证成功场景."""
    ...

def test_client_authentication_failure():
    """测试客户端认证失败场景."""
    ...
```

## 项目结构

```
src/sa_openapi/
├── __init__.py          # 公开 API
├── client.py            # 同步客户端
├── async_client.py      # 异步客户端
├── _base_client.py      # 共享逻辑
├── _auth.py             # 认证
├── _config.py           # 配置
├── _transport.py        # HTTP 传输
├── _response.py         # 响应处理
├── _pagination.py       # 分页
├── _exceptions.py       # 异常
├── models/              # 数据模型
│   ├── common.py
│   ├── dashboard.py
│   ├── channel.py
│   ├── dataset.py
│   └── model.py
├── services/            # API 服务
│   ├── dashboard.py
│   ├── channel.py
│   ├── dataset.py
│   └── model.py
└── cli/                 # CLI 工具
    ├── main.py
    ├── config.py
    ├── output.py
    └── ...
```

## 发布流程

1. 更新版本号（在 `pyproject.toml` 和 `__init__.py`）
2. 更新 `README.md` 中的变更日志
3. 创建 Git tag
4. 推送到 GitHub
5. CI/CD 自动构建并发布到 PyPI

## 获取帮助

- 查看 [README.md](README.md) 了解项目概述
- 查看现有的 [Issues](https://github.com/popomore/sa-openapi/issues)
- 提出新的 Issue 或 Discussion

## 行为准则

- 尊重所有贡献者
- 欢迎建设性的反馈
- 保持友好和专业的态度

感谢你的贡献！🎉
