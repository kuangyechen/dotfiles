#!/bin/bash

# Required parameters:
# @raycast.schemaVersion 1
# @raycast.title list-git-config
# @raycast.mode fullOutput

# Optional parameters:
# @raycast.icon 💻
# @raycast.packageName System Utils

# Documentation:
# @raycast.description List global git config
# @raycast.author KuangyeChen
# @raycast.authorURL https://raycast.com/KuangyeChen

git config --global --list
