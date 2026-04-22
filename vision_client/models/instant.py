from enum import StrEnum
from typing import List, Literal, Optional
from uuid import UUID

from pydantic import BaseModel
from .fingerprint import OSType, SmartMode


class SameSite(StrEnum):
    UNSPECIFIED = 'unspecified'
    NORESTRICTION = 'norestriction'
    LAX = 'lax'
    STRICT = 'strict'


class InstantNavigator(BaseModel):
    user_agent: Optional[str] = None
    language: Optional[str] = None
    languages: Optional[List[str]] = None
    timezone: Optional[str] = None
    hardware_concurrency: Optional[int] = None
    device_memory: Optional[float] = None


class InstantScreen(BaseModel):
    resolution: Optional[str] = None
    pixel_ratio: Optional[float] = None


class InstantMediaDevices(BaseModel):
    audio_input: Optional[int] = None
    audio_output: Optional[int] = None
    video_input: Optional[int] = None


class InstantGeolocation(BaseModel):
    latitude: float
    longitude: float
    accuracy: int


class InstantNoise(BaseModel):
    canvas: Optional[bool] = None
    webgl: Optional[bool] = None
    client_rects: Optional[bool] = None


class InstantFingerprint(BaseModel):
    navigator: Optional[InstantNavigator] = None
    screen: Optional[InstantScreen] = None
    webgl_renderer: Optional[str] = None
    media_devices: Optional[InstantMediaDevices] = None
    geolocation: Optional[InstantGeolocation] = None
    noise: Optional[InstantNoise] = None
    canvas: Optional[Literal['off']] = None
    webgl: Optional[Literal['off']] = None
    webrtc: Optional[str] = None
    ports_protection: Optional[List[int]] = None


class InstantBehavior(BaseModel):
    urls: Optional[List[str]] = None
    args: Optional[List[str]] = None
    headless: Optional[bool] = None
    remote_debugging_port: Optional[int] = None
    timeout: Optional[int] = None


class InstantCookie(BaseModel):
    name: str
    value: str
    domain: str
    path: str
    expires: Optional[int] = None
    secure: Optional[bool] = None
    http_only: Optional[bool] = None
    same_site: Optional[SameSite | str] = None


class InstantStartBody(BaseModel):
    name: Optional[str] = None
    os: Optional[OSType | str] = None
    version: Optional[int] = None
    smart: Optional[SmartMode | str] = None
    fingerprint: Optional[InstantFingerprint] = None
    proxy: Optional[str] = None
    extensions: Optional[List[str]] = None
    cookies: Optional[List[InstantCookie]] = None
    behavior: Optional[InstantBehavior] = None


class InstantStart(BaseModel):
    success: bool
    profile_id: UUID
    port: int


class InstantStop(BaseModel):
    success: bool
    profile_id: UUID
    folder_id: UUID
    cookies: List[InstantCookie]