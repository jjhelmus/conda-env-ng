from argparse import ArgumentParser

from conda import plugins

from conda.cli.helpers import add_parser_prefix

from typing import List


def turbo_command(arguments: List[str]):

    parser = ArgumentParser()
    add_parser_prefix(parser)

    args = parser.parse_args(arguments)
    print(args)

    from conda.base.context import context, determine_target_prefix, env_name
    from .env import from_environment
    prefix = determine_target_prefix(context, args)
    env = from_environment(
        env_name(prefix),
        prefix,
        #no_builds=args.no_builds,
        #ignore_channels=args.ignore_channels,
        #from_history=args.from_history,
    )
    breakpoint()
    print(env.to_yaml())

@plugins.hookimpl
def conda_subcommands():
    yield plugins.CondaSubcommand(
        name="turbo",
        summary="Improved environment.yaml files.",
        action=turbo_command,
    )
