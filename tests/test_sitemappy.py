import unittest

from typer.testing import CliRunner

from sitemappy.main import app

SUCCESS_EXIT_CODE = 0
INVALID_ARGS_EXIT_CODE = 2


class SitemappyCLI(unittest.TestCase):
    def setUp(self) -> None:
        self.runner = CliRunner()

    def test_url_arg_is_output(self) -> None:
        # Arrange
        expected = "TEST_URL"

        # Act
        cli_output = self.runner.invoke(app, "TEST_URL")

        # Assert
        self.assertEqual(SUCCESS_EXIT_CODE, cli_output.exit_code)
        self.assertIn(expected, cli_output.stdout)

    def test_url_not_provided(self) -> None:
        # Act
        cli_output = self.runner.invoke(app)

        # Assert
        self.assertEqual(INVALID_ARGS_EXIT_CODE, cli_output.exit_code)

    def test_too_many_args(self) -> None:
        # Act
        cli_output = self.runner.invoke(app, "TEST_URL_ONE TEST_URL_TWO")

        # Assert
        self.assertEqual(INVALID_ARGS_EXIT_CODE, cli_output.exit_code)
