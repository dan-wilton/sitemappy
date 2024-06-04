from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

HTTP_TRANSPORTS = ["http://", "https://"]


class AsyncScraper:
    def __init__(
        self,
        base_url: str,
        client: httpx.AsyncClient | None = None,
    ):
        self.base_url = base_url
        self.parsed_base_url = urlparse(base_url)
        self.client = client if client else httpx.AsyncClient()

    async def get_links(self, url: str) -> list[str]:
        links = []

        page = await self.client.get(url=url)
        soup = BeautifulSoup(page.text, "html.parser")

        for html_link_element in soup.find_all("a"):
            link: str = html_link_element.get("href")

            if link:
                if not any(link.startswith(prefix) for prefix in HTTP_TRANSPORTS):
                    link = urljoin(self.base_url, link)

                links.append(link)

        return links

    def is_in_same_subdomain(self, link: str) -> bool:
        return any(
            link.startswith(f"{prefix}{self.parsed_base_url.hostname}/")
            for prefix in HTTP_TRANSPORTS
        )
