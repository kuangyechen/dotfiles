import os
import shutil
import subprocess

from .config import Config


__all__ = [
    "print_verbose",
    "make_link",
    "confirm_then_execute",
    "execute_shell_command",
    "confirm_then_execute_shell_command",
    "is_executable_exists",
    "print_section",
    "git_clone",
]


def print_verbose(*args):
    if Config.verbose:
        print(*args)


def print_section(*args):
    print("\n=====>", *args)


def make_link(src, dst):
    print_verbose(f"Link {dst} -> {src}")

    if not os.path.exists(src):
        print(f"{src} not exists.")
    if os.path.exists(dst):
        print(f"{dst} exists, backup to {dst}.bak")
        if not Config.dry_run:
            shutil.move(src=dst, dst=f"{dst}.bak")

    is_dir = os.path.isdir(src)
    if not Config.dry_run:
        os.symlink(src, dst, is_dir)


def confirm_then_execute(prompt):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if Config.yes:
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
    if not Config.dry_run:
        return subprocess.run([command], shell=True)


def confirm_then_execute_shell_command(prompt, command):
    func = confirm_then_execute(prompt)(
        lambda: execute_shell_command(command) if not Config.dry_run else 0
    )
    func()


def is_executable_exists(executable):
    return shutil.which(executable) is not None


def git_clone(target, repo):
    if not os.path.exists(target):
        execute_shell_command(f"git clone {repo} {target}")
    else:
        print("{} already installed.".format(target))
