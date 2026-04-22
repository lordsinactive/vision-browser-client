from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class TagColors(StrEnum):
    GREEN = '#00AB55'
    BLUE = '#3366FF'
    YELLOW = '#FFC107'
    RED = '#FF4842'
    BLUE_WHITE = '#00C2FF'
    PINK = '#F263B5'


class Tag(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    team_id: Optional[UUID] = None
    folder_id: UUID
    tag_name: str
    color: str
    created_at: datetime
    updated_at: datetime