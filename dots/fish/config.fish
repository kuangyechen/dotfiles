# Local bin
fish_add_path {$HOME}/.local/bin
# Rust
fish_add_path {$HOME}/.cargo/bin
# Docker
fish_add_path -a {$HOME}/.docker/bin
# Foundry
fish_add_path -a {$HOME}/.foundry/bin
# Rye
set -Ua fish_user_paths "$HOME/.rye/shims"

if status is-interactive
    # Commands to run in interactive sessions can go here

    # Utility functions
    function command_exists
        command -v $argv[1] >/dev/null 2>&1
    end

    # Starship
    if command_exists starship
        starship init fish | source
    end

    # Zoxide
    if command_exists zoxide
        zoxide init fish | source
    end

    # Eza
    if command_exists eza
        # general use aliases

        # just replace ls by eza and allow all other eza arguments
        abbr --add ls eza
        # list, size, type, git
        abbr --add l eza -lbF --git
        # long, all
        abbr --add ll eza -lbGF --git
        # list, long, sort by modification date
        abbr --add llm eza -lbGd --git --sort=modified
        # all list
        abbr --add la eza -lbhHigUmuSa --time-style=long-iso --git --color-scale
        # all list and extended
        abbr --add lx eza -lbhHigUmuSa@ --time-style=long-iso --git --color-scale
        # tree view
        abbr --add tree eza --tree
        # one column by just names
        abbr --add lS eza -1
        # tree level 2
        abbr --add lt eza --tree --level=2
    end

    # rm2trash
    if command_exists rm2trash
        abbr --add rm rm2trash rm
        abbr --add ls_trash rm2trash ls
        abbr --add cd_trash cd $(rm2trash trash-path)
        abbr --add empty_trash rm2trash empty
    end

    # Bat
    if command_exists bat
        set -l CAT bat
        abbr --add cat bat
    else
        set -l CAT cat
    end

    # Alias
    abbr --add cat_fish_config {$CAT} {$HOME}/.config/fish/config.fish
    abbr --add cat_fish_variable {$CAT} {$HOME}/.config/fish/fish_variables

    # Environments
    set -g fish_key_bindings fish_vi_key_bindings
    set -g fish_greeting
    set -g SSH_KEY_PATH {$HOME}/.ssh/id_ed25519

    if command_exists hx
        set -g EDITOR hx
    else if command_exists vim
        set -g EDITOR vim
    else
        set -g EDITOR vi
    end

end
