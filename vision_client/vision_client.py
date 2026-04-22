from typing import Optional
from httpx import AsyncClient

from .methods import (
    Folders, Profiles, Proxies,
    Statuses, Tags, Local,
    Fingerprints, Instant, Cookies,
)

class VisionClient(
    Folders,
    Profiles,
    Proxies,
    Statuses,
    Tags,
    Local,
    Fingerprints,
    Instant,
    Cookies,
):
    def __init__(
            self,
            x_token: Optional[str] = None,
            x_team_token: Optional[str] = None,
            local_url: str = 'http://127.0.0.1:3030',
            base_url: str = 'https://api.browser.vision',
    ) -> None:
        if not (x_token or x_team_token):
            raise ValueError("x_token or x_team_token must be provided")

        if x_token and x_team_token:
            raise ValueError("only one of x_token or x_team_token must be provided")

        headers_session = {
            'Content-Type': 'application/json',
        }

        if x_token:
            headers_session['X-Token'] = x_token
        elif x_team_token:
            headers_session['X-Team-Token'] = x_team_token

        self.session = AsyncClient(
            timeout=120,
            follow_redirects=True,
            headers=headers_session,
        )
        self.base_url = base_url
        self.local_url = local_url

    async def __aenter__(self) -> 'VisionClient':
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.close()

    async def close(self) -> None:
        await self.session.aclose()