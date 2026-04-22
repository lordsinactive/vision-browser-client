from typing import List, Optional
from httpx import AsyncClient
from ..models import Fingerprint, OSType, SmartMode


class Fingerprints:
    session: AsyncClient
    base_url: str
    local_url: str

    async def get_fingerprint(
            self,
            os: OSType | str,
            version: int | str = 'latest',
            crc: Optional[str] = None,
            mode: Optional[SmartMode | str] = None,
    ) -> Fingerprint:
        url = f'{self.base_url}/api/v1/fingerprints/{os}/{version}'
        params: dict = {}
        if crc is not None:
            params['crc'] = crc
        if mode is not None:
            params['mode'] = str(mode)

        response = await self.session.get(url, params=params or None)
        response.raise_for_status()

        return Fingerprint.model_validate(response.json()['data']['fingerprint'])

    async def get_languages(self) -> List[str]:
        url = f'{self.local_url}/variations/language'

        response = await self.session.get(url)
        response.raise_for_status()

        return response.json()

    async def get_timezones(self) -> List[str]:
        url = f'{self.local_url}/variations/timezone'

        response = await self.session.get(url)
        response.raise_for_status()

        return response.json()

    async def get_renderers(
            self,
            os: OSType | str,
            version: int | str = 'latest',
    ) -> List[str]:
        url = f'{self.local_url}/variations/renderer'
        params = {'os': str(os), 'version': str(version)}

        response = await self.session.get(url, params=params)
        response.raise_for_status()

        return response.json()