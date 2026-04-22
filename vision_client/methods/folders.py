from typing import List, Optional
from uuid import UUID

from httpx import AsyncClient

from ..models import (
    Folder,
    FolderDelete,
    FolderIcons,
    FolderColors,
)


class Folders:
    session: AsyncClient
    base_url: str

    async def get_folders(self) -> List[Folder]:
        url = f'{self.base_url}/api/v1/folders'

        response = await self.session.get(url)
        response.raise_for_status()

        return [Folder.model_validate(f) for f in response.json()['data']]

    async def create_folder(
            self,
            folder_name: str,
            folder_icon: FolderIcons | str,
            folder_color: FolderColors | str,
    ) -> Folder:
        url = f'{self.base_url}/api/v1/folders'
        body = {
            'folder_name': folder_name,
            'folder_icon': folder_icon,
            'folder_color': folder_color,
        }

        response = await self.session.post(url, json=body)
        response.raise_for_status()

        return Folder.model_validate(response.json()['data'])

    async def delete_folder(self, folder_id: UUID | str) -> FolderDelete:
        url = f'{self.base_url}/api/v1/folders/{folder_id}'

        response = await self.session.delete(url)
        response.raise_for_status()

        return FolderDelete.model_validate(response.json())

    async def edit_folder(
            self,
            folder_id: UUID | str,
            folder_name: Optional[str] = None,
            folder_icon: Optional[FolderIcons | str] = None,
            folder_color: Optional[FolderColors | str] = None,
    ) -> Folder:
        url = f'{self.base_url}/api/v1/folders/{folder_id}'
        body = {}
        if folder_name is not None:
            body['folder_name'] = folder_name
        if folder_icon is not None:
            body['folder_icon'] = folder_icon
        if folder_color is not None:
            body['folder_color'] = folder_color

        response = await self.session.patch(url, json=body)
        response.raise_for_status()

        return Folder.model_validate(response.json()['data'])