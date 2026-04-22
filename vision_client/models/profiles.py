from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from .fingerprint import Fingerprint
from .folders import FolderUsage
from .proxy import Proxy as ProxyModel


class Profile(BaseModel):
    id: UUID
    owner: UUID
    folder_id: UUID
    proxy_id: Optional[UUID] = None
    profile_name: str
    profile_notes: str
    profile_status: Optional[UUID] = None
    profile_tags: List[UUID]
    browser: str
    platform: str
    fingerprint: Fingerprint
    running: bool
    pinned: bool
    worktime: int
    last_run_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    recovered: Optional[int] = None
    is_received: Optional[bool] = None
    app_version: Optional[str] = None
    proxy: Optional[ProxyModel] = None


class ProfileListItem(BaseModel):
    id: UUID
    owner: UUID
    folder_id: UUID
    proxy_id: Optional[UUID] = None
    profile_name: str
    profile_notes: str
    profile_status: Optional[UUID] = None
    profile_tags: List[UUID]
    browser: str
    platform: str
    major: int
    running: bool
    pinned: bool
    worktime: int
    last_run_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    recovered: Optional[int] = None
    is_received: Optional[bool] = None
    app_version: Optional[str] = None
    proxy: Optional[ProxyModel] = None


class ProfilesList(BaseModel):
    total: int
    items: List[ProfileListItem]


class ProfileCreate(BaseModel):
    data: Profile
    usage: Optional[FolderUsage] = None


class ProfileDelete(BaseModel):
    data: UUID
    usage: Optional[FolderUsage] = None