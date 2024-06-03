import typer

app = typer.Typer()


@app.command()
def main(base_url: str) -> None:
    print(base_url)
