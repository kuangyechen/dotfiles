#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-focus-west
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai focus west
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

yabai -m window --focus west && echo "Yabai focused west"
