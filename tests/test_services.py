"""Tests for service wrappers."""

from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

from sa_openapi._auth import AuthHandler
from sa_openapi._transport import Response
from sa_openapi.models.channel import ChannelUrlData
from sa_openapi.models.dataset import DatasetListRequest
from sa_openapi.models.smart_alarm import SmartAlarmListRequest
from sa_openapi.services.channel import ChannelServiceV1
from sa_openapi.services.dashboard import DashboardServiceV1
from sa_openapi.services.dataset import DatasetServiceV1
from sa_openapi.services.event_meta import EventMetaServiceV1
from sa_openapi.services.model import ModelServiceV1
from sa_openapi.services.property_meta import PropertyMetaServiceV1
from sa_openapi.services.smart_alarm import SmartAlarmServiceV1

pytestmark = pytest.mark.asyncio


class StubTransport:
    """Minimal async transport stub for service tests."""

    def __init__(self):
        self.config = SimpleNamespace(
            dashboard_v1_base_url="https://example.sensorsdata.cn/api/v3/analytics/v1",
            model_v1_base_url="https://example.sensorsdata.cn/api/v3/analytics/v1",
        )
        self.get = AsyncMock()
        self.post = AsyncMock()


def make_transport() -> StubTransport:
    return StubTransport()


def make_auth() -> AuthHandler:
    return AuthHandler(api_key="sk-test", project="default")


def make_response(data=None, *, content: bytes | None = None) -> Response:
    if content is None:
        content = json.dumps(data or {}).encode("utf-8")
    return Response(_data=data, content=content, status_code=200)


async def test_dashboard_service_list_navigation_supports_groups_payload():
    """Test navigation parsing from grouped API payloads."""
    transport = make_transport()
    transport.get.return_value = make_response(
        {
            "data": {
                "groups": [
                    {"id": 1, "name": "Main", "type": "PRIVATE"},
                    "skip-me",
                ]
            }
        }
    )
    service = DashboardServiceV1(transport, make_auth())

    items = await service.list_navigation(nav_type="PUBLIC")

    transport.get.assert_awaited_once_with(
        "https://example.sensorsdata.cn/api/v3/analytics/v1/dashboard/navigation",
        params={"type": "PUBLIC"},
    )
    assert [item.display_name for item in items] == ["Main"]


async def test_dashboard_service_list_navigation_accepts_plain_list_payload():
    """Test navigation parsing from list payloads."""
    transport = make_transport()
    transport.get.return_value = make_response(
        {"data": [{"id": 2, "title": "Shared", "type": "PUBLIC"}, 123]}
    )
    service = DashboardServiceV1(transport, make_auth())

    items = await service.list_navigation()

    assert len(items) == 1
    assert items[0].display_name == "Shared"


async def test_dashboard_service_list_bookmarks_builds_optional_filters():
    """Test bookmark filter conversion and parsing."""
    transport = make_transport()
    transport.get.return_value = make_response(
        {"data": {"bookmarks": [{"id": 10, "name": "North Star", "type": "CHART", "user_id": 7}]}}
    )
    service = DashboardServiceV1(transport, make_auth())

    items = await service.list_bookmarks(
        bookmark_type="CHART",
        has_widget=True,
        has_lego=False,
    )

    transport.get.assert_awaited_once_with(
        "https://example.sensorsdata.cn/api/v3/analytics/v1/dashboard/bookmarks",
        params={"type": "CHART", "has_widget": "true", "has_lego": "false"},
    )
    assert items[0].name == "North Star"


async def test_channel_service_list_campaigns():
    """Test campaign listing."""
    transport = make_transport()
    transport.post.return_value = make_response(
        {
            "data": {
                "campaign_details": [{"campaign_name": "spring-launch"}],
                "total_rows": 1,
            }
        }
    )
    service = ChannelServiceV1(transport, make_auth())

    result = await service.list_campaigns(page_num=2, page_size=50)

    transport.post.assert_awaited_once_with(
        "https://example.sensorsdata.cn/api/v3/analytics/v1/channel/campaigns/list",
        json={"page_num": 2, "page_size": 50},
    )
    assert result.total_rows == 1
    assert result.campaign_details[0].campaign_name == "spring-launch"


async def test_channel_service_list_links():
    """Test link listing."""
    transport = make_transport()
    transport.post.return_value = make_response(
        {
            "data": {
                "detail_results": [{"id": 9, "name": "ios-link", "channel_type": "APP"}],
                "total_rows": 1,
            }
        }
    )
    service = ChannelServiceV1(transport, make_auth())

    result = await service.list_links()

    transport.post.assert_awaited_once_with(
        "https://example.sensorsdata.cn/api/v3/analytics/v1/channel/links/list",
        json={"page_num": 1, "page_size": 20},
    )
    assert result.detail_results[0].name == "ios-link"


