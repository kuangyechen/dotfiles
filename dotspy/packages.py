from abc import ABC, abstractmethod

from .utils import *


__all__ = [
    "Rye",
    "HomeBrew",
    "Starship",
    "Fish",
    "Rust",
    "RustApps",
    "Fisher",
    "FishPlugins",
    "Foundry",
    "Dotfiles",
    "PythonApps",
]


class Package(ABC):
    def __init__(self, config):
        self.config = config

    @staticmethod
    @abstractmethod
    def name():
        pass

    @abstractmethod
    def run(self):
        pass


class Rye(Package):
    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def name():
        return "rye"

    @skip_if_executable_exists("rye")
    def run(self):
        if self.config.os_type == self.config.MACOS:
            self.run_mac()
        elif self.config.os_type == self.config.LINUX:
            self.run_linux()
        else:
            raise RuntimeError(f"Cannot run for os_type: {self.config.os_type}")

    def run_mac(self):
        homebrew_install("rye")

    def run_linux(self):
        confirm_then_execute_shell_command(
            "Do you want to install rye?",
            "curl -sSf https://rye-up.com/get | bash",
        )


class HomeBrew(Package):
    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def name():
        return "homebrew"

    @skip_if_executable_exists("brew", "homebrew")
    def run(self):
        if self.config.os_type == self.config.MACOS:
            self.run_mac()
        else:
            raise RuntimeError(f"Cannot run for os_type: {self.config.os_type}")

    def run_mac(self):
        confirm_then_execute_shell_command(
            "Do you want to install homebrew?",
            '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
        )


class Starship(Package):
    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def name():
        return "starship"

    @skip_if_executable_exists("starship")
    def run(self):
        if self.config.os_type == self.config.MACOS:
            self.run_mac()
        elif self.config.os_type == self.config.LINUX:
            self.run_linux()
        else:
            raise RuntimeError(f"Cannot run for os_type: {self.config.os_type}")

    def run_mac(self):
        homebrew_install("starship")

    def run_linux(self):
        confirm_then_execute_shell_command(
            "Do you want to install starship?",
            "curl -sS https://starship.rs/install.sh | sh",
        )


class Fish(Package):
    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def name():
        return "fish"

    @skip_if_executable_exists("fish")
    def run(self):
        if self.config.os_type == self.config.MACOS:
            self.run_mac()
        elif self.config.os_type == self.config.LINUX:
            self.run_linux()
        else:
            raise RuntimeError(f"Cannot run for os_type: {self.config.os_type}")

    def run_mac(self):
        homebrew_install("fish")

    def run_linux(self):
        linux_install("fish")


class Rust(Package):
    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def name():
        return "rust"

    @skip_if_executable_exists("cargo")
    def run(self):
        if self.config.os_type in {self.config.MACOS, self.config.LINUX}:
            confirm_then_execute_shell_command(
                "Do you want to install rust?",
                "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh",
            )
        else:
            raise RuntimeError(f"Cannot run for os_type: {self.config.os_type}")


class RustApps(Package):
    def __init__(self, config):
        super().__init__(config)

        self.apps = [
            {"brew": "zellij", "cargo": "zellij"},
            {"brew": "bat", "cargo": "bat"},
            {"brew": "eza", "cargo": "eza"},
            {"brew": "bottom", "cargo": "bottom"},
            {"brew": "grex", "cargo": "grex"},
            {"brew": "dust", "cargo": "du-dust"},
            {"brew": "sk", "cargo": "skim"},
            {"brew": "fd", "cargo": "fd-find"},
            {"brew": "sd", "cargo": "sd"},
            {"brew": "gitui", "cargo": "gitui"},
            {"brew": "zoxide", "cargo": "zoxide"},
            {"brew": "ripgrep", "cargo": "ripgrep"},
            {"brew": "ouch", "cargo": "ouch"},
            {"brew": "dotter", "cargo": "dotter"},
            {"brew": "tokei", "cargo": "tokei"},
            {"brew": "rm-improved", "cargo": "rm-improved"},
        ]

    @staticmethod
    def name():
        return "rust_apps"

    def run(self):
        if self.config.os_type == self.config.MACOS:
            self.run_mac()
        elif self.config.os_type == self.config.LINUX:
            self.run_linux()
        else:
            raise RuntimeError(f"Cannot run for os_type: {self.config.os_type}")

    def run_linux(self):
        cargo_install([app["cargo"] for app in self.apps if app["cargo"] is not None])

    def run_mac(self):
        homebrew_install([app["brew"] for app in self.apps if app["brew"] is not None])

        apps = [
            app["cargo"]
            for app in self.apps
            if app["brew"] is None and app["cargo"] is not None
        ]
        if len(apps) > 0:
            cargo_install(apps)


