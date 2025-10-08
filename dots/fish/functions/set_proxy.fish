function set_proxy --description 'Set HTTP and SOCKS proxy for terminal'
    # Initialize variables
    set -l proxy_host
    set -l http_port
    set -l socks_port
    set -l action set

    # Parse arguments
    for i in (seq (count $argv))
        switch $argv[$i]
            case -h --host
                if test $i -lt (count $argv)
                    set proxy_host $argv[(math $i + 1)]
                end
            case -p --port
                if test $i -lt (count $argv)
                    set http_port $argv[(math $i + 1)]
                end
            case -s --socks-port
                if test $i -lt (count $argv)
                    set socks_port $argv[(math $i + 1)]
                end
            case -u --unset
                set action unset
            case -c --clear
                set action clear
            case -h --help
                echo "Usage: set_proxy [OPTIONS]"
                echo ""
                echo "Options:"
                echo "  -h, --host HOST        Proxy host (required for set)"
                echo "  -p, --port PORT        HTTP proxy port (required for set)"
                echo "  -s, --socks-port PORT  SOCKS proxy port (required for set)"
                echo "  -u, --unset           Unset proxy variables"
                echo "  -c, --clear           Clear proxy variables"
                echo "  --help                Show this help message"
                echo ""
                echo "Examples:"
                echo "  set_proxy -h 127.0.0.1 -p 8080 -s 1080  # Set proxy"
                echo "  set_proxy -h 192.168.1.100 -p 3128 -s 1081  # Custom settings"
                echo "  set_proxy --unset                   # Unset proxy"
                echo "  set_proxy --clear                   # Clear proxy"
                return 0
        end
    end

    # Validate required arguments for set action
    if test $action = set
        if test -z "$proxy_host" -o -z "$http_port" -o -z "$socks_port"
            echo "❌ Error: All proxy settings are required when setting proxy"
            echo "Usage: set_proxy -h HOST -p HTTP_PORT -s SOCKS_PORT"
            echo "Example: set_proxy -h 127.0.0.1 -p 8080 -s 1080"
            return 1
        end
    end

    # Set proxy URLs
    set -l http_proxy_url "http://$proxy_host:$http_port"
    set -l https_proxy_url "http://$proxy_host:$http_port"
    set -l socks_proxy_url "socks5://$proxy_host:$socks_port"

    switch $action
        case set
            # Set HTTP proxy environment variables
            set -gx http_proxy $http_proxy_url
            set -gx https_proxy $https_proxy_url
            set -gx HTTP_PROXY $http_proxy_url
            set -gx HTTPS_PROXY $https_proxy_url

            # Set SOCKS proxy environment variables
            set -gx all_proxy $socks_proxy_url
            set -gx ALL_PROXY $socks_proxy_url

            # Set no_proxy for local addresses
            set -gx no_proxy "localhost,127.0.0.1,::1"
            set -gx NO_PROXY "localhost,127.0.0.1,::1"

            echo "✅ Proxy settings applied:"
            echo "  HTTP/HTTPS: $http_proxy_url"
            echo "  SOCKS5: $socks_proxy_url"
            echo "  No proxy: localhost,127.0.0.1,::1"

        case unset
            # Unset proxy environment variables
            set -e http_proxy
            set -e https_proxy
            set -e HTTP_PROXY
            set -e HTTPS_PROXY
            set -e all_proxy
            set -e ALL_PROXY
            set -e no_proxy
            set -e NO_PROXY

            echo "✅ Proxy settings unset"

        case clear
            # Clear proxy environment variables
            set -e http_proxy
            set -e https_proxy
            set -e HTTP_PROXY
            set -e HTTPS_PROXY
            set -e all_proxy
            set -e ALL_PROXY
            set -e no_proxy
            set -e NO_PROXY

            echo "✅ Proxy settings cleared"
    end
end
