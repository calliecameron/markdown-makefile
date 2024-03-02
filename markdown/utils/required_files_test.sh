#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") updater [src dst dst_mode]..."
    exit 1
}

test -z "${1:-}" && usage
UPDATER="${1}"
shift

if [ -z "${1:-}" ]; then
    echo 'No files specified'
    exit 1
fi

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

while (($#)); do
    test -z "${1:-}" && usage
    test -e "${1}" || usage
    SRC="${1}"
    if [ -z "${2:-}" ]; then
        echo "A required file is missing, run 'bazel run ${UPDATER}' to create it"
        exit 1
    fi
    test -e "${2}" || usage
    DST="${2}"
    test -z "${3:-}" && usage
    DST_MODE="${3}"

    diff_file "${SRC}" "${DST}" "${DST_MODE}"
    shift 3
done

if [ -n "${DIFF}" ]; then
    echo "Found diff; 'bazel run ${UPDATER}' to fix"
    exit 1
fi

echo 'All OK'
exit 0
