from typing import Any, List
from uuid import UUID

from httpx import AsyncClient

from ..models import Cookie


class Cookies:
    session: AsyncClient
    base_url: str

    async def get_cookies(
            self,
            folder_id: UUID | str,
            profile_id: UUID | str,
    ) -> List[Cookie]:
        url = f'{self.base_url}/api/v1/cookies/{folder_id}/{profile_id}'

        response = await self.session.get(url)
        response.raise_for_status()

        return [Cookie.model_validate(c) for c in response.json()['data']]

    async def import_cookies(
            self,
            folder_id: UUID | str,
            profile_id: UUID | str,
            cookies: List[Cookie | dict],
    ) -> Any:
        url = f'{self.base_url}/api/v1/cookies/import/{folder_id}/{profile_id}'
        items = [
            c.model_dump(by_alias=True, exclude_none=True) if isinstance(c, Cookie) else c
            for c in cookies
        ]

        response = await self.session.post(url, json={'cookies': items})
        response.raise_for_status()

        return response.json().get('data')