"""Inspect declared paths and Git metadata, never write or display file contents."""

import configparser
import hashlib
import os
import stat
import subprocess
from collections import Counter
from pathlib import Path

from .catalog import read_toml
from .dotter import Configuration, Mapping, repo_path


def _digest(path: Path) -> bytes:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").digest()


def _entry(mapping: Mapping) -> dict:
    result = {
        "package": mapping.package,
        "source": str(mapping.source),
        "target": str(mapping.target),
        "kind": mapping.kind,
    }
    try:
        if not mapping.source.exists():
            result["status"] = "source-missing"
        elif mapping.condition is not None or mapping.kind == "template":
            result["status"] = "manual"
            result["reason"] = "Template, condition or ownership needs Dotter/manual review"
        else:
            mode = mapping.target.lstat().st_mode
            if stat.S_ISLNK(mode):
                result["link_target"] = os.readlink(mapping.target)
                if mapping.target.resolve() == mapping.source.resolve():
                    result["status"] = "linked"
                elif mapping.target.exists():
                    result["status"] = "foreign-link"
                else:
                    result["status"] = "broken-link"
            elif mapping.target.resolve() == mapping.source.resolve():
                # Includes files reached through a correctly linked parent directory.
                result["status"] = "linked"
            elif mapping.kind == "automatic":
                result["status"] = "manual"
                result["reason"] = (
                    "Automatic target type needs Dotter review; use explicit symbolic mappings"
                )
            elif mapping.source.is_file() and stat.S_ISREG(mode):
                result["status"] = (
                    "identical"
                    if _digest(mapping.source) == _digest(mapping.target)
                    else "different"
                )
            else:
                result["status"] = "type-conflict"
    except FileNotFoundError:
        result["status"] = "missing"
    except NotADirectoryError:
        result["status"] = "parent-conflict"
    except (OSError, RuntimeError) as error:
        result["status"] = "unreadable"
        result["reason"] = type(error).__name__
    return result


def _walk_mapping(mapping: Mapping, repo: Path, ancestors: frozenset[Path] = frozenset()):
    source = mapping.source
    resolved = source.resolve()
    if not resolved.is_relative_to(repo):
        raise ValueError(f"Configuration source escapes the checkout: {source}")
    if resolved in ancestors:
        raise ValueError(f"Configuration source directory cycle: {source}")
    if (
        mapping.condition
        or mapping.kind == "template"
        or not mapping.recurse
        or not source.is_dir()
    ):
        yield mapping
        return
    # Do not walk a foreign target directory symlink and compare its contents.
    if mapping.target.is_symlink() and mapping.target.resolve() != resolved:
        yield mapping
        return
    children = sorted(source.iterdir())
    if not children:
        return  # Dotter also expands an empty recursive directory to zero files.
    for child in children:
        yield from _walk_mapping(
            mapping.model_copy(update={"source": child, "target": mapping.target / child.name}),
            repo,
            ancestors | {resolved},
        )


def _extra_files(mapping: Mapping, expected: set[Path]) -> list[dict]:
    if not mapping.recurse or mapping.kind == "template" or mapping.condition:
        return []
    if not mapping.source.is_dir() or not mapping.target.is_dir():
        return []
    if mapping.target.is_symlink() and mapping.target.resolve() != mapping.source.resolve():
        return []
    extra = []
    for root, directories, filenames in os.walk(mapping.target, followlinks=False):
        # Directory symlinks are entries, not trees to inspect.
        names = filenames + [name for name in directories if (Path(root) / name).is_symlink()]
        for name in sorted(names):
            target = Path(root) / name
            if target not in expected:
                extra.append(
                    {"package": mapping.package, "target": str(target), "status": "unmanaged"}
                )
    return extra


def _git(repo: Path, *arguments: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git", "--no-optional-locks", "-C", str(repo), *arguments],
        capture_output=True,
        text=True,
        errors="surrogateescape",
        check=False,
    )


def git_status(repo: Path) -> dict:
    try:
        root = _git(repo, "rev-parse", "--show-toplevel")
        if root.returncode or Path(root.stdout.strip()).resolve() != repo.resolve():
            return {"status": "unavailable", "changes": []}
        output = _git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=normal")
    except OSError:
        return {"status": "unavailable", "changes": []}
    if output.returncode:
        return {"status": "unavailable", "changes": []}
    records = iter(output.stdout.split("\0"))
    changes = []
    for record in records:
        if not record:
            continue
        item = {"status": record[:2], "path": record[3:]}
        if "R" in record[:2] or "C" in record[:2]:
            item["original_path"] = next(records)
        changes.append(item)
    return {"status": "dirty" if changes else "clean", "changes": changes}


def _submodules(repo: Path) -> list[dict]:
    path = repo / ".gitmodules"
    if not path.exists():
        return []
    config = configparser.ConfigParser(interpolation=None)
    config.read(path)
    result = []
    for section in config.sections():
        if not section.startswith("submodule "):
            continue
        relative = config[section]["path"].strip('"')
        directory = repo_path(repo, relative)
        state = (
            "initialized"
            if (directory / ".git").exists()
            else "uninitialized"
            if directory.exists()
            else "missing"
        )
        item = {"path": relative, "state": state}
        if state == "initialized":
            item["git"] = git_status(directory)
        result.append(item)
    return result


def inspect(repo: Path, configuration: Configuration) -> dict:
    repo = repo.resolve()
    expanded = []
    for mapping in configuration.mappings:
        expanded.extend(_walk_mapping(mapping, repo))
    # Directory expansion can reveal collisions not visible in the root mappings.
    targets: set[Path] = set()
    for mapping in expanded:
        if mapping.target in targets:
            raise ValueError(f"Expanded Dotter mappings overlap at {mapping.target}")
        targets.add(mapping.target)
    files = [_entry(mapping) for mapping in expanded]
    unmanaged = []
    for mapping in configuration.mappings:
        unmanaged.extend(_extra_files(mapping, targets))
    # A profile change can cause Dotter to remove previously deployed links.
    # Report cache-only entries even though they are no longer in the selection.
    previous = []
    cache_file = repo / ".dotter/cache.toml"
    if cache_file.exists():
        cache = read_toml(cache_file)
        active = {(str(item.source.relative_to(repo)), str(item.target)) for item in expanded}
        for kind in ("symlinks", "templates"):
            for source, target in cache.get(kind, {}).items():
                if (source, target) not in active:
                    previous.append({"source": source, "target": target, "kind": kind})
    return {
        "repository": str(repo),
        "selection": configuration.selection,
        "packages": configuration.packages,
        "summary": dict(sorted(Counter(item["status"] for item in files).items())),
        "files": files,
        "unmanaged": unmanaged,
        "previous_deployments": previous,
        "git": git_status(repo),
        "submodules": _submodules(repo),
    }
