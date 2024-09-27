#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") file1 file2 tool [tool_helpers...]"
    exit 1
}

test -z "${1:-}" && usage
FILE1="${1}"
test -z "${2:-}" && usage
FILE2="${2}"
test -z "${3:-}" && usage
TOOL="${3}"

if cmp "${FILE1}" "${FILE2}" &>/dev/null; then
    # If the files are identical, we don't need to run 'tool', which can be
    # slow.
    exit 0
fi

"${TOOL}" "${@:4}" "$(readlink -f "${FILE1}")" >"${TEST_TMPDIR}/file1"
"${TOOL}" "${@:4}" "$(readlink -f "${FILE2}")" >"${TEST_TMPDIR}/file2"

diff -a "${TEST_TMPDIR}/file1" "${TEST_TMPDIR}/file2"
