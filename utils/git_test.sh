#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") gitattributes gitconfig gitignore precommit local_gitattributes local_gitconfig local_gitinore local_repo_config local_precommit"
    exit 1
}

test -z "${1:-}" && usage
GITATTRIBUTES="${1}"
test -z "${2:-}" && usage
GITCONFIG="${2}"
test -z "${3:-}" && usage
GITIGNORE="${3}"
test -z "${4:-}" && usage
PRECOMMIT="${4}"
test -z "${5:-}" && usage
LOCAL_GITATTRIBUTES="${5}"
test -z "${6:-}" && usage
LOCAL_GITCONFIG="${6}"
test -z "${7:-}" && usage
LOCAL_GITIGNORE="${7}"
test -z "${8:-}" && usage
LOCAL_REPO_CONFIG="${8}"
test -z "${9:-}" && usage
LOCAL_PRECOMMIT="${9}"

DIFF=''

function diff_file() {
    local MODE
    MODE="$(stat -L -c '%a' "${2}")"
    echo "Diffing $(basename "${2}")"
    if ! diff "${1}" "${2}"; then
        DIFF='t'
    elif [ "${MODE}" != "${3}" ]; then
        echo "Modes differ: want ${3}, got ${MODE}"
        DIFF='t'
    else
        echo 'OK'
    fi
    echo
}

diff_file "${GITATTRIBUTES}" "${LOCAL_GITATTRIBUTES}" '600'
diff_file "${GITCONFIG}" "${LOCAL_GITCONFIG}" '600'
diff_file "${GITIGNORE}" "${LOCAL_GITIGNORE}" '600'
diff_file "${PRECOMMIT}" "${LOCAL_PRECOMMIT}" '700'

echo "Checking gitconfig setup"
if ! grep 'path = ../.gitconfig' "${LOCAL_REPO_CONFIG}" &>/dev/null; then
    echo 'Config line missing'
    DIFF='t'
else
    echo 'OK'
fi
echo

if [ -n "${DIFF}" ]; then
    echo "Found diff; 'bazel run :git_update' to fix"
    exit 1
fi

echo 'All OK'
exit 0
