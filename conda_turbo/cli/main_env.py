# Copyright (C) 2012 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
"""Entry point for all conda env-ng subcommands."""
from __future__ import annotations

from argparse import ArgumentParser, Namespace


def configure_parser(parser: ArgumentParser) -> ArgumentParser:
    from conda.cli import (
        main_env_config,
        main_env_create,
        main_env_export,
        main_env_list,
        main_env_remove,
        main_env_update,
    )
    env_parsers = parser.add_subparsers(
        metavar="command",
        dest="cmd"
    )

    # conda env parsers
    config_parser = main_env_config.configure_parser(env_parsers)
    create_parser = main_env_create.configure_parser(env_parsers)
    export_parser = main_env_export.configure_parser(env_parsers)
    list_parser = main_env_list.configure_parser(env_parsers)
    remove_parser = main_env_remove.configure_parser(env_parsers)
    update_parser = main_env_update.configure_parser(env_parsers)

    # conda env-ng specific
    export_parser.add_argument(
        "--no-additional-fields",
        action="store_true",
        help="Do not include additional fields in the output, only base fields"
    )
    export_parser.set_defaults(func="conda_turbo.cli.main_env_export.execute")
    create_parser.set_defaults(func="conda_turbo.cli.main_env_create.execute")
    parser.set_defaults(func="conda_turbo.cli.main_env.execute")
    return parser


def execute(args: Namespace, parser: ArgumentParser) -> int:
    parser.parse_args(["--help"])

    return 0
