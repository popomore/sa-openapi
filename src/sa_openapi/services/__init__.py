"""Services for sa-openapi."""

from .channel import ChannelServiceV1
from .dashboard import DashboardServiceV1
from .dataset import DatasetServiceV1
from .event_meta import EventMetaServiceV1
from .model import ModelServiceV1
from .property_meta import PropertyMetaServiceV1
from .smart_alarm import SmartAlarmServiceV1

__all__ = [
    "ChannelService",
    "ChannelServiceV1",
    "DashboardService",
    "DashboardServiceV1",
    "DatasetService",
    "DatasetServiceV1",
    "EventMetaService",
    "EventMetaServiceV1",
    "ModelService",
    "ModelServiceV1",
    "PropertyMetaService",
    "PropertyMetaServiceV1",
    "SmartAlarmService",
    "SmartAlarmServiceV1",
]

# Backward-compatible aliases
ChannelService = ChannelServiceV1
DashboardService = DashboardServiceV1
DatasetService = DatasetServiceV1
EventMetaService = EventMetaServiceV1
ModelService = ModelServiceV1
PropertyMetaService = PropertyMetaServiceV1
SmartAlarmService = SmartAlarmServiceV1
