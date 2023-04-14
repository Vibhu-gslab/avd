from .eos_cli_config_gen import eos_cli_config_gen
from .eos_designs_facts import eos_designs_facts
from .eos_designs_structured_configs import eos_designs_structured_configs
from .version import VERSION
from .tools.multiprocess_runners import run_eos_cli_config_gen
import argparse

""" Library for running Arista Validated Designs (AVD) in Python
"""
DESCRIPTION = __doc__
NAME = "pyavd"

__author__ = "Arista Networks"
__copyright__ = "Copyright 2023 Arista Networks"
__license__ = "Apache 2.0"
__version__ = VERSION

__all__ = ["eos_cli_config_gen", "eos_designs_facts", "eos_designs_structured_configs"]

def runner1():
    parser = argparse.ArgumentParser(
        prog="Runner",
        description="Run AVD Components like eos_cli_config_gen for multiple devices",
        epilog="See https://avd.sh/en/stable/ for details on supported variables",
    )
    parser.add_argument(
        "--eos_cli_config_gen",
        "-3",
        help=(
            "Run eos_cli_config_gen. Vars are read from dir set in --struct_cfgfiles combined with any --common_struct_cfgfile."
            " Configs are written to dir set in --cfgfiles if the option is set."
            " Documentation markdown files are written to dir set in --docfiles if the option is set."
        ),
        action="count",
        default=0,
    )
    parser.add_argument(
        "--common_struct_cfgfile",
        "-t",
        help=(
            "YAML or JSON File where common structured_config are read from."
            " Multiple files can be added by repeating the argument."
            " Data will be deepmerged in the order of the common_struct_cfgfiles arguments."
        ),
        action="append",
        default=[],
    )
    parser.add_argument(
        "--struct_cfgfiles",
        "-s",
        help=(
            "Source/Destination directory for device structured configuration files Filenames will be <hostname>.yml"
            " Will be used as input for eos_cli_config_gen and output for eos_designs"
        ),
    )
    parser.add_argument(
        "--cfgfiles",
        "-c",
        help="Destination directory for device configuration files Filenames will be <hostname>.cfg",
    )
    parser.add_argument(
        "--docfiles",
        "-d",
        help="Destination directory for device documentation files Filenames will be <hostname>.md",
    )
    args = parser.parse_args()
    if args.eos_cli_config_gen:
        run_eos_cli_config_gen(args.common_struct_cfgfile, args.struct_cfgfiles, args.cfgfiles, args.docfiles)



