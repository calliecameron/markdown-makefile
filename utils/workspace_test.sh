#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") workspace_status workspace_summary local_workspace_status local_workspace_summary"
    exit 1
}

test -z "${1:-}" && usage
WORKSPACE_STATUS="${1}"
test -z "${2:-}" && usage
WORKSPACE_SUMMARY="${2}"
test -z "${3:-}" && usage
LOCAL_WORKSPACE_STATUS="${3}"
test -z "${4:-}" && usage
LOCAL_WORKSPACE_SUMMARY="${4}"

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
diff_file "${WORKSPACE_SUMMARY}" "${LOCAL_WORKSPACE_SUMMARY}" '700'

if [ -n "${DIFF}" ]; then
    echo "Found diff; 'bazel run :workspace_update' to fix"
    exit 1
fi

echo 'All OK'
exit 0
