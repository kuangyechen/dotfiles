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
