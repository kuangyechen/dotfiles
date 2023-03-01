from .utils import *
from .config import Config

__all__ = [
    "linux_install_zsh",
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

    if is_executable_exists("apt"):
        command = "sudo apt install -y zsh"
    else:
        print("WARNING!!! Cannot find a way to install zsh on this linux.")

    confirm_then_execute_shell_command("Do you want to install zsh?", command)
