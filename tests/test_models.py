"""Tests for models."""

from sa_openapi.models.channel import CampaignDetail, ChannelLinkDetail
from sa_openapi.models.dashboard import Bookmark, DashboardType, Navigation
from sa_openapi.models.dataset import (
    Dataset,
    DatasetDetailResponse,
    DatasetRefreshResponse,
    DatasetSyncTaskDetailResponse,
    Schema,
    SchemaField,
)
from sa_openapi.models.event_meta import EventDefine, TagInfo
from sa_openapi.models.model import (
    AddictionReportResponse,
    FunnelReportRequest,
    FunnelReportResponse,
    IntervalReportResponse,
    LtvReportResponse,
    Measure,
    RetentionReportRequest,
    RetentionReportResponse,
    SegmentationReportResponse,
    SessionReportResponse,
    UserPropertyReportResponse,
)
from sa_openapi.models.property_meta import (
    EventWithProperty,
    GetPropertyValueRequest,
    PropertyDefine,
    UserGroupDefine,
    UserTagDirDefine,
)
from sa_openapi.models.smart_alarm import (
    SmartAlarmConfig,
    SmartAlarmListResponse,
)


def test_dashboard_type():
    assert DashboardType.PRIVATE == "PRIVATE"
    assert DashboardType.PUBLIC == "PUBLIC"


def test_navigation_model():
    nav = Navigation(
        id=1,
        name="Test Navigation",
        type=DashboardType.PRIVATE,
        ownerId=100,
        createdAt="2024-01-01T00:00:00",
    )
    assert nav.id == 1
    assert nav.name == "Test Navigation"
    assert nav.type == DashboardType.PRIVATE
    assert nav.owner_id == 100


def test_bookmark_model():
    bookmark = Bookmark(
        id=1,
        name="Test Bookmark",
        type="CHART",
        user_id=100,
        create_time="2024-01-01T00:00:00",
    )
    assert bookmark.id == 1
    assert bookmark.name == "Test Bookmark"
    assert bookmark.user_id == 100


def test_campaign_detail_model():
    campaign = CampaignDetail(
        campaign_name="春节活动",
        branch_num=5,
        latest_use_time="2024-01-01T00:00:00",
    )
    assert campaign.campaign_name == "春节活动"
    assert campaign.branch_num == 5


def test_channel_link_detail_model():
    link = ChannelLinkDetail(
        id=1,
        name="APP通用渠道",
        channel_type="APP",
        device_type="iOS",
        short_url="https://short.url/abc",
    )
    assert link.id == 1
    assert link.channel_type == "APP"


def test_dataset_model():
    dataset = Dataset(
        id=1,
        name="Test Dataset",
        type="EVENT",
        createdAt="2024-01-01T00:00:00",
    )
    assert dataset.id == 1
    assert dataset.type == "EVENT"


def test_schema_model():
    schema = Schema(
        fields=[
            SchemaField(name="user_id", field_type="string", nullable=False),
            SchemaField(name="event", field_type="string", nullable=False),
        ]
    )
    assert len(schema.fields) == 2
    assert schema.fields[0].name == "user_id"


def test_measure_model():
    # v1 uses event_name instead of event
    measure = Measure(event_name="view_product", aggregator="COUNT")
    assert measure.event_name == "view_product"
    assert measure.aggregator == "COUNT"


def test_filter_model():
    # v1 model uses 'field' instead of 'property'
    from sa_openapi.models.model import ApiRequestElementCondition

    cond = ApiRequestElementCondition(field="user_id", function="=", params=["123"])
    assert cond.field == "user_id"
    assert cond.function == "="


def test_funnel_request():
    params = FunnelReportRequest(
        funnel={"steps": [{"event_name": "view_product"}]},
        fromDate="2024-01-01",
        toDate="2024-01-31",
    )
    assert params.funnel is not None
    assert params.from_date == "2024-01-01"


def test_funnel_response():
    report = FunnelReportResponse(
        metadata_columns={"step": "string", "count": "number"},
        detail_rows=[["step1", 100], ["step2", 50]],
    )
    assert report.metadata_columns is not None
    assert len(report.detail_rows) == 2


