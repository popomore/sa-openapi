"""Model service implementation - OpenAPI v1 aligned."""

from typing import Any

from .._auth import AuthHandler
from .._transport import AiohttpTransport
from ..models.model import (
    AddictionReportResponse,
    AttributionReportResponse,
    FunnelReportResponse,
    IntervalReportResponse,
    LtvReportResponse,
    RetentionReportResponse,
    SegmentationReportResponse,
    SessionReportResponse,
    SqlExplainResult,
    SqlQueryResponse,
    SqlValidateResult,
    UserPropertyReportResponse,
)


class ModelServiceV1:
    """Model service for Sensors Analytics (v1 API: funnel, retention, attribution)."""

    def __init__(self, transport: AiohttpTransport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.model_v1_base_url

    async def funnel_report(
        self,
        funnel: dict[str, Any] | None = None,
        from_date: str | None = None,
        to_date: str | None = None,
        filter: dict[str, Any] | None = None,
        by_fields: list[str] | None = None,
        **kwargs: Any,
    ) -> FunnelReportResponse:
        """Get funnel analysis report (v1)."""
        params: dict[str, Any] = {}
        if funnel is not None:
            params["funnel"] = funnel
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        if filter:
            params["filter"] = filter
        if by_fields:
            params["byFields"] = by_fields
        for k, v in kwargs.items():
            if v is not None:
                params[k] = v

        response = await self._transport.post(
            f"{self._base_url}/model/funnel/report",
            json=params,
        )
        data = response.json()
        payload = data.get("data", {})
        return FunnelReportResponse(**payload)

    async def retention_report(
        self,
        from_date: str | None = None,
        to_date: str | None = None,
        duration: int | None = None,
        first_event: dict[str, Any] | None = None,
        second_event: dict[str, Any] | None = None,
        filter: dict[str, Any] | None = None,
        measures: list[dict[str, Any]] | None = None,
        **kwargs: Any,
    ) -> RetentionReportResponse:
        """Get retention analysis report (v1)."""
        params: dict[str, Any] = {}
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        if duration is not None:
            params["duration"] = duration
        if first_event:
            params["firstEvent"] = first_event
        if second_event:
            params["secondEvent"] = second_event
        if filter:
            params["filter"] = filter
        if measures:
            params["measures"] = measures
        for k, v in kwargs.items():
            if v is not None:
                params[k] = v

        response = await self._transport.post(
            f"{self._base_url}/model/retention/report",
            json=params,
        )
        data = response.json()
        payload = data.get("data", {})
        return RetentionReportResponse(**payload)

    async def attribution_report(
        self,
        from_date: str | None = None,
        to_date: str | None = None,
        target_event: dict[str, Any] | None = None,
        link_events: list[dict[str, Any]] | None = None,
        model_type: str | None = None,
        **kwargs: Any,
    ) -> AttributionReportResponse:
        """Get attribution analysis report (v1)."""
        params: dict[str, Any] = {}
        if from_date:
            params["fromDate"] = from_date
        if to_date:
            params["toDate"] = to_date
        if target_event:
            params["targetEvent"] = target_event
        if link_events:
            params["linkEvents"] = link_events
        if model_type:
            params["modelType"] = model_type
        for k, v in kwargs.items():
            if v is not None:
                params[k] = v

        response = await self._transport.post(
            f"{self._base_url}/model/attribution/report",
            json=params,
        )
        data = response.json()
        payload = data.get("data", {})
        return AttributionReportResponse(**payload)

    async def sql_query(
        self,
        sql: str,
        limit: str | None = None,
    ) -> SqlQueryResponse:
        """Execute custom SQL query (v1)."""
        params: dict[str, Any] = {"sql": sql}
        if limit is not None:
            params["limit"] = str(limit)

        response = await self._transport.post(
            f"{self._base_url}/model/sql/query",
            json=params,
        )
        data = response.json()
        payload = data.get("data", {})
        return SqlQueryResponse(**payload)

    async def segmentation_report(self, **kwargs: Any) -> SegmentationReportResponse:
        """Get segmentation (事件分析) report.

        Args:
            **kwargs: Report parameters (measures, from_date, to_date, unit, filter, by_fields, etc.)

        Returns:
            Segmentation report response
        """
        params: dict[str, Any] = {k: v for k, v in kwargs.items() if v is not None}
        response = await self._transport.post(
            f"{self._base_url}/model/segmentation/report",
            json=params,
        )
        data = response.json()
        return SegmentationReportResponse(**data.get("data", {}))

    async def interval_report(self, **kwargs: Any) -> IntervalReportResponse:
        """Get interval (间隔分析) report.

        Args:
            **kwargs: Report parameters (filter, first_event, second_event, unit, from_date, to_date, etc.)

        Returns:
            Interval report response
        """
        params: dict[str, Any] = {k: v for k, v in kwargs.items() if v is not None}
        response = await self._transport.post(
            f"{self._base_url}/model/interval/report",
            json=params,
        )
        data = response.json()
        return IntervalReportResponse(**data.get("data", {}))

    async def addiction_report(self, **kwargs: Any) -> AddictionReportResponse:
        """Get addiction (分布分析) report.

        Args:
            **kwargs: Report parameters (event_name, from_date, to_date, filter, unit, etc.)

        Returns:
            Addiction report response
        """
        params: dict[str, Any] = {k: v for k, v in kwargs.items() if v is not None}
        response = await self._transport.post(
            f"{self._base_url}/model/addiction/report",
            json=params,
        )
        data = response.json()
        return AddictionReportResponse(**data.get("data", {}))

    async def user_property_report(self, **kwargs: Any) -> UserPropertyReportResponse:
        """Get user analytics (属性分析) report.

        Args:
            **kwargs: Report parameters (measures, filter, by_fields, x_axis_field, etc.)

        Returns:
            User property report response
        """
        params: dict[str, Any] = {k: v for k, v in kwargs.items() if v is not None}
        response = await self._transport.post(
            f"{self._base_url}/model/user-analytics/report",
            json=params,
        )
        data = response.json()
        return UserPropertyReportResponse(**data.get("data", {}))

    async def ltv_report(self, **kwargs: Any) -> LtvReportResponse:
        """Get LTV analysis report.

        Args:
            **kwargs: Report parameters (from_date, to_date, duration, start_sign, measures, unit, etc.)

        Returns:
            LTV report response
        """
        params: dict[str, Any] = {k: v for k, v in kwargs.items() if v is not None}
        response = await self._transport.post(
            f"{self._base_url}/model/ltv/report",
            json=params,
        )
        data = response.json()
        return LtvReportResponse(**data.get("data", {}))

    async def session_report(self, **kwargs: Any) -> SessionReportResponse:
        """Get session analysis report.

        Args:
            **kwargs: Report parameters (measures, from_date, to_date, unit, filter, session_name, etc.)

        Returns:
            Session report response
        """
        params: dict[str, Any] = {k: v for k, v in kwargs.items() if v is not None}
        response = await self._transport.post(
            f"{self._base_url}/model/session/report",
            json=params,
        )
        data = response.json()
        return SessionReportResponse(**data.get("data", {}))

    async def explain_sql(self, sql: str) -> SqlExplainResult:
        raise NotImplementedError("explain-sql is not supported by Model v1 API")

    async def validate_sql(self, sql: str) -> SqlValidateResult:
        raise NotImplementedError("validate-sql is not supported by Model v1 API")
