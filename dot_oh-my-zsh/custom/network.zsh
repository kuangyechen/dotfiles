function set_http_proxy() {
    export https_proxy=${1}
    export http_proxy=${1}
    printf "Set HTTP Proxy: ${http_proxy}\n"
    printf "Set HTTPS Proxy: ${https_proxy}\n"
}

function set_socks_proxy() {
    export all_proxy=${1}
    printf "Set Socks Proxy: ${all_proxy}\n"
}

function set_proxy() {
    set_http_proxy ${1}
    set_socks_proxy ${1}
}

function unset_http_proxy() {
    unset http_proxy
    unset https_proxy
    printf "HTTP proxy unset.\n"
}

function unset_socks_proxy() {
    unset all_proxy
    printf "Socks proxy unset.\n"
}

function unset_proxy() {
    printf "Unset all proxy.\n"
    unset_http_proxy
    unset_socks_proxy
}
