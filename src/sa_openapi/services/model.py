"""Model service implementation."""

from typing import Any

from .._auth import AuthHandler
from .._transport import AiohttpTransport
from ..models.model import (
    AttributionReport,
    FunnelReport,
    RetentionReport,
    SqlExplainResult,
    SqlValidateResult,
)


class ModelServiceV1:
    """Model service for Sensors Analytics (v1 API: funnel, retention, attribution)."""

    def __init__(self, transport: AiohttpTransport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.model_v1_base_url

    async def funnel_report(
        self,
        measures: list[dict[str, Any]],
        filter: dict[str, Any] | None = None,
        by_fields: list[dict[str, Any]] | None = None,
        window: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> FunnelReport:
        """Get funnel analysis report.

        Args:
            measures: List of measure definitions
            filter: Filter conditions
            by_fields: Group by fields
            window: Conversion window in days
            start_date: Start date
            end_date: End date

        Returns:
            Funnel report
        """
        params: dict[str, Any] = {"measures": measures}
        if filter:
            params["filter"] = filter
        if by_fields:
            params["byFields"] = by_fields
        if window is not None:
            params["window"] = window
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        response = await self._transport.post(
            f"{self._base_url}/model/funnel/report",
            json=params,
        )
        data = response.json()
        return FunnelReport(**data.get("data", {}))

    async def retention_report(
        self,
        initial_event: str,
        return_event: str,
        periods: list[int],
        filter: dict[str, Any] | None = None,
        by_fields: list[dict[str, Any]] | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> RetentionReport:
        """Get retention analysis report.

        Args:
            initial_event: Initial event name
            return_event: Return event name
            periods: Retention periods [1, 3, 7, 14, 30]
            filter: Filter conditions
            by_fields: Group by fields
            start_date: Start date
            end_date: End date

        Returns:
            Retention report
        """
        params: dict[str, Any] = {
            "initialEvent": initial_event,
            "returnEvent": return_event,
            "periods": periods,
        }
        if filter:
            params["filter"] = filter
        if by_fields:
            params["byFields"] = by_fields
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        response = await self._transport.post(
            f"{self._base_url}/model/retention/report",
            json=params,
        )
        data = response.json()
        return RetentionReport(**data.get("data", {}))

    async def attribution_report(
        self,
        conversion_event: str,
        touch_points: list[str],
        model: str,
        window: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> AttributionReport:
        """Get attribution analysis report.

        Args:
            conversion_event: Conversion event name
            touch_points: List of touch point event names
            model: Attribution model (FIRST_TOUCH, LAST_TOUCH, LINEAR, etc.)
            window: Attribution window in days
            start_date: Start date
            end_date: End date

        Returns:
            Attribution report
        """
        params: dict[str, Any] = {
            "conversionEvent": conversion_event,
            "touchPoints": touch_points,
            "model": model,
        }
        if window is not None:
            params["window"] = window
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date

        response = await self._transport.post(
            f"{self._base_url}/model/attribution/report",
            json=params,
        )
        data = response.json()
        return AttributionReport(**data.get("data", {}))

    async def sql_query(
        self,
        sql: str,
        limit: int | None = None,
    ) -> Any:
        """Execute custom SQL query.

        Args:
            sql: SQL query string
            limit: Result limit

        Returns:
            Query result
        """
        params: dict[str, Any] = {"sql": sql}
        if limit is not None:
            params["limit"] = limit

        response = await self._transport.post(
            f"{self._base_url}/model/sql/query",
            json=params,
        )
        data = response.json()
        result = data.get("data") or {}
        # v1 uses "data" for rows; may be flat array (single row) or list of lists
        if "data" in result and "rows" not in result:
            raw = result.pop("data")
            # v1 single row: flat array [v1, v2, ...]; multi row: [[v1,v2], [v1,v2], ...]
            if raw and not isinstance(raw[0], (list, tuple)):
                raw = [raw]
            result["rows"] = raw
        return result

    async def explain_sql(self, sql: str) -> SqlExplainResult:
        """Get SQL execution plan.

        Args:
            sql: SQL query string

        Returns:
            SQL execution plan
        """
        response = await self._transport.post(
            f"{self._base_url}/model/sql/explain",
            json={"sql": sql},
        )
        data = response.json()
        return SqlExplainResult(**data.get("data", {}))

    async def validate_sql(self, sql: str) -> SqlValidateResult:
        """Validate SQL syntax.

        Args:
            sql: SQL query string

        Returns:
            Validation result
        """
        response = await self._transport.post(
            f"{self._base_url}/model/sql/validate",
            json={"sql": sql},
        )
        data = response.json()
        return SqlValidateResult(**data.get("data", {}))
