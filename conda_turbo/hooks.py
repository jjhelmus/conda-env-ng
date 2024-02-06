from argparse import ArgumentParser
from importlib import import_module

from conda import plugins

from conda.base.context import context, determine_target_prefix, env_name
from .env import from_environment

from typing import List

from .cli import parse_arguments
from .cmd_export import env_export
from . import  cmd_create


def turbo_command(arguments: List[str]):
    args = parse_arguments(arguments)
    # args.func
    # args.cmd
    module_name, func_name = args.func.rsplit(".", 1)
    module = import_module(module_name)
    #breakpoint()
    result = getattr(module, func_name)(args, None)
    return result
    if args.cmd == "export":
        return env_export(args)
    elif args.cmd == "create":
        return cmd_create.execute(args)


@plugins.hookimpl
def conda_subcommands():
    yield plugins.CondaSubcommand(
        name="turbo",
        summary="Improved environment.yaml files.",
        action=turbo_command,
    )
