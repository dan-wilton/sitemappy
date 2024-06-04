import unittest
from unittest import mock
from unittest.mock import AsyncMock, call

from parameterized import parameterized

from sitemappy.crawler import Crawler


@mock.patch("sitemappy.crawler.AsyncScraper.get_links", new_callable=AsyncMock)
class TestCrawler(unittest.IsolatedAsyncioTestCase):
    @parameterized.expand(  # type: ignore[misc]
        [
            # Base URL, Links to Return
            ("https://monzo.com", []),
            ("https://monzo.com", ["+442038720620"]),
            ("https://monzo.com", ["mailto:careers@monzo.com"]),
            ("https://monzo.com", ["https://monzo.commalformedurl"]),
            ("https://monzo.com", ["+442038720620", "mailto:careers@monzo.com"]),
        ]
    )
    async def test_base_url_crawl_links(
        self,
        mock_scraper_get_links: AsyncMock,
        base_url: str,
        links_to_return: list[str],
    ) -> None:
        # Arrange
        expected = {
            base_url: links_to_return,
        }
        mock_scraper_get_links.return_value = links_to_return

        crawler = Crawler(base_url)

        # Act
        results = await crawler.crawl()

        # Assert
        mock_scraper_get_links.assert_called_once()
        self.assertDictEqual(expected, results)

    async def test_base_url_with_relative_links(
        self,
        mock_scraper_get_links: AsyncMock,
    ) -> None:
        # Arrange
        base_url = "https://monzo.com"
        second_crawl_url = f"{base_url}/test"

        base_url_links = [second_crawl_url, "mailto:careers@monzo.com"]
        subdomain_links = ["+442038720620"]

        expected = {
            base_url: base_url_links,
            second_crawl_url: subdomain_links,
        }

        mock_scraper_get_links.side_effect = [base_url_links, subdomain_links]
        crawler = Crawler(base_url)

        # Act
        results = await crawler.crawl()

        # Assert
        mock_scraper_get_links.assert_has_calls(
            [call(base_url), call(second_crawl_url)]
        )
        self.assertDictEqual(expected, results)

    async def test_crawl_depth_less_than_one(
        self,
        mock_scraper_get_links: AsyncMock,
    ) -> None:
        # Arrange
        base_url = "https://monzo.com"
        second_crawl_url = f"{base_url}/test"

        base_url_links = [second_crawl_url, "mailto:careers@monzo.com"]
        subdomain_links = ["+442038720620"]

        expected = {
            base_url: base_url_links,
            second_crawl_url: subdomain_links,
        }

        mock_scraper_get_links.side_effect = [base_url_links, subdomain_links]
        crawler = Crawler(base_url)

        # Act
        results = await crawler.crawl()

        # Assert
        mock_scraper_get_links.assert_has_calls(
            [call(base_url), call(second_crawl_url)]
        )
        self.assertDictEqual(expected, results)

    async def test_crawl_depth_one_only_crawls_single_page(
        self,
        mock_scraper_get_links: AsyncMock,
    ) -> None:
        # Arrange
        crawl_depth = 1
        base_url = "https://monzo.com"
        second_crawl_url = f"{base_url}/careers"

        base_url_links = [second_crawl_url, "mailto:careers@monzo.com"]
        subdomain_links = ["+442038720620"]

        expected = {
            base_url: base_url_links,
        }

        mock_scraper_get_links.side_effect = [base_url_links, subdomain_links]
        crawler = Crawler(base_url, crawl_depth=crawl_depth)

        # Act
        results = await crawler.crawl()

        # Assert
        # Only called once due to depth set to 1
        mock_scraper_get_links.assert_has_calls([call(base_url)])
        self.assertDictEqual(expected, results)
