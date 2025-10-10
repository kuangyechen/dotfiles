function zellij_edit --description "Open file in zellij editor"
    if test "$argv[1]" = --float
        set -l args (string join " " $argv[2..-1])
        zellij edit --floating "$args"
    else
        set -l args (string join " " $argv)
        zellij edit "$args"
    end
end
