import unittest
from unittest import mock
from unittest.mock import Mock

from parameterized import parameterized
from typer.testing import CliRunner

import sitemappy
from sitemappy.crawler import Crawler
from sitemappy.main import app

SUCCESS_EXIT_CODE = 0
ERROR_EXIT_CODE = 1
INVALID_ARGS_EXIT_CODE = 2


@mock.patch("sitemappy.main.Crawler")
class BaseUrlArg(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    @parameterized.expand(  # type: ignore[misc]
        [
            "https://www.monzo.com",
            "http://monzo.com",
            "http://monzo.com/",
            "https://monzo.com/careers",
            "https://www.harley-davidson.com/",
        ]
    )
    def test_valid_url_arg_is_output(
        self,
        mock_crawler: Mock,
        valid_url: str,
    ) -> None:
        # Arrange
        mock_crawler_instance = Mock(Crawler)
        mock_crawler.return_value = mock_crawler_instance
        mock_crawler_instance.crawl.return_value = {valid_url: []}

        # Act
        cli_output = self.runner.invoke(app, valid_url)

        # Assert
        self.assertEqual(SUCCESS_EXIT_CODE, cli_output.exit_code)
        self.assertIn(
            valid_url,
            # Replace newlines and empty spaces generated by line wrapping - Typer dep
            cli_output.stdout.replace("\n", "").replace(" ", ""),
        )

        mock_crawler.assert_called_once_with(
            valid_url,
            number_of_workers=sitemappy.main.DEFAULT_WORKERS,
            crawl_depth=sitemappy.main.DEFAULT_CRAWL_DEPTH,
            politeness_delay=sitemappy.main.DEFAULT_POLITENESS_DELAY_S,
        )
        mock_crawler_instance.crawl.assert_called_once()

    def test_url_not_provided(
        self,
        mock_crawler: Mock,
    ) -> None:
        # Arrange
        mock_crawler_instance = Mock(Crawler)
        mock_crawler.return_value = mock_crawler_instance

        # Act
        cli_output = self.runner.invoke(app)

        # Assert
        self.assertEqual(INVALID_ARGS_EXIT_CODE, cli_output.exit_code)
        mock_crawler_instance.crawl.assert_not_called()

    def test_too_many_args(
        self,
        mock_crawler: Mock,
    ) -> None:
        # Arrange
        mock_crawler_instance = Mock()
        mock_crawler.return_value = mock_crawler_instance

        # Act
        cli_output = self.runner.invoke(app, "https://monzo.com http://facebook.com")

        # Assert
        self.assertEqual(INVALID_ARGS_EXIT_CODE, cli_output.exit_code)
        mock_crawler_instance.crawl.assert_not_called()

    @parameterized.expand(["www.monzo.com", "monzo.com", "ftp://monzo.com"])  # type: ignore[misc]
    def test_url_does_not_contain_correct_scheme(
        self,
        mock_crawler: Mock,
        invalid_url: str,
    ) -> None:
        # Arrange
        mock_crawler_instance = Mock(Crawler)
        mock_crawler.return_value = mock_crawler_instance

        # Act
        cli_output = self.runner.invoke(app, invalid_url)

        # Assert
        self.assertEqual(INVALID_ARGS_EXIT_CODE, cli_output.exit_code)
        mock_crawler_instance.crawl.assert_not_called()


@mock.patch("sitemappy.main.Crawler")
class WorkersOptionalArg(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_valid_custom_number_of_workers(
        self,
        mock_crawler: Mock,
    ) -> None:
        # Arrange
        valid_url: str = "https://monzo.com"
        expected_number_of_workers = 99

        mock_crawler_instance = Mock(Crawler)
        mock_crawler.return_value = mock_crawler_instance
        mock_crawler_instance.crawl.return_value = {valid_url: []}

        # Act
        cli_output = self.runner.invoke(
            app, f"{valid_url} --workers {expected_number_of_workers}"
        )

        # Assert
        self.assertEqual(SUCCESS_EXIT_CODE, cli_output.exit_code)

        mock_crawler.assert_called_once_with(
            valid_url,
            number_of_workers=expected_number_of_workers,
            crawl_depth=sitemappy.main.DEFAULT_CRAWL_DEPTH,
            politeness_delay=sitemappy.main.DEFAULT_POLITENESS_DELAY_S,
        )
        mock_crawler_instance.crawl.assert_called_once()

    def test_invalid_workers_arg_type(
        self,
        mock_crawler: Mock,
    ) -> None:
        # Arrange
        valid_url: str = "https://monzo.com"
        expected_number_of_workers = "ten"

        mock_crawler_instance = Mock(Crawler)
        mock_crawler.return_value = mock_crawler_instance
        mock_crawler_instance.crawl.return_value = {valid_url: []}

        # Act
        cli_output = self.runner.invoke(
            app, f"{valid_url} --workers {expected_number_of_workers}"
        )

        # Assert
        self.assertEqual(INVALID_ARGS_EXIT_CODE, cli_output.exit_code)

        mock_crawler.assert_not_called()
        mock_crawler_instance.crawl.assert_not_called()

    def test_invalid_workers_arg_less_than_one(
        self,
        mock_crawler: Mock,
    ) -> None:
        # Arrange
        valid_url: str = "https://monzo.com"
        expected_number_of_workers = 0

        mock_crawler_instance = Mock(Crawler)
        mock_crawler.return_value = mock_crawler_instance
        mock_crawler_instance.crawl.return_value = {valid_url: []}

        # Act
        cli_output = self.runner.invoke(
            app, f"{valid_url} --workers {expected_number_of_workers}"
        )

        # Assert
        self.assertEqual(INVALID_ARGS_EXIT_CODE, cli_output.exit_code)

        mock_crawler.assert_not_called()
        mock_crawler_instance.crawl.assert_not_called()


@mock.patch("sitemappy.main.Crawler")
class CrawlDepthOptionalArg(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_valid_custom_crawl_depth(
        self,
        mock_crawler: Mock,
    ) -> None:
        # Arrange
        valid_url: str = "https://monzo.com"
        expected_crawl_depth = 99

        mock_crawler_instance = Mock(Crawler)
        mock_crawler.return_value = mock_crawler_instance
        mock_crawler_instance.crawl.return_value = {valid_url: []}

        # Act
        cli_output = self.runner.invoke(
            app, f"{valid_url} --crawl-depth {expected_crawl_depth}"
        )

        # Assert
        self.assertEqual(SUCCESS_EXIT_CODE, cli_output.exit_code)

        mock_crawler.assert_called_once_with(
            valid_url,
            number_of_workers=sitemappy.main.DEFAULT_WORKERS,
            crawl_depth=expected_crawl_depth,
            politeness_delay=sitemappy.main.DEFAULT_POLITENESS_DELAY_S,
        )
        mock_crawler_instance.crawl.assert_called_once()

    def test_invalid_crawl_depth_arg_type(
        self,
        mock_crawler: Mock,
    ) -> None:
        # Arrange
        valid_url: str = "https://monzo.com"
        invalid_crawl_depth = "ten"

        mock_crawler_instance = Mock(Crawler)
        mock_crawler.return_value = mock_crawler_instance
        mock_crawler_instance.crawl.return_value = {valid_url: []}

        # Act
        cli_output = self.runner.invoke(
            app, f"{valid_url} --crawl-depth {invalid_crawl_depth}"
        )

        # Assert
        self.assertEqual(INVALID_ARGS_EXIT_CODE, cli_output.exit_code)

        mock_crawler.assert_not_called()
        mock_crawler_instance.crawl.assert_not_called()

    def test_invalid_crawl_depth_arg_less_than_zero(
        self,
        mock_crawler: Mock,
    ) -> None:
        # Arrange
        valid_url: str = "https://monzo.com"
        invalid_crawl_depth = -1

        mock_crawler_instance = Mock(Crawler)
        mock_crawler.return_value = mock_crawler_instance
        mock_crawler_instance.crawl.return_value = {valid_url: []}

        # Act
        cli_output = self.runner.invoke(
            app, f"{valid_url} --crawl-depth {invalid_crawl_depth}"
        )

        # Assert
        self.assertEqual(INVALID_ARGS_EXIT_CODE, cli_output.exit_code)

        mock_crawler.assert_not_called()
        mock_crawler_instance.crawl.assert_not_called()


@mock.patch("sitemappy.main.Crawler")
class PolitenessDelayOptionalArg(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_valid_custom_politeness_delay(
        self,
        mock_crawler: Mock,
    ) -> None:
        # Arrange
        valid_url: str = "https://monzo.com"
        expected_politeness_delay = 99

        mock_crawler_instance = Mock(Crawler)
        mock_crawler.return_value = mock_crawler_instance
        mock_crawler_instance.crawl.return_value = {valid_url: []}

        # Act
        cli_output = self.runner.invoke(
            app, f"{valid_url} --politeness-delay {expected_politeness_delay}"
        )

        # Assert
        self.assertEqual(SUCCESS_EXIT_CODE, cli_output.exit_code)

        mock_crawler.assert_called_once_with(
            valid_url,
            number_of_workers=sitemappy.main.DEFAULT_WORKERS,
            crawl_depth=sitemappy.main.DEFAULT_POLITENESS_DELAY_S,
            politeness_delay=expected_politeness_delay,
        )
        mock_crawler_instance.crawl.assert_called_once()

    def test_invalid_politeness_delay_arg_type(
        self,
        mock_crawler: Mock,
    ) -> None:
        # Arrange
        valid_url: str = "https://monzo.com"
        invalid_politeness_delay = "ten"

        mock_crawler_instance = Mock(Crawler)
        mock_crawler.return_value = mock_crawler_instance
        mock_crawler_instance.crawl.return_value = {valid_url: []}

        # Act
        cli_output = self.runner.invoke(
            app, f"{valid_url} --politeness-delay {invalid_politeness_delay}"
        )

        # Assert
        self.assertEqual(INVALID_ARGS_EXIT_CODE, cli_output.exit_code)

        mock_crawler.assert_not_called()
        mock_crawler_instance.crawl.assert_not_called()

    def test_invalid_crawl_depth_arg_less_than_zero(
        self,
        mock_crawler: Mock,
    ) -> None:
        # Arrange
        valid_url: str = "https://monzo.com"
        invalid_politeness_delay = -1

        mock_crawler_instance = Mock(Crawler)
        mock_crawler.return_value = mock_crawler_instance
        mock_crawler_instance.crawl.return_value = {valid_url: []}

        # Act
        cli_output = self.runner.invoke(
            app, f"{valid_url} --politeness-delay {invalid_politeness_delay}"
        )

        # Assert
        self.assertEqual(INVALID_ARGS_EXIT_CODE, cli_output.exit_code)

        mock_crawler.assert_not_called()
        mock_crawler_instance.crawl.assert_not_called()
