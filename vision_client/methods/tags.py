from typing import List, Optional, Tuple
from uuid import UUID

from httpx import AsyncClient

from ..models import Tag, TagColors


class Tags:
    session: AsyncClient
    base_url: str

    async def get_tags(self, folder_id: UUID | str) -> List[Tag]:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/tags'

        response = await self.session.get(url)
        response.raise_for_status()

        return [Tag.model_validate(t) for t in response.json()['data']]

    async def create_tags(
            self,
            folder_id: UUID | str,
            tags: List[str | Tuple[str, TagColors | str]],
    ) -> List[Tag]:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/tags'
        names: List[str] = []
        with_color: List[List[str]] = []
        for item in tags:
            if isinstance(item, str):
                names.append(item)
            else:
                name, color = item
                with_color.append([name, str(color)])

        bodies: List[dict] = []
        if names and with_color:
            bodies.append({'tags': names, 'tags_with_color': []})
            bodies.append({'tags': [], 'tags_with_color': with_color})
        else:
            bodies.append({'tags': names, 'tags_with_color': with_color})

        created: List[Tag] = []
        for body in bodies:
            response = await self.session.post(url, json=body)
            response.raise_for_status()
            created.extend(Tag.model_validate(t) for t in response.json()['data'])

        return created

    async def edit_tag(
            self,
            folder_id: UUID | str,
            tag_id: UUID | str,
            name: Optional[str] = None,
            color: Optional[TagColors | str] = None,
    ) -> Tag:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/tags/{tag_id}'
        body: dict = {}
        if name is not None:
            body['name'] = name
        if color is not None:
            body['color'] = str(color)

        response = await self.session.put(url, json=body)
        response.raise_for_status()

        return Tag.model_validate(response.json()['data'])

    async def delete_tags(
            self,
            folder_id: UUID | str,
            tag_ids: List[UUID | str],
    ) -> List[Tag]:
        url = f'{self.base_url}/api/v1/folders/{folder_id}/tags'
        body = {'tag_ids': [str(tid) for tid in tag_ids]}

        response = await self.session.request('DELETE', url, json=body)
        response.raise_for_status()

        return [Tag.model_validate(t) for t in response.json()['data']]