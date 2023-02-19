import os
import shutil

__all__ = [
    "verbose_print",
    "make_link",
    "confirm_then_execute",
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
                answer = input(f"{prompt}, [Y/n]").upper()
                if answer in {"Y", "YES"}:
                    return func(*args, **kwargs)
                elif answer in {"N", "NO"}:
                    break
                else:
                    print("Please input y/n")

        return wrapper

    return decorator
