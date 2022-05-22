function log_section() {
    printf "\033[0;32m==>\033[0m\033[1m ${*}\033[0m\n"
}

function log_warning() {
    printf "\033[1mWARN\033[0m: ${*}\n"
}

function log_error() {
    printf "\033[1mERROR\033[0m: ${*}\n"
}

function safe_git_clone() {
    if [[ ! -d ${2} ]]; then
        git clone ${1} ${2}
    else
        log_warning "${2} exists, do nothing."
    fi
}
