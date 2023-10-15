#!/usr/bin/env python3

import argparse
import os

from field_dotfiles.utils import *
from field_dotfiles.install import *
from field_dotfiles.config import Config


def main(args):
    Config.dry_run = args.dry_run
    Config.verbose = args.verbose
    Config.yes = args.yes
    Config.dotfiles_dir = os.path.dirname(os.path.realpath(__file__))
    print_verbose(f"OS type: {Config.os_type}")
    print_verbose(f"Home directory: {Config.home_dir}")
    print_verbose(f"Dotfiles directory: {Config.dotfiles_dir}")

    install_linux_libraries()
    install_homebrew()
    install_brewfile()
    install_mackup()
    # install_fish()
    install_zsh()
    install_rust()
    install_oh_my_zsh()
    install_oh_my_zsh_customs()
    install_pyenv()
    install_rust_apps()
    install_config_files()


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

    args = parser.parse_args()
    main(args)
