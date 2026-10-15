# Historical implementations

`installer/` contains the retired Python installer (`dotspy`) and its shell
entry points. `mackup/` contains the previous configuration snapshots.

These files are archived for reference. Their original relative paths and
installation assumptions are not maintained; do not run them for setup.
The active entry point is the root `AGENTS.md`, with procedures in `workflows/`.
The new Python package never imports this directory.

The old `dots/homebrew/Brewfile` remains at its original path because an existing
`~/.Brewfile` may still link to it. It is a frozen snapshot, not an installation
source. Software choices now live in `catalog.toml`.

Existing source files such as `dots/zsh/zshrc`, `dots/fish/config.fish`, and
`dots/git/gitconfig` also keep their paths so current home-directory links keep
working. New default mappings use portable alternatives. Switching mappings is
an explicit setup operation, preceded by a Dotter dry run.

An existing local selection may therefore report `foreign-link` before its first
migration: the link still points at a preserved old source. Compare the old
deployment cache and the source diff before choosing the new mapping. The full
old Zsh environment is now the optional `oh-my-zsh` component; personal Zed
settings use `zed-private` instead of the shared `zed` component.
