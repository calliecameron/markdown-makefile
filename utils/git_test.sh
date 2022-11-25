#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") docdump pdfdump zipdump gitattributes gitconfig gitignore precommit local_docdump local_pdfdump local_zipdump local_gitattributes local_gitconfig local_gitinore local_repo_config local_precommit"
    exit 1
}

test -z "${1:-}" && usage
DOCDUMP="${1}"
test -z "${2:-}" && usage
PDFDUMP="${2}"
test -z "${3:-}" && usage
ZIPDUMP="${3}"
test -z "${4:-}" && usage
GITATTRIBUTES="${4}"
test -z "${5:-}" && usage
GITCONFIG="${5}"
test -z "${6:-}" && usage
GITIGNORE="${6}"
test -z "${7:-}" && usage
PRECOMMIT="${7}"
LOCAL_DOCDUMP="${8:-}"
LOCAL_PDFDUMP="${9:-}"
LOCAL_ZIPDUMP="${10:-}"
LOCAL_GITATTRIBUTES="${11:-}"
LOCAL_GITCONFIG="${12:-}"
LOCAL_GITIGNORE="${13:-}"
LOCAL_REPO_CONFIG="${14:-}"
LOCAL_PRECOMMIT="${15:-}"

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

diff_file "${DOCDUMP}" "${LOCAL_DOCDUMP}" '700'
diff_file "${PDFDUMP}" "${LOCAL_PDFDUMP}" '700'
diff_file "${ZIPDUMP}" "${LOCAL_ZIPDUMP}" '700'
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
