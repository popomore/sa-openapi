"""Services for sa-openapi."""

from .channel import ChannelServiceV1
from .dashboard import DashboardServiceV1
from .dataset import DatasetServiceV1
from .model import ModelServiceV1

__all__ = [
    "ChannelService",
    "ChannelServiceV1",
    "DashboardService",
    "DashboardServiceV1",
    "DatasetService",
    "DatasetServiceV1",
    "ModelService",
    "ModelServiceV1",
]

# Backward-compatible aliases
ChannelService = ChannelServiceV1
DashboardService = DashboardServiceV1
DatasetService = DatasetServiceV1
ModelService = ModelServiceV1
