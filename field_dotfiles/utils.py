import os
import shutil
import subprocess


__all__ = [
    "verbose_print",
    "make_link",
    "confirm_then_execute",
    "execute_shell_command",
    "confirm_then_execute_shell_command",
    "is_executable_exists",
]


def verbose_print(verbose, *args):
    if verbose:
        print(*args)


def make_link(src, dst, verbose, dry_run):
    verbose_print(verbose, f"Link {dst} -> {src}")

    if not os.path.exists(src):
        print(f"{src} not exists.")
    if os.path.exists(dst):
        print(f"{dst} exists, backup to {dst}.bak")
        if not dry_run:
            shutil.move(src=dst, dst=f"{dst}.bak")

    is_dir = os.path.isdir(src)
    if not dry_run:
        os.symlink(src, dst, is_dir)


def confirm_then_execute(prompt):
    def decorator(func):
        def wrapper(*args, **kwargs):
            while True:
                answer = input(f"{prompt} [Y/n]").upper()
                if answer in {"Y", "YES"}:
                    return func(*args, **kwargs)
                elif answer in {"N", "NO"}:
                    break
                else:
                    print("Please input y/n")

        return wrapper

    return decorator


def execute_shell_command(command):
    return subprocess.run(command, shell=True)


def confirm_then_execute_shell_command(prompt, command, dry_run):
    confirm_then_execute(prompt)(lambda: execute_shell_command(command) if not dry_run else 0)


def is_executable_exists(executable):
    return shutil.which(executable) is not None