async def test_channel_service_create_link_normalizes_payload_and_response():
    """Test channel link creation request/response normalization."""
    transport = make_transport()
    transport.post.return_value = make_response(
        {
            "data": {
                "created": 2,
                "duplicated": 0,
                "failed": 0,
                "status": "SUCCESS",
                "channel_urls": {
                    "channel_urls": [
                        {"id": 1, "short_url": "https://s.example/1"},
                        {"id": 2, "short_url": "https://s.example/2"},
                    ]
                },
            }
        }
    )
    service = ChannelServiceV1(transport, make_auth())

    result = await service.create_link(
        [
            {"channel_type": "APP", "target_url": "https://example.com/app"},
            ChannelUrlData(channel_type="WEB", web_landing_page="https://example.com/web"),
        ]
    )

    transport.post.assert_awaited_once_with(
        "https://example.sensorsdata.cn/api/v3/analytics/v1/channel/links/create",
        json={
            "channel_urls": [
                {"channel_type": "APP", "target_url": "https://example.com/app"},
                {"channel_type": "WEB", "web_landing_page": "https://example.com/web"},
            ]
        },
    )
    assert result.created == 2
    assert [item.short_url for item in result.channel_urls] == [
        "https://s.example/1",
        "https://s.example/2",
    ]


async def test_dataset_service_get_detail_and_groups():
    """Test dataset detail and group list requests."""
    transport = make_transport()
    transport.get.side_effect = [
        make_response({"data": {"dataset_id": 11, "dataset_type": "SQL"}}),
        make_response({"data": {"dataset_groups": [{"id": 2, "group_name": "BI"}]}}),
    ]
    service = DatasetServiceV1(transport, make_auth())

    detail = await service.get_dataset_detail(dataset_id=11, model_type="SQL")
    groups = await service.list_dataset_groups()

    assert detail.dataset_id == 11
    assert detail.dataset_type == "SQL"
    assert groups[0].group_name == "BI"
    assert transport.get.await_args_list[0].kwargs["params"] == {
        "dataset_id": 11,
        "model_type": "SQL",
    }


async def test_dataset_service_list_datasets_supports_none_dict_and_model():
    """Test dataset listing request bodies."""
    transport = make_transport()
    transport.post.side_effect = [
        make_response({"data": {"datasets": [{"dataset_id": 1, "dataset_type": "SQL"}]}}),
        make_response({"data": {"datasets": [{"dataset_id": 2, "dataset_type": "VIEW"}]}}),
        make_response({"data": {"datasets": [{"dataset_id": 3, "dataset_type": "EVENT"}]}}),
    ]
    service = DatasetServiceV1(transport, make_auth())

    no_params = await service.list_datasets()
    dict_params = await service.list_datasets({"page_index": 2})
    model_params = await service.list_datasets(
        DatasetListRequest(page_index=3, page_size=25, dataset_types=["SQL"])
    )

    assert no_params[0].dataset_id == 1
    assert dict_params[0].dataset_type == "VIEW"
    assert model_params[0].dataset_type == "EVENT"
    assert [call.kwargs["json"] for call in transport.post.await_args_list] == [
        {},
        {"page_index": 2},
        {"dataset_types": ["SQL"], "page_index": 3, "page_size": 25},
    ]


async def test_dataset_service_sql_and_model_query():
    """Test SQL and model query request serialization."""
    transport = make_transport()
    transport.post.side_effect = [
        make_response({"data": {"columns": ["city"], "data": [["shanghai"]]}}),
        make_response({"data": {"columns": ["cnt"], "data": [[10]]}}),
    ]
    service = DatasetServiceV1(transport, make_auth())

    sql_result = await service.sql_query(
        "select city from users where city = :city",
        query_parameters=[{"param_key": "city", "param_value": "shanghai"}],
        description="city lookup",
    )
    model_result = await service.model_query({"dataset_id": 8, "dimensions": ["city"]})

    assert sql_result.columns == ["city"]
    assert model_result.data == [[10]]
    assert transport.post.await_args_list[0].kwargs["json"] == {
        "sql": "select city from users where city = :city",
        "description": "city lookup",
        "query_parameters": [{"param_key": "city", "param_value": "shanghai"}],
    }
    assert transport.post.await_args_list[1].kwargs["json"] == {
        "dataset_id": 8,
        "dimensions": ["city"],
    }


