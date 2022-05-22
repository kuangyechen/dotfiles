function upgrade_oh_my_zsh_custom() {
    local repo
    for repo in `find ${ZSH_CUSTOM} -type d -maxdepth 2 -mindepth 2`; do
        log_section "Upgrading $(basename ${repo})"
        if [[ ! -d ${repo}/.git ]]; then
            log_warning "Directory is not a git repo, do nothing."
            continue
        fi

        local branch=$(git -C ${repo} rev-parse --abbrev-ref HEAD)
        if [[ ${branch} != "master" ]]; then
            log_warning "Repo is at branch ${branch}."
        fi

        if [[ -z $(git -C ${repo} status --porcelain) ]]; then
            git -C ${repo} pull
        else
            log_warning "Directory is not clean, do nothing."
        fi
    done
}
