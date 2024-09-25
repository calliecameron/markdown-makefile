#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") file"
    exit 1
}

test -z "${1:-}" && usage
FILE="${1}"

if [[ "${FILE}" != /* ]]; then
    FILE="${BUILD_WORKING_DIRECTORY}/${FILE}"
fi

printf 'File hash: %s\n' "$(md5sum <"${FILE}")"
catdoc "${FILE}"
