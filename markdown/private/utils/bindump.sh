#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") hexdump file"
    exit 1
}

test -z "${1:-}" && usage
HEXDUMP="${1}"
test -z "${2:-}" && usage
FILE="${2}"

if [[ "${FILE}" != /* ]]; then
    FILE="${BUILD_WORKING_DIRECTORY}/${FILE}"
fi

printf 'File hash: %s\n' "$(md5sum <"${FILE}")"
"${HEXDUMP}" -v -C "${FILE}"
