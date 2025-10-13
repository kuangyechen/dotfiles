#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title yabai-maximize
# @raycast.mode silent

# Optional parameters:
# @raycast.icon 🤖
# @raycast.packageName Yabai

# Documentation:
# @raycast.description Yabai move east
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

yabai -m window --grid 1:1:0:0:1:1 && echo "Yabai maximized"
