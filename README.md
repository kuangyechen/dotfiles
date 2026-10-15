# Dotfiles

A personal environment repository maintained by AI agents for macOS and Ubuntu/Debian servers.
Clone it on the target device, start an agent session in the repository, and describe the task:

> Set up this new Mac with the default environment, Zed, and Aerospace.
>
> Sync this device's configuration and software choices into the repository, preserving local overrides.

[AGENTS.md](AGENTS.md) routes agents to [setup](workflows/setup.md) or [sync](workflows/sync.md).
[catalog.toml](catalog.toml) defines software choices and profiles; Dotter defines configuration mappings.

## Layout

- `src/dotfiles_tools/`: profile and inspection helpers, exposed as `dots`.
- `dots/`: configurations; `dots/private-dotfiles/` holds personal settings.
- `.dotter/`: mappings; local selections and caches remain untracked.
- `workflows/`: agent procedures and decision rules.
- `raycast_scripts/`: independent project with its own Python environment.
- `legacy/`: retired installers and Mackup snapshots, for reference only.

## Helper commands

Install [uv](https://docs.astral.sh/uv/getting-started/installation/). It uses the pinned
**Python 3.12.15** from `.python-version`, independently of system Python. The project supports
Python 3.12 and uses Pydantic for catalog and configuration models.

```sh
uv run dots profile mac
uv run dots profile linux-server
uv run dots profile mac --with zed --with aerospace
uv run dots profile mac --without zsh --with oh-my-zsh

uv run dots inspect
uv run dots inspect --json
uv run dots inspect --profile linux-server --home /tmp/example-home
```

`profile` prints Dotter configuration without saving it. The agent compares existing choices
before saving `.dotter/local.toml`. Default software selections live only in the catalog.

`inspect` reads the existing local selection, with Dotter's hostname fallback. Use `--profile`
to preview defaults. It does not modify configuration, deployment, or caches, or print file contents.
The first uv invocation may install Python and create the project environment.

Reports distinguish linked, identical/different regular files, missing paths, incorrect links,
type conflicts, and manually handled templates. Extra directory files are listed separately,
not marked for deletion. `previous_deployments` lists cached deployments outside the selection;
review these before deploying. Exit `0` means inspection completed, not that no differences exist;
invalid configuration or inspection failure returns `2`. JSON includes paths and Git state
and may contain personal information; keep it local.

## Development

```sh
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv build
```

Modules are `cli`, `catalog`, `dotter`, and `inspect`. Typer provides the CLI. Helpers do not install
software or merge configs. Add components to the catalog first; add code only for reusable
mechanical operations. Keep all agent-facing documentation in concise English.

Old Brewfile and configuration source paths remain available for existing device links.
See [legacy/README.md](legacy/README.md) for migration details.
