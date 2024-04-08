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

    create_parser.add_argument(
        "--no-solve",
        action="store_true",
        help="Do not solve the environment, determine from package details, can fail."
    )
    env_field_group = create_parser.add_argument_group(
        "Environment Field",
        "The field from the environment.yaml file that is used to create the environment."
    )
    exclusive_field_group = env_field_group.add_mutually_exclusive_group()
    exclusive_field_group.add_argument(
        "--from-explicit",
        action="store_const",
        const="explicit",
        dest="env_field",
        help="The explicit field."
    )
    exclusive_field_group.add_argument(
        "--from-requested",
        action="store_const",
        const="requested",
        dest="env_field",
        help="The requested field."
    )
    exclusive_field_group.add_argument(
        "--from-dependencies",
        action="store_const",
        const="dependencies",
        dest="env_field",
        help="The dependencies field."
    )

    create_parser.set_defaults(func="conda_turbo.cli.main_env_create.execute")
    parser.set_defaults(func="conda_turbo.cli.main_env.execute")
    """
        If the environment.yaml file contains additional fields (subdir, requested and explicit)
        then the explicit environment will be created when the environment described an environment
        from the same platform. Otherwise the requested specification will be used. This behavior
        be modified using the --from-* options.

        Note that default packages are not installed into explicit environments.
    """
    return parser


def execute(args: Namespace, parser: ArgumentParser) -> int:
    parser.parse_args(["--help"])

    return 0
