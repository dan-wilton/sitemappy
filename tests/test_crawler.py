import unittest
from http import HTTPStatus

import httpx
from parameterized import parameterized

from sitemappy.crawler import Crawler


class TestCrawler(unittest.TestCase):
    def __generate_html_page_of_links(self, links: list[str]) -> str:
        html_links = [f"<a href={link}>{index}</a>" for index, link in enumerate(links)]
        return f"<html>{html_links}</html>"

    def test_successful_get_url(self) -> None:
        # Arrange
        expected_response = [
            "https://monzo.com/careers",
            "https://monzo.com/about",
        ]
        client = httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(
                    HTTPStatus.OK,
                    content=self.__generate_html_page_of_links(expected_response),
                )
            )
        )

        class_under_test = Crawler("https://monzo.com", client=client)

        # Act
        response = class_under_test.run()

        # Assert
        self.assertEqual(expected_response, response)

    @parameterized.expand(
        [
            (
                "https://monzo.com",
                [
                    "https://monzo.com#careers",
                    "https://monzo.com/business-banking",
                ],
                ["#careers", "/business-banking"],
            ),
            (
                "https://www.monzo.com/",
                [
                    "https://www.monzo.com/#careers",
                    "https://www.monzo.com/business-banking",
                ],
                ["#careers", "/business-banking"],
            ),
        ]
    )  # type: ignore[misc]
    def test_successful_get_relative_url(
        self, base_url: str, expected_urls: list[str], relative_urls: list[str]
    ) -> None:
        # Arrange
        client = httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(
                    HTTPStatus.OK,
                    content=self.__generate_html_page_of_links(relative_urls),
                )
            )
        )

        class_under_test = Crawler(base_url, client=client)

        # Act
        response = class_under_test.run()

        # Assert
        self.assertEqual(expected_urls, response)

    def test_unsuccessful_get_url(self) -> None:
        # Arrange
        expected_number_of_links = 0
        client = httpx.AsyncClient(
            transport=httpx.MockTransport(
                lambda _: httpx.Response(HTTPStatus.INTERNAL_SERVER_ERROR)
            )
        )

        class_under_test = Crawler("https://monzo.com", client=client)

        # Act
        response = class_under_test.run()

        # Assert
        self.assertEqual(expected_number_of_links, len(response))
