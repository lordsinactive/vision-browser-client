from typing import List, Literal, Optional
from uuid import UUID

from httpx import AsyncClient

from ..models import (
    Fingerprint,
    Profile,
    ProfilesList,
    ProfileCreate,
    ProfileDelete,
)


class Profiles:
    session: AsyncClient
    base_url: str

    async def get_profiles(self, folder_id: UUID | str) -> ProfilesList:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/profiles'

        response = await self.session.get(url)
        response.raise_for_status()

        return ProfilesList.model_validate(response.json()['data'])

    async def get_profile(
            self,
            folder_id: UUID | str,
            profile_id: UUID | str,
    ) -> Profile:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/profiles/{profile_id}'

        response = await self.session.get(url)
        response.raise_for_status()

        return Profile.model_validate(response.json()['data'])

    async def create_profile(
            self,
            folder_id: UUID | str,
            profile_name: str,
            fingerprint: Fingerprint | dict,
            browser: str = 'Chrome',
            platform: str = 'Windows',
            profile_notes: str = '',
            profile_tags: Optional[List[UUID | str]] = None,
            new_profile_tags: Optional[List[str]] = None,
            profile_status: Optional[UUID | str] = None,
            proxy_id: Optional[UUID | str] = None,
    ) -> ProfileCreate:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/profiles'
        body = {
            'profile_name': profile_name,
            'profile_notes': profile_notes,
            'profile_tags': [str(t) for t in (profile_tags or [])],
            'new_profile_tags': new_profile_tags or [],
            'proxy_id': str(proxy_id) if proxy_id is not None else None,
            'profile_status': str(profile_status) if profile_status is not None else None,
            'browser': browser,
            'platform': platform,
            'fingerprint': (
                fingerprint.model_dump(exclude_none=True)
                if isinstance(fingerprint, Fingerprint)
                else fingerprint
            ),
        }

        response = await self.session.post(url, json=body)
        response.raise_for_status()

        return ProfileCreate.model_validate(response.json())

    async def edit_profile(
            self,
            folder_id: UUID | str,
            profile_id: UUID | str,
            profile_name: Optional[str] = None,
            profile_notes: Optional[str] = None,
            profile_tags: Optional[List[UUID | str]] = None,
            new_profile_tags: Optional[List[str]] = None,
            profile_status: Optional[UUID | str] = None,
            pinned: Optional[bool] = None,
            proxy_id: Optional[UUID | str | Literal['none']] = None,
    ) -> Profile:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/profiles/{profile_id}'
        body: dict = {}
        if profile_name is not None:
            body['profile_name'] = profile_name
        if profile_notes is not None:
            body['profile_notes'] = profile_notes
        if profile_tags is not None:
            body['profile_tags'] = [str(t) for t in profile_tags]
        if new_profile_tags is not None:
            body['new_profile_tags'] = new_profile_tags
        if profile_status is not None:
            body['profile_status'] = str(profile_status)
        if pinned is not None:
            body['pinned'] = pinned
        if proxy_id is not None:
            body['proxy_id'] = 'none' if proxy_id == 'none' else {'id': str(proxy_id)}

        response = await self.session.patch(url, json=body)
        response.raise_for_status()

        return Profile.model_validate(response.json()['data'])

    async def delete_profile(
            self,
            folder_id: UUID | str,
            profile_id: UUID | str,
    ) -> ProfileDelete:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/profiles/{profile_id}'

        response = await self.session.delete(url)
        response.raise_for_status()

        return ProfileDelete.model_validate(response.json())