def test_retention_request():
    params = RetentionReportRequest(
        fromDate="2024-01-01",
        toDate="2024-01-31",
        duration=7,
    )
    assert params.from_date == "2024-01-01"
    assert params.duration == 7


def test_retention_response():
    report = RetentionReportResponse(
        metadata_columns={"period": "int", "rate": "number"},
        detail_rows=[[1, 0.8], [3, 0.6]],
    )
    assert report.metadata_columns is not None
    assert len(report.detail_rows) == 2


# ============================================================================
# EventMeta models
# ============================================================================


def test_event_define_model():
    event = EventDefine(
        id=1,
        name="$pageview",
        cname="页面浏览",
        is_virtual=False,
        tags=[10, 20],
        total_count=5000,
        platforms=["iOS", "Android"],
    )
    assert event.id == 1
    assert event.name == "$pageview"
    assert event.cname == "页面浏览"
    assert event.is_virtual is False
    assert event.tags == [10, 20]
    assert event.total_count == 5000
    assert event.platforms == ["iOS", "Android"]


def test_event_define_defaults():
    event = EventDefine(id=2, name="click", cname="点击")
    assert event.is_virtual is False
    assert event.tags == []
    assert event.platforms == []
    assert event.comment is None


def test_tag_info_model():
    tag = TagInfo(id=10, name="核心事件", color="#FF5733")
    assert tag.id == 10
    assert tag.name == "核心事件"
    assert tag.color == "#FF5733"


def test_tag_info_no_color():
    tag = TagInfo(id=11, name="其他事件")
    assert tag.color is None


# ============================================================================
# PropertyMeta models
# ============================================================================


def test_property_define_model():
    prop = PropertyDefine(
        id=1,
        name="city",
        cname="城市",
        data_type="string",
        is_virtual=False,
        has_dict=True,
        platforms=["Web"],
    )
    assert prop.id == 1
    assert prop.name == "city"
    assert prop.data_type == "string"
    assert prop.has_dict is True
    assert prop.platforms == ["Web"]


def test_user_group_define_model():
    group = UserGroupDefine(
        id=100,
        name="high_value_users",
        cname="高价值用户",
        data_type="string",
        create_time="2024-01-01",
    )
    assert group.id == 100
    assert group.name == "high_value_users"
    assert group.cname == "高价值用户"
    assert group.create_time == "2024-01-01"


def test_user_tag_dir_define_model():
    node = UserTagDirDefine(
        name="rfm_level",
        cname="RFM等级",
        data_type="string",
        type="tag",
    )
    assert node.name == "rfm_level"
    assert node.type == "tag"
    assert node.sub_nodes == []


def test_user_tag_dir_define_recursive():
    child = UserTagDirDefine(name="tag_a", cname="标签A", data_type="string", type="tag")
    parent = UserTagDirDefine(
        name="dir_root",
        cname="根目录",
        data_type="string",
        type="dir",
        sub_nodes=[child],
    )
    assert len(parent.sub_nodes) == 1
    assert parent.sub_nodes[0].name == "tag_a"


def test_event_with_property_model():
    ewp = EventWithProperty(
        eventDefine={"id": 1, "name": "$pageview"},
        properties=[
            {"id": 1, "name": "city", "cname": "城市", "data_type": "string"}
        ],
    )
    assert ewp.event_define["name"] == "$pageview"
    assert len(ewp.properties) == 1
    assert ewp.properties[0].name == "city"


def test_get_property_value_request():
    req = GetPropertyValueRequest(tableType="event", propertyName="city", limit=50)
    assert req.table_type == "event"
    assert req.property_name == "city"
    assert req.limit == 50
    dumped = req.model_dump(by_alias=True, exclude_none=True)
    assert dumped["tableType"] == "event"
    assert dumped["propertyName"] == "city"


# ============================================================================
# SmartAlarm models
# ============================================================================


