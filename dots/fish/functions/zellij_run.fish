function zellij_run --description "Run command in zellij pane"
    set -l floating false
    set -l shell fish
    set -l command_args

    # Parse arguments
    for arg in $argv
        switch $arg
            case --float
                set floating true
            case --shell
                set shell $argv[2]
                set -e argv[1..2]
                break
            case '*'
                set -a command_args $arg
        end
    end

    # Build command
    set -l cmd "zellij run --name \"$command_args\""
    if test $floating = true
        set cmd "$cmd --floating"
    end

    # Add shell and command
    set cmd "$cmd -- $shell -c \"$command_args\""

    # Execute
    eval $cmd
end
