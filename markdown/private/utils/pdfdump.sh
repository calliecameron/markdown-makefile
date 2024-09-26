#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") pdfinfo pdf2txt file"
    exit 1
}

test -z "${1:-}" && usage
PDF2TXT="${1}"
test -z "${2:-}" && usage
PDFINFO="${2}"
test -z "${3:-}" && usage
FILE="${3}"

if [[ "${FILE}" != /* ]]; then
    FILE="${BUILD_WORKING_DIRECTORY}/${FILE}"
fi

printf 'File hash: %s\n' "$(md5sum <"${FILE}")"
"${PDFINFO}" "${FILE}"
echo '----------'
"${PDF2TXT}" "${FILE}"
