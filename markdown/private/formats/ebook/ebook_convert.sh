#!/bin/bash
# ebook-convert is chatty, so we wrap it and capture the output.

set -u

function usage() {
    echo "Usage: $(basename "${0}") ebook_convert args..."
    exit 1
}

test -z "${1:-}" && usage
EBOOK_CONVERT="${1}"

OUTPUT="$("${EBOOK_CONVERT}" "${@:2}" 2>&1)"
EXIT_CODE="$?"

if [ "${EXIT_CODE}" != '0' ]; then
    echo "${OUTPUT}" >&2
fi

exit "${EXIT_CODE}"
