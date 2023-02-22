#!/usr/bin/env python3

import argparse
import platform
import os

from field_dotfiles.utils import *


def main(args):
    os_type = platform.system()
    verbose_print(args.verbose, f"OS type: {os_type}")
    if os_type != "Darwin":
        print("Currently only tested on MacOS, exit.")
        return

    home_dir = os.path.expanduser("~")
    verbose_print(args.verbose, f"Home directory: {home_dir}")
    dotfiles_dir = os.path.dirname(os.path.realpath(__file__))
    verbose_print(args.verbose, f"Dotfiles directory: {dotfiles_dir}")

    if not is_executable_exists("zsh"):
        if os_type == "Darwin":
            print("WARNING!!! MacOS should always has ZSH installed.")

    if is_executable_exists("zsh"):
        if os.path.exists(os.path.join(home_dir, "./.oh-my-zsh")):
            print("=====> Oh-My-Zsh installed.")
        else:
            print("=====> Install Oh-My-Zsh")
            confirm_then_execute_shell_command(
                "Do you want to install oh-my-zsh?",
                [
                    'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended'
                ],
                args.dry_run,
            )

    if os_type == "Darwin":
        if not is_executable_exists("brew"):
            print("=====> Install Homebrew")
            confirm_then_execute_shell_command(
                "Do you want to install homebrew?",
                [
                    '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
                ],
                args.dry_run,
            )
        else:
            print("=====> Homebrew installed.")

    print("=====> Setup: Mackup")
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
