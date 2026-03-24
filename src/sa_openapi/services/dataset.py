"""Dataset service implementation."""

from typing import Any

from .._auth import AuthHandler
from .._transport import AiohttpTransport
from ..models.dataset import (
    DatasetDetailResponse,
    DatasetGroup,
    DatasetListRequest,
    DatasetModelRequest,
    DatasetModelResponse,
    DatasetRefreshRequest,
    DatasetRefreshResponse,
    DatasetResponse,
    DatasetSyncTaskDetailResponse,
    DatasetTableSqlRequest,
    DatasetTableSqlResponse,
)


class DatasetServiceV1:
    """Dataset service for Sensors Analytics (OpenAPI v1)."""

    def __init__(self, transport: AiohttpTransport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.dashboard_v1_base_url

    async def get_dataset_detail(
        self,
        dataset_id: int,
        model_type: str | None = None,
    ) -> DatasetDetailResponse:
        """Get dataset detail information.

        Args:
            dataset_id: Dataset ID
            model_type: Optional model type filter

        Returns:
            Dataset detail
        """
        params: dict[str, Any] = {"dataset_id": dataset_id}
        if model_type is not None:
            params["model_type"] = model_type

        response = await self._transport.get(
            f"{self._base_url}/dataset/detail",
            params=params,
        )
        data = response.json()
        return DatasetDetailResponse(**data.get("data", {}))

    async def list_datasets(
        self,
        params: DatasetListRequest | dict[str, Any] | None = None,
    ) -> list[DatasetResponse]:
        """Get dataset list.

        Args:
            params: Filter parameters

        Returns:
            List of datasets
        """
        if params is None:
            body: dict[str, Any] = {}
        elif isinstance(params, dict):
            body = params
        else:
            body = params.model_dump(by_alias=True, exclude_none=True)

        response = await self._transport.post(
            f"{self._base_url}/dataset/detail_list",
            json=body,
        )
        data = response.json()
        raw = data.get("data", {})
        datasets = raw.get("datasets", []) if isinstance(raw, dict) else []
        return [DatasetResponse(**item) for item in datasets if isinstance(item, dict)]

    async def list_dataset_groups(self) -> list[DatasetGroup]:
        """Get dataset group list.

        Returns:
            List of dataset groups
        """
        response = await self._transport.get(
            f"{self._base_url}/dataset/group/list",
        )
        data = response.json()
        raw = data.get("data", {})
        groups = (
            raw.get("datasetGroups", raw.get("dataset_groups", [])) if isinstance(raw, dict) else []
        )
        return [DatasetGroup(**item) for item in groups if isinstance(item, dict)]

    async def sql_query(
        self,
        sql: str,
        query_parameters: list[dict[str, str]] | None = None,
        description: str | None = None,
    ) -> DatasetTableSqlResponse:
        """Execute SQL query on dataset.

        Args:
            sql: SQL query string
            query_parameters: Optional named query parameters
            description: Optional description

        Returns:
            Query result with columns and data
        """
        req = DatasetTableSqlRequest(
            sql=sql,
            description=description,
        )
        body = req.model_dump(by_alias=True, exclude_none=True)
        if query_parameters:
            body["query_parameters"] = query_parameters

        response = await self._transport.post(
            f"{self._base_url}/dataset/table/sql_query",
            json=body,
        )
        data = response.json()
        return DatasetTableSqlResponse(**data.get("data", {}))

    async def model_query(
        self,
        params: DatasetModelRequest | dict[str, Any],
    ) -> DatasetModelResponse:
        """Query dataset using dimension/measure rules.

        Args:
            params: Query parameters including dataset_id, dimensions, measures

        Returns:
            Query result
        """
        if isinstance(params, dict):
            params = DatasetModelRequest(**params)

        response = await self._transport.post(
            f"{self._base_url}/dataset/model/query",
            json=params.model_dump(by_alias=True, exclude_none=True),
        )
        data = response.json()
        return DatasetModelResponse(**data.get("data", {}))

    async def refresh_dataset(
        self,
        dataset_id: int,
        sync_type: str | None = None,
        refresh_from_date: str | None = None,
        refresh_to_date: str | None = None,
    ) -> DatasetRefreshResponse:
        """Trigger dataset data refresh.

        Args:
            dataset_id: Dataset ID
            sync_type: Sync type
            refresh_from_date: Start date for incremental refresh
            refresh_to_date: End date for incremental refresh

        Returns:
            Refresh task response with sync_task_id
        """
        req = DatasetRefreshRequest(
            dataset_id=dataset_id,
            sync_type=sync_type,
            refresh_from_date=refresh_from_date,
            refresh_to_date=refresh_to_date,
        )
        response = await self._transport.post(
            f"{self._base_url}/dataset/refresh",
            json=req.model_dump(by_alias=True, exclude_none=True),
        )
        data = response.json()
        return DatasetRefreshResponse(**data.get("data", {}))

    async def get_sync_task_detail(self, sync_task_id: str) -> DatasetSyncTaskDetailResponse:
        """Get the status of a dataset sync task.

        Args:
            sync_task_id: Sync task ID returned by refresh_dataset

        Returns:
            Sync task status
        """
        response = await self._transport.get(
            f"{self._base_url}/dataset/sync_task_detail",
            params={"sync_task_id": sync_task_id},
        )
        data = response.json()
        return DatasetSyncTaskDetailResponse(**data.get("data", {}))
