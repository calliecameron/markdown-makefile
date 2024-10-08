#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") strip_nondeterminism in_file out_file"
    exit 1
}

test -z "${1:-}" && usage
STRIP_NONDETERMINISM="${1}"
test -z "${2:-}" && usage
IN_FILE="${2}"
test -x "${3:-}" && usage
OUT_FILE="${3}"

cp "${IN_FILE}" "${OUT_FILE}"
"${STRIP_NONDETERMINISM}" -t zip "${OUT_FILE}"
