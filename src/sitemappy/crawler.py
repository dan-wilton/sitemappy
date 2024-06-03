import asyncio
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

HTTP_TRANSPORTS = ["http://", "https://"]


class Crawler:
    def __init__(
        self,
        url: str,
        client: httpx.AsyncClient | None = None,
    ):
        self.base_url = url
        self.parsed_base_url = urlparse(url)
        self.client = client if client else httpx.AsyncClient()

    async def __get_links(self, url: str) -> list[str]:
        links = []
        page = await self.client.get(url=url)
        soup = BeautifulSoup(page.text, "html.parser")

        for html_link_element in soup.find_all("a"):
            link: str = html_link_element.get("href")

            if not any(link.startswith(prefix) for prefix in HTTP_TRANSPORTS):
                link = urljoin(self.base_url, link)

            # if any(
            #     link.startswith(f"{prefix}{self.parsed_base_url.hostname}")
            #     for prefix in HTTP_TRANSPORTS
            # ):
            links.append(link)

        return links

    def run(self) -> list[str]:
        return asyncio.run(self.__get_links(self.base_url))
