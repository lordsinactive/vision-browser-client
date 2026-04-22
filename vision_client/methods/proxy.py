from typing import List, Optional
from uuid import UUID

from httpx import AsyncClient

from ..models import (
    ProxyType,
    Geolocation,
    Proxy,
    ProxyCreateItem,
)


class Proxies:
    session: AsyncClient
    base_url: str

    async def get_proxies(self, folder_id: UUID | str) -> List[Proxy]:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/proxies'

        response = await self.session.get(url)
        response.raise_for_status()

        return [Proxy.model_validate(p) for p in response.json()['data']]

    async def create_proxies(
            self,
            folder_id: UUID | str,
            proxies: List[ProxyCreateItem | dict],
    ) -> List[Proxy]:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/proxies'
        items = [
            p.model_dump(exclude_none=True) if isinstance(p, ProxyCreateItem) else p
            for p in proxies
        ]

        response = await self.session.post(url, json={'proxies': items})
        response.raise_for_status()

        return [Proxy.model_validate(p) for p in response.json()['data']]

    async def edit_proxy(
            self,
            folder_id: UUID | str,
            proxy_id: UUID | str,
            proxy_name: str,
            proxy_type: ProxyType | str,
            proxy_ip: str,
            proxy_port: int,
            proxy_username: Optional[str] = None,
            proxy_password: Optional[str] = None,
            update_url: Optional[str] = None,
            proxy_geo: Optional[Geolocation | dict] = None,
    ) -> Proxy:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/proxies/{proxy_id}'
        body: dict = {
            'proxy_name': proxy_name,
            'proxy_type': str(proxy_type),
            'proxy_ip': proxy_ip,
            'proxy_port': proxy_port,
        }
        if proxy_username is not None:
            body['proxy_username'] = proxy_username
        if proxy_password is not None:
            body['proxy_password'] = proxy_password
        if update_url is not None:
            body['update_url'] = update_url
        if proxy_geo is not None:
            body['proxy_geo'] = (
                proxy_geo.model_dump(exclude_none=True)
                if isinstance(proxy_geo, Geolocation)
                else proxy_geo
            )

        response = await self.session.put(url, json=body)
        response.raise_for_status()

        return Proxy.model_validate(response.json()['data'])

    async def delete_proxies(
            self,
            folder_id: UUID | str,
            proxy_ids: List[UUID | str],
    ) -> List[Proxy]:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/proxies'
        body = {'proxy_ids': [str(pid) for pid in proxy_ids]}

        response = await self.session.request('DELETE', url, json=body)
        response.raise_for_status()

        return [Proxy.model_validate(p) for p in response.json()['data']]