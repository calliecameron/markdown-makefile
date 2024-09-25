#!/bin/bash

set -eux

function usage() {
    echo "Usage: $(basename "${0}") script"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${1}"

(
    cd "${TEST_TMPDIR}"
    mkdir a
    cd a
    git init .
)

# In repo; success
DST_DIR="${TEST_TMPDIR}/a" "${SCRIPT}"
grep 'path = ../.gitconfig' "${TEST_TMPDIR}/a/.git/config" >/dev/null

# Not in repo; failure
DST_DIR="${TEST_TMPDIR}" "${SCRIPT}" && exit 1

exit 0
