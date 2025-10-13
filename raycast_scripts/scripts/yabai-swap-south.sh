#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-swap-south
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai swap south
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

yabai -m window --swap south && echo "Yabai swapped south"
