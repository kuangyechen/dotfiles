# Utility functions
function command_exists
    command -v $argv[1] >/dev/null 2>&1
end

# Local bin
fish_add_path {$HOME}/.local/bin
# Rust
fish_add_path {$HOME}/.cargo/bin
# Docker
fish_add_path -a {$HOME}/.docker/bin
# Foundry
fish_add_path -a {$HOME}/.foundry/bin
# Rye
if command_exists rye
    set -Ua fish_user_paths "$HOME/.rye/shims"
end

if status is-interactive
    # Commands to run in interactive sessions can go here

    # Starship
    if command_exists starship
        starship init fish | source
    end

    # Zoxide
    if command_exists zoxide
        zoxide init fish | source
    end

    # eza
    if command_exists eza
        # general use aliases
        alias ls='eza'                                  # just replace ls by eza and allow all other eza arguments
        alias l='eza -lbF --git'                        # list, size, type, git
        alias ll='eza -lbGF --git'                      # long, all
        alias llm='eza -lbGd --git --sort=modified'     # list, long, sort by modification date
        alias la='eza -lbhHigUmuSa --time-style=long-iso --git --color-scale'      # all list
        alias lx='eza -lbhHigUmuSa@ --time-style=long-iso --git --color-scale'     # all list and extended
        alias tree='eza --tree'                         # tree view
        alias lS='eza -1'                               # one column by just names
        alias lt='eza --tree --level=2'                 # tree level 2
    end

    # rm2trash
    if command_exists rm2trash
        alias rm='rm2trash rm'
        alias ls_trash='rm2trash ls'
        alias cd_trash='cd $(rm2trash trash-path)'
        alias empty_trash='rm2trash empty'
    end

    # Zellij
    if command_exists zellij
        function zr
            set -l args (string join " " $argv)
            zellij run --name "$args" -- zsh -ic "$args"
        end
        function zrf
            set -l args (string join " " $argv)
            zellij run --name "$args" --floating -- zsh -ic "$args"
        end
        function ze
            set -l args (string join " " $argv)
            zellij edit "$args"
        end
        function zef
            set -l args (string join " " $argv)
            zellij edit --floating "$args"
        end
    end

    # Bat
    if command_exists bat
        alias cat bat
    end

    # Common alias
    alias cat_fish_config='cat {$HOME}/.config/fish/config.fish'

    # Environments
    set -g fish_key_bindings fish_vi_key_bindings
end
