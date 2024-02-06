import json
import os
from argparse import (
    ArgumentParser,
    Namespace,
)

from conda import CondaError

def execute(args: Namespace, parser: ArgumentParser) -> int:
    from conda.auxlib.ish import dals
    from conda.base.context import context, determine_target_prefix
    from conda.core.prefix_data import PrefixData
    from conda.env import specs
    from conda.env.env import get_filename, print_result
    from conda.env.installers.base import get_installer
    from conda.exceptions import InvalidInstaller
    from conda.gateways.disk.delete import rm_rf
    from conda.misc import touch_nonadmin
    from conda.cli import install as cli_install

    spec = specs.detect(
        name=args.name,
        filename=get_filename(args.file),
        directory=os.getcwd(),
        remote_definition=args.remote_definition,
    )
    env = spec.environment

    # FIXME conda code currently requires args to have a name or prefix
    # don't overwrite name if it's given. gh-254
    if args.prefix is None and args.name is None:
        args.name = env.name

    prefix = determine_target_prefix(context, args)

    if args.yes and prefix != context.root_prefix and os.path.exists(prefix):
        rm_rf(prefix)
    cli_install.check_prefix(prefix, json=args.json)

    # TODO, add capability
    # common.ensure_override_channels_requires_channel(args)
    # channel_urls = args.channel or ()

    result = {"conda": None, "pip": None}

    args_packages = (
        context.create_default_packages if not args.no_default_packages else []
    )

    if args.dry_run:
        installer_type = "conda"
        installer = get_installer(installer_type)

        pkg_specs = env.dependencies.get(installer_type, [])
        pkg_specs.extend(args_packages)

        solved_env = installer.dry_run(pkg_specs, args, env)
        if args.json:
            print(json.dumps(solved_env.to_dict(), indent=2))
        else:
            print(solved_env.to_yaml(), end="")

    else:
        if args_packages:
            installer_type = "conda"
            installer = get_installer(installer_type)
            result[installer_type] = installer.install(prefix, args_packages, args, env)

        if len(env.dependencies.items()) == 0:
            installer_type = "conda"
            pkg_specs = []
            installer = get_installer(installer_type)
            result[installer_type] = installer.install(prefix, pkg_specs, args, env)
        else:
            for installer_type, pkg_specs in env.dependencies.items():
                try:
                    installer = get_installer(installer_type)
                    result[installer_type] = installer.install(
                        prefix, pkg_specs, args, env
                    )
                except InvalidInstaller:
                    raise CondaError(
                        dals(
                            f"""
                            Unable to install package for {installer_type}.

                            Please double check and ensure your dependencies file has
                            the correct spelling. You might also try installing the
                            conda-env-{installer_type} package to see if provides
                            the required installer.
                            """
                        )
                    )

        if env.variables:
            pd = PrefixData(prefix)
            pd.set_environment_env_vars(env.variables)

        touch_nonadmin(prefix)
        print_result(args, prefix, result)

    return 0
