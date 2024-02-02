from argparse import ArgumentParser

from conda import plugins

from conda.base.context import context, determine_target_prefix, env_name
from .env import from_environment

from typing import List

from .cli import parse_arguments
from .cmds import env_export


def turbo_command(arguments: List[str]):
    args = parse_arguments(arguments)
    if args.cmd == "export":
        return env_export(args)


@plugins.hookimpl
def conda_subcommands():
    yield plugins.CondaSubcommand(
        name="turbo",
        summary="Improved environment.yaml files.",
        action=turbo_command,
    )
