#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") contents_build contents_bzl contents_update summary publications local_contents_build local_contents_bzl local_contents_update local_summary local_publications"
    exit 1
}

test -z "${1:-}" && usage
CONTENTS_BUILD="${1}"
test -z "${2:-}" && usage
CONTENTS_BZL="${2}"
test -z "${3:-}" && usage
CONTENTS_UPDATE="${3}"
test -z "${4:-}" && usage
SUMMARY="${4}"
test -z "${5:-}" && usage
PUBLICATIONS="${5}"
test -z "${6:-}" && usage
LOCAL_CONTENTS_BUILD="${6}"
test -z "${7:-}" && usage
LOCAL_CONTENTS_BZL="${7}"
test -z "${8:-}" && usage
LOCAL_CONTENTS_UPDATE="${8}"
test -z "${9:-}" && usage
LOCAL_SUMMARY="${9}"
test -z "${10:-}" && usage
LOCAL_PUBLICATIONS="${10}"

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

function diff_mode_only() {
    local MODE
    MODE="$(stat -L -c '%a' "${2}")"
    echo "Diffing $(basename "${2}")"
    if [ "${MODE}" != "${3}" ]; then
        echo "Modes differ: want ${3}, got ${MODE}"
        DIFF='t'
    else
        echo 'OK'
    fi
    echo
}

diff_file "${CONTENTS_BUILD}" "${LOCAL_CONTENTS_BUILD}" '600'
diff_mode_only "${CONTENTS_BZL}" "${LOCAL_CONTENTS_BZL}" '600'
diff_file "${CONTENTS_UPDATE}" "${LOCAL_CONTENTS_UPDATE}" '700'
diff_file "${SUMMARY}" "${LOCAL_SUMMARY}" '700'
diff_file "${PUBLICATIONS}" "${LOCAL_PUBLICATIONS}" '700'

if [ -n "${DIFF}" ]; then
    echo "Found diff; 'bazel run :dynamic_group_update' to fix"
    exit 1
fi

echo 'All OK'
exit 0
