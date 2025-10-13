#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-focus-north
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai focus north
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

yabai -m window --focus north && echo "Yabai focused north"
