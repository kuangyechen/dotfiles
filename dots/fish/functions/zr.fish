function zr
    set -l args (string join " " $argv)
    zellij run --name "$args" -- zsh -ic "$args"
end