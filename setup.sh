#!/bin/sh
# Shell script to clone subprojects and set up Python virtual environments

REPOS="\
  TruCtrl-API=https://github.com/YourOrg/TruCtrl-API.git \
  TruCtrl-App=https://github.com/YourOrg/TruCtrl-App.git \
  TruCtrl-Docs=https://github.com/YourOrg/TruCtrl-Docs.git \
  TruCtrl-Web=https://github.com/YourOrg/TruCtrl-Web.git \
"

for entry in $REPOS; do
  NAME=$(echo $entry | cut -d= -f1)
  URL=$(echo $entry | cut -d= -f2)
  if [ ! -d "$NAME" ]; then
    git clone "$URL"
  fi
  if [ -f "$NAME/requirements.txt" ]; then
    if [ ! -d "$NAME/.venv" ]; then
      python3 -m venv "$NAME/.venv"
    fi
    "$NAME/.venv/bin/pip" install -r "$NAME/requirements.txt"
  fi
done

echo "All subprojects cloned and Python environments set up."
