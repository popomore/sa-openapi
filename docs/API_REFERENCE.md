# 神策 API 参考文档

本文档基于 OpenAPI 规范，提供神策分析、数界、业务门户三大服务的完整 API 接口参考。

---

## 目录

- [Analytics 服务（神策分析）](#analytics-服务神策分析)
  - [Dashboard（概览）](#dashboard概览)
  - [Channel（渠道追踪）](#channel渠道追踪)
  - [Dataset（业务集市）](#dataset业务集市)
  - [EventMeta（事件元数据）](#eventmeta事件元数据)
  - [Model（分析模型）](#model分析模型)
  - [PropertyMeta（属性元数据）](#propertymeta属性元数据)
  - [SmartAlarm（智能预警）](#smartalarm智能预警)
- [Horizon 服务（神策数界）](#horizon-服务神策数界)
  - [Catalog（目录服务）](#catalog目录服务)
  - [DataSubscription（订阅管理）](#datasubscription订阅管理)
  - [Schema（元数据管理）](#schema元数据管理)
  - [Segment（分群管理）](#segment分群管理)
  - [Table（数据表服务）](#table数据表服务)
  - [Tag（标签管理）](#tag标签管理)
- [Portal 服务（神策业务门户）](#portal-服务神策业务门户)
  - [Identity（身份服务）](#identity身份服务)
  - [Management（管理服务）](#management管理服务)
  - [ResourceManagement（资源管理服务）](#resourcemanagement资源管理服务)
- [通用数据模型](#通用数据模型)

---

## Analytics 服务（神策分析）

### Dashboard（概览）

**服务描述**: 概览书签开放接口
**Base URL**: `/api/v3/analytics/v1`

#### API Endpoints

##### 1. 获取所有的概览分组信息

- **HTTP Method**: `GET`
- **Path**: `/dashboard/navigation`
- **OperationId**: `QueryDashboardNavigation`
- **描述**: 获取所有的概览分组信息

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| type | string | 否 | 概览类型 | PRIVATE |
| request_id | string | 否 | 本次请求 ID, 方便后续追踪问题 | 12345696321548954 |

**Response Schema**: `sensorsdata.analytics.v1.DashboardNavigationResponse`
```json
{
  "groups": [
    {
      "id": "666666",
      "title": "数据概览",
      "dashboards": [101, 102]
    }
  ],
  "type": "PRIVATE",
  "dashboard_navigation_items": []
}
```

##### 2. 获取所有基础数据概览数据

- **HTTP Method**: `GET`
- **Path**: `/dashboard/lego`
- **OperationId**: `QueryLegoDashboard`
- **描述**: 获取所有基础数据概览数据

**Response Schema**: `sensorsdata.analytics.v1.LegoDashboardResponse`
```json
{
  "lego_dashboard_items": [
    {
      "name": "实时统计",
      "navigation_name": "整体概览",
      "source_type": "WEB"
    }
  ]
}
```

##### 3. 获取单个概览详情

- **HTTP Method**: `GET`
- **Path**: `/dashboard/detail`
- **OperationId**: `QueryDashboard`
- **描述**: 获取单个概览详情

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 |
|--------|------|------|------|
| id | integer | 否 | 概览 ID |
| request_id | string | 否 | 请求 ID |

**Response Schema**: `sensorsdata.analytics.v1.DashboardDetailResponse`

##### 4. 添加概览分组信息

- **HTTP Method**: `POST`
- **Path**: `/dashboard/navigation/create`
- **OperationId**: `AddDashboardNavigation`
- **描述**: 添加概览分组信息

**Request Body**: `sensorsdata.analytics.v1.AddDashboardRequest`
```json
{
  "groups": [
    {
      "id": "666666",
      "title": "数据概览2",
      "dashboards": [201, 202]
    }
  ],
  "type": "PRIVATE",
  "request_id": "12345696321548954"
}
```

**Response Schema**: `sensorsdata.analytics.v1.CommonResponse`

##### 5. 概览分享接口

- **HTTP Method**: `POST`
- **Path**: `/dashboard/share`
- **OperationId**: `ShareDashboard`
- **描述**: 概览分享接口，可以实现分享和取消概览分享的能力

**Request Body**: `sensorsdata.analytics.v1.ShareDashboardRequest`
```json
{
  "dashboard_ids": [101, 102],
  "owners": [
    {
      "id": 5,
      "type": "ACCOUNT"
    }
  ],
  "publish": true
}
```

##### 6. 获取所有的书签信息

- **HTTP Method**: `GET`
- **Path**: `/dashboard/bookmarks`
- **OperationId**: `QueryAllBookmarks`
- **描述**: 获取所有的书签信息

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| type | integer | 否 | 书签类型，0 私有书签，1 公共书签 | 1 |
| has_widget | string | 否 | 是否包含组件类型的书签 | true |
| has_lego | string | 否 | 是否包含 lego 类型的书签 | true |
| request_id | string | 否 | 本次请求 ID | 12345696321548954 |

**Response Schema**: `sensorsdata.analytics.v1.BookmarksResponse`

---

### Channel（渠道追踪）

**服务描述**: 渠道追踪开放接口
**Base URL**: `/api/v3/analytics/v1`

#### API Endpoints

##### 1. 新建渠道链接

- **HTTP Method**: `POST`
- **Path**: `/channel/links/create`
- **OperationId**: `CreateChannelUrl`
- **描述**: 渠道链接 - 新建渠道链接

**Request Body**: `sensorsdata.analytics.v1.CreateChannelUrlGrpcRequest`
```json
{
  "channel_urls": [
    {
      "channel_type": "app_normal",
      "app_address": "http://{hostname}:{post}/sa/channel_sa/link_manage",
      "parameters": {
        "utm_source": "广告来源",
        "utm_campaign": "活动"
      },
      "device_type": "通用"
    }
  ]
}
```

**Response Schema**: `sensorsdata.analytics.v1.CreateChannelUrlGrpcResponse`

##### 2. 更新渠道链接

- **HTTP Method**: `POST`
- **Path**: `/channel/links/update`
- **OperationId**: `UpdateChannelUrl`

**Request Body**: `sensorsdata.analytics.v1.UpdateChannelUrlGrpcRequest`
```json
{
  "channel_urls": [
    {
      "id": 1,
      "name": "修改后渠道名称"
    }
  ]
}
```

##### 3. 获取渠道链接列表

- **HTTP Method**: `POST`
- **Path**: `/channel/links/list`
- **OperationId**: `GetChannelUrl`

**Request Body**: `sensorsdata.analytics.v1.GetChannelUrlGrpcRequest`
```json
{
  "page_num": 0,
  "page_size": 20,
  "sort_type": 1,
  "campaign_filters": ["周末大促"],
  "device_type_filters": ["通用", "iOS"]
}
```

**Response Schema**: `sensorsdata.analytics.v1.GetChannelUrlGrpcResponse`
```json
{
  "total_rows": 200,
  "total_page": 10,
  "page_num": 0,
  "page_size": 20,
  "detail_results": [
    {
      "id": 1,
      "name": "APP 通用渠道_测试活动",
      "channel_type": "app_normal",
      "device_type": "通用",
      "short_url": "http://{hostname}:{port}/r/U",
      "parameters": {
        "utm_campaign": "测试活动"
      }
    }
  ]
}
```

##### 4. 删除渠道链接

- **HTTP Method**: `POST`
- **Path**: `/channel/links/delete`
- **OperationId**: `DeleteChannleUrl`

**Request Body**: `sensorsdata.analytics.v1.DeleteChannelUrlGrpcRequest`
```json
{
  "channel_link_ids": [1, 3, 5, 7]
}
```

##### 5. 获取活动列表

- **HTTP Method**: `POST`
- **Path**: `/channel/campaigns/list`
- **OperationId**: `GetCampaignList`

**Request Body**: `sensorsdata.analytics.v1.CampaignListGrpcRequest`
```json
{
  "page_num": 0,
  "page_size": 20,
  "sort_info": {
    "sort_field": "latest_use_time",
    "sort_strategy": "DESC"
  }
}
```

**Response Schema**: `sensorsdata.analytics.v1.CampaignListGrpcResponse`

---

### Dataset（业务集市）

**服务描述**: 业务集市的数据查询开放接口
**Base URL**: `/api/v3/analytics/v1`

#### API Endpoints

##### 1. 查询业务模型详情信息

- **HTTP Method**: `GET`
- **Path**: `/dataset/detail`
- **OperationId**: `DatasetDetail`

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| dataset_id | integer | 是 | 业务模型ID | 1 |

**Response**: 返回业务模型的详细配置和结构信息

---

### EventMeta（事件元数据）

**服务描述**: 事件相关基础元数据
**Base URL**: `/api/v3/analytics/v1`

#### API Endpoints

##### 1. 获取事件列表

- **HTTP Method**: `GET`
- **Path**: `/event-meta/events/all`
- **OperationId**: `ListEventsAll`
- **描述**: 获取事件列表

**Response Schema**: `sensorsdata.analytics.v1.ListEventAllResponse`
```json
{
  "events": [
    {
      "id": 1,
      "name": "$AppStart",
      "cname": "应用启动",
      "is_virtual": false,
      "tags": [1, 2],
      "comment": "应用启动事件",
      "platforms": ["iOS", "Android"]
    }
  ]
}
```

##### 2. 获取事件标签列表

- **HTTP Method**: `GET`
- **Path**: `/event-meta/events/tags`
- **OperationId**: `ListEventTags`

**Response Schema**: `sensorsdata.analytics.v1.ListEventTagsResponse`

---

### Model（分析模型）

**服务描述**: 分析模型开放接口
**Base URL**: `/api/v3/analytics/v1`

#### API Endpoints

##### 1. 查询事件分析报告

- **HTTP Method**: `POST`
- **Path**: `/model/segmentation/report`
- **OperationId**: `QuerySegmentationReport`

**Request Body**: `sensorsdata.analytics.v1.SegmentationReportRequest`

**Response Schema**: `sensorsdata.analytics.v1.SegmentationReportResponse`
```json
{
  "metadata_columns": {
    "date": "DATE",
    "小程序显示的总次数": "DOUBLE"
  },
  "truncated": false,
  "detail_rows": [
    ["2022-07-11 00:00:00", 144, "37", "1"]
  ]
}
```

##### 2. 查询漏斗分析报告

- **HTTP Method**: `POST`
- **Path**: `/model/funnel/report`
- **OperationId**: `QueryFunnelReport`

**Request Body**: `sensorsdata.analytics.v1.FunnelReportRequest`

**Response Schema**: `sensorsdata.analytics.v1.FunnelReportResponse`

##### 3. 查询留存分析报告

- **HTTP Method**: `POST`
- **Path**: `/model/retention/report`
- **OperationId**: `QueryRetentionReport`

**Request Body**: `sensorsdata.analytics.v1.RetentionReportRequest`

**Response Schema**: `sensorsdata.analytics.v1.RetentionReportResponse`

##### 4. 查询间隔分析报告

- **HTTP Method**: `POST`
- **Path**: `/model/interval/report`
- **OperationId**: `QueryIntervalReport`

**Request Body**: `sensorsdata.analytics.v1.IntervalReportRequest`

**Response Schema**: `sensorsdata.analytics.v1.IntervalReportResponse`

##### 5. 查询分布分析报告

- **HTTP Method**: `POST`
- **Path**: `/model/addiction/report`
- **OperationId**: `QueryAddictionReport`

**Request Body**: `sensorsdata.analytics.v1.AddictionReportRequest`

**Response Schema**: `sensorsdata.analytics.v1.AddictionReportResponse`

---

### PropertyMeta（属性元数据）

**服务描述**: 属性相关基础元数据
**Base URL**: `/api/v3/analytics/v1`

#### API Endpoints

##### 1. 获取所有事件属性

- **HTTP Method**: `GET`
- **Path**: `/property-meta/event-properties/all`
- **OperationId**: `ListAllEventProperties`

**Response Schema**: `sensorsdata.analytics.v1.EventPropertyAllResponse`
```json
{
  "properties": [
    {
      "id": 1,
      "name": "$city",
      "cname": "城市",
      "data_type": "STRING",
      "has_dict": true
    }
  ]
}
```

##### 2. 获取指定的事件和相关属性

- **HTTP Method**: `POST`
- **Path**: `/property-meta/event-properties`
- **OperationId**: `ListEventProperties`

**Request Body**: `sensorsdata.analytics.v1.EventPropertyRequest`
```json
{
  "events": ["$AppStart", "$AppClick"]
}
```

##### 3. 获取所有用户属性列表

- **HTTP Method**: `GET`
- **Path**: `/property-meta/user-properties/all`
- **OperationId**: `ListAllUserProperties`

**Response Schema**: `sensorsdata.analytics.v1.UserPropertyAllResponse`

##### 4. 获取所有用户分群列表

- **HTTP Method**: `GET`
- **Path**: `/property-meta/user-groups/all`
- **OperationId**: `ListUserGroups`

**Response Schema**: `sensorsdata.analytics.v1.UserGroupAllResponse`

##### 5. 获取带有目录结构的用户标签列表

- **HTTP Method**: `GET`
- **Path**: `/property-meta/user-tags/dir`
- **OperationId**: `ListUserTagsWithDir`

**Response Schema**: `sensorsdata.analytics.v1.UserTagDirResponse`

##### 6. 获取属性候选值

- **HTTP Method**: `POST`
- **Path**: `/property-meta/property/values`
- **OperationId**: `GetPropertyValues`

**Request Body**: `sensorsdata.analytics.v1.GetPropertyValueRequest`
```json
{
  "table_type": "EVENT",
  "property_name": "$city",
  "limit": 100
}
```

---

### SmartAlarm（智能预警）

**服务描述**: 智能预警开放接口
**Base URL**: `/api/v3/analytics/v1`

#### API Endpoints

##### 1. 获取一个预警配置的详细信息

- **HTTP Method**: `GET`
- **Path**: `/smart-alarm/detail`
- **OperationId**: `QueryAlarmConfig`

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| config_id | integer | 否 | 配置 ID | 1 |
| request_id | string | 否 | 本次请求 ID | 12345696321548954 |

**Response Schema**: `sensorsdata.analytics.v1.SmartAlarmConfigResponse`
```json
{
  "id": 1,
  "title": "测试预警",
  "emails": ["test1@test.cn", "test2@test.cn"],
  "unit": "HOUR",
  "send_alarm": true,
  "history": {
    "execute_time": "2023-01-08 23:00:00",
    "alarm_value": "0",
    "alarm_last_value": "1"
  }
}
```

##### 2. 获取所有的预警列表

- **HTTP Method**: `POST`
- **Path**: `/smart-alarm/all`
- **OperationId**: `QueryAllAlarms`

**Request Body**: `sensorsdata.analytics.v1.SmartAlarmRequest`
```json
{
  "title": "测试预警信息",
  "units": ["DAY"],
  "create_user_ids": [1, 2, 3],
  "disables": [true]
}
```

**Response Schema**: `sensorsdata.analytics.v1.SmartAlarmConfigListResponse`

---

## Horizon 服务（神策数界）

### Catalog（目录服务）

**服务描述**: 目录服务
**Base URL**: `/api/v3/horizon/v1`

#### API Endpoints

##### 1. 查询目录树

- **HTTP Method**: `POST`
- **Path**: `/catalog/tree/list`
- **OperationId**: `ListCatalogTrees`

**Request Body**: `sensorsdata.horizon.v1.ListCatalogTreesRequest`
```json
{
  "business_type": "ENTITY",
  "business_names": ["user"],
  "query_catalog_node_type": "ONLY_UNDELETE",
  "show_resource": false
}
```

**Response Schema**: `sensorsdata.horizon.v1.ListCatalogTreesResponse`
```json
{
  "catalog_trees": [
    {
      "business_name": "user",
      "catalog": {
        "type": "CATALOG",
        "name": "8998a014-f8e3-4d8a-8b2c-ec7beeeefc97",
        "display_name": "user",
        "catalogs": []
      }
    }
  ]
}
```

##### 2. 挂载资源节点

- **HTTP Method**: `POST`
- **Path**: `/catalog/resource/bind`
- **OperationId**: `BindCatalogResource`

**Request Body**: `sensorsdata.horizon.v1.BindCatalogResourceRequest`
```json
{
  "parent_name": "8998a014-f8e3-4d8a-8b2c-ec7beeeefc97",
  "resource_type": "TAG",
  "resource_id": "user_tag_bq_meta_string"
}
```

##### 3. 解绑资源节点

- **HTTP Method**: `POST`
- **Path**: `/catalog/resource/unbind`
- **OperationId**: `UnbindCatalogResource`

**Request Body**: `sensorsdata.horizon.v1.UnbindCatalogResourceRequest`
```json
{
  "business_type": "ENTITY",
  "business_name": "user",
  "resource_type": "TAG",
  "resource_id": "user_tag_bq_meta_string",
  "skip_trash": true
}
```

---

### DataSubscription（订阅管理）

**服务描述**: 订阅管理服务
**Base URL**: `/api/v3/horizon/v1`

#### API Endpoints

##### 1. 创建订阅方

- **HTTP Method**: `POST`
- **Path**: `/data-subscription/application/add`
- **OperationId**: `AddSubscriptionApplication`

**Request Body**: `sensorsdata.horizon.v1.AddSubscriptionApplicationRequest`
```json
{
  "application": {
    "application_name": "shence",
    "application_type": "KAFKA_BASED_APP",
    "kafka_based_app_config": {
      "data_format_type": "NESTED_JSON",
      "event_kafka_descriptor": {
        "type": "CUSTOMIZED_KAFKA",
        "customized_kafka_descriptor": {
          "bootstrap_servers": "broker1:9092,broker2:9092",
          "topic_name": "shence_data_topic"
        }
      }
    }
  }
}
```

##### 2. 补充订阅方配置信息

- **HTTP Method**: `POST`
- **Path**: `/data-subscription/application/config/append`
- **OperationId**: `AppendSubscriptionApplicationConfig`

**Request Body**: `sensorsdata.horizon.v1.AppendSubscriptionApplicationConfigRequest`

##### 3. 查询订阅方信息

- **HTTP Method**: `POST`
- **Path**: `/data-subscription/application/get`
- **OperationId**: `GetSubscriptionApplication`

**Request Body**: `sensorsdata.horizon.v1.GetSubscriptionApplicationRequest`
```json
{
  "application_name": "shence"
}
```

##### 4. 删除订阅方

- **HTTP Method**: `POST`
- **Path**: `/data-subscription/application/delete`
- **OperationId**: `DeleteSubscriptionApplication`

**Request Body**: `sensorsdata.horizon.v1.DeleteSubscriptionApplicationRequest`

##### 5. 创建数据订阅

- **HTTP Method**: `POST`
- **Path**: `/data-subscription/create`
- **OperationId**: `CreateDataSubscription`

**Request Body**: `sensorsdata.horizon.v1.CreateDataSubscriptionRequest`
```json
{
  "subscription": {
    "application": "shence.org-sep-111.app.sensorsdata.cloud",
    "subscriber": "sa",
    "target_type": "ENTITY_DATA",
    "entity_data_subscription_config": {
      "entity_name": "user",
      "attribute_type": "SIMPLE",
      "simple_attribute_config": {
        "attribute_names": ["name", "gender", "age"]
      }
    }
  }
}
```

##### 6. 批量查询订阅记录列表

- **HTTP Method**: `GET`
- **Path**: `/data-subscription/list`
- **OperationId**: `ListDataSubscriptions`

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| application | string | 是 | 订阅方的唯一标识 | shence.sep-org-111.app.sensorsdata.cloud |
| subscriber | string | 否 | 订阅方业务标识 | sa |

##### 7. 批量取消订阅

- **HTTP Method**: `POST`
- **Path**: `/data-subscription/batch-delete`
- **OperationId**: `BatchDeleteDataSubscriptions`

**Request Body**: `sensorsdata.horizon.v1.BatchDeleteDataSubscriptionsRequest`
```json
{
  "application": "shence.sep-org-111.app.sensorsdata.cloud",
  "subscriber": "sa",
  "subscription_ids": [1001, 1002, 1003]
}
```

---

### Schema（元数据管理）

**服务描述**: 元数据管理服务
**Base URL**: `/api/v3/horizon/v1`

#### API Endpoints

##### 1. 获取事件定义列表

- **HTTP Method**: `POST`
- **Path**: `/schema/event/list`
- **OperationId**: `ListEventSchemas`

**Request Body**: `sensorsdata.horizon.v1.ListLogicalSchemasRequest`
```json
{
  "expand": "custom_params",
  "page_size": 1
}
```

**Response Schema**: `sensorsdata.horizon.v1.ListLogicalSchemasResponse`

##### 2. 获取事件定义

- **HTTP Method**: `POST`
- **Path**: `/schema/event/get`
- **OperationId**: `GetEvent`

**Request Body**: `sensorsdata.horizon.v1.GetSchemaByOriginalNameRequest`
```json
{
  "expand": "custom_params",
  "original_name": "ViewProduct"
}
```

##### 3. 创建事件定义

- **HTTP Method**: `POST`
- **Path**: `/schema/event/create`
- **OperationId**: `CreateEvent`

**Request Body**: 事件定义创建请求

---

### Segment（分群管理）

**服务描述**: 分群管理服务
**Base URL**: `/api/v3/horizon/v1`

#### API Endpoints

##### 1. 获取分群列表

- **HTTP Method**: `POST`
- **Path**: `/segment/definition/list`
- **OperationId**: `ListSegmentDefinitions`

**Request Body**: `sensorsdata.horizon.v1.ListSegmentDefinitionsRequest`
```json
{
  "entity_name": "user",
  "segment_definition_names": ["user_segment_t"],
  "has_valid_segment": true,
  "show_invisible": true,
  "page_size": 20,
  "page": -1
}
```

**Response Schema**: `sensorsdata.horizon.v1.ListSegmentDefinitionsResponse`

##### 2. 获取分群信息

- **HTTP Method**: `POST`
- **Path**: `/segment/definition/get`
- **OperationId**: `GetSegmentDefinition`

**Request Body**: `sensorsdata.horizon.v1.GetSegmentDefinitionRequest`
```json
{
  "entity_name": "user",
  "name": "user_segment_t"
}
```

---

### Table（数据表服务）

**服务描述**: 数据表服务
**Base URL**: `/api/v3/horizon/v1`

#### API Endpoints

##### 1. 批量查询数据表信息

- **HTTP Method**: `POST`
- **Path**: `/table/list`
- **OperationId**: `ListTables`

**Request Body**: `sensorsdata.horizon.v1.ListTablesRequest`
```json
{
  "project_id": 1,
  "db_name": "horizon_default_db",
  "page_size": -1
}
```

**Response Schema**: `sensorsdata.horizon.v1.ListTablesResponse`
```json
{
  "tables": [
    {
      "project_id": 1,
      "db_name": "horizon_default_1",
      "name": "events",
      "display_name": "事件表",
      "type": "VIEW",
      "columns": []
    }
  ],
  "total_size": 3,
  "has_next": false
}
```

##### 2. 查询数据表信息

- **HTTP Method**: `POST`
- **Path**: `/table/get`
- **OperationId**: `GetTable`

**Request Body**: `sensorsdata.horizon.v1.GetTableRequest`
```json
{
  "project_id": 1,
  "db_name": "horizon_default_db",
  "table_name": "users"
}
```

##### 3. 创建数据表

- **HTTP Method**: `POST`
- **Path**: `/table/create`
- **OperationId**: `CreateTable`

**Request Body**: `sensorsdata.horizon.v1.CreateTableRequest`
```json
{
  "project_id": 1,
  "table": {
    "db_name": "test_db",
    "name": "test_table",
    "type": "TABLE",
    "engine": "MUTABLE",
    "primary_keys": ["id"],
    "columns": [
      {
        "name": "id",
        "dw_data_type": "STRING"
      }
    ]
  }
}
```

---

### Tag（标签管理）

**服务描述**: 标签管理服务
**Base URL**: `/api/v3/horizon/v1`

#### API Endpoints

##### 1. 查询标签列表

- **HTTP Method**: `POST`
- **Path**: `/tag/definition/list`
- **OperationId**: `ListTagDefinitions`

**Request Body**: `sensorsdata.horizon.v1.ListTagDefinitionsRequest`
```json
{
  "page_size": 2,
  "page": 1,
  "entity_name": "user",
  "show_deleted": true,
  "show_invisible": true
}
```

**Response Schema**: `sensorsdata.horizon.v1.ListTagDefinitionsResponse`

##### 2. 查询单个标签信息

- **HTTP Method**: `POST`
- **Path**: `/tag/definition/get`
- **OperationId**: `GetTagDefinition`

**Request Body**: `sensorsdata.horizon.v1.GetTagDefinitionRequest`
```json
{
  "entity_name": "user",
  "name": "user_tag_c1",
  "show_deleted": true
}
```

---

## Portal 服务（神策业务门户）

### Identity（身份服务）

**服务描述**: 身份服务主要负责管理账号权限相关的接口
**Base URL**: `/api/v3/portal/v2`

#### API Endpoints

##### 1. 获取账号列表

- **HTTP Method**: `GET`
- **Path**: `/identity/account/list`
- **OperationId**: `ListAccounts`
- **描述**: 获取账号列表，包含账号的基本信息、角色的简要信息以及账号的扩展属性值

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| page_index | integer | 否 | 列表页号，默认值：1 | 1 |
| page_size | integer | 否 | 单页返回最大记录数，默认值：20，取值范围：1-100 | 20 |

**Response Schema**: `sensorsdata.portal.v2.api.ListAccountResponse`
```json
{
  "accounts": [
    {
      "account": {
        "id": 1,
        "name": "admin",
        "cname": "管理员",
        "email": "demo@sensorsdata.com",
        "phone": "12399999999",
        "disabled": false,
        "is_global": true
      },
      "roles": [
        {
          "id": 1,
          "name": "analyst",
          "cname": "管理员"
        }
      ],
      "related_extra_attributes": []
    }
  ],
  "page": {
    "total": 100,
    "current_page": 1,
    "page_count": 100
  }
}
```

##### 2. 获取单个账号

- **HTTP Method**: `GET`
- **Path**: `/identity/account/get`
- **OperationId**: `GetAccount`
- **描述**: 获取单个账号信息；包括账号基本信息、账号关联的角色信息、账号扩展属性等

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| id | string | 否 | 账号 id | 1 |
| uuid | string | 否 | 账号 uuid | 38135721-2938-4585-b19b-396ceb910d88 |

**Response Schema**: `sensorsdata.portal.v2.api.GetAccountResponse`

##### 3. 通过名称获取单个账号

- **HTTP Method**: `GET`
- **Path**: `/identity/account/get-by-name`
- **OperationId**: `GetAccountByName`

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| account_name | string | 是 | 账号名称 | lh@qq.com |
| is_global | boolean | 是 | 是否平台账号 | true |

---

### Management（管理服务）

**服务描述**: 管理服务主要负责管理 SBP 一些通用产品功能组件的 open api 接口；例如：操作日志，消息通知，数据迁移等
**Base URL**: `/api/v3/portal/v2`

#### API Endpoints

##### 1. 获取操作日志定义列表

- **HTTP Method**: `GET`
- **Path**: `/management/behavior/define/list`
- **OperationId**: `ListBehaviorDefines`
- **描述**: 获取操作日志定义列表；该接口支持翻页，每页最多返回 100 条记录

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| page_index | integer | 否 | 当前访问页号，默认值：1 | 1 |
| page_size | integer | 否 | 单页返回最大记录数，默认值：20，取值范围：1-100 | 20 |
| product | string | 否 | 声明该「操作日志定义」的产品线 | SBP |

**Response Schema**: `sensorsdata.portal.v2.api.ListBehaviorDefineResponse`
```json
{
  "code": "SUCCESS",
  "data": {
    "behavior_defines": [
      {
        "product": "SBP",
        "operation_type_name": "登录",
        "operation_type": "login",
        "module": "passport",
        "module_name": "系统"
      }
    ],
    "page": {
      "total": 100,
      "current_page": 1,
      "page_count": 100
    }
  },
  "request_id": "1"
}
```

##### 2. 获取操作日志列表

- **HTTP Method**: `GET`
- **Path**: `/management/behavior/list`
- **OperationId**: `ListBehaviors`
- **描述**: 获取操作日志列表；为了方便于加载不同项目操作日志的数据，需要在请求参数中携带项目 ID，如果请求头携带了 sensorsdata-project 或者在请求参数中携带了 project 参数，会被忽略掉；该接口支持翻页，每页最多返回 100 条记录

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| project_id | integer | 是 | 项目 id | 1 |
| operation_start_time | string | 否 | 日志开始时间，日期格式：yyyy-MM-dd HH:mm:ss | 2022-01-01 00:00:00 |
| operation_end_time | string | 否 | 日志结束时间，日期格式：yyyy-MM-dd HH:mm:ss | 2022-01-01 00:00:00 |
| page_index | integer | 否 | 当前访问页号，默认值：1 | 1 |
| page_size | integer | 否 | 单页返回最大记录数，默认值：20，取值范围：1-100 | 20 |
| module | string | 否 | 功能模块，该字段由 sbp_behavior_define.module 定义 | passport |
| user_name | string | 否 | 用户名，指定时查询当前用户名的操作日志 | zhang_san |
| ip | string | 否 | ip地址，指定时查询该ip地址的操作记录 | 182.150.28.141 |
| sort_order | string | 否 | 排序，升序还是降序，为空默认为降序，asc：升序，desc：降序 | asc |

**Request Body**: `sensorsdata.portal.v2.api.ListBehaviorRequestBody`
```json
{
  "operation_types": ["login", "logout"]
}
```

**Response Schema**: `sensorsdata.portal.v2.api.ListBehaviorResponse`
```json
{
  "code": "SUCCESS",
  "data": {
    "page": {
      "total": 100,
      "current_page": 1,
      "page_count": 100
    },
    "behavior_infos": [
      {
        "operation_type_name": "编辑",
        "operation_time": "2022-01-01 00:00:00",
        "project_id": 1,
        "user_name": "平台管理员",
        "ip": "127.0.0.1",
        "resource_id": "1",
        "description": {
          "content": "角色「管理员」"
        },
        "duty": "销售",
        "module_name": "角色管理",
        "resource_name": "管理员",
        "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
      }
    ]
  },
  "request_id": "1"
}
```

##### 3. 查询许可证组件

- **HTTP Method**: `GET`
- **Path**: `/management/license/product`
- **OperationId**: `GetLicenseProduct`
- **描述**: 查询私有端的所有授权组件信息（主要包括版本信息和授权情况）

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| product_name | string | 否 | 产品线名称 | SBP |

**Response Schema**: `sensorsdata.portal.v2.api.GetLicenseProductResponse`
```json
{
  "code": "SUCCESS",
  "data": {
    "project_name": "production",
    "product_name": "SBP"
  },
  "request_id": "1"
}
```

##### 4. 发送站内消息

- **HTTP Method**: `POST`
- **Path**: `/management/notice/send`
- **OperationId**: `SendNoticeMessage`
- **描述**: 发送站内消息，支持发送给项目下指定的用户列表或者发送给某一项目下的所有用户；使用该接口发送的消息可以在神策系统右上角的「消息通知」处查看

**Request Body**: `sensorsdata.portal.v2.api.NoticeMessageRequestBody`
```json
{
  "uuid": "38135721-2938-4585-b19b-396ceb910d88",
  "priority": "MEDDLE",
  "operation_type": "QUERY",
  "description": "{\"jump_url\": \"https://www.sensorsdata.cn/\", \"content\": {\"line\": \"神策数据\", \"line2\": \"欢迎使用神策分析\", \"reservation_day\": 18924,\"is_success\": true}}",
  "accounts": [1, 2, 3],
  "to_all_accounts": false
}
```

**Response Schema**: `sensorsdata.portal.v2.api.NoticeMessageResponse`
```json
{
  "code": "SUCCESS",
  "data": {
    "notice": {
      "product_line": "SA",
      "operation_time": "2022-01-01 00:00:00",
      "operation_type": "DASHBOARD",
      "id": 1,
      "priority": "LOW",
      "uuid": "38135721-2938-4585-b19b-396ceb910d88"
    }
  },
  "request_id": "1"
}
```

##### 5. 查询产品版本信息

- **HTTP Method**: `GET`
- **Path**: `/management/product/versions`
- **OperationId**: `GetAllProductVersion`
- **描述**: 查询私有端的版本信息

**Response Schema**: `sensorsdata.portal.v2.api.AllProductVersionResponse`
```json
{
  "code": "SUCCESS",
  "data": {
    "product_versions": [
      {
        "product_version": "1.5.1.224",
        "product_name": "SBP"
      }
    ]
  },
  "request_id": "1"
}
```

##### 6. 获取项目详情

- **HTTP Method**: `GET`
- **Path**: `/management/project/get`
- **OperationId**: `GetProjectByIdOrName`
- **描述**: 获取项目的详细信息

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| project_id | integer | 否 | 项目 id | 2 |
| project_name | string | 否 | 项目名称 | default |

**Response Schema**: `sensorsdata.portal.v2.api.ProjectWithConfig`
```json
{
  "code": "SUCCESS",
  "data": {
    "project": {
      "create_time": "2022-01-01 00:00:00",
      "name": "default",
      "cname": "默认项目",
      "project_status": "NORMAL",
      "id": 1
    },
    "config": {
      "is_schema_limited": false,
      "is_csm": false,
      "customize_default_roles": "admin",
      "is_duty_required": true,
      "is_new_sign_up": false
    }
  },
  "request_id": "1"
}
```

##### 7. 按账号 ID 查询项目

- **HTTP Method**: `GET`
- **Path**: `/management/project/get-by-account-id`
- **OperationId**: `GetProjectsByAccountId`
- **描述**: 获取账号绑定的项目

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| account_id | integer | 是 | 账号 id | 1 |

**Response Schema**: `sensorsdata.portal.v2.api.GetProjectsByAccountIdResponse`
```json
{
  "code": "SUCCESS",
  "data": {
    "projects": [
      {
        "create_time": "2022-01-01 00:00:00",
        "name": "default",
        "cname": "默认项目",
        "project_status": "NORMAL",
        "id": 1
      }
    ]
  },
  "request_id": "1"
}
```

##### 8. 获取项目列表

- **HTTP Method**: `GET`
- **Path**: `/management/project/list`
- **OperationId**: `ListProjects`
- **描述**: 获取当前账号已启用的项目信息和项目配置

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| product_name | string | 否 | 产品名称，指定该参数则获取的项目信息为该产品下能够访问的项目列表 | SA |

**Response Schema**: `sensorsdata.portal.v2.api.ListProjectResponse`
```json
{
  "code": "SUCCESS",
  "data": {
    "total": 10,
    "projects": [
      {
        "project": {
          "create_time": "2022-01-01 00:00:00",
          "name": "default",
          "cname": "默认项目",
          "project_status": "NORMAL",
          "id": 1
        },
        "config": {
          "is_schema_limited": false,
          "is_csm": false,
          "customize_default_roles": "admin",
          "is_duty_required": true,
          "is_new_sign_up": false
        }
      }
    ]
  },
  "request_id": "1"
}
```

---

### ResourceManagement（资源管理服务）

**服务描述**: 资源管理服务主要负责资源管理相关模块的 open api 接口，例如：获取查询任务明细表
**Base URL**: `/api/v3/portal/v2`

#### API Endpoints

##### 1. 获取资源信息和使用量

- **HTTP Method**: `POST`
- **Path**: `/resource-management/assets/list`
- **OperationId**: `ListAssets`
- **描述**: 获取指定资产的基本信息和使用情况列表，包含资产名称、创建时间、查询次数、被引用次数等，该接口支持翻页，每页最多返回 100 条记录。【注：该接口在每日 06:00-23:59 时段返回数据为 T-1，00:00-6:00 时段返回数据为 T-2（前天）】

**Request Body**: `sensorsdata.portal.v2.api.ResourceManagementListAssetsRequest`
```json
{
  "asset_type": "ASSET_USER_GROUP",
  "condition": {
    "conditions": [
      {
        "field": "TRIGGER_TYPE",
        "operator": "IN",
        "values": ["UI", "API"]
      },
      {
        "field": "QUERY_INITIATOR",
        "operator": "NOT_IN",
        "values": ["system"]
      },
      {
        "field": "CATEGORY",
        "operator": "IN",
        "values": ["USERGROUP", "SEGMENT"]
      }
    ]
  },
  "asset_ids": ["178", "467", "124"],
  "page_index": 1,
  "page_size": 20,
  "project": "default"
}
```

**Response Schema**: `sensorsdata.portal.v2.api.ResourceManagementAssetsResponse`
```json
{
  "code": "SUCCESS",
  "data": {
    "assets": [
      {
        "asset_cname": "分布分析",
        "creator": "admin",
        "asset_name": "user_group_508",
        "create_time": "2022-04-01 16:00:29",
        "query_count": 511,
        "asset_type": "ASSET_USER_GROUP",
        "project": "default",
        "asset_id": "127",
        "ref_count": 988
      }
    ],
    "page": {
      "total": 100,
      "current_page": 1,
      "page_count": 100
    }
  },
  "request_id": "1"
}
```

##### 2. 获取资源相关查询任务

- **HTTP Method**: `POST`
- **Path**: `/resource-management/assets/query/list`
- **OperationId**: `ListAssetQuery`
- **描述**: 获取资产相关的查询任务详情列表，需要指定是「由资产主动发起」的或是「引用了该资产」的任务，包含任务描述，任务耗时，CPU 开销，内存消耗量，文件扫描量等，该接口支持翻页，每页最多返回 100 条记录

**Request Body**: `sensorsdata.portal.v2.api.ResourceManagementListAssetQueryRequest`
```json
{
  "asset_type": "ASSET_USER_GROUP",
  "asset_id": "187",
  "project": "production",
  "query_type": "REF_QUERY",
  "condition": {
    "conditions": []
  },
  "page_index": 1,
  "page_size": 20,
  "sort_key": "START_TIME",
  "sort_order": "DESC"
}
```

**Response Schema**: `sensorsdata.portal.v2.api.QueryCompletedTaskTableResponse`
```json
{
  "code": "SUCCESS",
  "data": {
    "page": {
      "total": 100,
      "current_page": 1,
      "page_count": 100
    },
    "task_details": [
      {
        "functional_module_type": "其他",
        "exception": "OK",
        "query_ref_count": 5,
        "total_cpu_time": 304,
        "project_cname": "测试项目",
        "query_id": "814d0491c18653cc:bd04dfb700000000",
        "entity_name": "概览1-书签1",
        "trigger_type": "例行任务",
        "end_time": "2022-04-01 16:00:30",
        "project": "default",
        "functional_module": "事件分析",
        "entity_id": "123456-67890",
        "duration": 339,
        "start_time": "2022-04-01 16:00:29",
        "speed_evaluation": "normal",
        "ext_tags": "[\"feature\":\"withtoday\"}]",
        "total_bytes_read": 224,
        "user_cname": "平台管理员",
        "workload_query_desc": "将新用户同步到 User 表。[任务 id = 47]",
        "workload_source": "后台任务-用户同步",
        "state": "FINISHED",
        "per_node_memory_usage": 72579568,
        "user": "admin"
      }
    ]
  },
  "request_id": "1"
}
```

##### 3. 获取已完成查询任务

- **HTTP Method**: `GET`
- **Path**: `/resource-management/query/task/completed`
- **OperationId**: `ListCompletedQueryTaskTable`
- **描述**: 获取已完成的任务详情列表，包含任务描述，任务耗时，CPU 开销，内存消耗量，文件扫描量等，该接口支持翻页，每页最多返回 100 条记录

**Query Parameters**:
| 参数名 | 类型 | 必填 | 描述 | 示例 |
|--------|------|------|------|------|
| start_time | string | 否 | 查询时间起点，日期格式：yyyy-MM-dd HH:mm:ss（默认时间为 2010-01-01 00:00:00） | 2022-01-01 00:00:00 |
| end_time | string | 否 | 查询时间终点，日期格式：yyyy-MM-dd HH:mm:ss（默认时间为当前日期两天后的午夜零点） | 2022-03-01 00:00:00 |
| sort_key | string | 否 | 排序依据，默认 START_TIME | START_TIME |
| sort_order | string | 否 | 排序顺序，默认降序 | DESC |
| page_index | integer | 否 | 列表页号，默认值：1，取值范围：>=1 | 1 |
| page_size | integer | 否 | 单页返回最大记录数，默认值：20，取值范围：1-100 | 20 |

**可选的 sort_key 值**:
- `START_TIME`: 开始时间
- `DURATION`: 耗时
- `TOTAL_CPU_TIME`: CPU 开销
- `PER_NODE_MEMORY_USAGE`: 内存消耗
- `TOTAL_BYTES_READ`: 文件扫描量
- `USER`: 用户

**可选的 sort_order 值**:
- `DESC`: 降序
- `ASC`: 升序

**Response Schema**: `sensorsdata.portal.v2.api.QueryCompletedTaskTableResponse`
```json
{
  "code": "SUCCESS",
  "data": {
    "page": {
      "total": 100,
      "current_page": 1,
      "page_count": 100
    },
    "task_details": [
      {
        "functional_module_type": "其他",
        "exception": "OK",
        "query_ref_count": 5,
        "total_cpu_time": 304,
        "project_cname": "测试项目",
        "query_id": "814d0491c18653cc:bd04dfb700000000",
        "entity_name": "概览1-书签1",
        "trigger_type": "例行任务",
        "end_time": "2022-04-01 16:00:30",
        "project": "default",
        "functional_module": "事件分析",
        "entity_id": "123456-67890",
        "duration": 339,
        "start_time": "2022-04-01 16:00:29",
        "speed_evaluation": "normal",
        "ext_tags": "[\"feature\":\"withtoday\"}]",
        "total_bytes_read": 224,
        "user_cname": "平台管理员",
        "workload_query_desc": "将新用户同步到 User 表。[任务 id = 47]",
        "workload_source": "后台任务-用户同步",
        "state": "FINISHED",
        "per_node_memory_usage": 72579568,
        "user": "admin"
      }
    ]
  },
  "request_id": "1"
}
```

##### 4. 获取执行中查询任务

- **HTTP Method**: `GET`
- **Path**: `/resource-management/query/task/executing`
- **OperationId**: `ListExecutingQueryTaskTable`
- **描述**: 获取执行中的任务详情列表（注：该接口服务于资源监控，故返回结果包含"已执行完成/执行失败，但仍未释放内存或其他资源的查询任务"）该接口不支持翻页或筛选，执行中任务数通常预期值小于 20 条

**Response Schema**: `sensorsdata.portal.v2.api.QueryExecutingTaskTableResponse`
```json
{
  "code": "SUCCESS",
  "data": {
    "task_details": [
      {
        "functional_module_type": "其他",
        "query_ref_count": 5,
        "total_cpu_time": 304,
        "project_cname": "default",
        "query_id": "814d0491c18653cc:bd04dfb700000000",
        "entity_name": "概览1-书签1",
        "trigger_type": "例行任务",
        "end_time": "2022-04-01 16:00:30",
        "functional_module": "事件分析",
        "entity_id": "123456-67890",
        "duration": 339,
        "start_time": "2022-04-01 16:00:29",
        "speed_evaluation": "normal",
        "ext_tags": "[\"feature\":\"withtoday\"}]",
        "total_bytes_read": 224,
        "user_cname": "平台管理员",
        "workload_query_desc": "将新用户同步到 User 表。[任务 id = 47]",
        "workload_source": "后台任务-用户同步",
        "per_node_peak_memory_percentage": "0.53%",
        "state": "RUNNING",
        "user": "admin",
        "estimated_per_node_peak_memory": 699998208
      }
    ]
  },
  "request_id": "1"
}
```

---

## 通用数据模型

### HttpApiResult 标准响应

所有 API 接口都遵循统一的响应格式：

```json
{
  "code": "SUCCESS",
  "message": "操作成功",
  "request_id": "12345696321548954",
  "data": {},
  "error_info": {
    "code": "XX-D-F-2-1",
    "description": "错误描述",
    "system_response": "系统终止了查询处理",
    "error_causes": [
      {
        "error_cause": "参数异常1",
        "action_suggestion": "检测入参的数据类型1"
      }
    ],
    "context": {
      "origin_stack": "异常堆栈",
      "origin_cause": "异常原因"
    }
  }
}
```

### ErrorInfo 错误信息结构

| 字段 | 类型 | 描述 |
|------|------|------|
| code | string | 具体的错误码 |
| description | string | 错误描述 |
| system_response | string | 系统响应信息 |
| error_causes | array | 致错原因列表 |
| context | object | 错误上下文信息 |

### AccessInfo 访问信息

```json
{
  "creator_id": "2",
  "modifier_id": "2",
  "create_time": "2025-06-09T02:54:33Z",
  "update_time": "2025-06-09T02:54:33Z"
}
```

### FilterCondition 筛选条件

```json
{
  "function": "EQUAL",
  "params": [
    {
      "param_type": "FIELD",
      "field": "user.city"
    },
    {
      "param_type": "VALUE",
      "value": {
        "data_type": "STRING",
        "string_value": "北京"
      }
    }
  ],
  "index": 0
}
```

**支持的函数类型**:
- `EQUAL`, `NOT_EQUAL`: 等于、不等于
- `IN`, `NOT_IN`: 包含、不包含
- `LESS`, `LESS_EQUAL`, `GREATER`, `GREATER_EQUAL`: 小于、小于等于、大于、大于等于
- `BETWEEN`: 区间判断
- `IS_SET`, `IS_NOT_SET`: 有值、无值
- `CONTAIN`, `NOT_CONTAIN`: 包含文本、不包含文本
- `IS_TRUE`, `IS_FALSE`: 布尔判断

### CompoundFilterCondition 复合筛选条件

```json
{
  "operator": "AND",
  "conditions": [
    {
      "function": "EQUAL",
      "params": []
    }
  ],
  "compound_conditions": [],
  "index": 0
}
```

---

## 公共请求头

所有 API 接口都需要以下请求头：

| Header 名称 | 类型 | 必填 | 描述 |
|-------------|------|------|------|
| api-key | string | 是 | 全局唯一的密钥，用于验证和授权访问 API 接口 |
| sensorsdata-project | string | 是 | 项目名, 指定请求所属项目 |

---

## 附录

### 枚举类型说明

#### DashboardType（概览类型）
- `DASHBOARD_TYPE_UNSPECIFIED`: 未指定
- `PRIVATE`: 私有
- `PUBLIC`: 公共

#### BookmarkModelType（书签模型类型）
- `SEGMENTATION_MODEL`: 事件分析
- `RETENTION_MODEL`: 留存分析
- `FUNNEL_MODEL`: 漏斗分析
- `LTV_MODEL`: LTV 分析
- `USER_ANALYTICS_MODEL`: 用户分析
- `ADDICTION_MODEL`: 分布分析
- `INTERVAL_MODEL`: 间隔分析
- `ATTRIBUTION_MODEL`: 归因分析
- `SESSION_MODEL`: 会话分析
- `FANCY_METRIC_MODEL`: 自定义指标
- `BEHAVIOR_PATH_MODEL`: 行为路径

#### UnitType（时间单位）
- `HOUR`: 小时
- `DAY`: 天
- `WEEK`: 周
- `MONTH`: 月
- `YEAR`: 年
- `QUARTER`: 季度
- `MINUTE`: 分钟
- `SECOND`: 秒

#### DataType（数据类型）
- `BOOL`: 布尔
- `INT`: 整数
- `NUMBER`: 数值
- `STRING`: 字符串
- `LIST`: 列表
- `DATETIME`: 日期时间
- `DATE`: 日期
- `BIGINT`: 大整数
- `DECIMAL`: 小数

---

**文档版本**: v1.0
**最后更新**: 2026-03-06
**文档生成工具**: Based on OpenAPI 3.0.1 Specifications
