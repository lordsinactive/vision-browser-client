from typing import List, Optional, Tuple
from uuid import UUID

from httpx import AsyncClient

from ..models import Status, StatusColors


class Statuses:
    session: AsyncClient
    base_url: str

    async def get_statuses(self, folder_id: UUID | str) -> List[Status]:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/statuses'

        response = await self.session.get(url)
        response.raise_for_status()

        return [Status.model_validate(s) for s in response.json()['data']]

    async def create_statuses(
            self,
            folder_id: UUID | str,
            statuses: List[Tuple[str, StatusColors | str]],
    ) -> List[Status]:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/statuses'
        body = {'statuses': [[name, str(color)] for name, color in statuses]}

        response = await self.session.post(url, json=body)
        response.raise_for_status()

        return [Status.model_validate(s) for s in response.json()['data']]

    async def edit_status(
            self,
            folder_id: UUID | str,
            status_id: UUID | str,
            name: Optional[str] = None,
            color: Optional[StatusColors | str] = None,
    ) -> Status:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/statuses/{status_id}'
        body: dict = {}
        if name is not None:
            body['name'] = name
        if color is not None:
            body['color'] = str(color)

        response = await self.session.put(url, json=body)
        response.raise_for_status()

        return Status.model_validate(response.json()['data'])

    async def delete_statuses(
            self,
            folder_id: UUID | str,
            status_ids: List[UUID | str],
    ) -> List[Status]:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/statuses'
        body = {'status_ids': [str(sid) for sid in status_ids]}

        response = await self.session.request('DELETE', url, json=body)
        response.raise_for_status()

        return [Status.model_validate(s) for s in response.json()['data']]