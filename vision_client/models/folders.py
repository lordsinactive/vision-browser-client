from datetime import datetime
from enum import StrEnum
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel


class FolderIcons(StrEnum):
    Cloud = 'Cloud'
    Google = 'Google'
    Facebook = 'Facebook'
    TikTok = 'TikTok'
    Amazon = 'Amazon'
    Bitcoin = 'Bitcoin'
    Meta = 'Meta'
    PayPal = 'PayPal'
    Discord = 'Discord'
    Twitter = 'Twitter'
    Vkontakte = 'Vkontakte'
    Youtube = 'Youtube'
    Tinder = 'Tinder'
    Onlyfans = 'Onlyfans'
    Threads = 'Threads'


class FolderColors(StrEnum):
    YELLOW = '#FFC1073D'
    LIGHT_BLUE = '#C8E4FFCD'
    BLUE = '#3366FF3D'
    GREEN = '#54D62C3D'
    RED = '#FF48423D'
    GRAY = '#919EAB3D'


class Folder(BaseModel):
    id: UUID
    owner: UUID
    folder_name: str
    folder_icon: FolderIcons
    folder_color: FolderColors
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class FolderUsage(BaseModel):
    users: int
    profiles: int


class FolderDelete(BaseModel):
    data: List[UUID]
    usage: FolderUsage
