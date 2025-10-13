#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-resize-down
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai resize down
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

(yabai -m window --resize bottom:0:50 || yabai -m window --resize top:0:50) && echo "Yabai resized down"
