import os
import shutil
import subprocess

from . import config


__all__ = [
    "print_verbose",
    "make_link",
    "confirm_then_execute",
    "execute_shell_command",
    "confirm_then_execute_shell_command",
    "is_executable_exists",
    "print_section",
    "git_clone",
    "homebrew_install",
    "linux_install",
    "run_os_type_func",
    "check_os",
    "check_executable_exists",
    "cargo_install",
]


def print_verbose(*args):
    if config.verbose:
        print(*args)


def print_section(*args):
    print("\n=====>", *args)


def make_link(src, dst):
    print_verbose(f"Link {dst} -> {src}")

    if not os.path.exists(src):
        print(f"{src} not exists.")
    if os.path.exists(dst):
        print(f"{dst} exists, backup to {dst}.bak")
        if not config.dry_run:
            shutil.move(src=dst, dst=f"{dst}.bak")

    is_dir = os.path.isdir(src)
    if not config.dry_run:
        os.symlink(src, dst, is_dir)


def confirm_then_execute(prompt):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if config.yes:
                return func(*args, **kwargs)
            while True:
                answer = input(f"{prompt} [Y/n]").upper()
                if answer in {"Y", "YES", ""}:
                    return func(*args, **kwargs)
                elif answer in {"N", "NO"}:
                    break
                else:
                    print("Please input y/n")

        return wrapper

    return decorator


def execute_shell_command(command):
    if not config.dry_run:
        return subprocess.run([command], shell=True)
    else:
        print_verbose(f"Dry run command: {command}")


def confirm_then_execute_shell_command(prompt, command):
    func = confirm_then_execute(prompt)(lambda: execute_shell_command(command))
    func()


def is_executable_exists(executable):
    return shutil.which(executable) is not None


def git_clone(target, repo):
    if not os.path.exists(target):
        execute_shell_command(f"git clone {repo} {target}")
    else:
        print("{} already installed.".format(target))


def homebrew_install(targets):
    if is_executable_exists("brew"):
        if isinstance(targets, str):
            targets_str = targets
        elif isinstance(targets, list):
            targets_str = " ".join(targets)
        else:
            raise ValueError(f"Get targets: {targets}")

        confirm_then_execute_shell_command(
            f"Do you want to install {targets_str}?",
            f"brew install {targets_str}",
        )
    else:
        print("Need homebrew, do nothing.")


def linux_install(targets):
    if isinstance(targets, str):
        targets_str = targets
    elif isinstance(targets, list):
        targets_str = " ".join(targets)
    else:
        raise ValueError(f"Get targets: {targets}")

    if is_executable_exists("apt"):
        command = f"sudo apt install -y {targets_str}"
    else:
        print(f"Cannot find a way to install {targets_str} on this linux.")
        command = None

    if command is not None:
        confirm_then_execute_shell_command(
            f"Do you want to install {targets_str}?", command
        )


def cargo_install(targets):
    if isinstance(targets, str):
        targets_str = targets
    elif isinstance(targets, list):
        targets_str = " ".join(targets)
    else:
        raise ValueError(f"Get targets: {targets}")

    if is_executable_exists("cargo"):
        confirm_then_execute_shell_command(
            f"Do you want to install {targets_str}?",
            f"cargo install --locked {targets_str}",
        )
    else:
        print("Need cargo, do nothing.")


def run_os_type_func(func_map):
    func = func_map.get(config.os_type, None)
    if func is not None:
        func()
    else:
        print(f"Cannot get func for os_type: {config.os_type}")


def check_os(os_type):
    def dec(func):
        def wrapper(*args, **kwargs):
            if config.os_type == os_type:
                return func(*args, **kwargs)
            else:
                raise RuntimeError(
                    f"Expect OS type and dist: {os_type}, but run in {config.os_type}"
                )

        return wrapper

    return dec


def check_executable_exists(executable, package_name=None):
    def dec(func):
        package = package_name or executable

        def wrapper(*args, **kwargs):
            if not is_executable_exists(executable):
                return func(*args, **kwargs)
            else:
                print(f"{package} already exists, skipped.")

        return wrapper

    return dec