def test_smart_alarm_config_model():
    alarm = SmartAlarmConfig(
        id=42,
        title="DAU异常报警",
        emails=["admin@example.com", "ops@example.com"],
        unit="day",
        sendAlarm=True,
    )
    assert alarm.id == 42
    assert alarm.title == "DAU异常报警"
    assert alarm.send_alarm is True
    assert len(alarm.emails) == 2


def test_smart_alarm_config_alias():
    # Test both alias and snake_case construction
    alarm1 = SmartAlarmConfig(
        id=1, title="test", unit="day", sendAlarm=False, emails=[]
    )
    alarm2 = SmartAlarmConfig(
        id=1, title="test", unit="day", send_alarm=False, emails=[]
    )
    assert alarm1.send_alarm is False
    assert alarm2.send_alarm is False


def test_smart_alarm_list_response():
    resp = SmartAlarmListResponse(total=5, ids=[1, 2, 3, 4, 5])
    assert resp.total == 5
    assert len(resp.ids) == 5


# ============================================================================
# Dataset models (new OpenAPI-aligned)
# ============================================================================


def test_dataset_detail_response_model():
    from sa_openapi.models.dataset import ColumnMeta

    detail = DatasetDetailResponse(
        dataset_id=123,
        dataset_type="EVENT",
        dataset_cname="用户行为数据集",
        columns=[
            ColumnMeta(column_name="user_id", data_type="string"),
            ColumnMeta(column_name="event_time", data_type="datetime"),
        ],
        sync_status="SUCCESS",
    )
    assert detail.dataset_id == 123
    assert detail.dataset_type == "EVENT"
    assert len(detail.columns) == 2
    assert detail.columns[0].column_name == "user_id"
    assert detail.sync_status == "SUCCESS"


def test_dataset_refresh_response():
    resp = DatasetRefreshResponse(sync_task_id="task-abc-123")
    assert resp.sync_task_id == "task-abc-123"


def test_dataset_sync_task_detail_response():
    task = DatasetSyncTaskDetailResponse(
        sync_task_id="task-abc-123",
        sync_status="RUNNING",
        start_time="2024-01-01T00:00:00",
        duration_seconds=120,
    )
    assert task.sync_task_id == "task-abc-123"
    assert task.sync_status == "RUNNING"
    assert task.duration_seconds == 120


# ============================================================================
# Model report responses (new)
# ============================================================================


def test_segmentation_report_response():
    report = SegmentationReportResponse(
        truncated=False,
        metadataColumns={"segment": "string", "count": "number"},
        detailRows=[["高价值", 1000], ["低价值", 500]],
    )
    assert report.truncated is False
    assert report.metadata_columns is not None
    assert len(report.detail_rows) == 2


def test_interval_report_response():
    report = IntervalReportResponse(
        truncated=True,
        metadataColumns={"interval": "int"},
        detailRows=[[1], [2], [3]],
    )
    assert report.truncated is True
    assert len(report.detail_rows) == 3


def test_addiction_report_response():
    report = AddictionReportResponse(
        truncated=False,
        byField="user_id",
        metadataColumns={"days": "int", "count": "number"},
        detailRows=[[1, 100], [2, 80]],
    )
    assert report.truncated is False
    assert report.by_field == "user_id"
    assert report.metadata_columns is not None


def test_user_property_report_response():
    report = UserPropertyReportResponse(
        metadataColumns={"city": "string", "count": "number"},
        detailRows=[["北京", 5000], ["上海", 4000]],
    )
    assert report.metadata_columns is not None
    assert len(report.detail_rows) == 2


def test_ltv_report_response():
    report = LtvReportResponse(
        truncated=False,
        metadataColumns={"day": "int", "ltv": "number"},
        detailRows=[[1, 10.5], [7, 35.2], [30, 120.0]],
    )
    assert report.truncated is False
    assert len(report.detail_rows) == 3


def test_session_report_response():
    report = SessionReportResponse(
        metadataColumns={"duration": "int", "sessions": "number"},
        detailRows=[[60, 200], [120, 150]],
    )
    assert report.metadata_columns is not None
    assert len(report.detail_rows) == 2
