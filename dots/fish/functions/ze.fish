function ze
    set -l args (string join " " $argv)
    zellij edit "$args"
end