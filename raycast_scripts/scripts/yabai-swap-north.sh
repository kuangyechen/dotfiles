#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-swap-north
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai swap north
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

yabai -m window --swap north && echo "Yabai swapped north"
