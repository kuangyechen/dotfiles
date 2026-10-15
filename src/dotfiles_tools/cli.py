"""Command-line entry points; no installation or deployment side effects."""

import json
import tomllib
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import Annotated

import typer

from .catalog import Catalog
from .dotter import load_configuration
from .inspect import inspect

app = typer.Typer(
    name="dots",
    help=__doc__,
    add_completion=False,
    pretty_exceptions_enable=False,
)


def find_repo(start: Path) -> Path:
    for path in (start, *start.parents):
        if (path / "catalog.toml").is_file() and (path / ".dotter/global.toml").is_file():
            return path
    raise ValueError("Cannot find the dotfiles checkout; run from it or pass --repo")


@contextmanager
def cli_errors() -> Iterator[None]:
    try:
        yield
    except (OSError, ValueError, KeyError, TypeError, RuntimeError) as error:
        typer.echo(f"dots: {error}", err=True)
        raise typer.Exit(code=2) from error


@app.callback()
def configure(
    ctx: typer.Context,
    repo: Annotated[
        Path | None,
        typer.Option("--repo", help="Dotfiles checkout (default: discover from cwd)"),
    ] = None,
) -> None:
    # Resolve in commands so all help remains usable outside a checkout.
    ctx.obj = repo


def repository(ctx: typer.Context) -> Path:
    return ctx.obj.expanduser().resolve() if ctx.obj is not None else find_repo(Path.cwd())


@app.command()
def profile(
    ctx: typer.Context,
    name: Annotated[str, typer.Argument(help="Profile name from catalog.toml")],
    additions: Annotated[
        list[str] | None,
        typer.Option("--with", help="Add a component; may be repeated", metavar="COMPONENT"),
    ] = None,
    exclusions: Annotated[
        list[str] | None,
        typer.Option("--without", help="Exclude a component; may be repeated", metavar="COMPONENT"),
    ] = None,
) -> None:
    """Print a Dotter local configuration; never save it."""
    with cli_errors():
        repo = repository(ctx)
        selection = Catalog(repo).select(name, tuple(additions or ()), tuple(exclusions or ()))
        text = selection.render()
        # Validate group names and collisions using the same mapping reader as inspect.
        load_configuration(repo, Path.home(), tomllib.loads(text), f"profile:{name}")
        typer.echo(text, nl=False)


@app.command("inspect")
def inspect_command(
    ctx: typer.Context,
    json_output: Annotated[
        bool, typer.Option("--json", help="Emit JSON, without file contents")
    ] = False,
    profile_name: Annotated[
        str | None,
        typer.Option(
            "--profile", help="Preview a default profile instead of the existing local selection"
        ),
    ] = None,
    home: Annotated[
        Path | None,
        typer.Option("--home", help="Inspect another HOME, e.g. a temporary test directory"),
    ] = None,
) -> None:
    """Inspect configuration paths and Git status without modifying them."""
    with cli_errors():
        repo = repository(ctx)
        selected_home = home.expanduser().absolute() if home else Path.home()
        local = None
        label = None
        if profile_name:
            local = tomllib.loads(Catalog(repo).select(profile_name).render())
            label = f"profile:{profile_name}"
        report = inspect(repo, load_configuration(repo, selected_home, local, label))
        if json_output:
            typer.echo(json.dumps(report, indent=2))
        else:
            print_report(report)


def print_report(report: dict) -> None:
    typer.echo(f"Selection: {report['selection']}")
    typer.echo(f"Packages: {', '.join(report['packages'])}")
    typer.echo(
        "Files: "
        + (", ".join(f"{key}={value}" for key, value in report["summary"].items()) or "none")
    )
    for item in report["files"]:
        if item["status"] != "linked":
            typer.echo(f"  {item['status']}: {item['target']} <- {item['source']}")
    for item in report["unmanaged"]:
        typer.echo(f"  unmanaged: {item['target']}")
    typer.echo(
        f"Previous deployments outside selection: {len(report['previous_deployments'])} (see --json)"
    )
    typer.echo(f"Repository: {report['git']['status']}")
    for item in report["git"]["changes"]:
        typer.echo(f"  {item['status']} {item['path']}")
    for item in report["submodules"]:
        state = item.get("git", {}).get("status", item["state"])
        typer.echo(f"Submodule {item['path']}: {state}")


if __name__ == "__main__":
    app()
