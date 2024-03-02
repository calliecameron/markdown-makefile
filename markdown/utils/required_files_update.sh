#!/bin/bash

set -eu

function usage() {
    echo "Usage: $(basename "${0}") package [src dst dst_mode]..."
    exit 1
}

PACKAGE="${1:-}" # Package will be empty in the root package.
shift

if [ -n "${PACKAGE}" ]; then
    DST_DIR="${BUILD_WORKSPACE_DIRECTORY}/${PACKAGE}"
else
    DST_DIR="${BUILD_WORKSPACE_DIRECTORY}"
fi

if [ -z "${1:-}" ]; then
    echo 'No files specified'
    exit 1
fi

while (($#)); do
    test -z "${1:-}" && usage
    test -e "${1}" || usage
    SRC="${1}"
    test -z "${2:-}" && usage
    DST="${DST_DIR}/${2}"
    test -z "${3:-}" && usage
    DST_MODE="${3}"

    cp "${SRC}" "${DST}"
    chmod "${DST_MODE}" "${DST}"

    shift 3
done