async def test_dataset_service_refresh_and_sync_task_detail():
    """Test dataset refresh and sync detail calls."""
    transport = make_transport()
    transport.post.return_value = make_response({"data": {"sync_task_id": "sync-1"}})
    transport.get.return_value = make_response(
        {"data": {"sync_task_id": "sync-1", "sync_status": "SUCCESS"}}
    )
    service = DatasetServiceV1(transport, make_auth())

    refresh = await service.refresh_dataset(
        dataset_id=7,
        sync_type="INCREMENTAL",
        refresh_from_date="2024-01-01",
        refresh_to_date="2024-01-31",
    )
    detail = await service.get_sync_task_detail("sync-1")

    assert refresh.sync_task_id == "sync-1"
    assert detail.sync_status == "SUCCESS"
    assert transport.post.await_args.kwargs["json"] == {
        "dataset_id": 7,
        "sync_type": "INCREMENTAL",
        "refresh_from_date": "2024-01-01",
        "refresh_to_date": "2024-01-31",
    }
    assert transport.get.await_args.kwargs["params"] == {"sync_task_id": "sync-1"}


async def test_event_meta_service_lists_events_and_tags():
    """Test event metadata list endpoints."""
    transport = make_transport()
    transport.get.side_effect = [
        make_response({"data": {"events": [{"id": 1, "name": "signup", "cname": "Signup"}]}}),
        make_response({"data": {"tag_infos": [{"id": 9, "name": "core"}]}}),
    ]
    service = EventMetaServiceV1(transport, make_auth())

    events = await service.list_events_all()
    tags = await service.list_event_tags()

    assert events[0].name == "signup"
    assert tags[0].name == "core"


@pytest.mark.parametrize(
    ("method_name", "path", "payload"),
    [
        (
            "funnel_report",
            "model/funnel/report",
            {"detailRows": [["step1", 100]], "metadataColumns": {"step": "string"}},
        ),
        (
            "retention_report",
            "model/retention/report",
            {"detailRows": [[1, 0.8]], "metadataColumns": {"day": "number"}},
        ),
        (
            "attribution_report",
            "model/attribution/report",
            {"detailRows": [["touch", 20]], "metadataColumns": {"name": "string"}},
        ),
        (
            "segmentation_report",
            "model/segmentation/report",
            {"detailRows": [["2024-01-01", 10]], "metadataColumns": {"date": "string"}},
        ),
        (
            "interval_report",
            "model/interval/report",
            {"detailRows": [[1, 3]], "metadataColumns": {"days": "number"}},
        ),
        (
            "addiction_report",
            "model/addiction/report",
            {"detailRows": [[5, 8]], "metadataColumns": {"bucket": "number"}},
        ),
        (
            "user_property_report",
            "model/user-analytics/report",
            {"detailRows": [["vip", 22]], "metadataColumns": {"segment": "string"}},
        ),
        (
            "ltv_report",
            "model/ltv/report",
            {"detailRows": [[0, 1.2]], "metadataColumns": {"period": "number"}},
        ),
        (
            "session_report",
            "model/session/report",
            {"detailRows": [[3, 7]], "metadataColumns": {"count": "number"}},
        ),
    ],
)
async def test_model_service_report_methods(method_name, path, payload):
    """Test report endpoints share request/response handling."""
    transport = make_transport()
    transport.post.return_value = make_response({"data": payload})
    service = ModelServiceV1(transport, make_auth())

    result = await getattr(service, method_name)(sample="value", ignored=None)

    transport.post.assert_awaited_once_with(
        f"https://example.sensorsdata.cn/api/v3/analytics/v1/{path}",
        json={"sample": "value"},
    )
    assert result.detail_rows == payload["detailRows"]


async def test_model_service_sql_query_parses_ndjson_rows():
    """Test NDJSON SQL responses are reduced to row data."""
    transport = make_transport()
    transport.post.return_value = make_response(
        None,
        content=(
            b'{"code":"SUCCESS","data":{"data":["alice", 10]}}\n'
            b"\n"
            b"not-json\n"
            b'{"code":"SUCCESS","data":{"data":["bob", 20]}}\n'
        ),
    )
    service = ModelServiceV1(transport, make_auth())

    result = await service.sql_query("select * from users", limit="100")

    transport.post.assert_awaited_once_with(
        "https://example.sensorsdata.cn/api/v3/analytics/v1/model/sql/query",
        json={"sql": "select * from users", "limit": "100"},
    )
    assert result.data == [["alice", 10], ["bob", 20]]