class Fisher(Package):
    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def name():
        return "fisher"

    def run(self):
        if self.config.os_type == self.config.MACOS:
            self.run_mac()
        elif self.config.os_type == self.config.LINUX:
            self.run_linux()
        else:
            raise RuntimeError(f"Cannot run for os_type: {self.config.os_type}")

    def run_linux(self):
        confirm_then_execute_shell_command(
            "Do you want to install fisher?",
            "curl -sL https://raw.githubusercontent.com/jorgebucaran/fisher/main/functions/fisher.fish | source && fisher install jorgebucaran/fisher",
        )

    def run_mac(self):
        homebrew_install("fisher")


class FishPlugins(Package):
    def __init__(self, config):
        super().__init__(config)

        self.plugins = ["jhillyerd/plugin-git", "LumaKernel/fish-fd-complete"]

    @staticmethod
    def name():
        return "fish_plugins"

    @need_executable_exists("fish")
    def run(self):
        if self.config.os_type in {self.config.MACOS, self.config.LINUX}:
            result = execute_shell_command('fish -c "fisher --version"')
            if result == 0:
                for plugin in self.plugins:
                    confirm_then_execute_shell_command(
                        f"Do you want to install {plugin}?",
                        f'fish -c "fisher install {plugin}"',
                    )
            else:
                print("Need fisher, skipped.")
        else:
            raise RuntimeError(f"Cannot run for os_type: {self.config.os_type}")


class Foundry(Package):
    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def name():
        return "foundry"

    @skip_if_executable_exists("foundryup")
    def run(self):
        if self.config.os_type in {self.config.MACOS, self.config.LINUX}:
            confirm_then_execute_shell_command(
                "Do you want to install foundryup?",
                "curl -L https://foundry.paradigm.xyz | bash",
            )
        else:
            raise RuntimeError(f"Cannot run for os_type: {self.config.os_type}")


class Dotfiles(Package):
    def __init__(self, config):
        super().__init__(config)

    @staticmethod
    def name():
        return "dotfiles"

    @need_executable_exists("dotter")
    def run(self):
        if self.config.os_type in {self.config.MACOS, self.config.LINUX}:
            confirm_then_execute_shell_command(
                "Do you want to link dotfiles with dotter?",
                "dotter -v",
            )
        else:
            raise RuntimeError(f"Cannot run for os_type: {self.config.os_type}")


class PythonApps(Package):
    def __init__(self, config):
        super().__init__(config)

        self.apps = [
            {"brew": "maturin", "pypi": "maturin"},
        ]

    @staticmethod
    def name():
        return "python_apps"

    def run(self):
        if self.config.os_type == self.config.MACOS:
            self.run_mac()
        elif self.config.os_type == self.config.LINUX:
            self.run_linux()
        else:
            raise RuntimeError(f"Cannot run for os_type: {self.config.os_type}")

    def run_linux(self):
        rye_install([app["pypi"] for app in self.apps if app["pypi"] is not None])

    def run_mac(self):
        homebrew_install([app["brew"] for app in self.apps if app["brew"] is not None])

        apps = [
            app["pypi"]
            for app in self.apps
            if app["brew"] is None and app["pypi"] is not None
        ]
        if len(apps) > 0:
            rye_install(apps)
