# Copyright (C) 2012 Anaconda, Inc
# SPDX-License-Identifier: BSD-3-Clause
"""Entry point for all conda env-ng subcommand."""

from argparse import ArgumentParser
from importlib import import_module

from typing import List

from .main_env import configure_parser


def main(arguments: List[str]) -> int:
    parser = configure_parser(ArgumentParser())
    args = parser.parse_args(arguments)
    module_name, func_name = args.func.rsplit(".", 1)
    module = import_module(module_name)
    result = getattr(module, func_name)(args, parser)
    return result
