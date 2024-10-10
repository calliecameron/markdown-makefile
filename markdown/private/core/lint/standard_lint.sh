#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") markdownlint config in_file out_file"
    exit 1
}

test -z "${1:-}" && usage
MARKDOWNLINT="${1}"
test -z "${2:-}" && usage
CONFIG="${2}"
test -z "${3:-}" && usage
IN_FILE="${3}"
test -z "${4:-}" && usage
OUT_FILE="${4}"

"${MARKDOWNLINT}" --config "${CONFIG}" "${IN_FILE}"

echo 'OK' >"${OUT_FILE}"
