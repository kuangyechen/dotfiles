#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-move-north
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai move north
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

yabai -m window --warp north && echo "Yabai moved north"
