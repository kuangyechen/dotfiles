import os

from .utils import *
from .config import Config

__all__ = [
    "linux_install_zsh",
    "linux_install_pyenv",
]


def check_is_linux(func):
    def wrapper(*args, **kwargs):
        if Config.os_type == "LINUX":
            return func(*args, **kwargs)

    return wrapper


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
