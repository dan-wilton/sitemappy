import asyncio

import httpx


class Crawler:
    def __init__(
        self,
        url: str,
        client: httpx.AsyncClient | None = None,
    ):
        self.url = url
        self.client = client if client else httpx.AsyncClient()

    async def __get_url(self, url: str) -> httpx.Response:
        return await self.client.get(url=url)

    def run(self) -> httpx.Response:
        return asyncio.run(self.__get_url(self.url))
