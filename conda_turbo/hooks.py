from conda import plugins

from .cli.main import main

@plugins.hookimpl
def conda_subcommands():
    yield plugins.CondaSubcommand(
        name="turbo",
        summary="Improved environment.yaml files.",
        action=main,
    )
