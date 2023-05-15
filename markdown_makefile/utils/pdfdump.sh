#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") pdf2txt file"
    exit 1
}

test -z "${1:-}" && usage
PDF2TXT="${1}"
test -z "${2:-}" && usage
FILE="${2}"

if [[ "${FILE}" != /* ]]; then
    FILE="${BUILD_WORKING_DIRECTORY}/${FILE}"
fi

printf 'File hash: %s\n' "$(md5sum <"${FILE}")"
pdfinfo "${FILE}"
echo '----------'
"${PDF2TXT}" "${FILE}"
