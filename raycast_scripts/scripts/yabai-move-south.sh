#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-move-south
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai move south
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

yabai -m window --warp south && echo "Yabai moved south"
