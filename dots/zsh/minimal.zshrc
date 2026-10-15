# Compatibility shell. Fish is the primary interactive environment.
typeset -U path PATH
for directory in "$HOME/.local/bin" "$HOME/.cargo/bin" /opt/homebrew/bin /usr/local/bin; do
    [[ -d "$directory" ]] && path=("$directory" $path)
done
unset directory

HISTFILE="$HOME/.zsh_history"
HISTSIZE=10000
SAVEHIST=10000
setopt APPEND_HISTORY HIST_IGNORE_DUPS

if [[ -o interactive ]]; then
    autoload -Uz compinit
    compinit
    bindkey -e
    if (( $+commands[hx] )); then
        export EDITOR=hx
    elif (( $+commands[vim] )); then
        export EDITOR=vim
    else
        export EDITOR=vi
    fi
    (( $+commands[starship] )) && eval "$(starship init zsh)"
    (( $+commands[zoxide] )) && eval "$(zoxide init zsh)"
fi

# Last, so machine-specific choices can override shared defaults.
if [[ -f "$HOME/.config/local_env" ]]; then
    source "$HOME/.config/local_env"
fi
if [[ -f "$HOME/.config/zsh/local.zsh" ]]; then
    source "$HOME/.config/zsh/local.zsh"
fi
