# If you come from bash you might have to change your $PATH.
export PATH="$HOME/.local/bin:$PATH:/usr/local/sbin"
# Rust
export PATH=${HOME}/.cargo/bin:${PATH}

if [[ ${OSTYPE} == linux-gnu ]]; then
    # Pyenv
    export PYENV_ROOT="${HOME}/.pyenv"
    export PATH="${PYENV_ROOT}/bin:${PATH}"

    # Solana
    export PATH=${HOME}/.local/share/solana/install/active_release/bin:${PATH}
fi


# Path to your oh-my-zsh installation.
export ZSH=${HOME}/.oh-my-zsh

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="powerlevel10k/powerlevel10k"
# To customize prompt, run `p10k configure` or edit ~/.p10k.zsh.
[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh

# Set list of themes to load
# Setting this variable when ZSH_THEME=random
# cause zsh load theme from this variable instead of
# looking in ~/.oh-my-zsh/themes/
# An empty array have no effect
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"

# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# The optional three formats: "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
    common-aliases
    pip
    sudo
    zsh-vi-mode
    zsh-autosuggestions
    zsh-syntax-highlighting
)

# Git
if [[ $(command -v git) ]]; then
    plugins+=(
        git
    )
fi

# Poetry
if [[ $(command -v poetry) ]]; then
    plugins+=(
        poetry
    )
fi

# Docker
if [[ $(command -v docker) ]]; then
    plugins+=(
        docker
    )
fi

# Tmux
if [[ $(command -v tmux) ]]; then
    plugins+=(
        tmux
    )
fi

# Macos
if [[ ${OSTYPE} == darwin* ]]; then
    plugins+=(
        macos
    )
fi

# Rust
if [[ $(command -v rustc) ]]; then
    plugins+=(
        rust
    )
fi

source ${ZSH}/oh-my-zsh.sh

# User configuration

# Manpage
export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
export LANG=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n ${SSH_CONNECTION} ]]; then
#     export EDITOR='vim'
# else
#     export EDITOR='vim'
# fi
if [[ $(command -v hx) ]]; then
    export EDITOR="hx"
elif [[ $(command -v vim) ]]; then
    export EDITOR="vim"
else
    export EDITOR="vi"
fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
export SSH_KEY_PATH="${HOME}/.ssh/id_ed25519"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
# show_size
alias show_size='du -sh'

# exa
if [[ $(command -v exa) ]]; then
    # general use aliases
    alias ls='exa'                                  # just replace ls by exa and allow all other exa arguments
    alias l='exa -lbF --git'                        # list, size, type, git
    alias ll='exa -lbGF --git'                      # long, all
    alias llm='exa -lbGd --git --sort=modified'     # list, long, sort by modification date
    alias la='exa -lbhHigUmuSa --time-style=long-iso --git --color-scale'      # all list
    alias lx='exa -lbhHigUmuSa@ --time-style=long-iso --git --color-scale'     # all list and extended
    alias tree='exa --tree'                         # tree view
    alias lS='exa -1'                               # one column by just names
    alias lt='exa --tree --level=2'                 # tree level 2
fi

# rm2trash
if [[ $(command -v rm2trash) ]]; then
    alias rm='rm2trash rm'
    alias ls_trash='rm2trash ls'
    alias cd_trash='cd $(rm2trash trash-path)'
    alias empty_trash='rm2trash empty'
fi

# Pyenv
if [[ $(command -v pyenv) ]]; then
    # Lazy init
    export PATH="${PYENV_ROOT}/bin:${PYENV_ROOT}/shims:${PATH}"
    function pyenv() {
        unset -f pyenv
        eval "$(command pyenv init -)"
        eval "$(command pyenv virtualenv-init -)"
        pyenv $@
    }
fi

# Pipx
# Use a pyenv python installation as default
if [[ $(command -v pipx) ]]; then
    export PIPX_DEFAULT_PYTHON_PYENV_VERSION="3.10.9"
    export PIPX_DEFAULT_PYTHON="${HOME}/.pyenv/versions/${PIPX_DEFAULT_PYTHON_PYENV_VERSION}/bin/python"
    if [[ ! $(command -v ${PIPX_DEFAULT_PYTHON}) ]]; then
        echo "Install python for pipx, with pyenv: pyenv install ${PIPX_DEFAULT_PYTHON_PYENV_VERSION}"
    fi
fi

# Zoxide
if [[ $(command -v zoxide) ]]; then
    eval "$(zoxide init zsh)"
fi

# Zellij
if [[ $(command -v zellij) ]]; then
    function zr () { zellij run --name "$*" -- zsh -ic "$*";}
    function zrf () { zellij run --name "$*" --floating -- zsh -ic "$*";}
    function ze () { zellij edit "$*";}
    function zef () { zellij edit --floating "$*";}
fi
