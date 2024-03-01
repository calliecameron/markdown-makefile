#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") workspace_status workspace_git_update bazelversion bazelrc local_workspace_status local_bazelversion local_bazelrc"
    exit 1
}

test -z "${1:-}" && usage
WORKSPACE_STATUS="${1}"
test -z "${2:-}" && usage
WORKSPACE_GIT_UPDATE="${2}"
test -z "${3:-}" && usage
BAZELVERSION="${3}"
test -z "${4:-}" && usage
BAZELRC="${4}"
test -z "${5:-}" && usage
LOCAL_WORKSPACE_STATUS="${5}"
test -z "${6:-}" && usage
LOCAL_WORKSPACE_GIT_UPDATE="${6}"
test -z "${7:-}" && usage
LOCAL_BAZELVERSION="${7}"
test -z "${8:-}" && usage
LOCAL_BAZELRC="${8}"

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

diff_file "${WORKSPACE_STATUS}" "${LOCAL_WORKSPACE_STATUS}" '700'
diff_file "${WORKSPACE_GIT_UPDATE}" "${LOCAL_WORKSPACE_GIT_UPDATE}" '700'
diff_file "${BAZELVERSION}" "${LOCAL_BAZELVERSION}" '600'
diff_file "${BAZELRC}" "${LOCAL_BAZELRC}" '600'

if [ -n "${DIFF}" ]; then
    echo "Found diff; 'bazel run :workspace_update' to fix"
    exit 1
fi

echo 'All OK'
exit 0
