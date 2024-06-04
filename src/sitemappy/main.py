import asyncio
import json
import os
from typing import Annotated

import typer
import validators
from rich import print
from rich.table import Table
from validators import ValidationError

from sitemappy.crawler import Crawler

app = typer.Typer(rich_markup_mode="rich")


def validate_base_url(url_string: str) -> str:
    url_validation = validators.url(url_string, consider_tld=True)

    if isinstance(url_validation, ValidationError) or not any(
        [url_string.startswith("http://"), url_string.startswith("https://")]
    ):
        raise Exception(f"Invalid URL provided: {url_string}")

    return url_string


@app.command(
    help="[magenta][bold]Sitemappy[/bold] (or sitemap-py 😉)[/magenta] is a CLI tool "
    "to crawl a website and create a JSON [red]sitemap[/red]."
    "\n\nFor more information about the tool go to https://github.com/dan-wilton/sitemappy/"
)
def main(
    base_url: Annotated[
        str,
        typer.Argument(
            help="a valid website URL to sitemap",
        ),
    ],
) -> None:
    # Validate the URL input is a valid HTTP URL with TLD
    validate_base_url(base_url)

    # The main bit ✨
    crawler = Crawler(base_url)
    results = asyncio.run(crawler.crawl())

    # Write the results and feedback to user
    with open("result.json", "w") as results_file:
        json.dump(results, results_file)

    total_number_of_links = 0

    for links in results.values():
        total_number_of_links += len(links)

    table = Table(
        title=f"{base_url} 🔎",
    )
    table.add_column(
        "Pages Crawled",
        style="magenta",
    )
    table.add_column("Links Found", style="cyan", justify="right")

    table.add_row(f"{len(results.keys())}", f"{total_number_of_links}")

    print(
        "\n\n",
        table,
        f"\n\n[green]Sitemap successfully written to file![/green]"
        f"\nfile:///{os.path.realpath(results_file.name)}",
    )
