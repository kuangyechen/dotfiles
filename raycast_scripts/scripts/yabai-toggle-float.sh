#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-toggle-float
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai swap west
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

yabai -m window --toggle float && echo "Yabai toggled float"
yabai -m window --grid 4:4:1:1:2:2 >/dev/null 2>&1 || true
