#!/bin/bash

set -eu

GIT_DIR="${DST_DIR}/.git"

if [ ! -d "${GIT_DIR}" ]; then
    echo "md_git_repo must be at the root of a git repo"
    exit 1
fi

cd "${DST_DIR}"
git config --local include.path ../.gitconfig
