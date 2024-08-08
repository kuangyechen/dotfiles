function zef
    set -l args (string join " " $argv)
    zellij edit --floating "$args"
end