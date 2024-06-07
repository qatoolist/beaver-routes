from typing import Any

import httpx


class RequestHandler:
    @staticmethod
    def sync_request(method: str, url: str, **kwargs: Any) -> httpx.Response:
        with httpx.Client() as client:
            return client.request(method=method, url=url, **kwargs)

    @staticmethod
    async def async_request(method: str, url: str, **kwargs: Any) -> httpx.Response:
        async with httpx.AsyncClient() as client:
            return await client.request(method=method, url=url, **kwargs)

