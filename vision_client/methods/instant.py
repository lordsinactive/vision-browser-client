from typing import Optional
from uuid import UUID

from httpx import AsyncClient

from ..models import InstantStartBody, InstantStart, InstantStop


class Instant:
    session: AsyncClient
    local_url: str

    async def start_instant_profile(
            self,
            config: Optional[InstantStartBody | dict] = None,
    ) -> InstantStart:
        url = f'{self.local_url}/start/instant'

        if config is None:
            response = await self.session.get(url)
        elif isinstance(config, InstantStartBody):
            response = await self.session.post(
                url,
                json=config.model_dump(exclude_none=True),
            )
        else:
            response = await self.session.post(url, json=config)
        response.raise_for_status()

        return InstantStart.model_validate(response.json())

    async def stop_instant_profile(
            self,
            profile_id: UUID | str,
    ) -> InstantStop:
        url = f'{self.local_url}/stop/instant/{profile_id}'

        response = await self.session.get(url)
        response.raise_for_status()

        return InstantStop.model_validate(response.json())