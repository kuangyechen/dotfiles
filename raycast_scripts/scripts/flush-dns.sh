#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title Flush DNS
# @raycast.mode silent
# @raycast.packageName System Utils

# Optional parameters:
# @raycast.icon 💨

# Documentation:
# @raycast.description Flush DNS cache
# @raycast.author Felipe Turcheti
# @raycast.authorURL https://felipeturcheti.com

set -e

# Raycast has no terminal for sudo; use the macOS authorization dialog.
/usr/bin/osascript -e 'do shell script "/usr/bin/dscacheutil -flushcache && /usr/bin/killall -HUP mDNSResponder" with administrator privileges'
echo "DNS cache flushed"
