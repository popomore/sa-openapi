"""SmartAlarm service implementation."""

from typing import Any

from .._auth import AuthHandler
from .._transport import AiohttpTransport
from ..models.smart_alarm import SmartAlarmConfig, SmartAlarmListRequest, SmartAlarmListResponse


class SmartAlarmServiceV1:
    """SmartAlarm service for Sensors Analytics."""

    def __init__(self, transport: AiohttpTransport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.dashboard_v1_base_url

    async def get_alarm_config(self, config_id: int) -> SmartAlarmConfig:
        """Get a smart alarm configuration detail.

        Args:
            config_id: Alarm config ID

        Returns:
            Alarm configuration
        """
        response = await self._transport.get(
            f"{self._base_url}/smart-alarm/detail",
            params={"config_id": config_id},
        )
        data = response.json()
        return SmartAlarmConfig(**data.get("data", {}))

    async def list_alarms(
        self,
        params: SmartAlarmListRequest | dict[str, Any] | None = None,
    ) -> SmartAlarmListResponse:
        """Get all smart alarms list.

        Args:
            params: Filter parameters (title, units, create_user_ids, disables)

        Returns:
            Alarm list response with total count and IDs
        """
        if params is None:
            body: dict[str, Any] = {}
        elif isinstance(params, dict):
            body = params
        else:
            body = params.model_dump(by_alias=True, exclude_none=True)

        response = await self._transport.post(
            f"{self._base_url}/smart-alarm/all",
            json=body,
        )
        data = response.json()
        return SmartAlarmListResponse(**data.get("data", {}))
