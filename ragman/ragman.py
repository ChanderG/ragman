import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument("page")
@click.argument("query")
def search(page, query):
    print(page, query)
