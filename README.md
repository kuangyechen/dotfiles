# Dotfiles

## Quick Start

- Clone the repo (if needed) and `cd` into it.
- Run the OS helper script from the repo root:
    - macOS: `./install_packages_mac.sh`
    - Ubuntu Server: `./install_packages_ubuntu_server.sh`
- Both helpers run with `-d` (dry-run); drop it to apply changes.
- Use `./install_packages.py -y -v -p "homebrew uv` from the repo root.

## Dotter `local.toml`

- Dotter reads `.dotter/local.toml` to decide which package groups to link.
- macOS default: `cp .dotter/mac.template.toml .dotter/local.toml`
- Linux default: `cp .dotter/linux.template.toml .dotter/local.toml`
- Edit the `packages = [...]` array to include the bundles you want
- (see `.dotter/global.toml` for the module names).
