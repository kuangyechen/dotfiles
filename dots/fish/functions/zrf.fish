function zrf
    set -l args (string join " " $argv)
    zellij run --name "$args" --floating -- zsh -ic "$args"
end