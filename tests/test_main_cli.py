import unittest
from unittest import mock
from unittest.mock import Mock

from parameterized import parameterized
from typer.testing import CliRunner

from sitemappy.main import app

SUCCESS_EXIT_CODE = 0
ERROR_EXIT_CODE = 1
INVALID_ARGS_EXIT_CODE = 2


@mock.patch("sitemappy.main.Crawler")
class TestSitemappyCLI(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    @parameterized.expand(  # type: ignore[misc]
        [
            "https://www.monzo.com",
            "http://monzo.com",
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
        mock_crawler_instance = Mock()
        mock_crawler.return_value = mock_crawler_instance

        # Act
        cli_output = self.runner.invoke(app, valid_url)

        # Assert
        self.assertEqual(SUCCESS_EXIT_CODE, cli_output.exit_code)
        self.assertIn(valid_url, cli_output.stdout)
        mock_crawler_instance.run.assert_called_once()

    def test_url_not_provided(
        self,
        mock_crawler: Mock,
    ) -> None:
        # Arrange
        mock_crawler_instance = Mock()
        mock_crawler.return_value = mock_crawler_instance

        # Act
        cli_output = self.runner.invoke(app)

        # Assert
        self.assertEqual(INVALID_ARGS_EXIT_CODE, cli_output.exit_code)
        mock_crawler_instance.run.assert_not_called()

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
        mock_crawler_instance.run.assert_not_called()

    @parameterized.expand(["www.monzo.com", "monzo.com", "ftp://monzo.com"])  # type: ignore[misc]
    def test_url_does_not_contain_correct_scheme(
        self,
        mock_crawler: Mock,
        invalid_url: str,
    ) -> None:
        # Arrange
        mock_crawler_instance = Mock()
        mock_crawler.return_value = mock_crawler_instance

        # Act
        cli_output = self.runner.invoke(app, invalid_url)

        # Assert
        self.assertEqual(ERROR_EXIT_CODE, cli_output.exit_code)
        mock_crawler_instance.run.assert_not_called()
