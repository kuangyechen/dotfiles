#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-swap-west
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai swap west
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

yabai -m window --swap west && echo "Yabai swapped west"
