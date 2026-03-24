# CLI 测试问题排查记录

测试环境：`kokoai.cloud.sensorsjourney.com`，project=`default`

---

## ✅ 已确认正常的命令

| 命令 | 示例参数 |
|------|---------|
| `dashboard list` | — |
| `dashboard bookmarks` | — |
| `channel campaigns` | — |
| `channel links` | — |
| `channel create-link` | `--channel-id 1 --name test --utm-campaign c1` |
| `smart-alarm list` | — |
| `smart-alarm get` | `1` |
| `model segmentation-report` | 见下方说明 |
| `model funnel-report` | 见下方说明 |
| `model retention-report` | 见下方说明 |
| `model user-property-report` | 见下方说明 |
| `model session-report` | 见下方说明 |

**model 正常命令的参数说明**：
- `unit` 必须大写枚举值：`DAY`、`HOUR`、`WEEK`、`MONTH`、`YEAR`（不能是 `day`）
- `measures[].name` 字段必填（segmentation、session、user-property）
- 参数以 snake_case 传入（与 OpenAPI 规范一致）

```bash
# segmentation-report 正确示例
uv run sa-openapi model segmentation-report \
  --json '{"measures":[{"event_name":"$pageview","aggregator":"general","name":"pv"}],
           "from_date":"2024-01-01","to_date":"2024-01-07","unit":"DAY","rollup":true}'

# funnel-report 正确示例
uv run sa-openapi model funnel-report \
  --json '{"funnel":{"steps":[{"event_name":"$pageview"},{"event_name":"$pageview"}],
           "max_convert_time":86400},"from_date":"2024-01-01","to_date":"2024-01-07","unit":"DAY"}'
```

---

## ❌ 有问题的命令

### 1. `model ltv-report` — 参数校验异常

**错误码**：`COMMON-D-27-1: 参数校验异常`（HTTP 400）

**现象**：以下参数仍报错，且 error_info 中 `error_extend_desc` 为空，无法定位具体字段：
```json
{
  "measures": [{"event_name": "$pageview", "aggregator": "general", "name": "pv"}],
  "from_date": "2024-01-01",
  "to_date": "2024-01-07",
  "unit": "DAY",
  "duration": 7,
  "start_sign": {"event_name": "$pageview"}
}
```

**OpenAPI 规范字段**（`LtvReportRequest`）：
```
from_date, to_date, duration, start_sign, measures, unit,
filter, by_fields, bucket_params, request_id, use_cache,
rollup, limit, need_show_ltv_columns, time_zone_mode,
server_time_zone, subject_id
```

**待排查**：
- [ ] `start_sign` 的具体结构是否正确（可能需要更多字段）
- [ ] `duration` 的取值范围（单位是天还是其他）
- [ ] 是否有隐式必填字段未提供（文档标记 required=[] 但实际有要求）
- [ ] 对比神策控制台发出的真实请求参数

---

### 2. `model addiction-report` — 事件不存在

**错误码**：`SA-D-32-1: 事件不存在`（HTTP 400）

**现象**：
```
origin_cause: "NotFoundException: EVENT: resource_id="" 由于分析中包含的事件（）已被隐藏或不存在"
```

`resource_id=""` 说明服务器收到的 `event_name` 为空字符串，参数结构可能有误。

**OpenAPI 规范路径**：`POST /model/addiction/report`

**待排查**：
- [ ] 获取 `AddictionReportRequest` 的完整 schema（当前服务用 `**kwargs` 直传，需确认字段名）
- [ ] 检查 `measures[].event_name` 是否被正确传递（或者该接口的 measures 结构与 segmentation 不同）
- [ ] 参考 `docs/openapi/3.0.4-analytics-Model-v1-swagger.json` 中 `AddictionReportRequest` 的 example

---

### 3. `model interval-report` — 没有权限

**错误码**：`SA-D-24-2: 没有权限`（HTTP 403）

**现象**：
```
error_cause: "当前登录用户的权限不足"
origin_cause: "ForbiddenException: FORBIDDEN"
```

**待排查**：
- [ ] 确认当前 API Key 是否有间隔分析权限
- [ ] 尝试用管理员账号的 API Key 测试
- [ ] 若是功能权限问题，需在神策控制台「系统设置 → 角色权限」中开启

---

### 4. `model attribution-report` — 查询引擎错误

**错误码**：`SA-R-33-12: 查询引擎错误`（HTTP 500）

**现象**：
```
origin_cause: "InternalServerException: SERVER_PROCESSING_ERROR"
```

参数：
```json
{
  "from_date": "2024-01-01",
  "to_date": "2024-01-07",
  "target_event": {"event_name": "$pageview"},
  "link_events": [{"event_name": "$pageview"}],
  "model_type": "LAST_TOUCH",
  "rollup": true
}
```

**待排查**：
- [ ] `link_events` 结构是否正确（OpenAPI 里是 `LinkEvent`，含 `link_properties` 字段）
- [ ] `model_type` 枚举值是否正确（检查 `AttributionReportRequest` schema）
- [ ] 服务器日志或诊断报告（SA 建议下载诊断报告联系技术支持）
- [ ] 尝试精简参数，只发 `from_date/to_date/target_event`，逐步增加排查

---

### 5. `model sql` — 服务器内部错误（确认为环境问题）

**错误码**：`COMMON-R-28-2: 服务器内部错误`（HTTP 500）

**现象**：`select 1`、`show tables`、复杂查询均返回同样错误，`error_extend_desc` 和 `origin_cause` 均为空。

**结论**：请求未到达 SQL 引擎即失败，SQL 查询服务在 `kokoai.cloud.sensorsjourney.com` 上**未部署或未启动**，与 SDK/CLI 代码无关。

**default/production 两个 project 均复现**。

**待排查**：
- [ ] 联系测试环境管理员确认 SQL 查询引擎服务状态
- [ ] 换有 SQL 引擎的环境验证 CLI 功能

---

### 6. `dataset *` / `event-meta *` / `property-meta *` — 服务器 500

**错误码**：HTTP 500，`INTERNAL_SERVER_ERROR: 服务端异常`

**现象**：所有 dataset、event-meta、property-meta 端点均返回 500，无结构化错误信息。

**待排查**：
- [ ] 确认测试环境 `kokoai.cloud.sensorsjourney.com` 是否部署了对应服务
- [ ] 检查 API 路径是否正确（v1 vs v2，是否需要其他前缀）
- [ ] 测试 dataset API：`GET /api/v3/analytics/v1/dataset/list`
- [ ] 测试 event-meta API：`GET /api/v3/analytics/v1/event-meta/all`
- [ ] 测试 property-meta API：`GET /api/v3/analytics/v1/property-meta/event-properties/all`
- [ ] 联系测试环境管理员确认服务状态

---

## 排查优先级

| 优先级 | 问题 | 判断依据 |
|--------|------|---------|
| P1 | `model ltv-report` 参数校验 | 可能是 SDK 参数拼装问题，可修复 |
| P1 | `model addiction-report` event_name 为空 | 可能是 SDK 参数拼装问题，可修复 |
| P1 | `dataset/event-meta/property-meta` 500 | 影响范围大，需确认是环境问题还是代码问题 |
| P2 | `model attribution-report` 查询引擎错误 | 可能是参数结构问题，可尝试修复 |
| P3 | `model interval-report` 权限不足 | 权限配置问题，需管理员介入 |
| P3 | `model sql` 服务器内部错误 | ✅ 确认为环境问题，SQL 引擎未部署，非代码问题 |
