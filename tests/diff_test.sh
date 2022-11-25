#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") file1 file2 tool"
    exit 1
}

test -z "${1:-}" && usage
FILE1="${1}"
test -z "${2:-}" && usage
FILE2="${2}"
test -z "${3:-}" && usage
TOOL="${3}"

"${TOOL}" "${FILE1}" >"${TEST_TMPDIR}/file1"
"${TOOL}" "${FILE2}" >"${TEST_TMPDIR}/file2"

diff "${TEST_TMPDIR}/file1" "${TEST_TMPDIR}/file2"
