function set_proxy --description 'Set HTTP and/or SOCKS proxy for terminal'
    set -l http_proxy
    set -l socks_proxy
    set -l clear_mode false

    # Parse arguments
    for i in (seq (count $argv))
        switch $argv[$i]
            case --http
                if test $i -lt (count $argv)
                    set http_proxy $argv[(math $i + 1)]
                end
            case --socks
                if test $i -lt (count $argv)
                    set socks_proxy $argv[(math $i + 1)]
                end
            case --clear
                set clear_mode true
        end
    end

    if test $clear_mode = true
        # Clear all proxy environment variables
        set -e http_proxy https_proxy HTTP_PROXY HTTPS_PROXY
        set -e all_proxy ALL_PROXY no_proxy NO_PROXY
        echo "✅ Proxy settings cleared"
        return 0
    end

    # Set HTTP proxy
    if test -n "$http_proxy"
        set -gx http_proxy "http://$http_proxy"
        set -gx https_proxy "http://$http_proxy"
        set -gx HTTP_PROXY "http://$http_proxy"
        set -gx HTTPS_PROXY "http://$http_proxy"
        echo "✅ HTTP proxy set: http://$http_proxy"
    end

    # Set SOCKS proxy
    if test -n "$socks_proxy"
        set -gx all_proxy "socks5://$socks_proxy"
        set -gx ALL_PROXY "socks5://$socks_proxy"
        echo "✅ SOCKS proxy set: socks5://$socks_proxy"
    end

    # Set no_proxy for local addresses
    set -gx no_proxy "localhost,127.0.0.1,::1"
    set -gx NO_PROXY "localhost,127.0.0.1,::1"
end
