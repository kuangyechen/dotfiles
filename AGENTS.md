# Agent instructions

Use the workflow matching the user's task:

- Set up or repair this device: read `workflows/setup.md`.
- Capture local configuration or software choices: read `workflows/sync.md`.
- Change repository code or docs: develop directly; do not run device setup or deployment.

## Sources of truth

- `catalog.toml`: component purposes, platforms, installation guidance, profiles, and Dotter groups.
- `.dotter/`: the only source of configuration path mappings. Do not duplicate them in code or docs.
- `dots/`: shared configuration; `dots/private-dotfiles/`: personal configuration submodule.
- `src/dotfiles_tools/`: mechanical helpers. The agent handles installation, choices, and merging.
- `legacy/`: reference only. Do not run its installers or import them into the new package.
- `raycast_scripts/`: independent project, not a member of the root uv workspace.

## Working rules

- Write all agent-facing instructions, workflows, and documentation in concise English.
- Inspect root and submodule changes first. Preserve user work; never reset, checkout, or blanket-copy away differences.
- Use `uv run dots profile ...` to preview selections and `uv run dots inspect --json` to inspect state.
- Complete routine steps continuously. Ask only for missing intent or unresolved conflict choices.
- Compare and back up before deploying. Dotter's `--force` overrides `--dry-run`; never combine them or force deployment indiscriminately.
- Keep keys, tokens, authentication state, and shell history device-local, outside mappings, report contents, and commits.
- Keep Codex configuration device-local too. Never link, deploy, or sync it from this repository or its private submodule.
- Store local selections, backups, and reports in `.local/` or ignored Dotter local files.
- Record lasting software needs. Do not replace the catalog with a machine package dump or add dependencies to defaults automatically.
- Sync produces local diffs by default. Commit or push only when requested.
- Record installation or permission blockers, continue independent steps, and do not report skipped requirements as complete.

## Development and validation

- Use uv with pinned Python 3.12.15; use Pydantic for models and validation, not dataclasses.
- Use Typer for the CLI and `typer.testing.CliRunner` for entry-point tests, not argparse.
- Support repository discovery from subdirectories; use `--repo` and `inspect --home` for temporary fixtures.
- Use pytest; run `uv run pytest` after helper changes.
- Use Ruff: `uv run ruff check .` and `uv run ruff format --check .`.
- Use Loguru when logging is needed. Current direct command output needs no logging dependency.
- After packaging changes, run `uv build`; verify artifacts exclude legacy files, configuration payloads, and private submodules.
- Test Dotter deployment with a temporary HOME and isolated cache, never the current user's HOME.
- Distinguish automated tests, local smoke tests, and untested platforms in validation reports.
