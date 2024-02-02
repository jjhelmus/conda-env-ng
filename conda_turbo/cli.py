from argparse import ArgumentParser

from typing import List

from conda.cli.helpers import add_parser_prefix
import conda.cli.main_env_export as main_env_export
import conda.cli.main_env_create as main_env_create



def parse_arguments(arguments: List[str]):
    parser = ArgumentParser()
    subparser = parser.add_subparsers(metavar="command", dest="cmd")
    main_env_export.configure_parser(subparser)
    main_env_create.configure_parser(subparser)
    args = parser.parse_args(arguments)
    return args
