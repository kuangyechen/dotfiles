import os

from .linux_install import *
from .mac_install import *
from .utils import *
from .config import Config

__all__ = [
    "install_zsh",
    "install_rust",
    "install_oh_my_zsh",
    "install_oh_my_zsh_customs",
    "install_homebrew",
    "install_config_files",
    "install_rust_apps",
    "install_brewfile",
]


def install_zsh():
    print_section("ZSH")
    mac_install_zsh()
    linux_install_zsh()


def install_rust():
    print_section("RUST")
    if not is_executable_exists("cargo"):
        confirm_then_execute_shell_command(
            "Do you want to install rust?",
            "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
        )
    else:
        print("Rust already installed.")


def install_oh_my_zsh():
    print_section("OH-MY-ZSH")
    if not os.path.exists(os.path.join(Config.home_dir, "./.oh-my-zsh")):
        if not is_executable_exists("curl"):
            print("Need curl command.")
            return
        confirm_then_execute_shell_command(
            "Do you want to install oh-my-zsh?",
            'sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended',
        )
    else:
        print("Oh-my-zsh already installed.")


def install_oh_my_zsh_customs():
    print_section("OH-MY-ZSH-CUSTOMS")
    if not os.path.exists(os.path.join(Config.home_dir, "./.oh-my-zsh")):
        return
    zsh_custom = os.path.join(Config.home_dir, ".oh-my-zsh/custom")

    @confirm_then_execute("Do you want to install oh-my-zsh customs?")
    def git_clone():
        target = os.path.join(zsh_custom, "plugins/zsh-autosuggestions")
        if not os.path.exists(target):
            execute_shell_command(
                f"git clone https://github.com/zsh-users/zsh-autosuggestions {target}"
            )
        else:
            print("{} already installed.".format(target))

        target = os.path.join(zsh_custom, "plugins/zsh-syntax-highlighting")
        if not os.path.exists(target):
            execute_shell_command(
                f"git clone https://github.com/zsh-users/zsh-syntax-highlighting.git {target}"
            )
        else:
            print("{} already installed.".format(target))

        target = os.path.join(zsh_custom, "themes/powerlevel10k")
        if not os.path.exists(target):
            execute_shell_command(
                f"git clone https://github.com/romkatv/powerlevel10k.git {target}"
            )
        else:
            print("{} already installed.".format(target))

    git_clone()


def install_homebrew():
    print_section("HOMEBREW")
    mac_install_homebrew()


def install_config_files():
    print_section("MACKUP CONFIGS")

    @confirm_then_execute("Do you want to link mackup configs?")
    def _mackup_link():
        mackup_dir = os.path.join(Config.dotfiles_dir, "mackup")
        print_verbose(f"Mackup directory: {mackup_dir}")
        make_link(
            os.path.join(mackup_dir, ".mackup.cfg"),
            os.path.join(Config.home_dir, ".mackup.cfg"),
        )
        make_link(
            os.path.join(mackup_dir, ".mackup"),
            os.path.join(Config.home_dir, ".mackup"),
        )

    _mackup_link()

    if is_executable_exists("mackup"):
        confirm_then_execute_shell_command(
            "Do you want to restore configs from mackup repo?",
            "mackup restore",
        )


def install_rust_apps():
    print_section("RUST APPS")

    apps = [
        {"brew": "zellij", "cargo": "zellij"},
        {"brew": "bat", "cargo": "bat"},
        {"brew": "bottom", "cargo": "bottom"},
        {"brew": "grex", "cargo": "grex"},
        {"brew": "dust", "cargo": "du-dust"},
        {"brew": "sk", "cargo": "skim"},
        {"brew": "helix", "cargo": "helix"},
        {"brew": "fd", "cargo": "fd-find"},
        {"brew": "sd", "cargo": "sd"},
        {"brew": "gitui", "cargo": "gitui"},
    ]

    @confirm_then_execute("Do you want to install all rust apps?")
    def _install():
        if is_executable_exists("brew"):
            execute_shell_command(
                "brew install {}".format(" ".join([app["brew"] for app in apps]))
            )
            return

        if not is_executable_exists("cargo"):
            print("Need cargo, do nothing.")
            return
        confirm_then_execute_shell_command(
            "Cargo install will build everything from source, confirm?",
            "cargo install --locked {}".format(
                " ".join([app["cargo"] for app in apps])
            ),
        )

    _install()


def install_brewfile():
    mac_install_homebrew_brewfile()
