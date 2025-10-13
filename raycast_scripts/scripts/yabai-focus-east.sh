#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-focus-east
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai focus east
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

yabai -m window --focus east && echo "Yabai focused east"
