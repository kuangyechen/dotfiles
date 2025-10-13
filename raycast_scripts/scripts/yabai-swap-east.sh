#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-swap-east
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai swap east
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

yabai -m window --swap east && echo "Yabai swapped east"