async def test_model_service_not_supported_sql_helpers():
    """Test unsupported SQL helper methods raise."""
    service = ModelServiceV1(make_transport(), make_auth())

    with pytest.raises(NotImplementedError, match="explain-sql"):
        await service.explain_sql("select 1")

    with pytest.raises(NotImplementedError, match="validate-sql"):
        await service.validate_sql("select 1")


async def test_property_meta_service_list_property_variants():
    """Test property meta list endpoints and fallback keys."""
    transport = make_transport()
    transport.get.side_effect = [
        make_response(
            {
                "data": {
                    "properties": [
                        {"id": 1, "name": "city", "cname": "City", "data_type": "string"}
                    ]
                }
            }
        ),
        make_response(
            {
                "data": {
                    "user_properties": [
                        {"id": 2, "name": "plan", "cname": "Plan", "data_type": "string"}
                    ]
                }
            }
        ),
        make_response(
            {
                "data": {
                    "user_groups": [{"id": 3, "name": "vip", "cname": "VIP", "data_type": "string"}]
                }
            }
        ),
        make_response(
            {
                "data": {
                    "user_tags": [
                        {"name": "rfm", "cname": "RFM", "data_type": "string", "type": "tag"}
                    ]
                }
            }
        ),
    ]
    service = PropertyMetaServiceV1(transport, make_auth())

    event_props = await service.list_all_event_properties()
    user_props = await service.list_all_user_properties()
    user_groups = await service.list_user_groups()
    user_tags = await service.list_user_tags_with_dir()

    assert event_props[0].name == "city"
    assert user_props[0].name == "plan"
    assert user_groups[0].name == "vip"
    assert user_tags[0].name == "rfm"


async def test_property_meta_service_event_properties_and_values():
    """Test event property query and value lookup."""
    transport = make_transport()
    transport.post.side_effect = [
        make_response(
            {
                "data": {
                    "event_properties": [
                        {
                            "eventDefine": {"name": "signup"},
                            "properties": [
                                {
                                    "id": 4,
                                    "name": "source",
                                    "cname": "Source",
                                    "data_type": "string",
                                }
                            ],
                        }
                    ]
                }
            }
        ),
        make_response({"data": {"values": ["organic", "ads"]}}),
        make_response({"data": []}),
    ]
    service = PropertyMetaServiceV1(transport, make_auth())

    event_properties = await service.list_event_properties(["signup"])
    values = await service.get_property_values("event", "source", limit=5)
    empty_values = await service.get_property_values("user", "plan")

    assert event_properties[0].event_define["name"] == "signup"
    assert values == ["organic", "ads"]
    assert empty_values == []
    assert transport.post.await_args_list[0].kwargs["json"] == {"events": ["signup"]}
    assert transport.post.await_args_list[1].kwargs["json"] == {
        "tableType": "event",
        "propertyName": "source",
        "limit": 5,
    }
    assert transport.post.await_args_list[2].kwargs["json"] == {
        "tableType": "user",
        "propertyName": "plan",
    }


async def test_smart_alarm_service_get_alarm_config():
    """Test smart alarm detail lookup."""
    transport = make_transport()
    transport.get.return_value = make_response(
        {
            "data": {
                "id": 1,
                "title": "traffic-alert",
                "emails": ["ops@example.com"],
                "unit": "day",
                "sendAlarm": True,
            }
        }
    )
    service = SmartAlarmServiceV1(transport, make_auth())

    result = await service.get_alarm_config(1)

    transport.get.assert_awaited_once_with(
        "https://example.sensorsdata.cn/api/v3/analytics/v1/smart-alarm/detail",
        params={"config_id": 1},
    )
    assert result.title == "traffic-alert"


async def test_smart_alarm_service_list_alarms_supports_none_dict_and_model():
    """Test smart alarm list request bodies."""
    transport = make_transport()
    transport.post.side_effect = [
        make_response({"data": {"total": 1, "ids": [1]}}),
        make_response({"data": {"total": 2, "ids": [2, 3]}}),
        make_response({"data": {"total": 1, "ids": [4]}}),
    ]
    service = SmartAlarmServiceV1(transport, make_auth())

    empty = await service.list_alarms()
    dict_params = await service.list_alarms({"title": "warning"})
    model_params = await service.list_alarms(
        SmartAlarmListRequest(title="critical", createUserIds=[9])
    )

    assert empty.total == 1
    assert dict_params.ids == [2, 3]
    assert model_params.ids == [4]
    assert [call.kwargs["json"] for call in transport.post.await_args_list] == [
        {},
        {"title": "warning"},
        {"title": "critical", "createUserIds": [9]},
    ]
