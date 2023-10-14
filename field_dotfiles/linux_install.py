import os

from .utils import *
from .config import Config

__all__ = [
    "linux_install_zsh",
    "linux_install_fish",
    "linux_install_pyenv",
    "linux_install_mackup",
]


def check_is_linux(func):
    def wrapper(*args, **kwargs):
        if Config.os_type == "LINUX":
            return func(*args, **kwargs)

    return wrapper


@check_is_linux
def linux_install_mackup():
    if is_executable_exists("mackup"):
        print("Mackup already installed.")
        return

    if is_executable_exists("apt"):
        command = "sudo apt install -y pipx"
    else:
        print("WARNING!!! Cannot find a way to install pipx on this linux.")
        return

    confirm_then_execute_shell_command("Do you want to install pipx?", command)
    confirm_then_execute_shell_command("Do you want to install mackup?", "pipx install mackup")


@check_is_linux
def linux_install_zsh():
    if is_executable_exists("zsh"):
        print("Zsh already installed.")
        return

    if is_executable_exists("apt"):
        command = "sudo apt install -y zsh"
    else:
        print("WARNING!!! Cannot find a way to install zsh on this linux.")
        return

    confirm_then_execute_shell_command("Do you want to install zsh?", command)


@check_is_linux
def linux_install_fish():
    if is_executable_exists("fish"):
        print("Fish already installed.")
        return

    if is_executable_exists("apt"):
        command = "sudo apt install -y fish"
    else:
        print("WARNING!!! Cannot find a way to install fish on this linux.")
        return

    confirm_then_execute_shell_command("Do you want to install fish?", command)


@check_is_linux
def linux_install_pyenv():
    @confirm_then_execute("Do you want to install pyenv?")
    def _install():
        git_clone(
            os.path.join(Config.home_dir, ".pyenv"),
            "https://github.com/pyenv/pyenv.git",
        )
        git_clone(
            os.path.join(Config.home_dir, ".pyenv/plugins/pyenv-virtualenv"),
            "https://github.com/pyenv/pyenv-virtualenv.git",
        )

    _install()
