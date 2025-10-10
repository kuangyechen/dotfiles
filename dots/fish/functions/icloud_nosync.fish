function icloud_nosync --description 'Add nosync attribute to file or folder to prevent iCloud syncing'
    # Check if running on macOS
    if not test (uname) = Darwin
        echo "Error: icloud_nosync only works on macOS"
        return 1
    end

    if test (count $argv) -eq 0
        echo "Usage: icloud_nosync <file_or_folder>"
        echo "Example: icloud_nosync node_modules"
        return 1
    end

    for item in $argv
        if test -e "$item"
            xattr -w 'com.apple.fileprovider.ignore#P' 1 "$item"
            echo "Added nosync attribute to: $item"
        else
            echo "Error: '$item' does not exist"
            return 1
        end
    end
end
