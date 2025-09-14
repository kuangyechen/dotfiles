#!/usr/bin/env sh

set -e

original_dir=$(pwd)

cd "$(dirname "$0")"

./install_packages.py -d -y -v -p "\
        homebrew \
        uv \
        starship \
        fish \
        rust \
        rust_apps \
        fisher \
        fish_plugins \
        dotfiles \
    "

cd "$original_dir"
