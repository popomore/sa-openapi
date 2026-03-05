"""Tests for models."""

from sa_openapi.models.channel import Channel, Link
from sa_openapi.models.dashboard import Bookmark, DashboardType, Navigation
from sa_openapi.models.dataset import Dataset, Schema, SchemaField
from sa_openapi.models.model import (
    Filter,
    FunnelParams,
    FunnelReport,
    FunnelStep,
    Measure,
    RetentionData,
    RetentionParams,
    RetentionReport,
)


def test_dashboard_type():
    """Test dashboard type enum."""
    assert DashboardType.PRIVATE == "PRIVATE"
    assert DashboardType.PUBLIC == "PUBLIC"


def test_navigation_model():
    """Test navigation model."""
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
    """Test bookmark model."""
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
    """Test channel model."""
    channel = Channel(
        id=1,
        name="Test Channel",
        createdAt="2024-01-01T00:00:00",
    )
    assert channel.id == 1
    assert channel.name == "Test Channel"


def test_link_model():
    """Test link model."""
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
    """Test dataset model."""
    dataset = Dataset(
        id=1,
        name="Test Dataset",
        type="EVENT",
        createdAt="2024-01-01T00:00:00",
    )
    assert dataset.id == 1
    assert dataset.type == "EVENT"


def test_schema_model():
    """Test schema model."""
    schema = Schema(
        fields=[
            SchemaField(name="user_id", field_type="string", nullable=False),
            SchemaField(name="event", field_type="string", nullable=False),
        ]
    )
    assert len(schema.fields) == 2
    assert schema.fields[0].name == "user_id"


def test_measure_model():
    """Test measure model."""
    measure = Measure(event="view_product", aggregator="COUNT")
    assert measure.event == "view_product"
    assert measure.aggregator == "COUNT"


def test_filter_model():
    """Test filter model."""
    filter = Filter(property="user_id", operator="=", value="123")
    assert filter.property == "user_id"
    assert filter.operator == "="
    assert filter.value == "123"


def test_funnel_params():
    """Test funnel params."""
    params = FunnelParams(
        measures=[
            Measure(event="view_product", aggregator="COUNT"),
            Measure(event="add_to_cart", aggregator="COUNT"),
        ],
        window=7,
        startDate="2024-01-01",
        endDate="2024-01-31",
    )
    assert len(params.measures) == 2
    assert params.window == 7


def test_funnel_report():
    """Test funnel report."""
    report = FunnelReport(
        steps=[
            FunnelStep(step=1, event="view_product", total=1000, conversion_rate=100.0),
            FunnelStep(step=2, event="add_to_cart", total=500, conversion_rate=50.0),
        ],
        total=1000,
        overall_conversion=50.0,
    )
    assert len(report.steps) == 2
    assert report.total == 1000


def test_retention_params():
    """Test retention params."""
    params = RetentionParams(
        initial_event="sign_up",
        return_event="login",
        periods=[1, 3, 7, 14, 30],
    )
    assert params.initial_event == "sign_up"
    assert params.periods == [1, 3, 7, 14, 30]


def test_retention_report():
    """Test retention report."""
    report = RetentionReport(
        data=[
            RetentionData(period=1, retention_rate=80.0, returned_users=800, total_users=1000),
            RetentionData(period=3, retention_rate=60.0, returned_users=600, total_users=1000),
        ],
        cohort_size=1000,
    )
    assert len(report.data) == 2
    assert report.cohort_size == 1000
