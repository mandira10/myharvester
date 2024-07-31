import click


@click.group(short_help="myharvester CLI.")
def myharvester():
    """myharvester CLI.
    """
    pass


@myharvester.command()
@click.argument("name", default="myharvester")
def command(name):
    """Docs.
    """
    click.echo("Hello, {name}!".format(name=name))


def get_commands():
    return [myharvester]
