from argparse import ArgumentParser, Namespace, _SubParsersAction

from typing import List

from conda.cli import (
    main_env_config,
    main_env_create,
    main_env_export,
    main_env_list,
    main_env_remove,
    main_env_update,
)

def configure_parser(parser: ArgumentParser) -> ArgumentParser:
    env_parsers = parser.add_subparsers(
        metavar="command",
        dest="cmd"
    )

    # use the parser from conda
    config_parser = main_env_config.configure_parser(env_parsers)
    create_parser = main_env_create.configure_parser(env_parsers)
    export_parser = main_env_export.configure_parser(env_parsers)
    list_parser = main_env_list.configure_parser(env_parsers)
    remove_parser = main_env_remove.configure_parser(env_parsers)
    update_parser = main_env_update.configure_parser(env_parsers)

    # local updates
    export_parser.set_defaults(func="conda_turbo.cmd_export.env_export")
    return parser


def parse_arguments(arguments: List[str]):
    parser = configure_parser(ArgumentParser())
    args = parser.parse_args(arguments)
    return args

