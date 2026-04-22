from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class Cookie(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    name: str
    value: str
    domain: str
    path: str
    expires: Optional[int] = None
    http_only: Optional[bool] = Field(default=None, alias='httpOnly')
    secure: Optional[bool] = None
    same_site: Optional[str] = Field(default=None, alias='sameSite')