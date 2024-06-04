import asyncio

from .link_scraper import AsyncScraper

HTTP_TRANSPORTS = ["http://", "https://"]


class Crawler:
    def __init__(self, base_url: str, number_of_workers: int = 100):
        self.number_of_workers = number_of_workers
        self.scraper = AsyncScraper(base_url)

        self._crawl_queue: asyncio.Queue[str] = asyncio.Queue()
        self._results: dict[str, list[str]] = {}
        self._crawled_urls: set[str] = set()

    async def _worker(self) -> None:
        while True:
            page_to_crawl: str = await self._crawl_queue.get()

            if page_to_crawl in self._crawled_urls:
                self._crawl_queue.task_done()
                continue

            self._crawled_urls.add(page_to_crawl)
            print(len(self._crawled_urls))

            links = await self.scraper.get_links(page_to_crawl)

            for link in links:
                if self.scraper.is_in_same_subdomain(link):
                    await self._crawl_queue.put(link)

            self._results[page_to_crawl] = links
            self._crawl_queue.task_done()

    async def crawl(self) -> dict[str, list[str]]:
        self._crawl_queue.put_nowait(self.scraper.base_url)

        workers = [
            asyncio.create_task(self._worker()) for _ in range(self.number_of_workers)
        ]

        await self._crawl_queue.join()

        for worker in workers:
            worker.cancel()

        return self._results
