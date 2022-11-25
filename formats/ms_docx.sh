#!/bin/bash
# md2short is chatty, so we wrap it and capture the output.

function usage() {
    echo "Usage: $(basename "${0}") script [args...]"
    exit 1
}

test -z "${1:-}" && usage
SCRIPT="${1}"

OUTPUT="$("${SCRIPT}" "${@:2}" 2>&1)"
EXIT_CODE="$?"

if [ "${EXIT_CODE}" != '0' ]; then
    echo "${OUTPUT}" >&2
fi

exit "${EXIT_CODE}"
