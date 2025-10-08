# Local bin
fish_add_path {$HOME}/.local/bin
fish_add_path /usr/local/sbin
fish_add_path /opt/homebrew/bin
# Rust
fish_add_path {$HOME}/.cargo/bin
# Docker
fish_add_path -a {$HOME}/.docker/bin
# Foundry
fish_add_path -a {$HOME}/.foundry/bin

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

    # Rip
    if command_exists rip
        abbr --add unrip rip --unbury
        abbr --add ls_trash rip --seance
        abbr --add empty_trash rip --decompose
    end

    # Bat
    if command_exists bat
        set -g FIELD_CAT_BIN bat
        abbr --add cat bat
    else
        set -g FIELD_CAT_BIN cat
    end

    # Environments
    set -g fish_config {$HOME}/.config/fish/config.fish
    set -g fish_variables {$HOME}/.config/fish/fish_variables
    set -g fish_key_bindings fish_vi_key_bindings
    set -g fish_greeting "Fish customized by Field."
    set -gx SSH_KEY_PATH {$HOME}/.ssh/id_ed25519
    set -gx LANG en_US.UTF-8

    # Alias
    abbr --add cat_fish_config {$FIELD_CAT_BIN} {$fish_config}
    abbr --add cat_fish_variable {$FIELD_CAT_BIN} {$fish_variables}

    if command_exists hx
        set -gx EDITOR hx
    else if command_exists vim
        set -gx EDITOR vim
    else
        set -gx EDITOR vi
    end

end
