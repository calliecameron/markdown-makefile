#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") bindump docdump pdfdump zipdump gitattributes gitconfig gitignore precommit local_bindump local_docdump local_pdfdump local_zipdump local_gitattributes local_gitconfig local_gitinore local_repo_config local_precommit"
    exit 1
}

test -z "${1:-}" && usage
BINDUMP="${1}"
test -z "${2:-}" && usage
DOCDUMP="${2}"
test -z "${3:-}" && usage
PDFDUMP="${3}"
test -z "${4:-}" && usage
ZIPDUMP="${4}"
test -z "${5:-}" && usage
GITATTRIBUTES="${5}"
test -z "${6:-}" && usage
GITCONFIG="${6}"
test -z "${7:-}" && usage
GITIGNORE="${7}"
test -z "${8:-}" && usage
PRECOMMIT="${8}"
test -z "${9:-}" && usage
LOCAL_BINDUMP="${9}"
test -z "${10:-}" && usage
LOCAL_DOCDUMP="${10}"
test -z "${11:-}" && usage
LOCAL_PDFDUMP="${11}"
test -z "${12:-}" && usage
LOCAL_ZIPDUMP="${12}"
test -z "${13:-}" && usage
LOCAL_GITATTRIBUTES="${13}"
test -z "${14:-}" && usage
LOCAL_GITCONFIG="${14}"
test -z "${15:-}" && usage
LOCAL_GITIGNORE="${15}"
test -z "${16:-}" && usage
LOCAL_REPO_CONFIG="${16}"
test -z "${17:-}" && usage
LOCAL_PRECOMMIT="${17}"

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

diff_file "${BINDUMP}" "${LOCAL_BINDUMP}" '700'
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
