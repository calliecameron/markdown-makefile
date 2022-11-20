#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") in_file out_file"
    exit 1
}

test -z "${1:-}" && usage
IN_FILE="${1}"
test -x "${2:-}" && usage
OUT_FILE="${2}"

cp "${IN_FILE}" "${OUT_FILE}"
strip-nondeterminism -t zip "${OUT_FILE}"
