#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") docdump pdfdump zipdump gitattributes gitconfig gitignore local_docdump local_pdfdump local_zipdump local_gitattributes local_gitconfig local_gitinore local_repo_config"
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
LOCAL_DOCDUMP="${7:-}"
LOCAL_PDFDUMP="${8:-}"
LOCAL_ZIPDUMP="${9:-}"
LOCAL_GITATTRIBUTES="${10:-}"
LOCAL_GITCONFIG="${11:-}"
LOCAL_GITIGNORE="${12:-}"
LOCAL_REPO_CONFIG="${13:-}"

DIFF=''

function diff_file() {
    echo "Diffing $(basename "${2}")"
    if ! diff "${1}" "${2}"; then
        DIFF='t'
    else
        echo 'OK'
    fi
    echo
}

diff_file "${DOCDUMP}" "${LOCAL_DOCDUMP}"
diff_file "${PDFDUMP}" "${LOCAL_PDFDUMP}"
diff_file "${ZIPDUMP}" "${LOCAL_ZIPDUMP}"
diff_file "${GITATTRIBUTES}" "${LOCAL_GITATTRIBUTES}"
diff_file "${GITCONFIG}" "${LOCAL_GITCONFIG}"
diff_file "${GITIGNORE}" "${LOCAL_GITIGNORE}"

echo "Checking gitconfig setup"
if ! grep 'path = ../.gitconfig' "${LOCAL_REPO_CONFIG}" &>/dev/null; then
    echo 'Config line missing'
    DIFF='t'
else
    echo 'OK'
fi
echo

if [ -n "${DIFF}" ]; then
    echo 'Found diff'
    exit 1
fi

echo 'All OK'
exit 0
