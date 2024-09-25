#!/bin/bash

set -eu

# Package will be empty in the root package.
if [ -n "${PACKAGE}" ]; then
    GIT_DIR="${PACKAGE}/.git"
else
    GIT_DIR='.git'
fi

if [ ! -d "${GIT_DIR}" ]; then
    echo "md_git_repo must be at the root of a git repo"
    exit 1
fi

echo "Checking gitconfig setup"
if ! grep 'path = ../.gitconfig' "${GIT_DIR}/config" &>/dev/null; then
    echo 'Config line missing'
    exit 1
fi
echo 'OK'

exit 0
