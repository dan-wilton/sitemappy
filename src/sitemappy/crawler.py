import asyncio
import time

from .link_scraper import AsyncScraper

HTTP_TRANSPORTS = ["http://", "https://"]

POLITENESS_DELAY_DEFAULT_S = 0

UNLIMITED_DEPTH = 0
STARTING_DEPTH = 0

DEFAULT_NUMBER_OF_WORKERS = 10


class Crawler:
    def __init__(
        self,
        base_url: str,
        number_of_workers: int = DEFAULT_NUMBER_OF_WORKERS,
        crawl_depth: int = UNLIMITED_DEPTH,
        politeness_delay: int = POLITENESS_DELAY_DEFAULT_S,
    ):
        self.number_of_workers = number_of_workers
        self.crawl_depth = crawl_depth
        self.politeness_delay = politeness_delay
        self.scraper = AsyncScraper(base_url)

        self._crawl_queue: asyncio.Queue[tuple[str, int]] = asyncio.Queue()
        self._results: dict[str, list[str]] = {}
        self._crawled_urls: set[str] = set()

    async def _worker(self) -> None:
        while True:
            page_to_crawl, depth = await self._crawl_queue.get()

            if page_to_crawl in self._crawled_urls or (
                UNLIMITED_DEPTH < self.crawl_depth <= depth
            ):
                self._crawl_queue.task_done()
                continue

            self._crawled_urls.add(page_to_crawl)
            print(len(self._crawled_urls))

            if self.politeness_delay > POLITENESS_DELAY_DEFAULT_S:
                # Pause all threads for x seconds
                time.sleep(self.politeness_delay)

            links = await self.scraper.get_links(page_to_crawl)

            for link in links:
                if self.scraper.is_in_same_subdomain(link):
                    new_depth = depth + 1
                    await self._crawl_queue.put((link, new_depth))

            self._results[page_to_crawl] = links
            self._crawl_queue.task_done()

    async def crawl(self) -> dict[str, list[str]]:
        self._crawl_queue.put_nowait((self.scraper.base_url, STARTING_DEPTH))

        workers = [
            asyncio.create_task(self._worker()) for _ in range(self.number_of_workers)
        ]

        await self._crawl_queue.join()

        for worker in workers:
            worker.cancel()

        return self._results
