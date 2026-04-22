from datetime import datetime
from enum import StrEnum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class ProxyTypes(StrEnum):
    SOCKS5 = 'socks5'
    HTTP = 'http'


class ProxyConfig(BaseModel):
    type: ProxyTypes | str
    address: str
    port: int
    username: Optional[str] = None
    password: Optional[str] = None


class ProxyType(StrEnum):
    HTTP = 'HTTP'
    HTTPS = 'HTTPS'
    SOCKS5 = 'SOCKS5'
    SSH = 'SSH'


class Geolocation(BaseModel):
    ip: Optional[str] = None
    country: Optional[str] = None
    region: Optional[str] = None
    city: Optional[str] = None
    zipcode: Optional[str] = None
    timezone: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class Proxy(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    team_id: Optional[UUID] = None
    folder_id: UUID
    proxy_name: str
    proxy_type: ProxyType | str
    proxy_ip: str
    proxy_port: int
    proxy_username: Optional[str] = None
    proxy_password: Optional[str] = None
    update_url: Optional[str] = None
    geo_info: Optional[Geolocation] = None
    last_check_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    profiles: Optional[int] = None


class ProxyCreateItem(BaseModel):
    proxy_name: str
    proxy_type: ProxyType | str
    proxy_ip: str
    proxy_port: int
    proxy_username: Optional[str] = None
    proxy_password: Optional[str] = None
    update_url: Optional[str] = None
    proxy_geo: Optional[Geolocation] = None