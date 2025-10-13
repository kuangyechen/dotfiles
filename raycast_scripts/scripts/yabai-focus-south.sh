#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-focus-south
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai focus south
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

yabai -m window --focus south && echo "Yabai focused south"
