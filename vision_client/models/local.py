from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class LocalProfile(BaseModel):
    folder_id: UUID
    profile_id: UUID
    pid: Optional[int] = None
    port: Optional[int] = None


class LocalProfilesList(BaseModel):
    profiles: List[LocalProfile]


class LocalStart(BaseModel):
    success: bool
    folder_id: UUID
    profile_id: UUID
    port: Optional[int] = None


class LocalStop(BaseModel):
    success: bool
    folder_id: UUID
    profile_id: UUID