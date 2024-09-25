#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") script"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="$(readlink -f "${1}")"

(
    cd "${TEST_TMPDIR}"
    mkdir -p a/a
    cd a/a
    git init .
)

cd "${TEST_TMPDIR}/a"

# Not in root of repo
PACKAGE='' "${SCRIPT}" && exit 1

# In root of repo, but no config line
PACKAGE='a' "${SCRIPT}" && exit 1

# In root of repo, with config line
echo 'path = ../.gitconfig' >>"${TEST_TMPDIR}/a/a/.git/config"
PACKAGE='a' "${SCRIPT}"

exit 0
