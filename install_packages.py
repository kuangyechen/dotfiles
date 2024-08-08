#!/usr/bin/env python3

import argparse
import sys
import os

# Ensure the directory of this script is in sys.path
current_dir = os.path.dirname(os.path.realpath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from dotspy.utils import *
from dotspy.register import ALL_PACKAGES
from dotspy import config


def main(args):
    config.dry_run = args.dry_run
    config.verbose = args.verbose
    config.yes = args.yes
    config.dotfiles_dir = os.path.dirname(os.path.realpath(__file__))

    print_verbose(f"OS type: {config.os_type}")
    print_verbose(f"Home directory: {config.home_dir}")
    print_verbose(f"Dotfiles directory: {config.dotfiles_dir}")

    for package in args.packages:
        print_section(f"Package: {package}")
        pack = ALL_PACKAGES.get(package, None)
        if pack is None:
            raise ValueError(f"Unknown package: {package}")
        else:
            pack = pack(config)
            pack.run()


def split_by_whitespace(string):
    """Splits the input string by any whitespace and returns a list of words."""
    return string.split()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Config Setup",
        description="The config setup script for Field.",
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Output verbose log."
    )
    parser.add_argument("-d", "--dry-run", action="store_true", help="Dry run.")
    parser.add_argument("-y", "--yes", action="store_true", help="Auto confirm.")
    parser.add_argument(
        "-p",
        "--packages",
        type=split_by_whitespace,
        required=True,
        help="Packages to install.",
    )

    args = parser.parse_args()
    main(args)
