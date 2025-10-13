#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-move-west
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai move west
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

yabai -m window --warp west && echo "Yabai moved west"
