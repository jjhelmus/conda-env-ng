# Copyright (C) 2012 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
"""CLI implementation for `conda env-ng export`.

Dumps specified environment package specifications to the screen.
"""
from argparse import Namespace, ArgumentParser


# modified from conda.cli.main_env_export.py::execute
def execute(args: Namespace, parser: ArgumentParser) -> int:
    from conda.base.context import context, determine_target_prefix, env_name
    from ..env.env import from_environment
    from conda.cli.common import stdout_json
    prefix = determine_target_prefix(context, args)
    env = from_environment(
        env_name(prefix),
        prefix,
        no_builds=args.no_builds,
        ignore_channels=args.ignore_channels,
        from_history=args.from_history,
        only_base_fields=args.no_additional_fields,
    )

    if args.override_channels:
        env.remove_channels()

    if args.channel is not None:
        env.add_channels(args.channel)

    if args.file is None:
        stdout_json(env.to_dict()) if args.json else print(env.to_yaml(), end="")
    else:
        fp = open(args.file, "wb")
        env.to_dict(stream=fp) if args.json else env.to_yaml(stream=fp)
        fp.close()

    return 0
