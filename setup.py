#!/usr/bin/env python3

import argparse
import platform
import os

from field_dotfiles.utils import *


def main(args):
    os_type = platform.system()
    verbose_print(args.verbose, f"OS type: {os_type}")
    
    home_dir = os.path.expanduser("~")
    dotfiles_dir = os.path.dirname(os.path.realpath(__file__))
    verbose_print(args.verbose, f"Dotfiles directory: {dotfiles_dir}")

    print("==> Setup: Mackup")
    mackup_dir = os.path.join(dotfiles_dir, "mackup")
    verbose_print(args.verbose, f"Mackup directory: {mackup_dir}")
    make_link(
        os.path.join(mackup_dir, ".mackup.cfg"),
        os.path.join(home_dir, ".mackup.cfg"),
        args.verbose,
        args.dry_run,
    )
    make_link(
        os.path.join(mackup_dir, ".mackup"),
        os.path.join(home_dir, ".mackup"),
        args.verbose,
        args.dry_run,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Config Setup",
        description="The config setup script for Field.",
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Output verbose log."
    )
    parser.add_argument("-d", "--dry-run", action="store_true", help="Dry run.")

    args = parser.parse_args()
    main(args)
