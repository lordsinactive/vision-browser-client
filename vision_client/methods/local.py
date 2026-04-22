from typing import List, Optional
from uuid import UUID

from httpx import AsyncClient

from ..models import LocalProfilesList, LocalStart, LocalStop, ProxyConfig


class Local:
    session: AsyncClient
    local_url: str

    async def get_active_profiles(self) -> LocalProfilesList:
        url = f'{self.local_url}/list'

        response = await self.session.get(url)
        response.raise_for_status()

        return LocalProfilesList.model_validate(response.json())

    async def start_profile(
            self,
            folder_id: UUID | str,
            profile_id: UUID | str,
            args: Optional[List[str]] = None,
            proxy: Optional[ProxyConfig | dict] = None,
    ) -> LocalStart:
        url = f'{self.local_url}/start/{folder_id}/{profile_id}'
        body: dict = {'args': args or []}
        if proxy is not None:
            body['proxy'] = (
                proxy.model_dump()
                if isinstance(proxy, ProxyConfig)
                else proxy
            )

        response = await self.session.post(url, json=body)
        response.raise_for_status()

        return LocalStart.model_validate(response.json())

    async def stop_profile(
            self,
            folder_id: UUID | str,
            profile_id: UUID | str,
    ) -> LocalStop:
        url = f'{self.local_url}/stop/{folder_id}/{profile_id}'

        response = await self.session.get(url)
        response.raise_for_status()

        return LocalStop.model_validate(response.json())