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
    "skip_if_executable_exists",
    "cargo_install",
    "prepend_to_path",
    "append_to_path",
    "need_executable_exists",
    "rye_install",
    "uv_install",
]


def skip_if_executable_exists(executable, package_name=None):
    def dec(func):
        package = package_name or executable

        def wrapper(*args, **kwargs):
            if not is_executable_exists(executable):
                return func(*args, **kwargs)
            else:
                print(f"{package} already exists, skipped.")

        return wrapper

    return dec


def need_executable_exists(executable):
    def dec(func):
        def wrapper(*args, **kwargs):
            if is_executable_exists(executable):
                return func(*args, **kwargs)
            else:
                print(f"Need {executable}, skipped.")

        return wrapper

    return dec


def parse_targets(targets):
    if isinstance(targets, str):
        targets_str = targets
    elif isinstance(targets, list):
        targets_str = " ".join(targets)
    else:
        raise ValueError(f"Get targets: {targets}")
    return targets_str


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
        result = subprocess.run([command], shell=True)
        return result.returncode
    else:
        print_verbose(f"Dry run command: {command}")
        return 0


def confirm_then_execute_shell_command(prompt, command):
    func = confirm_then_execute(prompt)(lambda: execute_shell_command(command))
    return func()


def is_executable_exists(executable):
    return shutil.which(executable) is not None


def git_clone(target, repo):
    if not os.path.exists(target):
        execute_shell_command(f"git clone {repo} {target}")
    else:
        print("{} already installed.".format(target))


@need_executable_exists("brew")
def homebrew_install(targets):
    targets_str = parse_targets(targets)

    confirm_then_execute_shell_command(
        f"Do you want to install {targets_str}?",
        f"brew install {targets_str}",
    )


@need_executable_exists("uv")
def uv_install(targets):
    targets_str = parse_targets(targets)

    confirm_then_execute_shell_command(
        f"Do you want to install {targets_str}?",
        f"uv tool install {targets_str}",
    )


@need_executable_exists("rye")
def rye_install(targets):
    targets_str = parse_targets(targets)

    confirm_then_execute_shell_command(
        f"Do you want to install {targets_str}?",
        f"rye install {targets_str}",
    )


def linux_install(targets):
    targets_str = parse_targets(targets)

    if is_executable_exists("apt"):
        command = f"sudo apt install -y {targets_str}"
    else:
        print(f"Cannot find a way to install {targets_str} on this linux.")
        command = None

    if command is not None:
        confirm_then_execute_shell_command(
            f"Do you want to install {targets_str}?", command
        )


@need_executable_exists("cargo")
def cargo_install(targets):
    targets_str = parse_targets(targets)

    confirm_then_execute_shell_command(
        f"Do you want to install {targets_str}?",
        f"cargo install --locked {targets_str}",
    )


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


def append_to_path(directories):
    """Append a directory to the PATH environment variable."""
    # Get the current PATH
    current_path = os.environ.get("PATH", "")
    path_list = current_path.split(os.pathsep)

    os.environ["PATH"] = os.pathsep.join(
        path_list + [dir_ for dir_ in directories if dir_ not in path_list]
    )


def prepend_to_path(directories):
    """Append a directory to the PATH environment variable."""
    # Get the current PATH
    current_path = os.environ.get("PATH", "")
    path_list = current_path.split(os.pathsep)

    os.environ["PATH"] = os.pathsep.join(
        [dir_ for dir_ in directories if dir_ not in path_list] + path_list
    )
