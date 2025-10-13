#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-move-east
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai move east
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

yabai -m window --warp east && echo "Yabai moved east"
