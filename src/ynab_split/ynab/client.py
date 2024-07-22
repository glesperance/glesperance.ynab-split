import httpx
from .config import client_settings


class APIClient:
    def __init__(
        self,
        api_token: str,
        base_url: str = client_settings.base_url,
    ):
        self.base_url = base_url
        self.headers = {"Authorization": f"Bearer {api_token}"}

    async def get(self, endpoint: str, params: dict = None):
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.headers
        ) as client:
            response = await client.get(endpoint, params=params)
            response.raise_for_status()
            return response.json()

    async def post(self, endpoint: str, data: dict):
        async with httpx.AsyncClient(
            base_url=self.base_url, headers=self.headers
        ) as client:
            response = await client.post(endpoint, json=data)
            response.raise_for_status()
            return response.json()
