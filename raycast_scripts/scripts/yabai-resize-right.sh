#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-resize-right
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai resize right
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

(yabai -m window --resize right:50:0 || yabai -m window --resize left:50:0) && echo "Yabai resized right"
