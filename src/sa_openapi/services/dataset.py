"""Dataset service implementation."""

from typing import Any

from .._auth import AuthHandler
from .._transport import AiohttpTransport
from ..models.common import QueryResult
from ..models.dataset import (
    CreateSavedQueryParams,
    Dataset,
    SavedQuery,
    Schema,
)


class DatasetServiceV1:
    """Dataset service for Sensors Analytics."""

    def __init__(self, transport: AiohttpTransport, auth: AuthHandler):
        self._transport = transport
        self._auth = auth
        self._base_url = transport.config.dashboard_v1_base_url

    async def list_dataset(self) -> list[Dataset]:
        """Get dataset list.

        Returns:
            List of datasets
        """
        response = await self._transport.get(f"{self._base_url}/dataset")
        data = response.json()
        return [Dataset(**item) for item in data.get("data", [])]

    async def get_dataset(self, dataset_id: int) -> Dataset:
        """Get specific dataset.

        Args:
            dataset_id: Dataset ID

        Returns:
            Dataset details
        """
        response = await self._transport.get(
            f"{self._base_url}/dataset/{dataset_id}",
        )
        data = response.json()
        return Dataset(**data.get("data", {}))

    async def sql_query(
        self,
        dataset_id: int,
        sql: str,
        limit: int | None = None,
        offset: int | None = None,
    ) -> QueryResult:
        """Execute SQL query on dataset.

        Args:
            dataset_id: Dataset ID
            sql: SQL query string
            limit: Result limit
            offset: Result offset

        Returns:
            Query result
        """
        params: dict[str, Any] = {"sql": sql}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        response = await self._transport.post(
            f"{self._base_url}/dataset/{dataset_id}/data",
            json=params,
        )
        data = response.json()
        return QueryResult(**data.get("data", {}))

    async def get_schema(self, dataset_id: int) -> Schema:
        """Get dataset schema.

        Args:
            dataset_id: Dataset ID

        Returns:
            Dataset schema
        """
        response = await self._transport.get(
            f"{self._base_url}/dataset/{dataset_id}/schema",
        )
        data = response.json()
        return Schema(**data.get("data", {}))

    async def list_saved_query(self, dataset_id: int) -> list[SavedQuery]:
        """Get saved query list for dataset.

        Args:
            dataset_id: Dataset ID

        Returns:
            List of saved queries
        """
        response = await self._transport.get(
            f"{self._base_url}/dataset/{dataset_id}/saved_query",
        )
        data = response.json()
        return [SavedQuery(**item) for item in data.get("data", [])]

    async def create_saved_query(
        self,
        dataset_id: int,
        name: str,
        sql: str,
        description: str | None = None,
    ) -> SavedQuery:
        """Create saved query.

        Args:
            dataset_id: Dataset ID
            name: Query name
            sql: SQL query string
            description: Query description

        Returns:
            Created saved query
        """
        params = CreateSavedQueryParams(
            name=name,
            sql=sql,
            description=description,
        )
        response = await self._transport.post(
            f"{self._base_url}/dataset/{dataset_id}/saved_query",
            json=params.model_dump(by_alias=True, exclude_none=True),
        )
        data = response.json()
        return SavedQuery(**data.get("data", {}))

    async def delete_saved_query(self, dataset_id: int, query_id: int) -> None:
        """Delete saved query.

        Args:
            dataset_id: Dataset ID
            query_id: Query ID
        """
        await self._transport.delete(
            f"{self._base_url}/dataset/{dataset_id}/saved_query/{query_id}",
        )
