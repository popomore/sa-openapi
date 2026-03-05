"""Tests for models."""

from sa_openapi.models.channel import Channel, Link
from sa_openapi.models.dashboard import Bookmark, DashboardType, Navigation
from sa_openapi.models.dataset import Dataset, Schema, SchemaField
from sa_openapi.models.model import (
    FunnelReportRequest,
    FunnelReportResponse,
    Measure,
    RetentionReportRequest,
    RetentionReportResponse,
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
        navigationId=1,
        ownerId=100,
        createdAt="2024-01-01T00:00:00",
    )
    assert bookmark.id == 1
    assert bookmark.name == "Test Bookmark"
    assert bookmark.navigation_id == 1


def test_channel_model():
    channel = Channel(
        id=1,
        name="Test Channel",
        createdAt="2024-01-01T00:00:00",
    )
    assert channel.id == 1
    assert channel.name == "Test Channel"


def test_link_model():
    link = Link(
        id=1,
        name="Test Link",
        channelId=1,
        url="https://example.com",
        createdBy=100,
        createdAt="2024-01-01T00:00:00",
    )
    assert link.id == 1
    assert link.url == "https://example.com"


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
