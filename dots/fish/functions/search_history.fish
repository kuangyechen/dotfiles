function search_history
    # Using sk to search through the command history
    set target (history | sk --query "$argv" --prompt "History > ")

    # Check if a command was selected
    if test -n "$target"
        # Set the selected command to the command line
        commandline -r $target
    end
end
