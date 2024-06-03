from typing import Annotated

import typer
import validators
from validators import ValidationError

from sitemappy.crawler import Crawler

app = typer.Typer()


def parse_url(url_string: str) -> str:
    url_validation = validators.url(url_string, consider_tld=True)

    if isinstance(url_validation, ValidationError) or not any(
        [url_string.startswith("http://"), url_string.startswith("https://")]
    ):
        raise Exception(f"Invalid URL provided: {url_string}")

    return url_string


@app.command()
def main(base_url: Annotated[str, typer.Argument(parser=parse_url)]) -> None:
    response = Crawler(url=base_url).run()
    print(response)
    print(str(base_url))
