"""Read the repository's Dotter configuration without deploying anything.

Includes patch package files in order, then local files patch the merged result.
Templates and conditions are reported for manual handling, never evaluated here.
"""

import os
import re
import socket
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict

from .catalog import read_toml, string_list


class Mapping(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, hide_input_in_errors=True)

    package: str
    source: Path
    target: Path
    kind: Literal["symbolic", "template", "automatic"] = "symbolic"
    recurse: bool = True
    condition: str | None = None


class Configuration(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True, hide_input_in_errors=True)

    selection: str
    packages: list[str]
    mappings: list[Mapping]


def repo_path(repo: Path, value: str) -> Path:
    path = repo / value
    if not path.resolve().is_relative_to(repo.resolve()):
        raise ValueError(f"Repository path escapes the checkout: {value!r}")
    return path


def target_path(repo: Path, value: str, home: Path) -> Path:
    def variable(match: re.Match) -> str:
        name = match.group(1) or match.group(2)
        if name == "HOME":
            return str(home)
        if name not in os.environ:
            raise ValueError(f"Undefined target environment variable: {name}")
        return os.environ[name]

    value = re.sub(r"\$\{([A-Za-z_]\w*)\}|\$([A-Za-z_]\w*)", variable, value)
    if value == "~" or value.startswith("~/"):
        value = str(home) + value[1:]
    elif value.startswith("~"):
        raise ValueError("Named-user home expansion is unsupported; use ~/ or $HOME")
    # Do not resolve: the identity of the target symlink is what inspect checks.
    return Path(os.path.abspath(repo / value))


def load_configuration(
    repo: Path,
    home: Path,
    local: dict | None = None,
    selection: str | None = None,
) -> Configuration:
    repo = repo.resolve()
    global_config = read_toml(repo / ".dotter/global.toml")
    settings = global_config.pop("settings", {})
    if "helpers" in global_config:
        raise ValueError("Dotter helpers require manual inspection")
    default_kind = settings.get("default_target_type", "automatic")
    if default_kind not in {"symbolic", "template", "automatic"}:
        raise ValueError(f"Unknown Dotter default target type: {default_kind}")
    if local is None:
        path = repo / ".dotter/local.toml"
        if not path.exists():
            path = repo / ".dotter" / f"{socket.gethostname()}.toml"
        if not path.exists():
            raise ValueError(
                "No Dotter local configuration; inspect --profile mac|linux-server first"
            )
        local = read_toml(path)
        selection = str(path.relative_to(repo))
    unknown = local.keys() - {"packages", "includes", "files", "variables"}
    if unknown:
        raise ValueError(f"Unsupported Dotter local fields: {', '.join(sorted(unknown))}")
    for include in string_list(local.get("includes", []), "Dotter includes"):
        for name, patch in read_toml(repo_path(repo, include)).items():
            if name not in global_config:
                global_config[name] = patch
            else:
                # Dotter replaces complete file targets, not their individual attributes.
                global_config[name].setdefault("files", {}).update(patch.get("files", {}))
                # Existing package dependencies are not replaced by includes.
    requested = string_list(local.get("packages"), "Dotter packages")
    enabled: set[str] = set()

    def enable(name: str) -> None:
        if name in enabled:
            return
        if name not in global_config:
            raise ValueError(f"Unknown Dotter package {name!r}")
        enabled.add(name)
        spec = global_config[name]
        unknown = spec.keys() - {"files", "depends", "variables"}
        if unknown:
            raise ValueError(f"Unsupported fields in Dotter package {name!r}: {sorted(unknown)}")
        for dependency in string_list(spec.get("depends", []), f"{name}.depends"):
            enable(dependency)

    for name in requested:
        enable(name)
    files: dict[str, tuple[str, object, str]] = {}
    for name in sorted(enabled):
        for source, target in global_config[name].get("files", {}).items():
            if source in files:
                raise ValueError(f"Dotter source appears in multiple selected packages: {source}")
            files[source] = (name, target, default_kind)
    for source, target in local.get("files", {}).items():
        # Dotter applies local file overrides after global default type conversion.
        files[source] = ("local", target, "automatic")
    mappings: list[Mapping] = []
    targets: dict[Path, Path] = {}
    for source, (name, spec, kind) in sorted(files.items()):
        recurse = True
        condition = None
        if isinstance(spec, str):
            destination = spec
        elif isinstance(spec, dict):
            unknown = spec.keys() - {
                "target",
                "type",
                "recurse",
                "if",
                "owner",
                "append",
                "prepend",
            }
            if unknown:
                raise ValueError(
                    f"Unsupported Dotter target fields for {source}: {sorted(unknown)}"
                )
            destination = spec.get("target")
            kind = spec.get("type")
            recurse = spec.get("recurse", True)
            condition = spec.get("if")
            if not isinstance(recurse, bool):
                raise ValueError(f"Dotter recurse must be boolean for {source}")
            if spec.get("owner") is not None:
                condition = condition or "owner requires manual inspection"
            if kind != "template" and ("append" in spec or "prepend" in spec):
                raise ValueError(f"append/prepend require a template target: {source}")
        else:
            raise ValueError(f"Invalid Dotter target for {source}")
        if not isinstance(destination, str) or kind not in {"symbolic", "template", "automatic"}:
            raise ValueError(f"Invalid Dotter target for {source}")
        if not destination:
            continue
        src = repo_path(repo, source)
        dst = target_path(repo, destination, home)
        if dst in targets:
            raise ValueError(f"Multiple Dotter sources target {dst}: {targets[dst]}, {src}")
        targets[dst] = src
        mappings.append(
            Mapping(
                package=name,
                source=src,
                target=dst,
                kind=kind,
                recurse=recurse,
                condition=condition,
            )
        )
    return Configuration(
        selection=selection or "provided configuration", packages=sorted(enabled), mappings=mappings
    )
